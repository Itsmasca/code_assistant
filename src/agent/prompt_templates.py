from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate,  AIMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import SystemMessage
from src.service.Redis_service import RedisService
from src.agent.state import GraphState
from src.api.core.services.embedding_service import EmbeddingService
class PromptService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service

    async def general_query_prompt_template(
            self, 
            state: GraphState
        ): 

        messages = [
            SystemMessage(content = "<instructions> ...existing instructions... Your response MUST include these three fields: 1) prefix (description), 2) imports (all required import statements), 3) code (the complete code block, not including imports). Structure your answer as a JSON object with these three fields. Do NOT omit any field. Invoke the code tool to structure the output correctly. \n\nExample response:\n{{\n  \"prefix\": \"Description of the solution...\",\n  \"imports\": \"import ...\",\n  \"code\": \"def suma(a, b): return a + b\"\n}}\n</instructions> ..."),
            SystemMessagePromptTemplate.from_template(template = "Generate a complete Next.js React component for a dynamic agent interface based on this agent specification:\nAgent Name: {agentName}\nImproved Prompt: {improvedPrompt}\nAgent JSON Configuration:\n{agentJson}\nCRITICAL REQUIREMENTS:\n1. Return ONLY valid code. Do NOT include markdown, explanations, or comments outside the code.\n2. The file MUST start with an import statement (e.g., import useState from 'react').\n3. On form submit, POST the user's plain text query and the agent's unique ID to /api/ask-agent as JSON: query, agentId.\n4. Use \"{agentName}\" as the agentId value.\n5. Display the response from the backend in the UI.\n6. Do NOT use mock data. Do NOT use JSON.parse on user input.\n7. Assume the backend endpoint will use the agent's JSON to call NeuralSeek and return the answer.\n8. Use fetch, not axios.\n9. Always use async/await.\nALSO GENERATE THIS FILE:\nCreate a Next.js API route at pages/api/ask-agent.ts that:\n- Accepts only POST requests with query, agentId in the body.\n- Calls https://stagingapi.neuralseek.com/v1/liam-demo/{agentId}/maistro with the query as the payload.\n- Uses the apikey from the environment variable process.env.NEURALSEEK_API_KEY.\n- Returns the NeuralSeek response as JSON.\n- Returns 405 for non-POST requests and 400 for missing fields."),
            SystemMessage(content= "Example implementation (as a string, not real code!):\n// pages/api/ask-agent.ts\nimport type {{ NextApiRequest, NextApiResponse }} from 'next';\nexport default async function handler(req: NextApiRequest, res: NextApiResponse) {{\nif (req.method !== 'POST') {{\nreturn res.status(405).json({{ error: 'Method not allowed' }});\n}}\nconst {{ query, agentId }} = req.body;\nif (!query || !agentId) {{\nreturn res.status(400).json({{ error: 'Missing query or agentId' }});\n}}\nconst nsRes = await fetch(\n\"https://stagingapi.neuralseek.com/v1/liam-demo/{agentId}/maistro\",\n{{\nmethod: 'POST',\nheaders: {{\n'Content-Type': 'application/json',\n'apikey': process.env.NEURALSEEK_API_KEY!,\n}},\nbody: JSON.stringify({{ params: {{ use_case_summary: query }} }}),\n}}\n);\nconst data = await nsRes.json();\nreturn res.status(200).json(data);\n}}"),
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
    
    