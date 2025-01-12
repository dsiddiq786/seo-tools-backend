from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class ThumbnailRequest(BaseModel):
    youtube_url: str = Field(..., title="YouTube URL", description="Enter the YouTube video URL.")

class ThumbnailResponse(BaseModel):
    thumbnail_url: str

@router.post("/youtube-thumbnail", response_model=ThumbnailResponse)
def download_thumbnail(request: ThumbnailRequest):
    """Get the thumbnail URL of a YouTube video."""
    try:
        video_id = request.youtube_url.split("v=")[-1]
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return ThumbnailResponse(thumbnail_url=thumbnail_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching thumbnail: {e}")
