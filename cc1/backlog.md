---
last_updated: {{TODAY}}
---

# BACKLOG
_Sliding window: max 5 features (current work + recently completed)._

---

## Currently Building (Max 2-3)

_Add features here when you start working on them. Each should have a spec in `specs/`._

Example:
```markdown
### 1. User Authentication `#spec:user-auth`
**Status:** Implementing
**Started:** {{TODAY}}
**Progress:** JWT tokens working, need refresh token flow
**Next:** Implement password reset
```

---

## Recently Completed (Max 2-3)

### 1. Project Setup from Boilerplate
**Completed:** {{TODAY}}
**Outcome:** FastAPI + Docker + PostgreSQL + CC1 initialized
**Learnings:** See learnings.md [E-001], [E-002], [E-003]

---

## Up Next (Parking Lot)

_Ideas waiting to be picked up. Move to "Currently Building" when starting._

**Core Features:**
- **User Authentication** - JWT-based auth with refresh tokens
- **Data Persistence Patterns** - Repository pattern examples
- **Basic CRUD Operations** - Template endpoints

**Improvements:**
- **API Rate Limiting** - Per-user request throttling
- **Request Logging** - Structured logging with request tracing
- **Admin Interface** - Basic admin dashboard

**Scale (if needed):**
- **Redis Caching** - Session and query caching
- **Background Jobs** - Async task processing
- **Multiple Workers** - Load handling

---

## Rules

1. **Max 5 items total** in Currently Building + Recently Completed
2. **When adding 6th item** - Archive oldest completed to `specs/archive/`
3. **"Currently Building"** - Only active work with specs
4. **"Recently Completed"** - Last 2-3 finished features
5. **"Up Next"** - Ideas, not commitments (unlimited)

---

_Semi-auto-updated by `/cc1-update`. Asks before moving features._
_Created from boilerplate: {{CREATION_DATE}}_
