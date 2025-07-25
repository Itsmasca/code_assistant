from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from typing import Any, List
from src.service.Qdrant import QdrantRetriever
from src.agent.prompt_templates import PromptService
from src.agent.state import GraphState
from src.api.modules.chats.messages.messages_service import MessagesService
from src.api.modules.chats.messages.messages_models import Message
from sqlalchemy.orm import Session
import uuid
from src.api.core.decorators.log_errors import log_exceptions
# imoport copntainer 
from src.api.core.dependencies.container import Container
load_dotenv
### Anthropic
from src.api.core.decorators.service_error_handler import service_error_handler

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
    
    @service_error_handler(module="claude.output.error")
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
    
    @service_error_handler(module="claude.code.error.inserts")
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

    @service_error_handler(module="claude.output.parse")
    def parse_output(self, solution, config=None):
        return solution["parsed"]
    
    @service_error_handler(module="chain.claude.retrieve")
    async def retrieve_chain(self, component: str, state: GraphState = None) -> ChatPromptTemplate:
        # Chain with output check
        prompt_template: PromptService = Container.resolve("prompt_templates")
        await prompt_template.rewriteimproved_prompt(state)
        if component == "layout":
            code_gen_prompt = prompt_template.layout_code_gen_prompt
            #code_gen_chian = 
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

    @staticmethod
    @log_exceptions("llm_service.chat_history")
    def get_agent_chat_history(db: Session, chat_id: uuid.UUID, num_of_messages: int = 12) -> List[Message]:
        messages_service: MessagesService = Container.resolve("messages_service")
        chat_history = messages_service.collection(db=db, chat_id=chat_id)

        if len(chat_history) != 0:
            return chat_history[:num_of_messages]
        
        return None