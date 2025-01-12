from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import zipfile

router = APIRouter()

@router.post("/favicon-generator")
async def generate_favicon(image_file: UploadFile = File(...)):
    """Generate a ZIP file containing favicons for various devices and platforms."""
    try:
        image = Image.open(image_file.file)

        # Define favicon sizes for various platforms
        favicon_sizes = {
            "favicon_16x16.ico": (16, 16),
            "favicon_32x32.png": (32, 32),
            "favicon_48x48.png": (48, 48),
            "favicon_64x64.png": (64, 64),
            "favicon_128x128.png": (128, 128),
            "favicon_180x180.png": (180, 180),  # Apple touch icon
            "favicon_192x192.png": (192, 192),  # Android Chrome
            "favicon_256x256.png": (256, 256),
        }

        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file_name, size in favicon_sizes.items():
                # Resize the image
                resized_image = image.resize(size)
                img_buffer = io.BytesIO()
                file_format = "ICO" if file_name.endswith(".ico") else "PNG"
                resized_image.save(img_buffer, format=file_format)
                img_buffer.seek(0)

                # Add the resized image to the ZIP file
                zip_file.writestr(file_name, img_buffer.getvalue())

        zip_buffer.seek(0)

        # Return the ZIP file as a downloadable response
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=favicons.zip"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating favicons: {e}")
