from __future__ import annotations

from app.core.settings import settings


class LLMService:
    """
    Keeps the project runnable even without a live API key.
    If a valid Groq key is present, the service can be extended to use ChatGroq directly.
    For assignment/demo readiness, deterministic fallback output is returned.
    """

    def summarize_interaction(self, text: str) -> str:
        excerpt = text.strip().replace("\n", " ")
        excerpt = excerpt[:220] + ("..." if len(excerpt) > 220 else "")
        return f"AI Summary: The representative discussed therapy usage, HCP feedback, objections, and agreed follow-up items. Source notes: {excerpt}"

    def extract_topics(self, text: str) -> list[str]:
        text_lower = text.lower()
        topics = []
        keyword_map = {
            "efficacy": "Efficacy",
            "safety": "Safety",
            "adherence": "Patient Adherence",
            "price": "Pricing",
            "sample": "Sampling Request",
            "outcome": "Clinical Outcomes",
            "availability": "Availability",
            "guideline": "Guideline Alignment",
        }
        for key, label in keyword_map.items():
            if key in text_lower:
                topics.append(label)
        return topics or ["Scientific Discussion", "Follow-up Planning"]

    def suggest_next_action(self, text: str) -> str:
        text_lower = text.lower()
        if "sample" in text_lower:
            return "Arrange approved sample follow-up with medical/commercial compliance review."
        if "price" in text_lower or "cost" in text_lower:
            return "Share approved value communication materials and schedule a budget-impact discussion."
        return "Plan a follow-up visit within 2 weeks and send approved scientific literature relevant to the HCP's questions."

    def generate_followup_email(self, hcp_name: str, summary: str) -> str:
        return (
            f"Subject: Thank you for today’s discussion\n\n"
            f"Dear {hcp_name},\n\n"
            f"Thank you for taking the time to meet today. As discussed, I am sharing the next steps based on our conversation.\n\n"
            f"Summary: {summary}\n\n"
            f"Please let me know a suitable time for a brief follow-up discussion.\n\n"
            f"Best regards,\nField Representative"
        )

    def compliance_review(self, text: str) -> str:
        flagged_terms = ["guaranteed", "cure", "100%", "no side effects"]
        if any(term in text.lower() for term in flagged_terms):
            return "needs_review"
        return "reviewed"


llm_service = LLMService()
