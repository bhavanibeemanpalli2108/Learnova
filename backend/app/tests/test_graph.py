from app.graph.workflow import StudyAssistantGraph

graph = StudyAssistantGraph().compile()

result = graph.invoke(
    {
        "query": "What is Tiger?",
        "retrieved_chunks": [],
        "context": "",
        "best_score": 0.0,
        "web_context": "",
        "answer": "",
        "needs_web_search": False,
        "source": "",
    }
)

print(result["best_score"])