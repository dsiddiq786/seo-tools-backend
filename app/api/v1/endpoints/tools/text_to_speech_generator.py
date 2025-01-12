from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from gtts import gTTS
import base64
import io

router = APIRouter()

class TextToSpeechRequest(BaseModel):
    text: str
    language: str = "en"

class TextToSpeechResponse(BaseModel):
    audio_data: str

@router.post("/text-to-speech", response_model=TextToSpeechResponse)
def generate_speech(request: TextToSpeechRequest):
    """Convert text to speech."""
    try:
        tts = gTTS(text=request.text, lang=request.language)
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        audio_base64 = base64.b64encode(buffer.getvalue()).decode()
        return TextToSpeechResponse(audio_data=f"data:audio/mpeg;base64,{audio_base64}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {e}")
