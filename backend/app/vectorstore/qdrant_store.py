from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from app.core.config import settings
from app.core.logger import logger
from app.models import EmbeddedChunk

import uuid

class QdrantService:
    """
    Handles all interactions with Qdrant.
    """

    def __init__(self):

        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

        self.collection = settings.QDRANT_COLLECTION

        self._create_collection()

    def _create_collection(self):
        """
        Create the collection if it does not exist.
        """

        collections = self.client.get_collections().collections

        exists = any(
            collection.name == self.collection
            for collection in collections
        )

        if exists:
            logger.info(
                f"Collection '{self.collection}' already exists."
            )
            return

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=1024,
                distance=Distance.COSINE,
            ),
        )

        logger.info(
            f"Created collection '{self.collection}'."
        )

    def upsert_chunks(
        self,
        embedded_chunks: List[EmbeddedChunk],
    ) -> None:
        """
        Store embedded chunks in Qdrant.
        """

        if not embedded_chunks:
            return

        logger.info(
            f"Uploading {len(embedded_chunks)} vectors to Qdrant."
        )

        points = []

        for chunk in embedded_chunks:

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=chunk.embedding,
                    payload={
                        "document_id": chunk.metadata.document_id,
                        "chunk_id": chunk.chunk_id,
                        "chunk_index": chunk.chunk_index,
                        "content": chunk.content,
                        "source": chunk.metadata.source,
                        "file_type": chunk.metadata.file_type,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection,
            points=points,
        )

        logger.info(
            f"Stored {len(points)} vectors in Qdrant."
        )

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[dict]:
        """
        Search the vector database and return
        payloads together with similarity scores.
        """

        logger.info(
            f"Searching Qdrant (top {limit})..."
        )

        results = self.client.query_points(
            collection_name=self.collection,
            query=query_embedding,
            limit=limit,
            with_payload=True,
        )

        response = []

        for point in results.points:
            response.append(
                {
                    "score": point.score,
                    "payload": point.payload,
                }
            )

        logger.info(
            f"Retrieved {len(response)} chunks."
        )

        return response