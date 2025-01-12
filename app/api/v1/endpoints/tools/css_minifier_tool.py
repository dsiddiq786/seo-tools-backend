from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import csscompressor

router = APIRouter()

class CSSMinifierRequest(BaseModel):
    css_code: str = Field(..., title="CSS Code", description="Enter the CSS code to minify.")

class CSSMinifierResponse(BaseModel):
    original_length: int
    minified_length: int
    minified_css: str

@router.post("/css-minifier", response_model=CSSMinifierResponse)
def minify_css(request: CSSMinifierRequest):
    """Minify CSS code."""
    try:
        minified_css = csscompressor.compress(request.css_code)
        return CSSMinifierResponse(
            original_length=len(request.css_code),
            minified_length=len(minified_css),
            minified_css=minified_css
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error minifying CSS: {e}")
