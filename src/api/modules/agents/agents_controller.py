from src.api.core.services.http_service import HttpService
from src.api.modules.agents.agents_service import AgentsService
from src.api.modules.agents.agents_models import AgentPublic, AgentCreate, AgentUpdate, AgentToDB, Agent
from fastapi import BackgroundTasks, Depends, Body, Request, HTTPException, params
from fastapi.responses import JSONResponse
from src.api.core.services.http_service import HttpService
from src.agent.agent import app as agent_graph 
from src.agent.agent_model import AgentRequest
from  src.agent.state import GraphState
import logging
from sqlalchemy.orm import Session
from src.api.modules.users.users_models import User
import uuid

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
        try:
            result = await agent_graph.ainvoke(initial_state)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return {
            "agentName": result.get("agentName", ""),
            "generatiotn": {
                "prefix": result.get("generation", {}).get("prefix", ""),
                "imports": result.get("generation", {}).get("imports", ""),
                "code": result.get("generation", {}).get("code", "")
            },
            "messages": result.get("messages", []),
    }
    
     

    



        