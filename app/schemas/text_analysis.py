from pydantic import BaseModel, Field

# Request Body Model with Swagger customization
class SentimentRequest(BaseModel):
    content: str = Field(..., title="Input Text", description="Provide the text to analyze", example="FastAPI is an amazing framework!")

# Response Model
class SentimentResponse(BaseModel):
    sentiment_score: float
    sentiment_description: str
    truncated_text: str

# Request Body Model
class ReadabilityRequest(BaseModel):
    content: str = Field(
        ..., title="Input Text", description="Provide the text to analyze for readability.", example="This is a sample text for readability testing."
    )

# Response Model
class ReadabilityResponse(BaseModel):
    readability_score: float
    grade_level: str
    total_sentences: int
    very_hard_sentences: int
    hard_sentences: int
    very_hard_sentences_list: list[str]  # New field
    hard_sentences_list: list[str]  # New field
    recommendations: str