# backend/app/api/routes/interactions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.graph import hcp_interaction_agent
from app.db.session import get_db
from app.schemas.interaction import (
    AgentDemoRequest,
    InteractionChatRequest,
    InteractionFormRequest,
    InteractionResponse,
    InteractionUpdateRequest,
)
from app.services.interaction_service import InteractionService

router = APIRouter()


@router.get("", response_model=list[InteractionResponse])
def list_interactions(db: Session = Depends(get_db)):
    return InteractionService(db).list_interactions()


@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    item = InteractionService(db).get_interaction(interaction_id)
    if not item:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return item


@router.post("/form", response_model=InteractionResponse)
def create_form_interaction(payload: InteractionFormRequest, db: Session = Depends(get_db)):
    try:
        return InteractionService(db).create_from_form(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/chat", response_model=InteractionResponse)
def create_chat_interaction(payload: InteractionChatRequest, db: Session = Depends(get_db)):
    try:
        return InteractionService(db).create_from_chat(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(interaction_id: int, payload: InteractionUpdateRequest, db: Session = Depends(get_db)):
    try:
        return InteractionService(db).update_interaction(interaction_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/agent/tools/demo")
def demo_tools(payload: AgentDemoRequest, db: Session = Depends(get_db)):
    service = InteractionService(db)
    hcp = service.hcp_repo.get_by_id(payload.hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")

    state = hcp_interaction_agent.run(
        {
            "hcp_id": payload.hcp_id,
            "hcp_name": hcp.full_name,
            "interaction_date": "2026-04-22",
            "raw_notes": payload.transcript,
        }
    )
    return state