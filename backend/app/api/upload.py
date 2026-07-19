from fastapi import APIRouter, File, UploadFile, HTTPException

from app.core.logger import logger
from app.services.upload_service import UploadService

router = APIRouter()

upload_service = UploadService()


@router.post(
    "/upload",
    summary="Upload a study document",
    description="Upload a PDF, DOCX, or TXT document for processing.",
)
async def upload_document(
    file: UploadFile = File(...)
):
    try:
        logger.info(f"Received upload request: {file.filename}")

        response = await upload_service.process_upload(file)

        logger.info(
            f"Successfully processed: {response['document']['filename']} "
            f"({response['chunk_count']} chunks)"
        )

        return response

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Unexpected upload error.")

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )