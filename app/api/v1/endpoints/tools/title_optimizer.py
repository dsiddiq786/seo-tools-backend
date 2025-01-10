from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class TitleOptimizerRequest(BaseModel):
    title: str = Field(..., title="Page Title", description="Provide the current title for optimization.")

class TitleOptimizerResponse(BaseModel):
    original_title: str
    optimized_title: str
    recommendations: str

@router.post("/optimize-title", response_model=TitleOptimizerResponse)
def optimize_title(request: TitleOptimizerRequest):
    """Optimize the title for better SEO."""
    try:
        original_title = request.title

        # Simulate optimization
        optimized_title = original_title.lower().capitalize()
        recommendations = (
            "Ensure the title contains primary keywords and is between 50-60 characters."
        )

        return TitleOptimizerResponse(
            original_title=original_title,
            optimized_title=optimized_title,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing title: {e}")
