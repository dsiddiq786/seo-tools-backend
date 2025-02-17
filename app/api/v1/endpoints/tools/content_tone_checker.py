# from fastapi import APIRouter, HTTPException, Request
# from pydantic import BaseModel, Field

# router = APIRouter()

# class ToneCheckRequest(BaseModel):
#     content: str = Field(..., title="Content", description="Enter the text to analyze.")

# class ToneCheckResponse(BaseModel):
#     tone: str

# @router.post("/content-tone", response_model=ToneCheckResponse)
# def check_content_tone(request: Request, data: ToneCheckRequest):
#     """Analyze the tone of the text."""
#     try:
#         # Fetch model from app state
#         tone_pipeline = request.app.state.pipelines["tone_analysis"]

#         result = tone_pipeline(data.content)
#         return ToneCheckResponse(tone=result[0]["label"])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error analyzing tone: {e}")
