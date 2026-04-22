from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HCP(Base):
    __tablename__ = "hcps"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    specialty: Mapped[str] = mapped_column(String(120), nullable=False)
    hospital_name: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    tier: Mapped[str] = mapped_column(String(20), default="A")
    preferred_channel: Mapped[str] = mapped_column(String(50), default="In-person")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
