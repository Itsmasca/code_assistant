from src.agent.agent import create_graph
from src.agent.agent_model import AgentRequest, ReactCodeGenerationRequest
from src.agent.state import GraphState
from src.agent.state import GenerateCodeState
from fastapi import BackgroundTasks, Request
from src.api.core.dependencies.container import Container
from src.api.modules.chats.messages.messages_service import MessagesService
from sqlalchemy.orm import Session
from src.api.modules.users.users_models import User
import uuid
from src.api.core.services.http_service import HttpService
from src.api.modules.chats.chats_models import Chat
from src.service.Llm_service import Llmservice
from src.service.Redis_service import RedisService

class AgentsController:
    def __init__(self, https_service: HttpService, llm_service: Llmservice, redis_service: RedisService):
        self._http_service = https_service
        self._llm_service = llm_service
        self._redis_service = redis_service

    async def prompted_code_generator(self, data: AgentRequest):
        initial_state: GraphState = {
            "error": "no",
            "messages": [],
            "generation": None,
            "iterations": 0,
            "agentName": data.agentName,
            "improvedPrompt": data.improvedPrompt,
            "agentJson": data.agentJson,
            "input": data.input,
        }
        graph = create_graph()
        result = await graph.ainvoke(initial_state)
        generation = result.get("generation")
        return {
            "agentName": result.get("agentName", ""),
            "generation": {
                "prefix": getattr(generation, "prefix", "") if generation else "",
                "imports": getattr(generation, "imports", "") if generation else "",
                "code": getattr(generation, "code", "") if generation else "",
            },
            "messages": result.get("messages", []),
    }
    

    async def prompted_react_code_generator(
        self, 
        request: Request, 
        db: Session, 
        graph, 
        chat_id: uuid.UUID, 
        data: ReactCodeGenerationRequest, 
        background_tasks: BackgroundTasks
    ):
        user: User = request.state.user

        chat_resource: Chat = self._http_service.request_validation_service.verify_resource(
            service_key="chats_service",
            params={"db": db, "chat_id": chat_id},
            not_found_message="Chat not found"
        )

        self._http_service.request_validation_service.validate_action_authorization(user.user_id, chat_resource.user_id)

        chat_history = self._llm_service.get_agent_chat_history(db=db, chat_id=chat_id)

        state: GenerateCodeState =  {
            "input": data.input,
            "chat_histroty": chat_history, 
            "generated_code": None,
            "final_code": None
        }

        final_state: GenerateCodeState = await graph.ainvoke(state)

        human_message = final_state["input"]
        ai_message = final_state["final_code"]

        messages_service: MessagesService = Container.resolve("messages_service")
        background_tasks.add_task(messages_service.handle_messages, db, self._redis_service, chat_id, human_message, ai_message)
        
        return { "data": final_state["final_code"]}
    
     

    



        