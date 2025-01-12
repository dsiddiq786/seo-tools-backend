from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline

router = APIRouter()

# meta_description_generator = pipeline("text2text-generation", model="t5-small")

# class MetaDescriptionRequest(BaseModel):
#     content: str = Field(..., title="Content", description="Enter the content to generate a meta description for.")

# class MetaDescriptionResponse(BaseModel):
#     meta_description: str

# @router.post("/generate-meta-description", response_model=MetaDescriptionResponse)
# def generate_meta_description(request: MetaDescriptionRequest):
#     """Generate an SEO meta description from content."""
#     try:
#         result = meta_description_generator(f"Summarize: {request.content}")
#         meta_description = result[0]["generated_text"]
#         return MetaDescriptionResponse(meta_description=meta_description)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error generating meta description: {e}")
