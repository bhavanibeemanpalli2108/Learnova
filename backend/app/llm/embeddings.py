from typing import List
import time
import voyageai

from app.core.config import settings
from app.core.logger import logger
from app.models import Chunk, EmbeddedChunk


class EmbeddingService:
    """
    Generates embeddings for document chunks using Voyage AI.
    """

    def __init__(self):
        self.client = voyageai.Client(
            api_key=settings.VOYAGE_API_KEY
        )

        self.model = settings.EMBEDDING_MODEL


    def embed_chunks(
        self,
        chunks: List[Chunk],
    ) -> List[EmbeddedChunk]:
        """
        Generate embeddings for all chunks using batched requests.
        """

        if not chunks:
            return []

        logger.info(
            f"Generating embeddings for {len(chunks)} chunks."
        )

        BATCH_SIZE = 20
        DELAY_SECONDS = 20

        embedded_chunks: List[EmbeddedChunk] = []

        total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE

        for batch_number, start in enumerate(
            range(0, len(chunks), BATCH_SIZE),
            start=1,
        ):

            batch = chunks[start:start + BATCH_SIZE]

            logger.info(
                f"Embedding batch {batch_number}/{total_batches} "
                f"({len(batch)} chunks)"
            )

            texts = [chunk.content for chunk in batch]

            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="document",
            )

            vectors = response.embeddings

            for chunk, vector in zip(batch, vectors):

                embedded_chunks.append(
                    EmbeddedChunk(
                        chunk_id=chunk.chunk_id,
                        chunk_index=chunk.chunk_index,
                        content=chunk.content,
                        embedding=vector,
                        metadata=chunk.metadata,
                    )
                )

            # Wait before the next batch
            if batch_number < total_batches:

                logger.info(
                    f"Waiting {DELAY_SECONDS} seconds to respect Voyage AI rate limits..."
                )

                time.sleep(DELAY_SECONDS)

        logger.info(
            f"Successfully generated {len(embedded_chunks)} embeddings."
        )

        return embedded_chunks

    # for the user uploaded query

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a user query.
        """

        logger.info("Generating query embedding.")

        response = self.client.embed(
            texts=[query],
            model=self.model,
            input_type="query",
        )

        return response.embeddings[0]