from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.workflow import StudyAssistantGraph
from app.services.retrieval_service import RetrievalService
from app.services.web_search_service import WebSearchService
from app.llm.gemini_service import GeminiService

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


# Create services once
retrieval_service = RetrievalService()
web_search_service = WebSearchService()
gemini_service = GeminiService()

# Create graph once
study_assistant_graph = StudyAssistantGraph(
    retrieval_service=retrieval_service,
    web_search_service=web_search_service,
    gemini_service=gemini_service,
).compile() 


@router.post("/chat")
async def chat(request: ChatRequest):

    initial_state = {
        "query": request.query,
        "retrieved_chunks": [],
        "context": "",
        "best_score": 0.0,
        "web_context": "",
        "web_sources": [],
        "answer": "",
        "needs_web_search": False,
        "source": "",
    }

    result = study_assistant_graph.invoke(initial_state)

    return {
        "query": request.query,
        "answer": result["answer"],
        "source": result["source"],
        "web_sources": result["web_sources"],
    }