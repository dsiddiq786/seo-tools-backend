from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import nltk
import os

# Ensure punkt is loaded
# Use environment variable or a relative path for nltk_data
project_root = os.getcwd()  # Gets the current working directory
nltk_data_path = os.path.join(project_root, "nltk_data", "tokenizers", "punkt", "english.pickle")
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)

try:
    nltk.data.find("tokenizers/punkt")
    print("Punkt tokenizer is correctly installed and accessible.")
except Exception as e:
    print("Punkt tokenizer is missing or inaccessible. Re-downloading...")
    nltk.download("punkt", download_dir=nltk_data_path)


class PunktTokenizerWrapper:
    def __init__(self, punkt_path):
        self.tokenizer = PunktSentenceTokenizer(punkt_path)

    def to_sentences(self, text):
        """Tokenize text into sentences."""
        return self.tokenizer.tokenize(text)

    def to_words(self, text):
        """Tokenize text into words."""
        return text.split()  # Simple word tokenization using whitespace


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

        # Use custom PunktTokenizerWrapper
        tokenizer = PunktTokenizerWrapper(nltk_data_path)

        # Parse content for summarization
        parser = PlaintextParser.from_string(content, tokenizer)
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
