---
last_updated: {{TODAY}}
---

# ARCHITECTURE
_Technical decisions, patterns, and constraints. Auto-updated by /cc1-update._

---

## Tech Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Framework | FastAPI | 0.100+ | REST API, async support |
| Database | PostgreSQL | 15+ | Primary data store |
| ORM | SQLAlchemy | 2.0+ | Database abstraction |
| Validation | Pydantic | 2.0+ | Request/response schemas |
| Container | Docker | 24+ | Development & deployment |
| Auth | python-jose | 3.3+ | JWT token handling |

---

## Architectural Decisions

### [D-001] No-Build Frontend
**Date:** {{TODAY}}
**Decision:** Use vanilla HTML/CSS/JS without build tools
**Rationale:** Simplicity, fast iteration, no Node.js dependency
**Trade-offs:** No TypeScript, no bundling optimization

### [D-002] Repository Pattern
**Date:** {{TODAY}}
**Decision:** All database access through repository classes
**Rationale:** Decouples business logic from ORM, easier testing
**Example:** `src/repositories/`

### [D-003] Layered Architecture
**Date:** {{TODAY}}
**Decision:** Routes → Services → Repositories → Models
**Rationale:** Clear separation of concerns, testable layers

---

## Patterns & Conventions

### API Structure
- Routes in `src/api/routes/`
- Schemas in `src/api/schemas/`
- Dependencies in `src/api/deps.py`
- All routes prefixed with `/api/v1/`

### Database Access
- Never import models directly in routes
- Use repository pattern for all DB operations
- Session management via FastAPI dependencies

### Error Handling
- Use FastAPI HTTPException for API errors
- Custom exceptions in `src/core/exceptions.py`
- Structured error responses with error codes

---

## Environment Variables

### Required
| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@db:5432/app` |
| `SECRET_KEY` | JWT signing key | `your-secret-key-here` |

### Optional
| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `CORS_ORIGINS` | Allowed CORS origins | `["*"]` |

---

## Database Schema

### Core Tables

```sql
-- users (example)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

_Update this section as you add models_

---

## Dependencies

### Production
| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.100.0+ | Web framework |
| uvicorn | 0.23.0+ | ASGI server |
| sqlalchemy | 2.0.0+ | ORM |
| pydantic | 2.0.0+ | Validation |
| python-jose | 3.3.0+ | JWT handling |
| passlib | 1.7.4+ | Password hashing |
| psycopg2-binary | 2.9.0+ | PostgreSQL driver |

### Development
| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 7.4.0+ | Testing |
| httpx | 0.24.0+ | Async test client |

---

## Constraints & Guardrails

### Security
- [ ] Never log passwords, tokens, or PII
- [ ] All inputs validated via Pydantic schemas
- [ ] Parameterized queries only (SQLAlchemy handles this)
- [ ] JWT tokens expire (configurable)
- [ ] CORS configured for production

### Performance
- [ ] Use async endpoints where possible
- [ ] Database connection pooling configured
- [ ] No N+1 queries (use eager loading)

### Code Quality
- [ ] Type hints on all public functions
- [ ] Docstrings on modules and classes
- [ ] Tests for all business logic

---

_Auto-updated by `/cc1-update`._
