from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from app.api.v1.routers import api_router
from app.core.token_limiter import TokenLimiterMiddleware
from app.db.session import engine
from app.db.models.user import Base

# Create tables in the database (best moved to database.py for separation of concerns)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="SEO Tools Platform", debug=True)

# OAuth2 Setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Middleware: Apply TokenLimiterMiddleware
app.add_middleware(TokenLimiterMiddleware)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the SEO Tools Platform"}

# Routes
app.include_router(api_router)

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
