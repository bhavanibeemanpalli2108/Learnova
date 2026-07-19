from pathlib import Path

from fastapi import HTTPException
from langchain_community.document_loaders import Docx2txtLoader

from app.core.logger import logger


def load_docx(file_path: Path) -> dict:
    """
    Load and extract text from a DOCX document.
    """

    try:
        logger.info(f"Loading DOCX: {file_path.name}")

        loader = Docx2txtLoader(str(file_path))
        documents = loader.load()

        text = "\n".join(
            doc.page_content.strip()
            for doc in documents
            if doc.page_content.strip()
        )

        if not text:
            raise HTTPException(
                status_code=400,
                detail="The document contains no readable text."
            )

        logger.info(
            f"Successfully extracted text from {file_path.name}"
        )

        return {
            "pages": 1,
            "text": text,
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("DOCX loading failed.")

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process DOCX: {str(e)}"
        )