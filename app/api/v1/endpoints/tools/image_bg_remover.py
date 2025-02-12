from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import remove, new_session
from PIL import Image, ImageEnhance
import io
import numpy as np
import onnxruntime as ort  # ONNX for faster model execution


# Load the model once and keep it in memory
MODEL_PATH = "./u2net/u2net.onnx"  # Ensure you have this model downloaded
session = new_session(model_name=MODEL_PATH)

router = APIRouter()

@router.post("/remove-background/")
async def remove_bg(image_file: UploadFile = File(...)):
    """Removes background from an uploaded image with optimized performance"""
    try:
        # Read image file
        image = Image.open(io.BytesIO(await image_file.read()))

        # Resize image for faster processing (keeping aspect ratio)
        max_size = 1024  # Adjust based on your hardware
        image.thumbnail((max_size, max_size))

        # Convert to RGBA
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # Convert to NumPy array
        image_np = np.array(image)

        # Remove background without alpha matting for speed
        output_image_np = remove(
            image_np,
            session=session,  # Use ONNX optimized session
            alpha_matting=False  # Disable to improve performance
        )

        # Convert back to PIL Image
        output_image = Image.fromarray(output_image_np)

        # Apply slight sharpening to improve edges
        enhancer = ImageEnhance.Sharpness(output_image)
        output_image = enhancer.enhance(1.8)  # Increase sharpness

        # Save to buffer
        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")  # Always return PNG
        buffer.seek(0)

        return Response(
            content=buffer.getvalue(),
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=removed_bg.png"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")



# from fastapi import APIRouter, File, UploadFile, HTTPException
# from fastapi.responses import Response
# from rembg import remove
# from PIL import Image
# import io

# router = APIRouter()

# @router.post("/remove-background/")
# async def remove_bg(image_file: UploadFile = File(...)):
#     """Removes background from an uploaded image"""
#     try:
#         # Read image file
#         image = Image.open(io.BytesIO(await image_file.read()))

#         # Convert image to RGBA (if needed)
#         if image.mode != "RGBA":
#             image = image.convert("RGBA")

#         # Remove background
#         output_image = remove(image)

#         # Save to buffer
#         buffer = io.BytesIO()
#         output_image.save(buffer, format="PNG")  # Always return PNG to preserve transparency
#         buffer.seek(0)

#         return Response(
#             content=buffer.getvalue(),
#             media_type="image/png",
#             headers={"Content-Disposition": "attachment; filename=removed_bg.png"}
#         )
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
