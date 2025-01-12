from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline

router = APIRouter()
# image_captioning_pipeline = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

# class AltTextRequest(BaseModel):
#     image_url: str = Field(..., title="Image URL", description="URL of the image.")

# class AltTextResponse(BaseModel):
#     alt_text: str

# @router.post("/image-alt-text", response_model=AltTextResponse)
# def generate_alt_text(request: AltTextRequest):
#     """Generate alt text for an image."""
#     try:
#         result = image_captioning_pipeline(request.image_url)
#         return AltTextResponse(alt_text=result[0]["generated_text"])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error generating alt text: {e}")
