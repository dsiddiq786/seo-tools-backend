from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class CaseConverterRequest(BaseModel):
    content: str = Field(..., title="Text", description="Provide the text to convert.")
    case_type: str = Field(..., title="Case Type", description="Choose case type: 'uppercase', 'lowercase', or 'titlecase'.")

class CaseConverterResponse(BaseModel):
    converted_text: str

@router.post("/convert-case", response_model=CaseConverterResponse)
def convert_case(request: CaseConverterRequest):
    """Convert the text to the specified case."""
    try:
        case_type = request.case_type.lower()
        if case_type == "uppercase":
            converted_text = request.content.upper()
        elif case_type == "lowercase":
            converted_text = request.content.lower()
        elif case_type == "titlecase":
            converted_text = request.content.title()
        else:
            raise HTTPException(status_code=400, detail="Invalid case type. Use 'uppercase', 'lowercase', or 'titlecase'.")

        return CaseConverterResponse(converted_text=converted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting case: {e}")
