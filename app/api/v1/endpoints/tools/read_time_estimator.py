from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class ReadTimeRequest(BaseModel):
    content: str = Field(..., title="Content", description="Provide the text to estimate reading time.")

class ReadTimeResponse(BaseModel):
    word_count: int
    estimated_read_time: str

@router.post("/estimate-read-time", response_model=ReadTimeResponse)
def estimate_read_time(request: ReadTimeRequest):
    """Estimate the reading time for the given content."""
    try:
        words = request.content.split()
        word_count = len(words)
        read_time = round(word_count / 200)  # Assuming average reading speed of 200 WPM

        return ReadTimeResponse(
            word_count=word_count,
            estimated_read_time=f"{read_time} minute{'s' if read_time != 1 else ''}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error estimating reading time: {e}")
