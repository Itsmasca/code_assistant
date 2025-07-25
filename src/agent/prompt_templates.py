from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate,  AIMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from src.service.Redis_service import RedisService
from src.agent.state import GraphState
from src.api.core.services.embedding_service import EmbeddingService
from src.api.core.decorators.service_error_handler import service_error_handler
from src.agent.state import GenerateCodeState
from src.api.core.decorators.log_errors import log_exceptions
from langchain_anthropic import ChatAnthropic
import os

class PromptService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
    async def rewriteimproved_prompt(self, state: GraphState):
        
        agentName = state["agentName"]
        improvedPrompt = state["improvedPrompt"]
        component = ""
        
        prompt = f"""<instructions>
            Favor de generar la parte "{component}" del sitio para el agente "{agentName}" con el siguiente prompt mejorado:
            {improvedPrompt}

            Agrega una página Next.js que incluya un componente de generación de código que:
            - Realice una petición POST a /api/agents/secure/generate-code con el cuerpo {{ query: input, agentId: "{agentName}" }}.
            - Muestre el código generado en un bloque de código.
            CRITICAL REQUIREMENT: Return ONLY valid code; do NOT include markdown, explanations, or comments outside the code.
            </instructions>"""        
        llm = ChatAnthropic(
            temperature=0.1,
            model="claude-opus-4-20250514",
            api_key=os.getenv("ANTROPHIC_API_KEY"),
            thinking={"type": "enabled", "budget_tokens": 2000}
        )
        rephrased = await llm.invoke(prompt)
        state["input"] = rephrased
        return {"input": rephrased}
            
    @log_exceptions(module="prompt.generating.layout.error")
    async def prompt_generating_layout(
            self, 
            state: GraphState
        ): 

        messages = [
            SystemMessage(content=f"""<instructions>
        Generate a Next.js page at pages/agents/[agentId].tsx that will:
        - Import React and necessary hooks.
        - Read agentId from Next.js router.
        - Render a container with:
            1. A heading displaying “Agent: {state.agentName}”.
            2. A subtitle showing {state.agentJson.get('info',{{}}).get('description','')}.
            3. A placeholder <CodeGenerator /> component.
        - Export a default React component.
        CRITICAL REQUIREMENT: Return ONLY valid code; do NOT include markdown, explanations, or comments outside the code.
        </instructions>"""),
            HumanMessagePromptTemplate.from_template(
                f"Agent Name: {state.agentName}\nAgent JSON Configuration: {state.agentJson}"
            )
        ]


        context = await self.embedding_service.search_for_context(
            input = state
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
    @log_exceptions(module="prompt.generating.component.error")
    async def prompt_generating_component(
            self, 
            state: GraphState
        ): 

        messages = [
                    SystemMessage(content=f"""<instructions>
        Generate a React component named CodeGenerator that:
        - Uses useState to track user input and response.
        - Renders:
            1. A text input bound to state.
            2. A “Generate” button that, on click, POSTs {{ query: input, agentId: "{state.agentName}" }} to /api/agents/secure/generate-code using async/await and native fetch.
            3. A loading indicator while waiting.
            4. Displays the returned code inside a <pre> block.
        CRITICAL REQUIREMENT: Return ONLY valid code; do NOT include markdown, explanations, or comments outside the code.
        </instructions>"""),
                    HumanMessagePromptTemplate.from_template(
                        f"Agent Name: {state.agentName}\nAgent JSON Configuration: {state.agentJson}"
                    )
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
    
    @log_exceptions(module="prompt.generating.routes.error")
    async def prompt_generating_routes(
            self, 
            state: GraphState
        ): 

        messages = [
        SystemMessage(content=f"""<instructions>
        Create a Next.js API route file at pages/api/ask-agent.ts that:
        - Accepts only POST requests with JSON body {{ query, agentId }}.
        - Returns 405 for non-POST methods.
        - Returns 400 if query or agentId is missing.
        - On valid requests, calls:
            POST https://stagingapi.neuralseek.com/v1/liam-demo/{state.agentName}/maistro
            with headers Content-Type: application/json and apikey: process.env.NEURALSEEK_API_KEY
            and body {{ params: {{ use_case_summary: query }} }}.
        - Returns the NeuralSeek JSON response with status 200.
        CRITICAL REQUIREMENT: Return ONLY valid code; do NOT include markdown or comments outside the code.
        </instructions>"""),
                    HumanMessagePromptTemplate.from_template(
                        f"Agent Name: {state.agentName}\nAgent JSON Configuration: {state.agentJson}"
                    )
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
    @log_exceptions(module="prompt.generating.assemble.error")
    async def prompt_generating_assemble(
            self, 
            state: GraphState
        ): 

        messages = [
        SystemMessage(content=f"""<instructions>
        Create a Next.js API route file at pages/api/ask-agent.ts that:
        - Accepts only POST requests with JSON body {{ query, agentId }}.
        - Returns 405 for non-POST methods.
        - Returns 400 if query or agentId is missing.
        - On valid requests, calls:
            POST https://stagingapi.neuralseek.com/v1/liam-demo/{state.agentName}/maistro
            with headers Content-Type: application/json and apikey: process.env.NEURALSEEK_API_KEY
            and body {{ params: {{ use_case_summary: query }} }}.
        - Returns the NeuralSeek JSON response with status 200.
        CRITICAL REQUIREMENT: Return ONLY valid code; do NOT include markdown or comments outside the code.
        </instructions>"""),
                    HumanMessagePromptTemplate.from_template(
                        f"Agent Name: {state.agentName}\nAgent JSON Configuration: {state.agentJson}"
                    )
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

        
        messages.append(HumanMessagePromptTemplate.from_template('{input}'))

        prompt = ChatPromptTemplate.from_messages(messages)
        
        # Carga de todas las variables para el prompt
        return prompt
    
    async def code_generation_prompt(
        self, 
        state: GenerateCodeState
    ):
        messages = [
            SystemMessage(content="""
                You are a senior front-end engineer expert in React and Tailwind CSS. Your task is to generate clean, production-ready React components, or pages based on user input.
                You always:
                - Use **functional React components**
                - Style only with **Tailwind utility classes**
                - Follow best practices: responsive, accessible (ARIA), semantic HTML
                - Ensure components are **modular, reusable, and syntactically valid**
                - Avoid external libraries unless explicitly required
                Input types:
                - Feature descriptions (e.g. "Build a navbar with CTA")
                - Modification requests (e.g. "Make this layout responsive")
                - Raw code that needs cleanup or improvement
                Output format:
                - Return only a complete code block (React JSX)
                - No explanations unless inside code comments
                - Use comments in the same language as the input
                """)
        ]

        context = await self.embedding_service.search_for_context(
            input=state["input"]
        )

        if context:
            messages.append(SystemMessage(content=f"""
                You have access to the following relevant context retrieved from documents. Use this information to inform your response.
                Do not make up facts outside of this context.
                Relevant context:
                {context}
            """))

        if state.get("chat_history"):
            chat_history = state["chat_history"]
            for msg in chat_history:
                if msg.sender == "human":
                    messages.append(HumanMessage(content=msg.text))
                elif msg.sender == "ai":
                    messages.append(AIMessage(content=msg.text))
        
        messages.append(HumanMessagePromptTemplate.from_template('{input}'))

        prompt = ChatPromptTemplate.from_messages(messages)
        
        return prompt
    

    async def code_revision_prompt(
        self
    ):
        messages = [
            SystemMessage(content=""""
                You are the second node in a multi-agent system.
                Your task is to analyze and revise a React + Tailwind component or page.
                - If the code is correct and no changes are required, respond only with: UNCHANGED
                - If the code has issues, return the full corrected version inside a code block.
                Do not add explanations, notes, or anything outside of the response format.
                Return only one of the following:
                1. The string "UNCHANGED"
                2. A full revised code snippet
            """)
        ]

        messages.append(HumanMessagePromptTemplate.from_template('Check this code: {code}'))
 
        prompt = ChatPromptTemplate.from_messages(messages)
        
        return prompt