from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hcp_id: Mapped[int] = mapped_column(ForeignKey("hcps.id"), nullable=False)
    interaction_type: Mapped[str] = mapped_column(String(50), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    interaction_date: Mapped[str] = mapped_column(String(30), nullable=False)
    raw_notes: Mapped[str] = mapped_column(Text, nullable=False)
    ai_summary: Mapped[str] = mapped_column(Text, nullable=False)
    key_topics: Mapped[str] = mapped_column(Text, default="[]")
    next_best_action: Mapped[str] = mapped_column(Text, nullable=False)
    follow_up_email: Mapped[str | None] = mapped_column(Text, nullable=True)
    compliance_status: Mapped[str] = mapped_column(String(30), default="reviewed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hcp = relationship("HCP")
