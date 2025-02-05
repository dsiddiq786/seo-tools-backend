from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Response
from typing import List, Dict
from PIL import Image, ImageFile
import io

ImageFile.LOAD_TRUNCATED_IMAGES = True

router = APIRouter()

# Supported Formats for Compression
SUPPORTED_COMPRESSORS = {"jpeg", "png", "gif"}

compressed_images = []
image_buffers = {}

@router.post("/compress-images")
def compress_images(
    compressor_type: str = Form(..., regex="^(jpeg|png|gif)$"),
    quality: int = Form(50),  # Default compression quality (JPEG/PNG)
    images: List[UploadFile] = File(...)
) -> Dict:
    """Compress multiple images and return them with size reduction details."""
    if compressor_type not in SUPPORTED_COMPRESSORS:
        raise HTTPException(status_code=400, detail="Unsupported compressor type. Use jpeg, png, or gif.")

    for image_file in images:
        try:
            # Read the image
            image = Image.open(image_file.file)
            image_file.file.seek(0)  # Reset file pointer
            original_size = len(image_file.file.read())  # Get original file size in bytes

            buffer = io.BytesIO()

            # JPEG Compression
            if compressor_type == "jpeg":
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")  # Convert PNGs with transparency to RGB
                image.save(buffer, format="JPEG", quality=quality, optimize=True)

            # PNG Compression (reduces color depth)
            elif compressor_type == "png":
                image = image.convert("P", palette=Image.ADAPTIVE)  # Reduce color depth
                image.save(buffer, format="PNG", optimize=True)

            # GIF Compression (optimize=True reduces file size)
            elif compressor_type == "gif":
                image.save(buffer, format="GIF", optimize=True)

            # Get compressed file size
            buffer.seek(0)
            compressed_size = len(buffer.getvalue())

            # Store compressed image buffer
            image_buffers[image_file.filename] = buffer.getvalue()

            # Append compressed image size details
            compressed_images.append({
                "filename": image_file.filename,
                "original_size_kb": round(original_size / 1024, 2),
                "compressed_size_kb": round(compressed_size / 1024, 2),
                "compression_ratio": round((1 - (compressed_size / original_size)) * 100, 2),
                "download_url": f"/tools/compressed-images/{image_file.filename}"
            })

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error compressing {image_file.filename}: {str(e)}")

    return {"compressed_images": compressed_images}


@router.get("/compressed-images/{filename}")
def get_compressed_image(filename: str):
    """Retrieve a compressed image by filename."""
    if filename not in image_buffers:
        raise HTTPException(status_code=404, detail="Compressed image not found")

    return Response(
        content=image_buffers[filename],
        media_type="image/jpeg",  # Adjust based on compressor type
        headers={"Content-Disposition": f"attachment; filename=compressed_{filename}"}
    )
