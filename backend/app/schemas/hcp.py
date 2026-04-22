from pydantic import BaseModel


class HCPBase(BaseModel):
    full_name: str
    specialty: str
    hospital_name: str
    city: str
    tier: str = "A"
    preferred_channel: str = "In-person"
    notes: str | None = None


class HCPCreate(HCPBase):
    pass


class HCPRead(HCPBase):
    id: int

    model_config = {"from_attributes": True}
