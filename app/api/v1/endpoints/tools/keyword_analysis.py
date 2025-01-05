from fastapi import APIRouter, HTTPException
from app.schemas.keyword import KeywordAnalysisRequest, KeywordAnalysisResponse, KeywordResponse
import random

router = APIRouter()

@router.post("/analyze-keywords", response_model=KeywordAnalysisResponse)
def analyze_keywords(request: KeywordAnalysisRequest):
    """Extract and analyze keywords based on user preferences."""
    try:
        # Split content into words (simulate keyword extraction)
        words = list(set(request.content.split()))
        random.shuffle(words)

        # Generate keyword metrics
        keywords = []
        for word in words[:10]:  # Default limit of 10 keywords for now
            keywords.append(KeywordResponse(
                keyword=word,
                volume=random.randint(100, 100000),
                competition=random.randint(10, 100),
                kei=random.randint(10, 500),
                no_click_searches=random.randint(100, 10000)
            ))

        return KeywordAnalysisResponse(keywords=keywords)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing keywords: {e}")
