from src.api.core.services.http_service import HttpService
from src.api.modules.agents.agents_service import AgentsService
from src.api.modules.agents.agents_models import AgentPublic, AgentCreate, AgentUpdate, AgentToDB, Agent, GenerateCode
from fastapi import BackgroundTasks, Depends, Body, Request, HTTPException, params
from fastapi.responses import JSONResponse
from src.api.core.services.http_service import HttpService
from src.agent.agent import create_graph
from src.agent.agent_model import AgentRequest
from  src.agent.state import GraphState
import logging
from sqlalchemy.orm import Session
from src.api.modules.users.users_models import User
import uuid
from src.agent.state import GenerateCodeState

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

    async def prompted_react_code_generator(self, graph, data: GenerateCode):
        state: GenerateCodeState =  {
            "input": data.input,
            "generated_code": None,
            "final_code": None
        }

        final_state: GenerateCodeState = await graph.ainvoke(state)

        return { "code": final_state["final_code"]}
    
     

    



        