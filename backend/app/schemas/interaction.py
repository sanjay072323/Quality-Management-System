from pydantic import BaseModel, Field


class InteractionFormRequest(BaseModel):
    hcp_id: int
    interaction_type: str = Field(..., examples=["Visit", "Call"])
    channel: str = Field(..., examples=["In-person", "Phone", "Email"])
    interaction_date: str
    raw_notes: str


class InteractionChatRequest(BaseModel):
    hcp_id: int
    transcript: str
    interaction_date: str


class InteractionUpdateRequest(BaseModel):
    interaction_type: str | None = None
    channel: str | None = None
    interaction_date: str | None = None
    raw_notes: str | None = None


class InteractionResponse(BaseModel):
    id: int
    hcp_id: int
    interaction_type: str
    channel: str
    interaction_date: str
    raw_notes: str
    ai_summary: str
    key_topics: str
    next_best_action: str
    follow_up_email: str | None = None
    compliance_status: str

    model_config = {"from_attributes": True}


class AgentDemoRequest(BaseModel):
    hcp_id: int
    transcript: str
