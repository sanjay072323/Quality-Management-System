from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.hcp import HCPRead
from app.services.interaction_service import InteractionService

router = APIRouter()


@router.get("", response_model=list[HCPRead])
def list_hcps(db: Session = Depends(get_db)):
    service = InteractionService(db)
    return service.list_hcps()
