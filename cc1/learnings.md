---
last_updated: {{TODAY}}
---

# LEARNINGS
_Errors solved, patterns discovered, gotchas found. Auto-updated by /cc1-update._

---

## Errors & Solutions

### [E-001] Port Conflicts on Startup
**Date:** {{TODAY}}
**Tags:** #docker #networking
**Problem:** Default ports (8000, 5432) often in use
**Solution:** Use non-standard ports: FastAPI on 8001, PostgreSQL on 5433
**File:** `docker-compose.yml`

### [E-002] Database Connection Refused
**Date:** {{TODAY}}
**Tags:** #database #postgresql #docker
**Problem:** App starts before PostgreSQL is ready
**Solution:** Add health checks and `depends_on` with condition in docker-compose
**Command:** `docker-compose logs db` to debug

### [E-003] CORS Errors in Browser
**Date:** {{TODAY}}
**Tags:** #fastapi #cors #frontend
**Problem:** Browser blocks requests due to CORS policy
**Solution:** Configure `allow_origins` in main.py - use `["*"]` for dev, specific URLs for prod
**File:** `src/main.py`

---

## Patterns & Best Practices

### [P-001] No-Build Frontend
**Tags:** #frontend #architecture
**Pattern:** Use vanilla HTML/CSS/JS without build tools
**When:** Simple to moderate frontends that don't need React/Vue complexity
**Why:**
- Edit → Save → Refresh (no compilation)
- No npm install delays
- No webpack configuration
- No node_modules folder (saves 500MB+)
- Works identically on any machine with Docker
**Example:** `static/` directory

### [P-002] Repository Pattern for Database
**Tags:** #architecture #database
**Pattern:** All database access through repository classes
**When:** Any database operation
**Why:** Decouples business logic from ORM, easier testing
**Example:** `src/repositories/`

---

## Commands & Scripts

### [C-001] Development Workflow
**Tags:** #docker #dev
```bash
docker-compose up              # Run with logs
docker-compose up -d           # Run in background
docker-compose down            # Stop everything
docker-compose down -v         # Stop and remove volumes (reset DB)
```

### [C-002] Debugging
**Tags:** #docker #debug
```bash
docker-compose ps                    # Check container status
docker-compose logs -f app           # View app logs
docker exec -it <container> bash     # Enter container shell
```

### [C-003] Database Operations
**Tags:** #database #postgresql
```bash
docker-compose exec db psql -U postgres -d app  # Access PostgreSQL CLI
```

---

## Gotchas & Workarounds

### [G-001] Hot Reload Not Working
**Tags:** #docker #dev
**Issue:** Code changes not reflected in running container
**Workaround:**
1. Check volume mounts in docker-compose.yml
2. Ensure `--reload` flag is set for uvicorn
3. Restart container: `docker-compose restart app`

### [G-002] .env Changes Not Applied
**Tags:** #docker #config
**Issue:** Environment variable changes ignored
**Workaround:** Must restart containers: `docker-compose down && docker-compose up`

---

_Auto-updated by `/cc1-update`. Your most valuable CC1 file._
_Created from boilerplate: {{CREATION_DATE}}_
