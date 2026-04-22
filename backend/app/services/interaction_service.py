from __future__ import annotations
import json
from sqlalchemy.orm import Session

from app.ai.graph import hcp_interaction_agent
from app.models.interaction import Interaction
from app.repositories.hcp_repository import HCPRepository
from app.repositories.interaction_repository import InteractionRepository
from app.schemas.interaction import (
    InteractionChatRequest,
    InteractionFormRequest,
    InteractionUpdateRequest,
)


def clean_ai_summary(text: str) -> str:
    if not text:
        return ""

    cleaned = text.strip()

    if cleaned.startswith("AI Summary:"):
        cleaned = cleaned.replace("AI Summary:", "", 1).strip()

    if "Source notes:" in cleaned:
        cleaned = cleaned.split("Source notes:")[0].strip()

    return cleaned


def clean_follow_up_email(email: str, cleaned_summary: str, hcp_name: str) -> str:
    if not email:
        return f"""Dear Dr. {hcp_name},

Thank you for taking the time to meet today.

Summary:
{cleaned_summary}

Please let me know a suitable time for a brief follow-up discussion.

Best regards,
Field Representative"""

    cleaned = email.strip()

    cleaned = cleaned.replace("Summary: AI Summary:", "Summary:")
    cleaned = cleaned.replace("AI Summary:", "")

    if "Source notes:" in cleaned:
        before, _sep, _after = cleaned.partition("Source notes:")
        if "Summary:" in before:
            cleaned = before.rstrip() + f"\n\nPlease let me know a suitable time for a brief follow-up discussion.\n\nBest regards,\nField Representative"

    return cleaned


class InteractionService:
    def _init_(self, db: Session):
        self.db = db
        self.hcp_repo = HCPRepository(db)
        self.interaction_repo = InteractionRepository(db)

    def list_hcps(self):
        self.hcp_repo.seed_if_empty()
        return self.hcp_repo.list_hcps()

    def list_interactions(self):
        return self.interaction_repo.list_interactions()

    def get_interaction(self, interaction_id: int):
        return self.interaction_repo.get_by_id(interaction_id)

    def create_from_form(self, payload: InteractionFormRequest) -> Interaction:
        hcp = self.hcp_repo.get_by_id(payload.hcp_id)
        if not hcp:
            raise ValueError("HCP not found")

        result = hcp_interaction_agent.run(
            {
                "hcp_id": payload.hcp_id,
                "hcp_name": hcp.full_name,
                "interaction_type": payload.interaction_type,
                "channel": payload.channel,
                "interaction_date": payload.interaction_date,
                "raw_notes": payload.raw_notes,
            }
        )

        cleaned_summary = clean_ai_summary(result["ai_summary"])
        cleaned_email = clean_follow_up_email(
            result.get("follow_up_email", ""),
            cleaned_summary,
            hcp.full_name,
        )

        interaction = Interaction(
            hcp_id=payload.hcp_id,
            interaction_type=payload.interaction_type,
            channel=payload.channel,
            interaction_date=payload.interaction_date,
            raw_notes=payload.raw_notes,
            ai_summary=cleaned_summary,
            key_topics=json.dumps(result["key_topics"]),
            next_best_action=result["next_best_action"],
            follow_up_email=cleaned_email,
            compliance_status=result["compliance_status"],
        )
        return self.interaction_repo.create(interaction)

    def create_from_chat(self, payload: InteractionChatRequest) -> Interaction:
        hcp = self.hcp_repo.get_by_id(payload.hcp_id)
        if not hcp:
            raise ValueError("HCP not found")

        inferred_channel = "Chat Assistant"
        inferred_type = "Discussion"

        result = hcp_interaction_agent.run(
            {
                "hcp_id": payload.hcp_id,
                "hcp_name": hcp.full_name,
                "interaction_type": inferred_type,
                "channel": inferred_channel,
                "interaction_date": payload.interaction_date,
                "raw_notes": payload.transcript,
            }
        )

        cleaned_summary = clean_ai_summary(result["ai_summary"])
        cleaned_email = clean_follow_up_email(
            result.get("follow_up_email", ""),
            cleaned_summary,
            hcp.full_name,
        )

        interaction = Interaction(
            hcp_id=payload.hcp_id,
            interaction_type=inferred_type,
            channel=inferred_channel,
            interaction_date=payload.interaction_date,
            raw_notes=payload.transcript,
            ai_summary=cleaned_summary,
            key_topics=json.dumps(result["key_topics"]),
            next_best_action=result["next_best_action"],
            follow_up_email=cleaned_email,
            compliance_status=result["compliance_status"],
        )
        return self.interaction_repo.create(interaction)

    def update_interaction(self, interaction_id: int, payload: InteractionUpdateRequest) -> Interaction:
        interaction = self.interaction_repo.get_by_id(interaction_id)
        if not interaction:
            raise ValueError("Interaction not found")

        raw_notes = payload.raw_notes or interaction.raw_notes

        state = hcp_interaction_agent.run(
            {
                "hcp_id": interaction.hcp_id,
                "hcp_name": interaction.hcp.full_name if interaction.hcp else "Doctor",
                "interaction_type": payload.interaction_type or interaction.interaction_type,
                "channel": payload.channel or interaction.channel,
                "interaction_date": payload.interaction_date or interaction.interaction_date,
                "raw_notes": raw_notes,
            }
        )
        state = hcp_interaction_agent.edit_interaction_tool(state)

        cleaned_summary = clean_ai_summary(state["ai_summary"])
        cleaned_email = clean_follow_up_email(
            state.get("follow_up_email", ""),
            cleaned_summary,
            interaction.hcp.full_name if interaction.hcp else "Doctor",
        )

        updated_values = {
            "interaction_type": payload.interaction_type or interaction.interaction_type,
            "channel": payload.channel or interaction.channel,
            "interaction_date": payload.interaction_date or interaction.interaction_date,
            "raw_notes": raw_notes,
            "ai_summary": cleaned_summary,
            "key_topics": json.dumps(state["key_topics"]),
            "next_best_action": state["next_best_action"],
            "follow_up_email": cleaned_email,
            "compliance_status": state["compliance_status"],
        }
        return self.interaction_repo.update(interaction, updated_values)