from __future__ import annotations

from typing import Any, TypedDict

from app.services.llm_service import llm_service


class InteractionGraphState(TypedDict, total=False):
    hcp_id: int
    hcp_name: str
    interaction_type: str
    channel: str
    interaction_date: str
    raw_notes: str
    ai_summary: str
    key_topics: list[str]
    next_best_action: str
    follow_up_email: str
    compliance_status: str
    tool_trace: list[str]


class HCPInteractionAgent:
    def fetch_hcp_profile_tool(self, state: InteractionGraphState) -> InteractionGraphState:
        state.setdefault("tool_trace", []).append("fetch_hcp_profile_tool")
        return state

    def log_interaction_tool(self, state: InteractionGraphState) -> InteractionGraphState:
        state["ai_summary"] = llm_service.summarize_interaction(state["raw_notes"])
        state["key_topics"] = llm_service.extract_topics(state["raw_notes"])
        state.setdefault("tool_trace", []).append("log_interaction_tool")
        return state

    def suggest_next_best_action_tool(self, state: InteractionGraphState) -> InteractionGraphState:
        state["next_best_action"] = llm_service.suggest_next_action(state["raw_notes"])
        state.setdefault("tool_trace", []).append("suggest_next_best_action_tool")
        return state

    def generate_followup_email_tool(self, state: InteractionGraphState) -> InteractionGraphState:
        state["follow_up_email"] = llm_service.generate_followup_email(state["hcp_name"], state["ai_summary"])
        state.setdefault("tool_trace", []).append("generate_followup_email_tool")
        return state

    def compliance_guardrail_tool(self, state: InteractionGraphState) -> InteractionGraphState:
        state["compliance_status"] = llm_service.compliance_review(state["raw_notes"])
        state.setdefault("tool_trace", []).append("compliance_guardrail_tool")
        return state

    def edit_interaction_tool(self, state: InteractionGraphState) -> InteractionGraphState:
        state.setdefault("tool_trace", []).append("edit_interaction_tool")
        return state

    def run(self, payload: dict[str, Any]) -> InteractionGraphState:
        state: InteractionGraphState = {
            "hcp_id": payload["hcp_id"],
            "hcp_name": payload.get("hcp_name", "Doctor"),
            "interaction_type": payload.get("interaction_type", "Visit"),
            "channel": payload.get("channel", "In-person"),
            "interaction_date": payload["interaction_date"],
            "raw_notes": payload["raw_notes"],
            "tool_trace": [],
        }
        state = self.fetch_hcp_profile_tool(state)
        state = self.log_interaction_tool(state)
        state = self.suggest_next_best_action_tool(state)
        state = self.generate_followup_email_tool(state)
        state = self.compliance_guardrail_tool(state)
        return state


hcp_interaction_agent = HCPInteractionAgent()
