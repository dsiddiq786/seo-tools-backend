from fastapi import APIRouter
from app.api.v1.endpoints import auth, users
from app.api.v1.endpoints.tools import (
    text_analysis,
    keyword_analysis,
    backlink_analysis,
    keyword_finder,
    meta_tag_generator,
    title_optimizer,
    word_counter,
    content_summary,
    slug_generator,
    read_time_estimator,
    url_validator,
    case_converter,
    serp_simulator,        # Newly added
    plagiarism_checker,    # Newly added
    heading_validator,     # Newly added
    keyword_density_analyzer,  # Newly added
    page_speed_parser      # Newly added
)


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(text_analysis.router, prefix="/tools/text", tags=["Text Tools"])

api_router.include_router(backlink_analysis.router, prefix="/tools/backlinks", tags=["Backlink Tools"])

api_router.include_router(keyword_analysis.router, prefix="/tools/keywords", tags=["Keyword Tools"])
api_router.include_router(keyword_finder.router, prefix="/tools/keyword-finder", tags=["Keyword Tools"])

api_router.include_router(meta_tag_generator.router, prefix="/tools/meta-tags", tags=["Meta Tag Generator"])
api_router.include_router(title_optimizer.router, prefix="/tools/title-optimizer", tags=["Title Optimizer"])
api_router.include_router(word_counter.router, prefix="/tools/word-counter", tags=["Word Counter"])

api_router.include_router(content_summary.router, prefix="/tools/content-summary", tags=["Content Summary"])
api_router.include_router(slug_generator.router, prefix="/tools/slug-generator", tags=["Slug Generator"])
api_router.include_router(read_time_estimator.router, prefix="/tools/read-time", tags=["Read Time Estimator"])
api_router.include_router(url_validator.router, prefix="/tools/url-validator", tags=["URL Validator"])
api_router.include_router(case_converter.router, prefix="/tools/case-converter", tags=["Case Converter"])


api_router.include_router(serp_simulator.router, prefix="/tools", tags=["SERP Simulator"])
api_router.include_router(plagiarism_checker.router, prefix="/tools", tags=["Text Tools"])
api_router.include_router(heading_validator.router, prefix="/tools", tags=["Heading Validator"])
api_router.include_router(keyword_density_analyzer.router, prefix="/tools", tags=["Keyword Tools"])
api_router.include_router(page_speed_parser.router, prefix="/tools", tags=["Page Speed Metrics Parser"])