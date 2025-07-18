from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from src.service.LCEL_langchain import concatenated_content
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from typing import Any, Optional
from src.service.Qdrant import retrieve

load_dotenv
### Anthropic

class code(BaseModel):
    """Schema for code solutions to questions about LCEL."""
    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")

# Prompt to enforce tool use
class Llmservice:
    def __init__(self):
        self.llm = ChatAnthropic(temperature=0.3, model="claude-3-opus-20240229", api_key= os.getenv("ANTHROPIC_API_KEY"), default_headers={"anthropic-beta": "tools-2024-04-04"})
        self.question = "Please build the webpage of the agent with the agent specification to have all the inputs to assure the agent are working as good as possible"
        self.structured_llm_claude = self.llm.with_structured_output(code, include_raw=True)
        self.code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """<instructions> You are a coding assistant with expertise in LCEL, LangChain expression language. \n 
            Here is the LCEL documentation:  \n ------- \n  {context} \n ------- \n Answer the user  question based on the \n 
            above provided documentation. Ensure any code you provide can be executed with all required imports and variables \n
            defined. Structure your answer: 1) a prefix describing the code solution, 2) the imports, 3) the functioning code block. \n
            Invoke the code tool to structure the output correctly. </instructions> \n Here is the user question:""",
            "system",
            """Generate a complete Next.js React component for a dynamic agent interface based on this agent specification:

            Agent Name: ${agentName or 'Custom Agent'}
            Agent ID: ${agentName or 'Custom Agent'} (use this as the agentId when calling /api/ask-agent)
            Improved Prompt: ${improvedPrompt or 'No additional context'}

            Agent JSON Configuration:
            {agentJson}

            CRITICAL REQUIREMENTS:
            1. Return ONLY valid code. Do NOT include markdown, explanations, or comments outside the code.
            2. The file MUST start with an import statement (e.g., import  useState  from 'react').
            3. On form submit, POST the user's plain text query and the agent's unique ID to /api/ask-agent as JSON:  query, agentId .
            4. Use "${agentName or 'Custom Agent'}" as the agentId value.
            5. Display the response from the backend in the UI.
            6. Do NOT use mock data. Do NOT use JSON.parse on user input.
            7. Assume the backend endpoint will use the agent's JSON to call NeuralSeek and return the answer.
            8. Use fetch, not axios.
            9. Always use async/await.

            ALSO GENERATE THIS FILE:

            Create a Next.js API route at pages/api/ask-agent.ts that:
            - Accepts only POST requests with  query, agentId  in the body.
            - Calls https://stagingapi.neuralseek.com/v1/liam-demo/agentId/maistro with the query as the payload.
            - Uses the apikey from the environment variable process.env.NEURALSEEK_API_KEY.
            - Returns the NeuralSeek response as JSON.
            - Returns 405 for non-POST requests and 400 for missing fields.

            """,
                "user",
                """
                Example implementation (as a string, not real code!):

            \`\`\`ts
            // pages/api/ask-agent.ts
            import type { NextApiRequest, NextApiResponse } from 'next';

            export default async function handler(req: NextApiRequest, res: NextApiResponse) {
            if (req.method !== 'POST') {
                return res.status(405).json({ error: 'Method not allowed' });
            }
            const { query, agentId } = req.body;
            if (!query || !agentId) {
                return res.status(400).json({ error: 'Missing query or agentId' });
            }
            const nsRes = await fetch(
                \`https://stagingapi.neuralseek.com/v1/liam-demo/\${agentId}/maistro\`,
                {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'apikey': process.env.NEURALSEEK_API_KEY!,
                },
                body: JSON.stringify({ params: { use_case_summary: query } }),
                }
            );
            const data = await nsRes.json();
            return res.status(200).json(data);
            }
            \`\`\`
                """
                    ),
                    ("placeholder", "{messages}"),
                ]
            )
    def get_context(self):
        """Returns the concatenated context from Qdrant."""
        concatenated_content = retrieve()
        return concatenated_content
    def set_question(self, question: str):
        """Sets the question for the code generation."""
        self.question = question
    # Optional: Check for errors in case tool use is flaky
    def check_claude_output(tool_output):
        # Error with parsing
        if tool_output["parsing_error"]:
            # Report back output and parsing errors
            print("Parsing error!")
            raw_output = str(tool_output["raw"].content)
            error = tool_output["parsing_error"]
            raise ValueError(
                f"Error parsing your output! Be sure to invoke the tool. Output: {raw_output}. \n Parse error: {error}"
            )

        # Tool was not invoked
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


    def parse_output(solution):

        return solution["parsed"]

    def retrieve_chain(self):
        # Chain with output check
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