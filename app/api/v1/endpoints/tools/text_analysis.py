# from app.schemas.text_analysis import SentimentRequest, SentimentResponse, ReadabilityRequest, ReadabilityResponse
# from fastapi import APIRouter, HTTPException
# from app.helpers.common import count_syllables
# from textblob import TextBlob
# import re

# router = APIRouter()

# @router.post("/analyze-sentiment", response_model=SentimentResponse)
# def analyze_sentiment(request: SentimentRequest):
#     """Analyze the sentiment of a given text with a 500-word limit."""
#     try:
#         # Limit text to 500 words
#         words = request.content.split()
#         truncated_text = " ".join(words[:500])

#         # Analyze sentiment
#         blob = TextBlob(truncated_text)
#         sentiment = blob.sentiment

#         # Convert polarity to percentage
#         normalized_score = round(sentiment.polarity * 100, 2)  # Scale: -100 to 100

#         # Interpret polarity
#         if normalized_score > 50:
#             sentiment_description = (
#                 "The text exudes a strongly positive vibe, conveying optimism and enthusiasm."
#             )
#         elif normalized_score > 0:
#             sentiment_description = (
#                 "The text reflects a mildly positive sentiment, evoking warmth and subtle excitement."
#             )
#         elif normalized_score == 0:
#             sentiment_description = (
#                 "The text carries a neutral tone, presenting information without emotional weight."
#             )
#         elif normalized_score > -50:
#             sentiment_description = (
#                 "The text has a slightly negative undertone, suggesting seriousness or mild concern."
#             )
#         else:
#             sentiment_description = (
#                 "The text expresses a strongly negative sentiment, conveying dissatisfaction or critical intensity."
#             )

#         # Generate detailed output
#         result_description = (
#             f"This text has a sentiment score of {normalized_score}. {sentiment_description}"
#         )

#         return SentimentResponse(
#             sentiment_score=normalized_score,
#             sentiment_description=result_description,
#             truncated_text=truncated_text,
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {e}")


# @router.post("/check-readability", response_model=ReadabilityResponse)
# def readability_checker(request: ReadabilityRequest):
#     """Check the readability of the provided text."""
#     try:
#         content = request.content

#         # Split into sentences and words
#         sentences = re.split(r'[.!?]', content)
#         sentences = [s.strip() for s in sentences if s.strip()]
#         words = re.findall(r'\w+', content)

#         # Count syllables
#         syllables = sum(count_syllables(word) for word in words)

#         # Calculate Flesch Reading Ease score
#         total_sentences = len(sentences)
#         total_words = len(words)
#         readability_score = (
#             206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (syllables / total_words)
#         )

#         # Map readability score to grade level
#         if readability_score >= 90:
#             grade_level = "Grade 5"
#         elif readability_score >= 80:
#             grade_level = "Grade 6"
#         elif readability_score >= 70:
#             grade_level = "Grade 7"
#         elif readability_score >= 60:
#             grade_level = "Grade 8-9"
#         elif readability_score >= 50:
#             grade_level = "Grade 10-12"
#         elif readability_score >= 30:
#             grade_level = "College"
#         else:
#             grade_level = "College Graduate"

#         # Analyze sentence difficulty
#         very_hard_sentences_list = []
#         hard_sentences_list = []
#         for sentence in sentences:
#             words_in_sentence = re.findall(r'\w+', sentence)
#             syllables_in_sentence = sum(count_syllables(word) for word in words_in_sentence)
#             if len(words_in_sentence) > 25 or syllables_in_sentence / len(words_in_sentence) > 2.0:
#                 very_hard_sentences_list.append(sentence)
#             elif len(words_in_sentence) > 15:
#                 hard_sentences_list.append(sentence)

#         # Recommendations
#         recommendations = (
#             "Shorten sentences, simplify vocabulary, and reduce the use of complex phrases "
#             "to improve readability."
#         )

#         return ReadabilityResponse(
#             readability_score=round(readability_score, 2),
#             grade_level=grade_level,
#             total_sentences=total_sentences,
#             very_hard_sentences=len(very_hard_sentences_list),
#             hard_sentences=len(hard_sentences_list),
#             very_hard_sentences_list=very_hard_sentences_list,
#             hard_sentences_list=hard_sentences_list,
#             recommendations=recommendations,
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error calculating readability: {e}")
