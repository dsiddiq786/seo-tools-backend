from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router = APIRouter()

class RobotsTxtRequest(BaseModel):
    disallowed_paths: list[str] = []  # List of disallowed paths
    allowed_paths: list[str] = []  # List of allowed paths

class RobotsTxtResponse(BaseModel):
    robots_txt: str

@router.post("/generate-robots-txt", response_model=RobotsTxtResponse)
def generate_robots_txt(request: RobotsTxtRequest):
    """Generate a robots.txt file."""
    try:
        lines = ["User-agent: *"]
        for path in request.disallowed_paths:
            lines.append(f"Disallow: {path}")
        for path in request.allowed_paths:
            lines.append(f"Allow: {path}")
        robots_txt = "\n".join(lines)
        return RobotsTxtResponse(robots_txt=robots_txt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating robots.txt: {e}")
