from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate,  AIMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import SystemMessage
from src.service.Redis_service import RedisService
from src.agent.state import GraphState
from src.api.core.services.embedding_service import EmbeddingService
class PromptService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service

    async def prompt_generating_agentlanding(
            self, 
            state: GraphState
        ): 

        messages = [
                    SystemMessage(content=f"""<instructions>
        Generate a complete Next.js React component for a dynamic agent interface based on this agent specification:
        - Agent Name: {state.agentName}
        - Improved Prompt: {state.improvedPrompt}
        - Agent JSON Configuration: {state.agentJson}
        CRITICAL REQUIREMENTS:
        1. Return ONLY valid code. Do NOT include markdown, explanations, or comments outside the code.
        2. The file MUST start with an import statement (e.g., import {{ useState }} from 'react').
        3. On form submit, POST the user's plain text query and the agent's unique ID to /api/ask-agent as JSON: {{ query, agentId }}.
        4. Use "{state.agentName}" as the agentId value.
        5. Display the response from the backend in the UI.
        6. Do NOT use mock data. Do NOT use JSON.parse on user input.
        7. Assume the backend endpoint will use the agent's JSON to call NeuralSeek and return the answer.
        8. Use fetch, not axios.
        9. Always use async/await.
        </instructions>"""),
                    HumanMessagePromptTemplate.from_template("{input}")
                ]


        context = await self.embedding_service.search_for_context(
            input=state["input"]
        )
 
        if context:
            messages.append(SystemMessage(content=f"""
                You have access to the following relevant context retrieved from documents. Use this information to inform your response. Do not make up facts outside of this context.

                Relevant context:
                {context}
            """))

        
        messages.append(HumanMessagePromptTemplate.from_template('{input}'))

        prompt = ChatPromptTemplate.from_messages(messages)
        
        # Carga de todas las variables para el prompt
        return prompt
    
    