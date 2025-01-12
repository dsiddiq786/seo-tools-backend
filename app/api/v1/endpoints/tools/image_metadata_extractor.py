from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from PIL import Image
from PIL.ExifTags import TAGS
import io

router = APIRouter()

class ImageMetadataResponse(BaseModel):
    metadata: dict

@router.post("/image-metadata-extractor", response_model=ImageMetadataResponse)
async def extract_metadata(image_file: UploadFile = File(...)):
    """Extract metadata from an uploaded image."""
    try:
        image = Image.open(image_file.file)
        exif_data = image._getexif()
        if not exif_data:
            return ImageMetadataResponse(metadata={})
        
        metadata = {
            TAGS.get(tag, tag): value
            for tag, value in exif_data.items()
            if tag in TAGS
        }
        return ImageMetadataResponse(metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting metadata: {e}")
