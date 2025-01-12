from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from PIL import Image
import io

router = APIRouter()

class ImageConversionResponse(BaseModel):
    message: str
    converted_image_url: str

@router.post("/convert-image", response_model=ImageConversionResponse)
async def convert_image(
    format: str = Form(..., regex="^(PNG|JPEG|JPG|ICO|WEBP)$"),
    image_file: UploadFile = File(...)
):
    """Convert an image to a specified format."""
    try:
        image = Image.open(image_file.file)
        buffer = io.BytesIO()
        image.save(buffer, format=format.upper())
        buffer.seek(0)

        # Save or return the converted image
        converted_image_url = f"/download/converted_image.{format.lower()}"
        return ImageConversionResponse(
            message=f"Image converted to {format} successfully",
            converted_image_url=converted_image_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting image: {e}")
