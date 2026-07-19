from pathlib import Path
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.logger import logger
from app.models import Chunk, ChunkMetadata, Document


class ChunkingService:
    """
    Splits extracted document text into
    chunks ready for embedding.
    """

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split_document(
        self,
        document: Document,
    ) -> List[Chunk]:
        """
        Split a document into chunks.
        """

        logger.info(
            f"Chunking document: {document.filename}"
        )

        pieces = self.splitter.split_text(document.text)

        chunks: List[Chunk] = []

        document_name = Path(document.filename).stem

        for index, piece in enumerate(pieces):

            chunk = Chunk(
                chunk_id=f"{document_name}_chunk_{index + 1:04}",
                chunk_index=index,
                content=piece,
                metadata=ChunkMetadata(
                    document_id=document.document_id,
                    source=document.filename,
                    file_type=document.file_type,
                ),
            )

            chunks.append(chunk)

        logger.info(
            f"Generated {len(chunks)} chunks."
        )

        return chunks