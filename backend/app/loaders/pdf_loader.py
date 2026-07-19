from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from fastapi import HTTPException

from app.core.logger import logger


def load_pdf(file_path: Path) -> dict:
    """
    Load and extract text from a PDF document.
    """

    try:
        logger.info(f"Loading PDF: {file_path.name}")

        loader = PyPDFLoader(str(file_path))
        documents = loader.load()

        text = "\n".join(
            doc.page_content.strip()
            for doc in documents
            if doc.page_content.strip()
        )

        if not text:
            raise HTTPException(
                status_code=400,
                detail="The PDF contains no readable text."
            )

        logger.info(
            f"Successfully extracted {len(documents)} pages from {file_path.name}"
        )

        return {
            "pages": len(documents),
            "text": text,
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("PDF loading failed.")

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )