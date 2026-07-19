from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.core.logger import logger

from app.loaders import LOADERS
import uuid

from app.models import Document
from app.processing.chunking import ChunkingService

from app.llm.embeddings import EmbeddingService

from app.vectorstore.qdrant_store import QdrantService


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


class UploadService:
    """
    Handles document upload, validation,
    storage, and text extraction.
    """

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIRECTORY)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    async def process_upload(
        self,
        file: UploadFile,   
    ) -> dict:

        self._validate_file(file)

        saved_path = await self._save_file(file)

        extracted_data = self._extract_text(saved_path)

        file_extension = Path(file.filename).suffix.lower()

        document = Document(
            document_id=str(uuid.uuid4()),
            filename=file.filename,
            file_type=file_extension,
            pages=extracted_data["pages"],
            text=extracted_data["text"],
        )

        chunks = self.chunking_service.split_document(document)

        embedded_chunks = self.embedding_service.embed_chunks(chunks)

        self.qdrant_service.upsert_chunks(embedded_chunks)

        logger.info(f"Uploaded: {saved_path.name}")

        return {
            "status": "success",
            "message": "Document processed and stored successfully.",
            "document": document.model_dump(),
            "chunk_count": len(chunks),
            "embedding_count": len(embedded_chunks),
        }

    def _validate_file(
        self,
        file: UploadFile,
    ):

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Filename missing.",
            )

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format.",
            )

    async def _save_file(
        self,
        file: UploadFile,
    ) -> Path:

        extension = Path(file.filename).suffix.lower()

        filename = f"{uuid4().hex}{extension}"

        destination = self.upload_dir / filename

        contents = await file.read()

        max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024

        if len(contents) > max_size:
            raise HTTPException(
                status_code=400,
                detail="File exceeds maximum size.",
            )

        destination.write_bytes(contents)

        return destination

    def _extract_text(
        self,
        file_path: Path,
    ) -> dict:

        extension = file_path.suffix.lower()

        loader = LOADERS.get(extension)

        if loader is None:
            raise HTTPException(
                status_code=400,
                detail="Unsupported document type.",
            )

        return loader(file_path)