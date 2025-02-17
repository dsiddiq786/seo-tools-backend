# import requests
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel, Field
# from bs4 import BeautifulSoup

# router = APIRouter()

# class PlagiarismRequest(BaseModel):
#     content: str = Field(..., title="Content", description="Text content to check for plagiarism.")

# class PlagiarismResponse(BaseModel):
#     matches: list

# @router.post("/plagiarism-checker", response_model=PlagiarismResponse)
# def plagiarism_checker(request: PlagiarismRequest):
#     """Check for plagiarism in the provided content."""
#     try:
#         search_url = f"https://www.google.com/search?q={'+'.join(request.content.split()[:10])}"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
#         }
#         response = requests.get(search_url, headers=headers)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         matches = []
#         for link in soup.find_all("a"):
#             href = link.get("href")
#             if "http" in href and "google" not in href:
#                 matches.append(href)

#         return PlagiarismResponse(matches=matches)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error checking plagiarism: {e}")
