from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import remove
from PIL import Image
import io

router = APIRouter()

@router.post("/remove-background/")
async def remove_bg(image_file: UploadFile = File(...)):
    """Removes background from an uploaded image"""
    try:
        # Read image file
        image = Image.open(io.BytesIO(await image_file.read()))

        # Convert image to RGBA (if needed)
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # Remove background
        output_image = remove(image)

        # Save to buffer
        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")  # Always return PNG to preserve transparency
        buffer.seek(0)

        return Response(
            content=buffer.getvalue(),
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=removed_bg.png"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
