from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
import textstat

router = APIRouter()

class ContentRequest(BaseModel):
    content: str = Field(..., title="Content", description="Enter the content to analyze.")
    target_keywords: list[str] = Field(..., title="Target Keywords", description="List of target keywords.")

class ContentPerformanceResponse(BaseModel):
    readability_score: float
    sentiment_score: float
    keyword_match_score: float
    engagement_insights: list[str]

@router.post("/content-performance", response_model=ContentPerformanceResponse)
def analyze_content_performance(request: Request, data: ContentRequest):
    """Analyze content performance and provide actionable insights."""
    try:
        content = data.content
        keywords = data.target_keywords

        # Fetch models from app state
        sentiment_analyzer = request.app.state.sentiment_analyzer
        keyword_pipeline = request.app.state.pipelines["keyword_analysis"]

        # Readability score
        readability_score = textstat.flesch_reading_ease(content)

        # Sentiment analysis
        sentiment_scores = sentiment_analyzer.polarity_scores(content)
        sentiment_score = sentiment_scores['compound'] * 100

        # Keyword match score
        keyword_match_count = sum(content.lower().count(keyword.lower()) for keyword in keywords)
        keyword_match_score = (keyword_match_count / len(keywords)) * 100 if keywords else 0

        # Engagement insights
        insights = []
        if readability_score < 50:
            insights.append("Consider simplifying your content for better readability.")
        if sentiment_score > 70:
            insights.append("Your content has a highly positive tone, great for marketing campaigns.")

        return ContentPerformanceResponse(
            readability_score=readability_score,
            sentiment_score=sentiment_score,
            keyword_match_score=keyword_match_score,
            engagement_insights=insights
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing content performance: {e}")
