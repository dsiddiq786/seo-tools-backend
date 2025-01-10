from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, HttpUrl
import requests

router = APIRouter()

class URLValidationRequest(BaseModel):
    url: HttpUrl = Field(..., title="URL", description="Provide a URL to validate.")

class URLValidationResponse(BaseModel):
    is_valid: bool
    is_accessible: bool

@router.post("/validate-url", response_model=URLValidationResponse)
def validate_url(request: URLValidationRequest):
    """Validate the structure and accessibility of the given URL."""
    try:
        # Check URL accessibility
        try:
            response = requests.head(request.url, timeout=5)
            accessible = response.status_code == 200
        except requests.RequestException:
            accessible = False

        return URLValidationResponse(is_valid=True, is_accessible=accessible)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating URL: {e}")
