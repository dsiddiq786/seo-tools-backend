from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import re

router = APIRouter()

class WordCounterRequest(BaseModel):
    content: str = Field(..., title="Input Text", description="Provide the text to analyze.")

class WordCounterResponse(BaseModel):
    word_count: int
    character_count: int
    sentence_count: int
    paragraph_count: int

@router.post("/word-counter", response_model=WordCounterResponse)
def count_words(request: WordCounterRequest):
    """Count words, characters, sentences, and paragraphs in the given text."""
    try:
        content = request.content

        word_count = len(content.split())
        character_count = len(content)
        sentence_count = len(re.split(r'[.!?]', content)) - 1
        paragraph_count = len(content.split("\n"))

        return WordCounterResponse(
            word_count=word_count,
            character_count=character_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting words: {e}")
