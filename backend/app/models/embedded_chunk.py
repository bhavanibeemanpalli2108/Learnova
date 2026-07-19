from typing import List

from pydantic import BaseModel, Field

from app.models.chunk import ChunkMetadata


class EmbeddedChunk(BaseModel):
    """
    Represents a chunk together with its embedding vector.
    """

    chunk_id: str = Field(
        ...,
        description="Unique identifier of the chunk"
    )

    chunk_index: int = Field(
        ...,
        ge=0,
        description="Position of the chunk in the document"
    )

    content: str = Field(
        ...,
        description="Chunk text"
    )

    embedding: List[float] = Field(
        ...,
        description="Voyage AI embedding vector"
    )

    metadata: ChunkMetadata