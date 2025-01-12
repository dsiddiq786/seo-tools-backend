from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

# class SimilarityRequest(BaseModel):
#     content1: str = Field(..., title="Content 1", description="The first piece of content to compare.")
#     content2: str = Field(..., title="Content 2", description="The second piece of content to compare.")

# class SimilarityResponse(BaseModel):
#     similarity_score: float
#     description: str

# @router.post("/check-similarity", response_model=SimilarityResponse)
# def check_similarity(request: SimilarityRequest):
#     """Calculate the similarity between two pieces of content."""
#     try:
#         # Extract content
#         text1 = request.content1.strip()
#         text2 = request.content2.strip()

#         # Vectorize using TF-IDF
#         vectorizer = TfidfVectorizer()
#         vectors = vectorizer.fit_transform([text1, text2])

#         # Calculate cosine similarity
#         score = cosine_similarity(vectors[0], vectors[1])[0][0] * 100

#         # Generate a descriptive response
#         if score > 80:
#             description = "The two contents are highly similar."
#         elif score > 50:
#             description = "The two contents have moderate similarity."
#         else:
#             description = "The two contents are largely dissimilar."

#         return SimilarityResponse(
#             similarity_score=round(score, 2),
#             description=description
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error calculating similarity: {e}")
