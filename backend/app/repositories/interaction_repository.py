from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interaction import Interaction


class InteractionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, interaction: Interaction) -> Interaction:
        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)
        return interaction

    def list_interactions(self) -> list[Interaction]:
        return list(self.db.scalars(select(Interaction).order_by(Interaction.created_at.desc())).all())

    def get_by_id(self, interaction_id: int) -> Interaction | None:
        return self.db.get(Interaction, interaction_id)

    def update(self, interaction: Interaction, payload: dict) -> Interaction:
        for key, value in payload.items():
            setattr(interaction, key, value)
        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)
        return interaction
