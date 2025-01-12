from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from textblob import TextBlob

router = APIRouter()

class GrammarRequest(BaseModel):
    content: str = Field(..., title="Content", description="Provide the text to check grammar.")

class CorrectionDetail(BaseModel):
    original: str
    corrected: str
    reason: str

class GrammarResponse(BaseModel):
    original_text: str
    corrected_text: str
    updates: list[CorrectionDetail]  # List of changes applied

@router.post("/check-grammar", response_model=GrammarResponse)
def check_grammar(request: GrammarRequest):
    """Check grammar and provide suggestions for improvement."""
    try:
        content = request.content

        # Use TextBlob for grammar correction
        blob = TextBlob(content)
        corrected_text = str(blob.correct())

        # Generate updates list
        updates = []
        original_words = content.split()
        corrected_words = corrected_text.split()

        for orig, corr in zip(original_words, corrected_words):
            if orig != corr:
                updates.append(CorrectionDetail(
                    original=orig,
                    corrected=corr,
                    reason="Likely grammar/spelling mistake"
                ))

        return GrammarResponse(
            original_text=content,
            corrected_text=corrected_text,
            updates=updates
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking grammar: {e}")
