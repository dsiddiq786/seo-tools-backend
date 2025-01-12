from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import htmlmin

router = APIRouter()

class HTMLMinifyRequest(BaseModel):
    html_content: str

class HTMLMinifyResponse(BaseModel):
    minified_html: str

@router.post("/minify-html", response_model=HTMLMinifyResponse)
def minify_html(request: HTMLMinifyRequest):
    """Minify HTML content."""
    try:
        minified_html = htmlmin.minify(request.html_content, remove_comments=True, remove_empty_space=True)
        return HTMLMinifyResponse(minified_html=minified_html)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error minifying HTML: {e}")
