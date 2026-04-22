# AI-First CRM HCP Module — Interview Submission

This repository is a complete assignment-ready submission for the **AI-First CRM HCP Module – Log Interaction Screen** and includes support material for the **QMS Module**.

## What is included

- `frontend/` — React + Redux Toolkit + TypeScript UI
- `backend/` — FastAPI + SQLAlchemy + LangGraph + Groq integration
- `docs/` — architecture notes, demo scripts, API collection, submission checklist
- `task2/` — QMS explanation document, deck, and speaking script

## Task 1 summary

The app gives field representatives two ways to log Healthcare Professional (HCP) interactions:

1. **Structured Form Mode**
2. **Conversational Chat Mode**

Both modes eventually pass through a **LangGraph agent** that standardizes, validates, summarizes, and saves the interaction.

### Minimum 5 LangGraph tools implemented

1. **log_interaction_tool** — normalizes and stores the interaction
2. **edit_interaction_tool** — updates a previously logged interaction
3. **fetch_hcp_profile_tool** — retrieves HCP profile/context
4. **suggest_next_best_action_tool** — recommends follow-up actions for sales reps
5. **generate_followup_email_tool** — drafts a compliant follow-up message
6. **compliance_guardrail_tool** — optional bonus safety tool for compliance checks

## Assignment-fit choices

The assignment explicitly asks for **LangGraph** and a **Groq LLM**. The backend uses LangGraph state + tools and is configured with:

- primary model: `gemma2-9b-it`
- optional fallback: `llama-3.3-70b-versatile`

> Note: Groq later deprecated `gemma2-9b-it` on their platform. For assignment compliance, this repo keeps it as the default env value, but the fallback is documented in `.env.example` and `settings.py`.

## Tech stack

### Frontend
- React 18
- TypeScript
- Redux Toolkit
- React Router
- Axios
- Inter font
- Plain CSS module-style organization for easy interview explanation

### Backend
- FastAPI
- SQLAlchemy
- Pydantic v2
- LangGraph
- LangChain Core / Groq integration
- PostgreSQL or MySQL via SQLAlchemy URL

## Folder structure

```text
frontend/
  src/
    app/
    components/
    features/
    pages/
    services/
    styles/
backend/
  app/
    api/
    core/
    db/
    models/
    repositories/
    schemas/
    services/
    ai/
```

## Core user flow

### Form mode
1. Rep opens HCP Log Interaction screen
2. Rep fills visit details
3. Frontend sends form payload to backend
4. LangGraph standardizes notes, extracts entities, checks gaps, stores interaction
5. UI shows summary, compliance notes, and next-best-action suggestions

### Chat mode
1. Rep opens conversational assistant
2. Rep types free-form visit notes
3. LLM + LangGraph extract structured fields from chat
4. Tools are invoked to fetch HCP details, validate data, log interaction, and suggest follow-up
5. UI displays final saved record and action recommendations

## Demo script for video

Use the file:
- `docs/TASK1_VIDEO_SCRIPT.md`

It gives a clean 10–15 minute walkthrough sequence.

## Local setup

### 1) Clone repo
```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2) Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### 3) Frontend setup
```bash
cd frontend
npm install
npm run dev
```

## Environment variables

See:
- `backend/.env.example`
- `frontend/.env.example`

Important backend vars:

```env
APP_NAME=AI First CRM HCP Module
ENVIRONMENT=development
DATABASE_URL=sqlite:///./crm_hcp.db
GROQ_API_KEY=replace_me
GROQ_MODEL=gemma2-9b-it
GROQ_FALLBACK_MODEL=llama-3.3-70b-versatile
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Database note

The repository is assignment-friendly and defaults to SQLite for easy demo, but the architecture is compatible with **PostgreSQL/MySQL**. For strict assignment submission, mention in the video that the ORM layer supports SQL engines and production deployment should use Postgres.

## API overview

- `GET /api/v1/health`
- `GET /api/v1/hcps`
- `POST /api/v1/interactions/form`
- `POST /api/v1/interactions/chat`
- `PUT /api/v1/interactions/{interaction_id}`
- `GET /api/v1/interactions`
- `GET /api/v1/interactions/{interaction_id}`
- `POST /api/v1/agent/tools/demo`

## Architecture highlights to say in interview

- **AI-first, not AI-added**: both input modes converge into an AI orchestration flow
- **LangGraph stateful workflow**: request → extraction → tool invocation → validation → persistence → action recommendations
- **Separation of concerns**: API, schemas, repositories, services, AI graph, and UI state are isolated
- **Compliance-aware**: a guardrail tool reviews promotional wording, missing follow-up fields, and suspicious claims
- **Field rep usability**: rep can either fill a form quickly or just talk/type naturally

## Task 2 support files

Inside `task2/`:
- `QMS_Module_Explainer.docx`
- `QMS_Module_Deck.pptx`
- `QMS_VIDEO_SCRIPT.md`

These are support materials to help you present the non-technical round clearly.

## Submission checklist

- Push this repo to GitHub
- Add your video links/files separately in the form
- Submit Task 1 and Task 2 separately per the assignment form
- Use `docs/SUBMISSION_CHECKLIST.md`

## What to say if asked “why LangGraph?”

LangGraph is a good fit because the assignment needs more than one prompt call. It needs a stateful flow that can:
- keep track of the interaction state,
- decide which tool to run,
- support editing and re-logging,
- save tool outputs,
- and provide transparent orchestration across form and chat modes.

## Final note

This repository is intentionally written in a way that is easy to explain in an interview. It prioritizes:
- clean folder structure
- understandable code flow
- assignment coverage
- demo readiness

