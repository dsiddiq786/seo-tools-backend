from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

class SimilarityRequest(BaseModel):
    content1: str = Field(..., title="Content 1", description="The first piece of content to compare.")
    content2: str = Field(..., title="Content 2", description="The second piece of content to compare.")

class SimilarityResponse(BaseModel):
    similarity_score: float
    description: str

@router.post("/check-similarity", response_model=SimilarityResponse)
def check_similarity(request: Request, data: SimilarityRequest):
    """Calculate the similarity between two pieces of content."""
    try:
        text1 = data.content1.strip()
        text2 = data.content2.strip()

        # Fetch TF-IDF Vectorizer from app state
        vectorizer = request.app.state.vectorizer
        vectors = vectorizer.fit_transform([text1, text2])

        # Calculate cosine similarity
        score = cosine_similarity(vectors[0], vectors[1])[0][0] * 100

        # Generate a descriptive response
        description = "Highly similar" if score > 80 else "Moderately similar" if score > 50 else "Largely dissimilar"

        return SimilarityResponse(similarity_score=round(score, 2), description=description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating similarity: {e}")
