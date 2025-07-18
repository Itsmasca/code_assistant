from typing import List
from typing_extensions import TypedDict


class GraphState(TypedDict):
    error: str
    messages: List
    generation: str
    iterations: int