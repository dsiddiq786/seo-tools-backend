from fastapi import APIRouter, HTTPException, File, UploadFile, Query
from pydantic import BaseModel
from PIL import Image
import io
import base64
import enum

router = APIRouter()

# Unit conversion factors (assuming 96 DPI)
UNIT_CONVERSION = {
    "px": 1,
    "inch": 96,
    "cm": 37.8,
    "mm": 3.78
}

# Enum for resize mode
class ResizeMode(str, enum.Enum):
    dimension = "dimension"
    percentage = "percentage"

class ImageResizerResponse(BaseModel):
    resized_image: str  # Base64 encoded resized image

@router.post("/resize-image", response_model=ImageResizerResponse)
async def resize_image(
    image_file: UploadFile = File(...),
    mode: str = Query(..., description="Resize mode: 'dimension' or 'percentage'"),
    width: float = Query(0, description="Width in selected unit or percentage"),
    height: float = Query(0, description="Height in selected unit or percentage"),
    unit: str = Query("px", description="Unit for width & height: px, inch, cm, mm"),
    lock_aspect_ratio: bool = Query(False, description="Maintain original aspect ratio"),
):
    """Resize image by dimension (px, inch, cm, mm) or percentage, with aspect ratio lock option."""
    try:
        # Validate mode manually (Fix Enum parsing issue)
        if mode not in ["dimension", "percentage"]:
            raise HTTPException(status_code=400, detail="Invalid mode. Choose 'dimension' or 'percentage'.")

        image = Image.open(image_file.file)
        original_width, original_height = image.size
        new_width, new_height = width, height

        if mode == "dimension":
            if unit not in UNIT_CONVERSION:
                raise HTTPException(status_code=400, detail="Invalid unit. Choose from px, inch, cm, mm.")

            # Convert to pixels
            conversion_factor = UNIT_CONVERSION[unit]
            new_width = int(new_width * conversion_factor)
            new_height = int(new_height * conversion_factor)

            # Lock aspect ratio
            if lock_aspect_ratio:
                aspect_ratio = original_width / original_height
                if new_width and not new_height:
                    new_height = int(new_width / aspect_ratio)
                elif new_height and not new_width:
                    new_width = int(new_height * aspect_ratio)

        elif mode == "percentage":
            if new_width <= 0 or new_height <= 0 or new_width > 100 or new_height > 100:
                raise HTTPException(status_code=400, detail="Percentage values should be between 1 and 100.")

            # Resize by percentage
            new_width = int((new_width / 100) * original_width)
            new_height = int((new_height / 100) * original_height)

            # Lock aspect ratio
            if lock_aspect_ratio:
                aspect_ratio = original_width / original_height
                if new_width and not new_height:
                    new_height = int(new_width / aspect_ratio)
                elif new_height and not new_width:
                    new_width = int(new_height * aspect_ratio)

        # Resize image
        resized_image = image.resize((new_width, new_height))
        buffer = io.BytesIO()
        resized_image.save(buffer, format=image.format or "PNG")
        buffer.seek(0)

        # Encode to Base64
        base64_image = base64.b64encode(buffer.getvalue()).decode()
        return ImageResizerResponse(resized_image=f"data:image/{image.format.lower()};base64,{base64_image}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resizing image: {e}")
