---
last_updated: {{TODAY}}
---

# FILE INDEX
_Directory structure and key files. Auto-updated by /cc1-update._

---

## Directory Structure

```
{{PROJECT_NAME}}/
├── cc1/                  # CC1 documentation system
│   ├── learnings.md      # Errors, patterns, gotchas
│   ├── file-index.md     # This file
│   ├── architecture.md   # Tech decisions, constraints
│   ├── vision.md         # Product vision
│   ├── backlog.md        # Features (max 5)
│   └── specs/            # Feature specifications
├── src/
│   ├── api/              # API endpoints
│   │   ├── routes/       # Route handlers
│   │   ├── schemas/      # Pydantic models
│   │   └── deps.py       # Dependencies
│   ├── models/           # SQLAlchemy models
│   ├── services/         # Business logic
│   ├── repositories/     # Data access layer
│   └── core/             # Config, security
├── tests/                # Test files
├── static/               # Static assets (no build tools)
│   ├── css/
│   ├── js/
│   └── index.html
├── logs/                 # Application logs
├── docker-compose.yml    # Container orchestration
├── Dockerfile            # App container definition
└── .env.example          # Environment template
```

---

## Key Entry Points

| File | Purpose |
|------|---------|
| `src/main.py` | Application startup, FastAPI app instance |
| `src/api/router.py` | API route registration |
| `src/core/config.py` | Settings and configuration |
| `src/models/base.py` | SQLAlchemy base model |
| `static/index.html` | Frontend entry point |

---

## Recently Changed

### Last Session ({{TODAY}})
- Project initialized from CC1 boilerplate

---

_Auto-updated by `/cc1-update`._
