from pathlib import Path

from fastapi import HTTPException
from langchain_community.document_loaders import TextLoader

from app.core.logger import logger


def load_text(file_path: Path) -> dict:
    """
    Load and extract text from a TXT document.
    """

    try:
        logger.info(f"Loading TXT: {file_path.name}")

        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        documents = loader.load()

        text = "\n".join(
            doc.page_content.strip()
            for doc in documents
            if doc.page_content.strip()
        )

        if not text:
            raise HTTPException(
                status_code=400,
                detail="The text file is empty."
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
        logger.exception("TXT loading failed.")

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process TXT: {str(e)}"
        )