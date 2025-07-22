from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from typing import Any, Optional
from src.service.Qdrant import QdrantRetriever

load_dotenv
### Anthropic

class code(BaseModel):
    """Schema for code solutions to questions about LCEL."""
    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: Any = Field(description="Code block not including import statements")

# Prompt to enforce tool use
class Llmservice:
    def __init__(self):
        self.llm = ChatAnthropic(temperature=0.1, model="claude-opus-4-20250514", api_key= os.getenv("ANTROPHIC_API_KEY"), default_headers={"anthropic-beta": "tools-2024-04-04"}, max_tokens= 32000)  # or the maximum allowed
        self.structured_llm_claude = self.llm.with_structured_output(code, include_raw=True)
    # Optional: Check for errors in case tool use is flaky
    @staticmethod
    def check_claude_output(tool_output, config=None):
        # Error with parsing
        if tool_output["parsing_error"]:
            print("Parsing error!")
            raw_output = str(tool_output["raw"].content)
            error = tool_output["parsing_error"]
            raise ValueError(
                f"Error parsing your output! Be sure to invoke the tool. Output: {raw_output}. \n Parse error: {error}"
            )
        elif not tool_output["parsed"]:
            print("Failed to invoke tool!")
            raise ValueError(
                "You did not use the provided tool! Be sure to invoke the tool to structure the output."
            )
        return tool_output

    def insert_errors(inputs):

        # Get errors
        error = inputs["error"]
        messages = inputs["messages"]
        messages += [
            (
                "assistant",
                f"Retry. You are required to fix the parsing errors: {error} \n\n You must invoke the provided tool.",
            )
        ]
        return {
            "messages": messages,
            "context": inputs["context"],
        }


    def parse_output(self, solution, config=None):
        return solution["parsed"]

    def retrieve_chain(self, improved_prompt: Optional[str] = None) -> ChatPromptTemplate:
        # Chain with output check
        code_gen_prompt = ChatPromptTemplate.from_messages([
        ("system", "<instructions> ...existing instructions... Your response MUST include these three fields: 1) prefix (description), 2) imports (all required import statements), 3) code (the complete code block, not including imports). Structure your answer as a JSON object with these three fields. Do NOT omit any field. Invoke the code tool to structure the output correctly. \n\nExample response:\n{{\n  \"prefix\": \"Description of the solution...\",\n  \"imports\": \"import ...\",\n  \"code\": \"def suma(a, b): return a + b\"\n}}\n</instructions> ..."),
        ("system", r"Generate a complete Next.js React component for a dynamic agent interface based on this agent specification:\nAgent Name: {agentName}\nAgent ID: {agentName}\nImproved Prompt: {improvedPrompt}\nAgent JSON Configuration:\n{agentJson}\nCRITICAL REQUIREMENTS:\n1. Return ONLY valid code. Do NOT include markdown, explanations, or comments outside the code.\n2. The file MUST start with an import statement (e.g., import useState from 'react').\n3. On form submit, POST the user's plain text query and the agent's unique ID to /api/ask-agent as JSON: query, agentId.\n4. Use \"{agentName}\" as the agentId value.\n5. Display the response from the backend in the UI.\n6. Do NOT use mock data. Do NOT use JSON.parse on user input.\n7. Assume the backend endpoint will use the agent's JSON to call NeuralSeek and return the answer.\n8. Use fetch, not axios.\n9. Always use async/await.\nALSO GENERATE THIS FILE:\nCreate a Next.js API route at pages/api/ask-agent.ts that:\n- Accepts only POST requests with query, agentId in the body.\n- Calls https://stagingapi.neuralseek.com/v1/liam-demo/{agentId}/maistro with the query as the payload.\n- Uses the apikey from the environment variable process.env.NEURALSEEK_API_KEY.\n- Returns the NeuralSeek response as JSON.\n- Returns 405 for non-POST requests and 400 for missing fields."),
        ("user", r"Example implementation (as a string, not real code!):\n// pages/api/ask-agent.ts\nimport type {{ NextApiRequest, NextApiResponse }} from 'next';\nexport default async function handler(req: NextApiRequest, res: NextApiResponse) {{\nif (req.method !== 'POST') {{\nreturn res.status(405).json({{ error: 'Method not allowed' }});\n}}\nconst {{ query, agentId }} = req.body;\nif (!query || !agentId) {{\nreturn res.status(400).json({{ error: 'Missing query or agentId' }});\n}}\nconst nsRes = await fetch(\n\"https://stagingapi.neuralseek.com/v1/liam-demo/{agentId}/maistro\",\n{{\nmethod: 'POST',\nheaders: {{\n'Content-Type': 'application/json',\n'apikey': process.env.NEURALSEEK_API_KEY!,\n}},\nbody: JSON.stringify({{ params: {{ use_case_summary: query }} }}),\n}}\n);\nconst data = await nsRes.json();\nreturn res.status(200).json(data);\n}}"),
        ("placeholder", "{messages}")
        ])
        code_chain_claude_raw = (
        self.code_gen_prompt | self.structured_llm_claude | self.check_claude_output
        )
        # This will be run as a fallback chain
        fallback_chain = self.insert_errors | code_chain_claude_raw
        N = 3  # Max re-tries
        code_gen_chain_re_try = code_chain_claude_raw.with_fallbacks(
            fallbacks=[fallback_chain] * N, exception_key="error"
        )
        code_gen_chain = code_gen_chain_re_try | self.parse_output
        
        # No re-try
        code_gen_chain_no_retry = self.code_gen_prompt | self.structured_llm_claude | self.parse_output

    
        return code_gen_chain