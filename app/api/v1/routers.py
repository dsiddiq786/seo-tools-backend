from fastapi import APIRouter
from app.api.v1.endpoints import auth, users
from app.api.v1.endpoints.tools import text_analysis, keyword_analysis, backlink_analysis,keyword_finder

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(text_analysis.router, prefix="/tools/text", tags=["Text Tools"])

api_router.include_router(backlink_analysis.router, prefix="/tools/backlinks", tags=["Backlink Tools"])

api_router.include_router(keyword_analysis.router, prefix="/tools/keywords", tags=["Keyword Tools"])
api_router.include_router(keyword_finder.router, prefix="/tools/keyword-finder", tags=["Keyword Tools"])