from src.agent.agent import create_graph
from src.agent.agent_model import AgentRequest, ReactCodeGenerationRequest
from  src.agent.state import GraphState
from src.agent.state import GenerateCodeState
from fastapi import BackgroundTasks
from src.api.core.dependencies.container import Container
from src.api.modules.chats.messages.messages_service import MessagesService

class AgentsController:
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
    

    async def prompted_react_code_generator(self, graph, data: ReactCodeGenerationRequest):
        state: GenerateCodeState =  {
            "input": data.input,
            "generated_code": None,
            "final_code": None
        }

        final_state: GenerateCodeState = await graph.ainvoke(state)

        human_message = final_state["input"]
        ai_message = final_state["final_code"]

        messages_service: MessagesService = Container.resolve("messages_service")
        BackgroundTasks.add_task(messages_service.handle_messages, human_message, ai_message)
        
        return { "code": final_state["final_code"]}
    
     

    



        