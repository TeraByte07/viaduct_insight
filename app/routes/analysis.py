from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.serpapi_service import SerpService
from app.schemas.analysis_schema import DomainRequest, DomainResponse
from app.core.security import optional_user
from app.utils.rate_limit import check_rate_limit

router = APIRouter(prefix="/analysis", tags=["Domain Analysis"])

@router.post("/serp", response_model=DomainResponse, status_code=status.HTTP_200_OK)
def analyze_domain(
    request: DomainRequest,
    req: Request,
    db: Session = Depends(get_db),
    current_user = Depends(optional_user)
):
    # Step 1: Apply rate limit for guests
    if not current_user:
        ip_address = req.client.host
        check_rate_limit(db, ip_address, "serp_analysis", limit_per_day=3)

    # Step 2: Continue with the main logic
    service = SerpService()
    result = service.analyze_domain(request)
    return result
