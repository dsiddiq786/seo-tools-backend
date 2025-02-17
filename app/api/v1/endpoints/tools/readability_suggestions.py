# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel, Field
# import textstat

# router = APIRouter()

# class ReadabilityRequest(BaseModel):
#     content: str = Field(..., title="Content", description="The text to analyze for readability improvements.")

# class ReadabilityResponse(BaseModel):
#     readability_score: float
#     grade_level: str
#     suggestions: list

# @router.post("/readability-improvement", response_model=ReadabilityResponse)
# def readability_improvement(request: ReadabilityRequest):
#     """Analyze content and provide readability improvement suggestions."""
#     try:
#         content = request.content.strip()

#         # Calculate readability score and grade level
#         score = textstat.flesch_reading_ease(content)
#         grade = textstat.text_standard(content, float_output=False)

#         # Generate improvement suggestions
#         suggestions = []
#         if score < 50:
#             suggestions.append("Consider shortening sentences to improve readability.")
#         if textstat.difficult_words(content) > 10:
#             suggestions.append("Simplify complex words to make the text more accessible.")
#         if textstat.sentence_count(content) > 30:
#             suggestions.append("Reduce the number of sentences to make the content more concise.")

#         return ReadabilityResponse(
#             readability_score=round(score, 2),
#             grade_level=grade,
#             suggestions=suggestions
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error analyzing readability: {e}")
