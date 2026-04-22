# Task 1 Video Script (10–15 minutes)

## 1. Introduction
- Introduce the assignment and objective.
- Explain that this is an AI-first CRM HCP module for field representatives in life sciences.
- Mention the two input modes: structured form and chat assistant.

## 2. Frontend walkthrough
- Show the dashboard header and stack badges.
- Open Structured Form Mode.
- Explain each input field.
- Submit the form and show the AI-generated output.

## 3. Chat mode walkthrough
- Open Conversational Chat Mode.
- Paste or type a free-text interaction.
- Submit it.
- Show how the assistant converts free text to a structured logged interaction.

## 4. LangGraph agent explanation
- Explain that both form mode and chat mode converge to the same orchestration layer.
- Mention state fields: HCP, notes, summary, topics, next-best-action, follow-up email, compliance.

## 5. Demonstrate the 5 tools
- Fetch HCP Profile Tool
- Log Interaction Tool
- Suggest Next Best Action Tool
- Generate Follow-up Email Tool
- Edit Interaction Tool
- Optionally mention Compliance Guardrail Tool as bonus

## 6. Backend code walkthrough
- Show FastAPI routes.
- Show service layer.
- Show repository layer.
- Show `app/ai/graph.py`.
- Explain how persistence works.

## 7. Architecture summary
- React + Redux frontend
- FastAPI backend
- SQLAlchemy ORM
- LangGraph orchestration
- Groq model integration/fallback strategy

## 8. What I understood
- CRM in life sciences needs accurate HCP tracking.
- AI helps reduce rep effort and improve note quality.
- LangGraph is useful because multiple tool steps happen in sequence.
- Compliance review matters in pharma-facing systems.
