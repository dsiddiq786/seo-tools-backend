from fastapi import APIRouter, HTTPException
from app.schemas.keyword import KeywordFinderRequest, KeywordFinderResponse, KeywordResponse
import random

router = APIRouter()

@router.post("/find-keywords", response_model=KeywordFinderResponse)
def find_keywords(request: KeywordFinderRequest):
    """Find related keywords for a given query."""
    try:
        # Simulate related keyword generation
        keywords = []
        base_keyword = request.query.replace(" ", "_")
        for i in range(10):  # Default limit of 10 keywords for now
            keywords.append(KeywordResponse(
                keyword=f"{base_keyword}_{i}",
                volume=random.randint(100, 100000),
                competition=random.randint(10, 100),
                kei=random.randint(10, 500),
                no_click_searches=random.randint(100, 10000)
            ))

        return KeywordFinderResponse(keywords=keywords)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding keywords: {e}")
