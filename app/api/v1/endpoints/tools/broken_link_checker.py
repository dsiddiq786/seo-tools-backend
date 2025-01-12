from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import requests

router = APIRouter()

class LinkCheckRequest(BaseModel):
    urls: list[str] = Field(..., title="URLs", description="List of URLs to check.")

class LinkCheckResponse(BaseModel):
    broken_links: list[str]
    total_checked: int

@router.post("/broken-link-checker", response_model=LinkCheckResponse)
def check_broken_links(request: LinkCheckRequest):
    """Check for broken links."""
    try:
        broken_links = []
        for url in request.urls:
            try:
                response = requests.head(url, timeout=5)
                if response.status_code >= 400:
                    broken_links.append(url)
            except requests.RequestException:
                broken_links.append(url)

        return LinkCheckResponse(broken_links=broken_links, total_checked=len(request.urls))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking links: {e}")
