from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import whois

router = APIRouter()

class DomainAvailabilityRequest(BaseModel):
    domain: str = Field(..., title="Domain Name", description="Enter the domain name to check availability.")

class DomainAvailabilityResponse(BaseModel):
    domain: str
    is_available: bool
    registrar: str = None
    expiration_date: str = None

@router.post("/check-domain-availability", response_model=DomainAvailabilityResponse)
def check_domain_availability(request: DomainAvailabilityRequest):
    """Check if a domain name is available."""
    try:
        domain_info = whois.whois(request.domain)
        is_available = domain_info.status is None
        return DomainAvailabilityResponse(
            domain=request.domain,
            is_available=is_available,
            registrar=domain_info.registrar,
            expiration_date=domain_info.expiration_date.isoformat() if domain_info.expiration_date else None
        )
    except Exception as e:
        if "No match for domain" in str(e):
            return DomainAvailabilityResponse(domain=request.domain, is_available=True)
        raise HTTPException(status_code=500, detail=f"Error checking domain availability: {e}")
