from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pytrends.request import TrendReq

router = APIRouter()
pytrends = TrendReq()

class KeywordTrendsRequest(BaseModel):
    keyword: str = Field(..., title="Keyword", description="Enter the keyword to track trends.")

class KeywordTrendsResponse(BaseModel):
    related_queries: dict
    interest_over_time: dict

@router.post("/keyword-trends", response_model=KeywordTrendsResponse)
def track_keyword_trends(request: KeywordTrendsRequest):
    """Fetch trending data for a keyword."""
    try:
        pytrends.build_payload([request.keyword])
        related_queries = pytrends.related_queries()
        interest_over_time = pytrends.interest_over_time().to_dict()

        return KeywordTrendsResponse(
            related_queries=related_queries,
            interest_over_time=interest_over_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching keyword trends: {e}")
