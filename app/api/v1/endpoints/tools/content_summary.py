from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

# Ensure `punkt` is loaded
try:
    nltk.data.find("tokenizers/punkt")
    print("Imported Successfully")
except LookupError:
    nltk.download("punkt", download_dir="/Users/apple/dsiddiq786/seo-tools-backend/venv/nltk_data", force=True)

router = APIRouter()

class SummaryRequest(BaseModel):
    content: str = Field(..., title="Content", description="Provide the text to summarize.")

class SummaryResponse(BaseModel):
    original_length: int
    summarized_length: int
    summary: str

@router.post("/generate-summary", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest):
    """Generate a summary of the given text."""
    try:
        content = request.content

        # Parse content for summarization
        parser = PlaintextParser.from_string(content, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 5)  # Limit to 5 sentences

        # Format the summary
        summary_text = " ".join([str(sentence) for sentence in summary])

        return SummaryResponse(
            original_length=len(content.split()),
            summarized_length=len(summary_text.split()),
            summary=summary_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {e}")
