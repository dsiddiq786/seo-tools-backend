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
    page_speed_parser,      # Newly added
    grammar_checker,
    content_similarity,
    readability_suggestions,
    sentence_rephraser,
    content_performance,
    image_alt_text_generator,  # New
    content_tone_checker,      # New
    broken_link_checker,       # New
    readability_insights,      # New
    keyword_trends_tracker,     # New
    image_resizer,
    favicon_generator,
    image_converter,
    qr_code_generator,
    robots_txt_generator,
    open_graph_generator,
    password_strength_checker,
    pdf_to_image_converter,
    json_validator,
    xml_to_json_converter,
    text_to_speech_generator,
    html_minifier,
    css_minifier_tool,  # New
    image_metadata_extractor,  # New
    seo_meta_description_generator,  # New
    domain_availability_checker,  # New
    youtube_thumbnail_downloader  # New
)

api_router = APIRouter()

# Authentication and User Management
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Text Tools
api_router.include_router(text_analysis.router, prefix="/tools/text", tags=["Text Tools"])
api_router.include_router(content_summary.router, prefix="/tools/content-summary", tags=["Text Tools"])
api_router.include_router(sentence_rephraser.router, prefix="/tools/sentence-rephraser", tags=["Text Tools"])
api_router.include_router(content_tone_checker.router, prefix="/tools/content-tone", tags=["Text Tools"])
api_router.include_router(plagiarism_checker.router, prefix="/tools/plagiarism", tags=["Text Tools"])
api_router.include_router(readability_suggestions.router, prefix="/tools/readability-suggestions", tags=["Text Tools"])
api_router.include_router(content_similarity.router, prefix="/tools/content-similarity", tags=["Text Tools"])
api_router.include_router(grammar_checker.router, prefix="/tools/grammar-checker", tags=["Text Tools"])

# Keyword Tools
api_router.include_router(keyword_analysis.router, prefix="/tools/keywords", tags=["Keyword Tools"])
api_router.include_router(keyword_finder.router, prefix="/tools/keyword-finder", tags=["Keyword Tools"])
api_router.include_router(keyword_density_analyzer.router, prefix="/tools/keyword-density", tags=["Keyword Tools"])
api_router.include_router(keyword_trends_tracker.router, prefix="/tools/keyword-trends", tags=["Keyword Tools"])

# Backlink Tools
api_router.include_router(backlink_analysis.router, prefix="/tools/backlinks", tags=["Backlink Tools"])

# SEO Tools
api_router.include_router(meta_tag_generator.router, prefix="/tools/meta-tags", tags=["SEO Tools"])
api_router.include_router(title_optimizer.router, prefix="/tools/title-optimizer", tags=["SEO Tools"])
api_router.include_router(seo_meta_description_generator.router, prefix="/tools/meta-description", tags=["SEO Tools"])
api_router.include_router(robots_txt_generator.router, prefix="/tools/robots-txt", tags=["SEO Tools"])
api_router.include_router(open_graph_generator.router, prefix="/tools/open-graph", tags=["SEO Tools"])
api_router.include_router(serp_simulator.router, prefix="/tools/serp-simulator", tags=["SEO Tools"])
api_router.include_router(page_speed_parser.router, prefix="/tools/page-speed", tags=["SEO Tools"])

# Image Tools
api_router.include_router(image_resizer.router, prefix="/tools/image-resizer", tags=["Image Tools"])
api_router.include_router(image_converter.router, prefix="/tools/image-converter", tags=["Image Tools"])
api_router.include_router(favicon_generator.router, prefix="/tools/favicon-generator", tags=["Image Tools"])
# api_router.include_router(image_alt_text_generator.router, prefix="/tools/image-alt-text", tags=["Image Tools"])
api_router.include_router(image_metadata_extractor.router, prefix="/tools/image-metadata", tags=["Image Tools"])

# Utility Tools
api_router.include_router(word_counter.router, prefix="/tools/word-counter", tags=["Utility Tools"])
api_router.include_router(slug_generator.router, prefix="/tools/slug-generator", tags=["Utility Tools"])
api_router.include_router(read_time_estimator.router, prefix="/tools/read-time", tags=["Utility Tools"])
api_router.include_router(url_validator.router, prefix="/tools/url-validator", tags=["Utility Tools"])
api_router.include_router(case_converter.router, prefix="/tools/case-converter", tags=["Utility Tools"])
api_router.include_router(qr_code_generator.router, prefix="/tools/qr-code-generator", tags=["Utility Tools"])
api_router.include_router(html_minifier.router, prefix="/tools/html-minifier", tags=["Utility Tools"])
api_router.include_router(css_minifier_tool.router, prefix="/tools/css-minifier", tags=["Utility Tools"])
api_router.include_router(json_validator.router, prefix="/tools/json-validator", tags=["Utility Tools"])
api_router.include_router(xml_to_json_converter.router, prefix="/tools/xml-to-json", tags=["Utility Tools"])
api_router.include_router(text_to_speech_generator.router, prefix="/tools/text-to-speech", tags=["Utility Tools"])
api_router.include_router(pdf_to_image_converter.router, prefix="/tools/pdf-to-image", tags=["Utility Tools"])
api_router.include_router(domain_availability_checker.router, prefix="/tools/domain-availability", tags=["Utility Tools"])
api_router.include_router(youtube_thumbnail_downloader.router, prefix="/tools/youtube-thumbnail", tags=["Utility Tools"])

api_router.include_router(password_strength_checker.router, prefix="/tools/password-checker", tags=["Passwords"])

# Content Performance Tools
api_router.include_router(content_performance.router, prefix="/tools/content-performance", tags=["Content Performance"])

# Website Analysis Tools
api_router.include_router(broken_link_checker.router, prefix="/tools/broken-link-checker", tags=["Website Analysis"])
api_router.include_router(readability_insights.router, prefix="/tools/readability-insights", tags=["Website Analysis"])
