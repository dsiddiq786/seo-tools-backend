from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import xmltodict
import json

router = APIRouter()

class XMLToJSONRequest(BaseModel):
    xml_data: str

class XMLToJSONResponse(BaseModel):
    json_data: dict

@router.post("/convert-xml-to-json", response_model=XMLToJSONResponse)
def convert_xml_to_json(request: XMLToJSONRequest):
    """Convert XML data to JSON."""
    try:
        json_data = json.loads(json.dumps(xmltodict.parse(request.xml_data)))
        return XMLToJSONResponse(json_data=json_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting XML to JSON: {e}")
