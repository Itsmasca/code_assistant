from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from typing import Any, Optional
from src.service.Qdrant import QdrantRetriever
from src.agent.prompt_templates import PromptService
from src.agent.state import GraphState
# imoport copntainer 
from src.api.core.dependencies.container import Container
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

    async def retrieve_chain(self, state: GraphState = None) -> ChatPromptTemplate:
        # Chain with output check
        prompt_template: PromptService = Container.resolve("prompt_templates")
        code_gen_prompt = await prompt_template.general_query_prompt_template(state)
        # implement the structured output
        structured_llm_claude = self.llm.with_structured_output(code, include_raw=True)
        code_chain_claude_raw = (
            code_gen_prompt | structured_llm_claude | self.check_claude_output | self.parse_output
        )
        # This will be run as a fallback chain
        fallback_chain = self.insert_errors | code_chain_claude_raw
        N = 3  # Max re-tries
        code_gen_chain_re_try = code_chain_claude_raw.with_fallbacks(
            fallbacks=[fallback_chain] * N, exception_key="error"
        )
        code_gen_chain = code_gen_chain_re_try | self.parse_output
        # No re-try & no check
        code_gen_chain_no_retry = code_gen_prompt | structured_llm_claude | self.parse_output
        return code_chain_claude_raw

    
