from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter()

class AltTextRequest(BaseModel):
    image_url: str = Field(..., title="Image URL", description="URL of the image.")

class AltTextResponse(BaseModel):
    alt_text: str

@router.post("/image-alt-text", response_model=AltTextResponse)
def generate_alt_text(request: Request, data: AltTextRequest):
    """Generate alt text for an image."""
    try:
        # Fetch model from app state
        image_captioning_pipeline = request.app.state.pipelines["image_captioning"]

        result = image_captioning_pipeline(data.image_url)
        return AltTextResponse(alt_text=result[0]["generated_text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating alt text: {e}")
