from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup

router = APIRouter()

class HeadingRequest(BaseModel):
    html_content: str = Field(..., title="HTML Content", description="HTML content to validate heading structure.")

class HeadingResponse(BaseModel):
    issues: list
    recommendations: list

@router.post("/heading-validator", response_model=HeadingResponse)
def heading_validator(request: HeadingRequest):
    """Validate and optimize heading structure."""
    try:
        soup = BeautifulSoup(request.html_content, "html.parser")
        headings = {f"H{i}": [] for i in range(1, 7)}

        for i in range(1, 7):
            for tag in soup.find_all(f"h{i}"):
                headings[f"H{i}"].append(tag.text.strip())

        issues = []
        if len(headings["H1"]) > 1:
            issues.append("Multiple H1 tags found.")
        if not headings["H1"]:
            issues.append("No H1 tag found.")

        recommendations = [
            "Use exactly one H1 tag per page.",
            "Ensure heading levels are hierarchical and sequential."
        ]

        return HeadingResponse(issues=issues, recommendations=recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating headings: {e}")
