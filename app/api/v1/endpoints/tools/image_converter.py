from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Response
from pydantic import BaseModel
from PIL import Image
import io
import pillow_heif  # For HEIC conversion

router = APIRouter()

# Supported Image Formats (SVG temporarily disabled)
SUPPORTED_FORMATS = {
    "PNG", "JPEG", "JPG", "GIF", "BMP", "ICO", "TIFF", "WEBP", "HEIC"
}

class ImageConversionResponse(BaseModel):
    message: str
    converted_image_url: str

@router.post("/convert-image")
async def convert_image(
    format: str = Form(..., regex="^(PNG|JPEG|JPG|GIF|BMP|ICO|TIFF|WEBP|HEIC)$"),
    image_file: UploadFile = File(...)
):
    """Convert an image to the specified format, ensuring PNG to JPG works properly."""
    try:
        # Ensure format is uppercase
        format = format.upper()
        if format == "JPG":
            format = "JPEG"  # Pillow uses "JPEG" instead of "JPG"

        if format not in SUPPORTED_FORMATS:
            raise HTTPException(status_code=400, detail=f"Unsupported-format: {format}")

        # Read image bytes
        image_bytes = await image_file.read()
        buffer = io.BytesIO()

        # Handling HEIC format
        if image_file.filename.lower().endswith(".heic"):
            heif_image = pillow_heif.read_heif(image_bytes)
            image = Image.frombytes(
                heif_image.mode, 
                heif_image.size, 
                heif_image.data
            )
        else:
            image = Image.open(io.BytesIO(image_bytes))

        # ✅ Fix PNG to JPG issue: Convert RGBA to RGB
        if format == "JPEG" and image.mode == "RGBA":
            image = image.convert("RGB")

        # Convert and save to buffer
        image.save(buffer, format=format)
        buffer.seek(0)

        # Return converted image as response
        return Response(
            content=buffer.getvalue(),
            media_type=f"image/{format.lower()}",
            headers={
                "Content-Disposition": f"attachment; filename=converted_image.{format.lower()}"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting image: {str(e)}")



# from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Response
# from pydantic import BaseModel
# from PIL import Image
# import io
# # import cairosvg  # For SVG conversion
# import pillow_heif  # For HEIC conversion

# router = APIRouter()

# # Supported Image Formats (Extended)
# SUPPORTED_FORMATS = {
#     "PNG", "JPEG", "JPG", "GIF", "BMP", "ICO", "TIFF", "WEBP", "HEIC", "SVG"
# }

# class ImageConversionResponse(BaseModel):
#     message: str
#     converted_image_url: str

# @router.post("/convert-image")
# async def convert_image(
#     format: str = Form(..., regex="^(PNG|JPEG|JPG|GIF|BMP|ICO|TIFF|WEBP|HEIC|SVG)$"),
#     image_file: UploadFile = File(...)
# ):
#     """Convert an image to the specified format, including SVG and HEIC."""
#     try:
#         # Ensure format is uppercase
#         format = format.upper()
#         if format == "JPG":
#             format = "JPEG"  # Pillow uses "JPEG" instead of "JPG"

#         if format not in SUPPORTED_FORMATS:
#             raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

#         # Read image bytes
#         image_bytes = await image_file.read()
#         buffer = io.BytesIO()

#         # Handling HEIC format
#         if image_file.filename.lower().endswith(".heic"):
#             heif_image = pillow_heif.read_heif(image_bytes)
#             image = Image.frombytes(
#                 heif_image.mode, 
#                 heif_image.size, 
#                 heif_image.data
#             )
#         # Handling SVG format
#         # elif image_file.filename.lower().endswith(".svg"):
#         #     png_data = cairosvg.svg2png(bytestring=image_bytes)
#         #     image = Image.open(io.BytesIO(png_data))
#         # else:
#         #     image = Image.open(io.BytesIO(image_bytes))

#         # # Convert and save to buffer
#         # if format == "SVG":
#         #     # Convert raster images (PNG, JPG, etc.) to SVG using cairosvg
#         #     cairosvg.svg2png(file_obj=io.BytesIO(image_bytes), write_to=buffer)
#         # else:
#         image.save(buffer, format=format)

#         buffer.seek(0)

#         # Return converted image as response
#         return Response(
#             content=buffer.getvalue(),
#             media_type=f"image/{format.lower()}",
#             headers={
#                 "Content-Disposition": f"attachment; filename=converted_image.{format.lower()}"
#             }
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error converting image: {str(e)}")
