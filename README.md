# CV/ML Tutor 🎓

An AI-powered tutor that explains Computer Vision and Machine Learning concepts in simple language, tailored for students. Built as a mini-project for the "AI Skills Development" course.

**Live demo:** https://cv-ml-tutor-agent.onrender.com/

Note: the app is hosted on Render's free tier, so the first request after inactivity may take 30-50 seconds to wake up the server.

## Problem

Students learning Computer Vision and Machine Learning often struggle with abstract concepts (CNNs, overfitting, data augmentation, etc.) and need an on-demand explainer that adapts to their level and checks their understanding afterward.

## How it works

Every question goes through a 3-agent pipeline, each step handled by a separate LLM call with its own system prompt:

Student question
-> Agent 1 (Planner): analyzes the topic, student's likely level, and key points to cover
-> Agent 2 (Explainer): writes a clear explanation with a concrete example or analogy
-> Agent 3 (Reviewer): fixes inaccuracies, simplifies, and appends a mini quiz question
-> Final answer shown to the student

This pipeline is implemented in tutor/services.py

## Tech stack

- Backend: Python, Django
- LLM: Groq API running llama-3.3-70b-versatile
- Frontend: Django templates + Bootstrap 5
- Deployment: Render.com (Gunicorn + WhiteNoise for static files)

## Development tooling

This project was built with Claude Code, using a custom subagent:

- .claude/agents/django-reviewer.md - a read-only subagent that audits the Django codebase for security issues (hardcoded secrets, DEBUG settings, etc.) and best-practice violations. It was used to catch and fix real issues (hardcoded SECRET_KEY, DEBUG=True, empty ALLOWED_HOSTS) before deployment.
- CLAUDE.md - project memory file describing architecture and hard constraints (e.g. never touch .env or venv/).

## Running locally

1. Clone the repository

git clone https://github.com/asalbanu-alymbaeva/cv-ml-tutor-agent.git
cd cv-ml-tutor-agent

2. Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate

(On macOS/Linux use: source venv/bin/activate)

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root with the following content:

GROQ_API_KEY=your-groq-api-key
DJANGO_SECRET_KEY=your-django-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

Get a free Groq API key at console.groq.com/keys

5. Run migrations and start the server

python manage.py migrate
python manage.py runserver

Open http://127.0.0.1:8000 in your browser.

## Project structure

cv-tutor/
- cvtutor_project/ - Django project settings
- tutor/
  - services.py - 3-agent LLM pipeline
  - views.py - chat view
  - templates/tutor/ - chat.html UI
- .claude/agents/ - Claude Code subagents
- CLAUDE.md - Claude Code project memory
- Procfile - Render start command
- requirements.txt

## Author

Asalbanu Alimbaeva
