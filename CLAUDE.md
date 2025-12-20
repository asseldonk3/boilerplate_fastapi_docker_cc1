# CLAUDE.md

This project uses the CC1 documentation system for knowledge management.

## Tech Stack
- **Backend**: FastAPI with auto-reload
- **Frontend**: Static files with Bootstrap CDN (no build tools)
- **Database**: PostgreSQL in Docker
- **AI**: OpenAI API configured in gpt_service.py

## Development Workflow
1. Run `docker-compose up` to start everything
2. Edit files directly - they auto-reload
3. Access at http://localhost:8001

## Important Notes
- **No Build Tools**: Edit HTML/CSS/JS directly
- **Docker First**: Everything runs in containers
- **Simple Scale**: Designed for small teams (1-10 users)

## CC1 Documentation
- `cc1/TASKS.md` - Current work tracking
- `cc1/LEARNINGS.md` - Knowledge capture
- `cc1/BACKLOG.md` - Future planning
- `cc1/PROJECT_INDEX.md` - Technical reference

## File Locations
- API: `backend/main.py`
- AI: `backend/gpt_service.py`
- UI: `frontend/index.html`
- Styles: `frontend/css/style.css`
- JS: `frontend/js/app.js`

---

## Debugging Workflow (AI-Optimized)

This project has an enhanced logging system optimized for AI debugging agents. Use these methods when investigating issues:

### Quick Diagnosis
```bash
# Get structured summary (best for AI parsing)
python logs/ai_debug_summary.py --json

# Human-readable summary
python logs/ai_debug_summary.py

# Last hour only
python logs/ai_debug_summary.py --hours 1
```

### Query Logs via API
When the app is running, use the debug API endpoints:

```bash
# Get recent errors
curl 'http://localhost:8001/api/debug/logs?level=ERROR&last=20'

# Trace a specific request by ID (from X-Request-ID header)
curl 'http://localhost:8001/api/debug/request/<request-id>'

# Get logs from last hour with analysis summary
curl 'http://localhost:8001/api/debug/logs?since_minutes=60&include_summary=true'

# Filter by module
curl 'http://localhost:8001/api/debug/logs?module=BACKEND&last=50'

# Search in log messages
curl 'http://localhost:8001/api/debug/logs?search=database&level=ERROR'
```

### View JSON Logs Directly
```bash
# Last 50 entries (machine-parseable)
tail -50 logs/application.jsonl | jq .

# Filter for errors only
tail -100 logs/application.jsonl | jq 'select(.level == "ERROR")'

# Find by request ID
grep "abc-123-def" logs/application.jsonl | jq .
```

### CLI Log Viewer
```bash
# View recent logs with colors
python logs/view_logs.py --lines 50

# Filter by level
python logs/view_logs.py --level ERROR

# Search by request ID
python logs/view_logs.py --request-id abc-123-def

# Follow mode (like tail -f)
python logs/view_logs.py --follow
```

### Key Log Fields (in application.jsonl)
- `request_id`: Trace across frontend/backend (correlate with X-Request-ID header)
- `span_id` + `span_op`: Track operation timing and nested operations
- `duration_ms`: Performance data for spans
- `context`: Additional debugging info (local variables on errors)
- `exception`: Structured error details with type, message, and traceback
- `module`: Component identifier (BACKEND, FRONTEND, DATABASE, etc.)

### Debugging Steps
1. **Start with summary**: `python logs/ai_debug_summary.py --json`
2. **Check error patterns**: Look at `suggestions` field for hints
3. **Trace specific request**: Use request_id from error to see full lifecycle
4. **Check performance**: Look at `slow_operations` in summary
5. **Frontend correlation**: Match `session_id` to track user journey

### Using Operation Spans in Code
```python
from shared_logging import get_logger, log_span, log_exception_context

logger = get_logger(__name__, module='MY_MODULE')

# Trace a complex operation
with log_span("process_order", order_id=123):
    validate_order()
    save_to_db()

# Enhanced exception logging
try:
    risky_operation()
except Exception as e:
    log_exception_context(logger, e, "Failed to process")
```

---
_Template initialized: {{CREATION_DATE}}_
