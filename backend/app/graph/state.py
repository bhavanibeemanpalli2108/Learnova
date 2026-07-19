from typing import TypedDict


class GraphState(TypedDict):
    """
    Shared state across the LangGraph workflow.
    """

    query: str
    retrieved_chunks: list[dict]
    context: str
    best_score: float

    web_context: str
    web_sources: list[dict]

    answer: str
    needs_web_search: bool
    source: str