from pydantic import BaseModel, Field

class KeywordAnalysisRequest(BaseModel):
    content: str = Field(..., title="Input Text", description="Provide the text to analyze keywords.")
    purpose: str = Field(..., title="Purpose", description="Purpose for keyword extraction (e.g., Social Media, SEO)", example="SEO")

class KeywordResponse(BaseModel):
    keyword: str
    volume: int
    competition: int
    kei: int
    no_click_searches: int

class KeywordAnalysisResponse(BaseModel):
    keywords: list[KeywordResponse]

class KeywordFinderRequest(BaseModel):
    query: str = Field(..., title="Keyword or Domain", description="Enter a keyword or domain to find related keywords.")

class KeywordFinderResponse(BaseModel):
    keywords: list[KeywordResponse]