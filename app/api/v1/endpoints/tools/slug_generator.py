from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import re

router = APIRouter()

class SlugRequest(BaseModel):
    title: str = Field(..., title="Title", description="Provide a title or phrase to generate an SEO-friendly slug.")

class SlugResponse(BaseModel):
    slug: str

@router.post("/generate-slug", response_model=SlugResponse)
def generate_slug(request: SlugRequest):
    """Generate an SEO-friendly slug."""
    try:
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', request.title.lower()).strip('-')
        return SlugResponse(slug=slug)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating slug: {e}")
