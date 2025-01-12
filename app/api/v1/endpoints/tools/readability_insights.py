from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import textstat

router = APIRouter()

class ReadabilityInsightsRequest(BaseModel):
    content: str = Field(..., title="Content", description="Enter the text to analyze.")

class ReadabilityInsightsResponse(BaseModel):
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    recommendations: str

@router.post("/readability-insights", response_model=ReadabilityInsightsResponse)
def generate_readability_insights(request: ReadabilityInsightsRequest):
    """Generate detailed readability insights."""
    try:
        ease = textstat.flesch_reading_ease(request.content)
        grade = textstat.flesch_kincaid_grade(request.content)
        recommendations = "Simplify vocabulary and shorten sentences for better readability." if ease < 60 else "Content readability is good."

        return ReadabilityInsightsResponse(
            flesch_reading_ease=ease,
            flesch_kincaid_grade=grade,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating readability insights: {e}")
