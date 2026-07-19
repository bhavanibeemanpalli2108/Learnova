from pydantic import BaseModel, Field

class Document(BaseModel):
    """
    Represents an uploaded document after text extraction.
    """

    document_id: str = Field(...,description="Unique identifier of the uploaded document")
    filename: str = Field(...,description="Original filename")
    file_type: str = Field(...,description="Document extension")
    pages: int = Field(...,ge=0,description="Number of pages extracted")
    text: str = Field(...,description="Extracted document text")