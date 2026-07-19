from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState
from app.services.retrieval_service import RetrievalService
from app.services.web_search_service import WebSearchService
from app.llm.gemini_service import GeminiService
from app.core.logger import logger


class StudyAssistantGraph:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        web_search_service: WebSearchService,
        gemini_service: GeminiService,
    ):

        self.builder = StateGraph(GraphState)

        self.retrieval_service = retrieval_service
        self.web_search_service = web_search_service
        self.gemini_service = gemini_service

        # ------------------------
        # Register Nodes
        # ------------------------

        self.builder.add_node(
            "retrieve",
            self.retrieve_node,
        )

        self.builder.add_node(
            "build_context",
            self.build_context_node,
        )

        self.builder.add_node(
            "evaluate_retrieval",
            self.evaluate_retrieval_node,
        )

        self.builder.add_node(
            "judge_context",
            self.judge_context_node,
        )

        self.builder.add_node(
            "web_search",
            self.web_search_node,
        )

        self.builder.add_node(
            "generate_answer",
            self.generate_answer_node,
        )

        # ------------------------
        # Graph
        # ------------------------

        self.builder.add_edge(
            START,
            "retrieve",
        )

        self.builder.add_edge(
            "retrieve",
            "build_context",
        )

        self.builder.add_edge(
            "build_context",
            "evaluate_retrieval",
        )

        self.builder.add_conditional_edges(
            "evaluate_retrieval",
            self.route_after_score_evaluation,
        )

        self.builder.add_conditional_edges(
            "judge_context",
            self.route_after_judge,
        )

        self.builder.add_edge(
            "web_search",
            "generate_answer",
        )

        self.builder.add_edge(
            "generate_answer",
            END,
        )

    def compile(self):
        return self.builder.compile()

    # -------------------------------------------------
    # Nodes
    # -------------------------------------------------

    def retrieve_node(
        self,
        state: GraphState,
    ) -> GraphState:

        retrieval_result = self.retrieval_service.retrieve(
            query=state["query"]
        )

        state["retrieved_chunks"] = retrieval_result["chunks"]
        state["best_score"] = retrieval_result["best_score"]

        return state

    def build_context_node(
        self,
        state: GraphState,
    ) -> GraphState:

        context = "\n\n".join(
            chunk["content"]
            for chunk in state["retrieved_chunks"]
        )

        state["context"] = context

        return state

    def evaluate_retrieval_node(
        self,
        state: GraphState,
    ) -> GraphState:

        SCORE_THRESHOLD = 0.75

        score = state["best_score"]

        logger.info(
            f"Best similarity score: {score:.4f}"
        )

        if score < SCORE_THRESHOLD:

            logger.info(
                "Similarity score below threshold."
            )

            state["needs_web_search"] = True

        else:

            logger.info(
                "Similarity score above threshold."
            )

            state["needs_web_search"] = False

        return state

    def judge_context_node(
        self,
        state: GraphState,
    ) -> GraphState:

        can_answer = self.gemini_service.judge_context(
            query=state["query"],
            context=state["context"],
        )

        if can_answer:
            state["source"] = "document"

        state["needs_web_search"] = not can_answer

        return state

    def web_search_node(
        self,
        state: GraphState,
    ) -> GraphState:

        result = self.web_search_service.search(
            state["query"]
        )

        state["web_context"] = result["context"]
        state["web_sources"] = result["sources"]
        state["source"] = "web"

        logger.info(
            "Retrieved web context successfully."
        )

        return state

    def generate_answer_node(
        self,
        state: GraphState,
    ) -> GraphState:

        final_context = ""

        if state["context"]:
            final_context += state["context"]

        if state["web_context"]:

            if final_context:
                final_context += "\n\n"

            final_context += state["web_context"]

        answer = self.gemini_service.generate_answer(
            query=state["query"],
            context=final_context,
        )

        state["answer"] = answer

        return state

    # -------------------------------------------------
    # Routing
    # -------------------------------------------------

    def route_after_score_evaluation(
        self,
        state: GraphState,
    ) -> str:

        if state["needs_web_search"]:
            return "web_search"

        return "judge_context"

    def route_after_judge(
        self,
        state: GraphState,
    ) -> str:

        if state["needs_web_search"]:
            return "web_search"

        return "generate_answer"