from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate,  AIMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import SystemMessage
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
                You are a full-stack front-end assistant specialized in building responsive, accessible, and performant React components and web pages using Tailwind CSS.

                Your main tasks include:
                1. Generating full webpages in React using Tailwind CSS, based on textual descriptions or feature lists.
                2. Creating individual React components with properly structured Tailwind classes.
                3. Modifying or improving existing React components based on user instructions.
                4. Ensuring all code is production-ready, clean, and follows best practices.
                5. Supporting responsive design, accessibility (ARIA), and semantic HTML when applicable.
                6. Writing modular and reusable components that can easily be integrated into larger React applications.

                ### Guidelines
                - Always use **functional components**.
                - Use **Tailwind CSS utility classes** to style elements, no inline styles or CSS files.
                - When modifying existing code, **preserve its logic and improve only what's requested**.
                - Wrap everything inside a top-level React component or exportable JSX.
                - Avoid external libraries unless explicitly requested.
                - Ensure the final JSX is **self-contained and syntactically valid**.

                ### Input Types
                You can receive:
                - Textual descriptions of a page or UI (e.g. “Build a hero section with a CTA and background image”).
                - Specific instructions (e.g. “Add dark mode support to this button”).
                - Raw React code to be modified (e.g. “Change this layout to 2 columns on desktop”).

                ### Output Format
                Always respond with:
                - A complete code snippet, wrapped in a code block.
                - Optional brief explanation (1-2 lines max).
                - If applicable, mention assumptions (e.g. "Assuming you use React 18").
                - All  comments must be in the language of the input
                - DO NOT ADD RESPONSES OR EXPLAIN JUST GIVE  ME THE CODE WITH ANY COMMENTS INSIDE THE VALID CODE

                ---

                ## 🛠 Example User Prompts
                1. "Build a landing page header with a logo, nav links, and a CTA button."
                2. "Generate a responsive card component for blog posts using Tailwind."
                3. "Modify this component to use a grid layout on desktop and a single column on mobile."
                4. "Add hover animations and transition effects to this button."
                5. "Turn this HTML layout into a React + Tailwind component."
                ---
                Act as a professional React developer and output valid, clean, and efficient React code using Tailwind CSS.

                """)
        ]

        context = await self.embedding_service.search_for_context(
            input=state["input"]
        )

        print("Got context")
 
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
    

    async def code_revision_prompt(
        self
    ):
        messages = [
            SystemMessage(content=""""
                You are the second node in a multi-agent system.

                Your job is to improve and fix a React + Tailwind component, or page.
                
                Do not Explain your answer just revise the code and fix the code if necessary 
            """)
        ]

        messages.append(HumanMessagePromptTemplate.from_template('Check this code and fix any errors, if no errors simply return the code as is {code}'))
 
        prompt = ChatPromptTemplate.from_messages(messages)
        
        # Carga de todas las variables para el prompt
        return prompt