from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from typing import List, Dict
from PIL import Image, ImageFile
import io
import base64

ImageFile.LOAD_TRUNCATED_IMAGES = True

router = APIRouter()

@router.post("/compress-images")
def compress_images(
    quality: int = Form(50),  # Default compression quality (JPEG/PNG/WebP)
    images: List[UploadFile] = File(...)
) -> Dict:
    """Compress multiple images and return base64-encoded compressed images with size reduction details."""
    compressed_images = []
    
    for image_file in images:
        try:
            # Read the image
            image = Image.open(image_file.file)
            image_file.file.seek(0)  # Reset file pointer
            original_size = len(image_file.file.read())  # Get original file size in bytes
            buffer = io.BytesIO()
            
            # Detect image format
            img_format = image.format.lower()
            
            # Apply compression based on detected format
            if img_format in {"jpeg", "jpg"}:
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")  # Convert PNGs with transparency to RGB
                image.save(buffer, format="JPEG", quality=quality, optimize=True)
            
            elif img_format == "png":
                if quality >= 90:
                    image.save(buffer, format="PNG", optimize=True)  # High quality (lossless)
                else:
                    image = image.convert("P", palette=Image.ADAPTIVE, colors=256)  # Reduce color depth
                    image.save(buffer, format="PNG", optimize=True)
            
            elif img_format == "gif":
                image.save(buffer, format="GIF", optimize=True)
            
            elif img_format == "webp":
                image.save(buffer, format="WEBP", quality=quality, optimize=True)
            
            elif img_format == "svg":
                # SVG files are usually small and text-based, no real compression available in PIL
                buffer.write(image_file.file.read())
            
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported image format: {img_format}")
            
            # Get compressed file size
            buffer.seek(0)
            compressed_size = len(buffer.getvalue())
            
            # Convert compressed image to Base64
            base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
            
            # Append compressed image details
            compressed_images.append({
                "filename": image_file.filename,
                "format": img_format,
                "original_size_kb": round(original_size / 1024, 2),
                "compressed_size_kb": round(compressed_size / 1024, 2),
                "compression_ratio": round((1 - (compressed_size / original_size)) * 100, 2) if original_size > 0 else 0,
                "base64_image": f"data:image/{img_format};base64,{base64_image}"
            })

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error compressing {image_file.filename}: {str(e)}")

    return {"compressed_images": compressed_images}

# from fastapi import APIRouter, HTTPException, File, UploadFile, Form
# from typing import List, Dict
# from PIL import Image, ImageFile
# import io
# import base64

# ImageFile.LOAD_TRUNCATED_IMAGES = True

# router = APIRouter()

# # Supported Formats for Compression
# SUPPORTED_COMPRESSORS = {"jpeg", "png", "gif"}

# @router.post("/compress-images")
# def compress_images(
#     compressor_type: str = Form(..., regex="^(jpeg|png|gif)$"),
#     quality: int = Form(50),  # Default compression quality (JPEG/PNG)
#     images: List[UploadFile] = File(...)
# ) -> Dict:
#     """Compress multiple images and return base64-encoded compressed images with size reduction details."""
#     if compressor_type not in SUPPORTED_COMPRESSORS:
#         raise HTTPException(status_code=400, detail="Unsupported compressor type. Use jpeg, png, or gif.")

#     compressed_images = []

#     for image_file in images:
#         try:
#             # Read the image
#             image = Image.open(image_file.file)
#             image_file.file.seek(0)  # Reset file pointer
#             original_size = len(image_file.file.read())  # Get original file size in bytes

#             buffer = io.BytesIO()

#             # JPEG Compression
#             if compressor_type == "jpeg":
#                 if image.mode in ("RGBA", "P"):
#                     image = image.convert("RGB")  # Convert PNGs with transparency to RGB
#                 image.save(buffer, format="JPEG", quality=quality, optimize=True)

#             # PNG Compression (adjustable based on quality)
#             elif compressor_type == "png":
#                 if quality >= 90:
#                     image.save(buffer, format="PNG", optimize=True)  # High quality (lossless)
#                 else:
#                     image = image.convert("P", palette=Image.ADAPTIVE, colors=256)  # Reduce color depth
#                     image.save(buffer, format="PNG", optimize=True)

#             # GIF Compression (optimize=True reduces file size)
#             elif compressor_type == "gif":
#                 image.save(buffer, format="GIF", optimize=True)

#             # Get compressed file size
#             buffer.seek(0)
#             compressed_size = len(buffer.getvalue())

#             # Convert compressed image to Base64
#             base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

#             # Append compressed image details
#             compressed_images.append({
#                 "filename": image_file.filename,
#                 "original_size_kb": round(original_size / 1024, 2),
#                 "compressed_size_kb": round(compressed_size / 1024, 2),
#                 "compression_ratio": round((1 - (compressed_size / original_size)) * 100, 2),
#                 "base64_image": f"data:image/{compressor_type};base64,{base64_image}"
#             })

#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error compressing {image_file.filename}: {str(e)}")

#     return {"compressed_images": compressed_images}
