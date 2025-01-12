from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router = APIRouter()

class OpenGraphRequest(BaseModel):
    title: str
    description: str
    image_url: str
    site_name: str
    url: str

class OpenGraphResponse(BaseModel):
    open_graph_tags: str

@router.post("/generate-open-graph", response_model=OpenGraphResponse)
def generate_open_graph(request: OpenGraphRequest):
    """Generate Open Graph meta tags."""
    try:
        tags = [
            f'<meta property="og:title" content="{request.title}" />',
            f'<meta property="og:description" content="{request.description}" />',
            f'<meta property="og:image" content="{request.image_url}" />',
            f'<meta property="og:site_name" content="{request.site_name}" />',
            f'<meta property="og:url" content="{request.url}" />',
        ]
        return OpenGraphResponse(open_graph_tags="\n".join(tags))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Open Graph tags: {e}")
