from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import random

router = APIRouter()

class MetaTagRequest(BaseModel):
    content: str = Field(..., title="Input Text", description="Provide the content for which meta tags need to be generated.")

class MetaTagResponse(BaseModel):
    title: str
    description: str
    keywords: list[str]

@router.post("/generate-meta-tags", response_model=MetaTagResponse)
def generate_meta_tags(request: MetaTagRequest):
    """Generate meta tags based on input content."""
    try:
        # Generate title and description
        words = request.content.split()
        title = " ".join(words[:6])  # Use the first 6 words as a simulated title
        description = " ".join(words[:25])  # Use the first 25 words for description

        # Simulate keyword generation
        keywords = list(set(words[:10]))  # Extract unique keywords (limit to 10)

        return MetaTagResponse(
            title=title,
            description=description,
            keywords=keywords
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating meta tags: {e}")
