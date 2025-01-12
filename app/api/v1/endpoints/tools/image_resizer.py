from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from PIL import Image
import io
import base64

router = APIRouter()

class ImageResizerRequest(BaseModel):
    width: int
    height: int

class ImageResizerResponse(BaseModel):
    resized_image: str  # Base64 encoded resized image

@router.post("/resize-image", response_model=ImageResizerResponse)
async def resize_image(image_file: UploadFile = File(...), request: ImageResizerRequest = None):
    """Resize an image to specified dimensions."""
    try:
        image = Image.open(image_file.file)
        resized_image = image.resize((request.width, request.height))
        buffer = io.BytesIO()
        resized_image.save(buffer, format=image.format or "PNG")
        buffer.seek(0)

        base64_image = base64.b64encode(buffer.getvalue()).decode()
        return ImageResizerResponse(resized_image=f"data:image/{image.format.lower()};base64,{base64_image}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resizing image: {e}")
