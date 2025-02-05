from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.v1.routers import api_router
from app.core.token_limiter import TokenLimiterMiddleware
from app.db.session import engine
from app.db.models.user import Base
import torch
import os
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForSequenceClassification
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="SEO Tools Platform", debug=True)

# Middleware
app.add_middleware(TokenLimiterMiddleware)

# ✅ Cache Directory Path
# CACHE_DIR = "./cache"

# # ✅ Function to Load Models If Not Cached
# def load_model_if_not_cached(model_name, model_type):
#     """Load model from cache, if missing, download it."""
#     model_path = os.path.join(CACHE_DIR, model_name.replace("/", "_"))

#     if os.path.exists(model_path):
#         print(f"✅ Found cached model: {model_name}, loading from cache...")
#     else:
#         print(f"🚀 Model {model_name} not found in cache. Downloading now...")

#     if model_type == "pipeline":
#         return pipeline("text2text-generation", model=model_name, cache_dir=CACHE_DIR)
#     elif model_type == "classification":
#         return pipeline("text-classification", model=model_name, cache_dir=CACHE_DIR)
#     elif model_type == "image":
#         return pipeline("image-to-text", model=model_name, model_kwargs={"cache_dir": CACHE_DIR})

#     elif model_type == "embedding":
#         return SentenceTransformer(model_name, cache_folder=CACHE_DIR)
#     else:
#         tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=CACHE_DIR)
#         model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=CACHE_DIR)
#         return tokenizer, model

# # ✅ Load Models Once at Startup
# @app.on_event("startup")
# async def load_models():
#     print("🔄 Loading all models from cache if available...")

#     model_paths = {
#         "keyword_analysis": ("facebook/bart-large-mnli", "classification"),
#         "text_analysis": ("bert-base-uncased", "classification"),
#         "plagiarism_checker": ("sentence-transformers/paraphrase-mpnet-base-v2", "embedding"),
#         "tone_analysis": ("facebook/bart-large-mnli", "classification"),
#         "image_captioning": ("nlpconnect/vit-gpt2-image-captioning", "image"),
#         "paraphrasing": ("t5-small", "pipeline"),
#         "meta_description": ("t5-small", "pipeline"),
#     }

#     app.state.models = {}
#     app.state.tokenizers = {}
#     app.state.pipelines = {}

#     for tool, (model_name, model_type) in model_paths.items():
#         if model_type in ["pipeline", "classification", "image", "embedding"]:
#             app.state.pipelines[tool] = load_model_if_not_cached(model_name, model_type)
#         else:
#             tokenizer, model = load_model_if_not_cached(model_name, model_type)
#             app.state.tokenizers[tool] = tokenizer
#             app.state.models[tool] = model

#     # Load other tools
#     app.state.sentiment_analyzer = SentimentIntensityAnalyzer()
#     app.state.vectorizer = TfidfVectorizer()
#     app.state.summarizer = LsaSummarizer()

#     # ✅ Ensure NLTK Punkt tokenizer is installed only once
#     nltk_path = os.path.join(CACHE_DIR, "nltk_data")
#     if not os.path.exists(nltk_path):
#         os.makedirs(nltk_path)
#         nltk.download("punkt", download_dir=nltk_path)  # ✅ Ensures it's only downloaded once
#     nltk.data.path.append(nltk_path)

#     torch.set_grad_enabled(False)  # Disable gradients for faster inference
#     print("✅ All models loaded successfully!")

# ✅ Register API Routes
app.include_router(api_router)

# ✅ Define an endpoint to check model status
@app.get("/status")
async def check_status():
    return {"message": "Models are loaded and API is ready!"}


# Custom OpenAPI Setup
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SEO Tools Platform",
        version="1.0.0",
        description="API documentation for the SEO Tools Platform",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
