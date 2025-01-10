from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict

router = APIRouter()

class KeywordDensityRequest(BaseModel):
    content: str = Field(..., title="Content", description="Text content to analyze.")
    focus_keywords: List[str] = Field(..., title="Focus Keywords", description="List of focus keywords.")

class KeywordDensityResponse(BaseModel):
    keyword_density: Dict[str, float]
    recommendations: List[str]

@router.post("/keyword-density", response_model=KeywordDensityResponse)
def keyword_density_analyzer(request: KeywordDensityRequest):
    """Analyze keyword density in the given content."""
    try:
        content_words = request.content.lower().split()
        keyword_density = {
            keyword: content_words.count(keyword.lower()) / len(content_words) * 100
            for keyword in request.focus_keywords
        }
        recommendations = [
            f"Keyword '{kw}' density is {density:.2f}%. Adjust usage for SEO."
            for kw, density in keyword_density.items()
        ]
        return KeywordDensityResponse(keyword_density=keyword_density, recommendations=recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing keyword density: {e}")
