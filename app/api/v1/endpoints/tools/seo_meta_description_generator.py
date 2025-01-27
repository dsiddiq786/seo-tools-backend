from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter()

class MetaDescriptionRequest(BaseModel):
    content: str = Field(..., title="Content", description="Enter the content to generate a meta description for.")

class MetaDescriptionResponse(BaseModel):
    meta_description: str

@router.post("/generate-meta-description", response_model=MetaDescriptionResponse)
def generate_meta_description(request: Request, data: MetaDescriptionRequest):
    """Generate an SEO meta description from content."""
    try:
        # Fetch model from app state
        meta_description_generator = request.app.state.pipelines["meta_description"]

        result = meta_description_generator(f"Summarize: {data.content}")
        meta_description = result[0]["generated_text"]
        return MetaDescriptionResponse(meta_description=meta_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating meta description: {e}")
