# FastAPI + Docker + CC1 Template

This is a **GitHub Template Repository** for quickly starting FastAPI projects with Docker and CC1 documentation.

## Using This Template

1. Click the "Use this template" button above
2. Name your new repository
3. Clone your new repo locally
4. Run the setup:
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   docker-compose up
   ```

## What's Included

- ✅ FastAPI backend with auto-reload
- ✅ PostgreSQL database in Docker
- ✅ Static frontend (no build tools!)
- ✅ OpenAI API integration
- ✅ CC1 documentation system
- ✅ Docker Compose setup
- ✅ GitHub Actions auto-initialization

## Template Features

When you create a repo from this template:
- Variables like `{{PROJECT_NAME}}` are auto-replaced
- Dates are automatically set to creation date
- Template-specific files are removed
- Clean git history (not a fork!)

## Customization

After creating from template:
1. Update `cc1/BACKLOG.md` with your product vision
2. Modify `backend/main.py` for your endpoints
3. Customize `frontend/index.html` for your UI
4. Update database schema in `backend/database.py`

---
Template maintained by: YOUR_NAME
