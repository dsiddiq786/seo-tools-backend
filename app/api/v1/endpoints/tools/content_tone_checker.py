from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline

router = APIRouter()
# tone_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli")

# class ToneCheckRequest(BaseModel):
#     content: str = Field(..., title="Content", description="Enter the text to analyze.")

# class ToneCheckResponse(BaseModel):
#     tone: str

# @router.post("/content-tone", response_model=ToneCheckResponse)
# def check_content_tone(request: ToneCheckRequest):
#     """Analyze the tone of the text."""
#     try:
#         result = tone_pipeline(request.content)
#         return ToneCheckResponse(tone=result[0]["label"])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error analyzing tone: {e}")
