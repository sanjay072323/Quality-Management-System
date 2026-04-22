# Architecture Notes

## Why this design
The assignment asks for a system that is useful to a life sciences field representative. That means the system should not only store notes, but also help the rep capture interactions in a cleaner, faster, and more actionable way.

## Major blocks
- React UI for rep-facing screens
- Redux store for predictable state handling
- FastAPI backend for APIs
- LangGraph orchestration for AI workflow control
- SQLAlchemy persistence layer for SQL databases
- Groq-compatible model layer for summarization and action support

## AI flow
1. Receive form payload or chat payload
2. Fetch HCP context
3. Summarize and standardize notes
4. Extract key topics
5. Suggest next best action
6. Draft follow-up email
7. Run compliance guardrail
8. Save final interaction

## Why this is AI-first
The AI is not a side feature. It is central to the logging workflow. The system is designed so that free text can become high-quality CRM data with minimal manual cleanup.
