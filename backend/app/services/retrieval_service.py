from app.core.logger import logger
from app.llm.embeddings import EmbeddingService
from app.vectorstore.qdrant_store import QdrantService


class RetrievalService:
    """
    Handles retrieval of relevant document chunks.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> dict:
        """
        Retrieve relevant chunks and their best similarity score.
        """

        logger.info(
            f"Retrieving context for query: {query}"
        )

        query_embedding = self.embedding_service.embed_query(
            query
        )

        results = self.qdrant_service.search(
            query_embedding=query_embedding,
            limit=limit,
        )

        chunks = [
            result["payload"]
            for result in results
        ]

        best_score = (
            results[0]["score"]
            if results
            else 0.0
        )

        logger.info(
            f"Retrieved {len(chunks)} chunks."
        )

        logger.info(
            f"Best similarity score: {best_score:.4f}"
        )

        return {
            "chunks": chunks,
            "best_score": best_score,
        }