from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

router = APIRouter()

class JSONValidationRequest(BaseModel):
    json_data: str

class JSONValidationError(BaseModel):
    error: str
    position: int

class JSONValidationResponse(BaseModel):
    is_valid: bool
    message: str
    errors: list[JSONValidationError] = []

@router.post("/validate-json", response_model=JSONValidationResponse)
def validate_json(request: JSONValidationRequest):
    """Validate if the input is a valid JSON and return errors if invalid."""
    try:
        json.loads(request.json_data)
        return JSONValidationResponse(is_valid=True, message="Valid JSON", errors=[])
    except json.JSONDecodeError as e:
        return JSONValidationResponse(
            is_valid=False,
            message="Invalid JSON",
            errors=[JSONValidationError(error=str(e), position=e.pos)]
        )
