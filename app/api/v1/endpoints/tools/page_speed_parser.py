from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

router = APIRouter()

class PageSpeedRequest(BaseModel):
    metrics: Dict[str, float] = Field(..., title="Metrics", description="Page speed metrics JSON data.")

class PageSpeedResponse(BaseModel):
    insights: Dict[str, str]

@router.post("/page-speed", response_model=PageSpeedResponse)
def page_speed_parser(request: PageSpeedRequest):
    """Analyze page speed metrics and provide insights."""
    try:
        metrics = request.metrics
        insights = {
            "load_time": f"{metrics.get('load_time', 0):.2f} seconds",
            "recommendations": "Optimize images and reduce JavaScript."
        }
        return PageSpeedResponse(insights=insights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing page speed: {e}")
