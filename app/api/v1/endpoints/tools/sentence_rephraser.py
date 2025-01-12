from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline
import textstat

# # Download necessary NLTK resources
# # nltk.download("punkt")

router = APIRouter()

# # Load the paraphrase generation model
# paraphrasing_pipeline = pipeline("text2text-generation", model="t5-small")

# class RephraseRequest(BaseModel):
#     content: str = Field(..., title="Content", description="The sentence or paragraph to rephrase.")
#     tone: str = Field("neutral", title="Tone", description="Desired tone: neutral, formal, casual, or persuasive.")

# class RephraseResponse(BaseModel):
#     original_text: str
#     rephrased_variants: list

# class RephraseVariant(BaseModel):
#     rephrased_text: str
#     readability_score: float
#     tone_match: bool
#     estimated_read_time: str

# @router.post("/rephrase-text", response_model=RephraseResponse)
# def rephrase_text(request: RephraseRequest):
#     """Generate rephrased versions of the input text with detailed analysis."""
#     try:
#         content = request.content.strip()

#         # Generate rephrased versions
#         rephrased_outputs = paraphrasing_pipeline(f"paraphrase: {content}", num_return_sequences=5, max_length=100)
#         rephrased_texts = [output['generated_text'] for output in rephrased_outputs]

#         variants = []
#         for text in rephrased_texts:
#             readability_score = textstat.flesch_reading_ease(text)
#             tone_match = request.tone.lower() in text.lower()  # Basic tone match check
#             estimated_read_time = f"{len(text.split()) // 200} minutes" if len(text.split()) >= 200 else "Less than a minute"
#             variants.append({
#                 "rephrased_text": text,
#                 "readability_score": readability_score,
#                 "tone_match": tone_match,
#                 "estimated_read_time": estimated_read_time
#             })

#         return RephraseResponse(
#             original_text=content,
#             rephrased_variants=variants
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error rephrasing text: {e}")
