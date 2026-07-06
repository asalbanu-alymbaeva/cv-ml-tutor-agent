# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

CV/ML Tutor — a Django web app that answers student questions about Computer Vision and Machine Learning using the Groq API (`llama-3.3-70b-versatile`). All responses are generated in Uzbek. There is a single Django app, `tutor`, with no models/database usage beyond the default Django scaffolding (`tutor/models.py` is empty).

## Commands

```
# Activate the existing virtualenv (already created at ./venv)
venv\Scripts\Activate.ps1

# Run the dev server
python manage.py runserver

# Apply/create migrations (only default Django app tables exist today)
python manage.py migrate
python manage.py makemigrations

# Manually exercise the 3-agent chain from the CLI (bypasses Django/HTTP)
python test_agents.py
```

There is no test suite wired up (`tutor/tests.py` is the empty Django stub) and no `requirements.txt` — dependencies (`django`, `groq`, `python-dotenv`) are installed directly into `venv`.

## Architecture

**Request flow**: `cvtutor_project/urls.py` → includes `tutor/urls.py` → single route `""` → `tutor/views.py:chat_view`. The view is a plain form-POST handler (no JS/AJAX, no API endpoints) that renders `tutor/templates/tutor/chat.html` with the question/answer/error in context.

**Agent chain** (`tutor/services.py`) is the core of the app: a single user question is passed through three sequential Groq chat-completion calls, each with a distinct system prompt, via the shared `call_agent(system_prompt, user_message)` helper:

1. **Planner** (`PLANNER_PROMPT`) — classifies the topic/sub-topic, estimates the student's level, and extracts 2-3 key points to cover. Output is plain structured text, not JSON.
2. **Explainer** (`EXPLAINER_PROMPT`) — takes the original question + the planner's output and writes a ~150-200 word explanation in simple language with an analogy.
3. **Reviewer** (`REVIEWER_PROMPT`) — takes the explainer's draft, fixes technical errors, simplifies, and appends one mini-quiz question. Returns the final answer as Markdown.

`get_tutor_response(user_question)` orchestrates all three calls and returns `{"plan", "draft", "final"}`; `chat_view` only surfaces `final` to the template. When modifying agent behavior, prompts are plain triple-quoted strings at module level in `services.py` — edit the relevant `*_PROMPT` constant rather than restructuring the call chain.

Errors from the Groq client are caught in `call_agent` and re-raised as `RuntimeError` with an Uzbek-language message; `chat_view` catches `RuntimeError` and surfaces it via `context["error"]`.

`GROQ_API_KEY` is loaded from `.env` via `python-dotenv` at import time in `services.py`.

## Constraints

- Never modify, read out, or suggest edits to `.env`. It is not to be viewed or changed.
- Do not touch anything inside `venv/`.
