from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from pdf2image import convert_from_bytes
import base64
import io

router = APIRouter()

class PDFToImageResponse(BaseModel):
    message: str
    images: list[str]

@router.post("/pdf-to-images", response_model=PDFToImageResponse)
async def pdf_to_images(pdf_file: UploadFile = File(...)):
    """Convert PDF to a list of images."""
    try:
        pdf_bytes = pdf_file.file.read()
        images = convert_from_bytes(pdf_bytes)
        
        encoded_images = []
        for image in images:
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            encoded_images.append(base64.b64encode(buffer.getvalue()).decode())

        return PDFToImageResponse(
            message="PDF successfully converted to images",
            images=[f"data:image/png;base64,{img}" for img in encoded_images]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting PDF to images: {e}")
