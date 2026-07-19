from pydantic import BaseModel, Field
from typing import Dict


class ChunkMetadata(BaseModel):
    """
    Metadata associated with a document chunk.
    """

    document_id: str = Field(...)
    source: str = Field(...)
    file_type: str = Field(...)


class Chunk(BaseModel):
    """
    Represents a single chunk of text produced during
    document processing.
    """

    chunk_id: str = Field(
        ...,
        description="Unique identifier for the chunk"
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

    metadata: ChunkMetadata