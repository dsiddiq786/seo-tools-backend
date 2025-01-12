from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import qrcode
import io
import base64

router = APIRouter()

class QRCodeRequest(BaseModel):
    url: str = Field(None, title="URL", description="Provide a URL to generate a QR code for.")
    title: str = Field(None, title="Title", description="Provide a title to include in the QR code.")
    custom_data: str = Field(None, title="Custom Data", description="Provide any custom data to include in the QR code.")

class QRCodeResponse(BaseModel):
    message: str
    qr_code_image: str

@router.post("/generate-qr-code", response_model=QRCodeResponse)
def generate_qr_code(request: QRCodeRequest):
    """Generate a QR code from the given data."""
    try:
        # Aggregate data for QR code
        data_parts = []
        if request.url:
            data_parts.append(f"URL: {request.url}")
        if request.title:
            data_parts.append(f"Title: {request.title}")
        if request.custom_data:
            data_parts.append(f"Custom Data: {request.custom_data}")

        if not data_parts:
            raise HTTPException(status_code=400, detail="At least one field (URL, Title, or Custom Data) must be provided.")

        aggregated_data = "\n".join(data_parts)

        # Create the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(aggregated_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        return QRCodeResponse(
            message="QR Code generated successfully",
            qr_code_image=f"data:image/png;base64,{qr_code_base64}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating QR code: {e}")
