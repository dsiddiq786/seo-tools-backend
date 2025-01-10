from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class SERPRequest(BaseModel):
    title: str = Field(..., title="Meta Title", description="The meta title for the page.")
    description: str = Field(..., title="Meta Description", description="The meta description for the page.")
    url: str = Field(..., title="URL", description="The URL of the page.")

class SERPResponse(BaseModel):
    snippet: str

@router.post("/serp-simulator", response_model=SERPResponse)
def serp_simulator(request: SERPRequest):
    """Simulate how a page appears on Google SERP."""
    try:
        snippet = (
            f"Title: {request.title[:60]}...\n"
            f"Description: {request.description[:160]}...\n"
            f"URL: {request.url}"
        )
        return SERPResponse(snippet=snippet)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating SERP snippet: {e}")
