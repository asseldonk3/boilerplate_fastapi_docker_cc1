from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict
import json
import os

# Import logging infrastructure
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared_logging import get_logger, get_frontend_logger, setup_centralized_logging, get_json_log_path
from backend.middleware.request_id import RequestIDMiddleware

# Setup centralized logging on app startup
setup_centralized_logging(log_level="INFO", console_output=True)

# Initialize logger for this module
logger = get_logger(__name__, module='BACKEND')

app = FastAPI(title="{{PROJECT_NAME}}", version="1.0.0")

# Request ID middleware (must be first to ensure all logs have request_id)
app.add_middleware(RequestIDMiddleware)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Pydantic models
class FrontendLogEntry(BaseModel):
    level: str
    message: str
    context: Optional[Dict[str, Any]] = None
    url: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: Optional[str] = None


@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {
        "status": "running",
        "project": "{{PROJECT_NAME}}",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "backend"}


@app.post("/api/generate")
async def generate_text(prompt: str):
    """Example endpoint for AI generation"""
    from gpt_service import simple_completion
    try:
        result = simple_completion(prompt)
        return {"response": result}
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# FRONTEND LOGGING ENDPOINT
# =============================================================================

@app.post("/api/log/frontend")
async def log_frontend_event(log_entry: FrontendLogEntry):
    """
    Receive frontend logs and write to centralized log

    Logs from browser JavaScript errors, API failures, and promise rejections
    are captured and stored with [FRONTEND] module tag
    """
    frontend_logger = get_frontend_logger(__name__)

    try:
        level = log_entry.level.lower()
        message = log_entry.message

        # Build context string
        context_parts = []
        if log_entry.session_id:
            context_parts.append(f"session={log_entry.session_id}")
        if log_entry.url:
            context_parts.append(f"URL: {log_entry.url}")
        if log_entry.context:
            # Sanitize context (remove sensitive data)
            safe_context = {k: v for k, v in log_entry.context.items()
                          if not any(s in k.lower() for s in ['password', 'token', 'key', 'secret'])}
            context_parts.append(f"Context: {json.dumps(safe_context)}")

        full_message = f"{message}"
        if context_parts:
            full_message += f" | {' | '.join(context_parts)}"

        # Log based on level
        if level in ['error', 'critical']:
            frontend_logger.error(full_message)
        elif level in ['warning', 'warn']:
            frontend_logger.warning(full_message)
        elif level == 'info':
            frontend_logger.info(full_message)
        else:
            frontend_logger.debug(full_message)

        return {"status": "logged", "level": level}

    except Exception as e:
        logger.error(f"Failed to process frontend log: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )


# =============================================================================
# AI DEBUG API ENDPOINTS
# =============================================================================

@app.get("/api/debug/logs")
async def get_debug_logs(
    last: int = Query(50, description="Number of log entries to return", le=1000),
    level: Optional[str] = Query(None, description="Filter by log level (ERROR, WARNING, INFO, DEBUG)"),
    request_id: Optional[str] = Query(None, description="Filter by request ID"),
    module: Optional[str] = Query(None, description="Filter by module (BACKEND, FRONTEND, etc)"),
    search: Optional[str] = Query(None, description="Search in message text"),
    since_minutes: Optional[int] = Query(None, description="Only logs from last N minutes"),
    include_summary: bool = Query(True, description="Include analysis summary")
):
    """
    AI-friendly log retrieval endpoint.
    Returns structured JSON that Claude can parse for debugging.

    Example usage:
    - GET /api/debug/logs?level=ERROR&last=20
    - GET /api/debug/logs?request_id=abc123
    - GET /api/debug/logs?since_minutes=30&include_summary=true
    """
    json_log_path = get_json_log_path()

    if not json_log_path.exists():
        return {"logs": [], "count": 0, "message": "No logs found"}

    logs = []
    cutoff_time = None

    if since_minutes:
        cutoff_time = (datetime.utcnow() - timedelta(minutes=since_minutes)).isoformat() + "Z"

    try:
        # Read and parse JSON logs (read from end for efficiency)
        with open(json_log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Process from newest to oldest
        for line in reversed(lines):
            if len(logs) >= last:
                break

            try:
                entry = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            # Apply filters
            if cutoff_time and entry.get('ts', '') < cutoff_time:
                continue
            if level and entry.get('level', '').upper() != level.upper():
                continue
            if request_id and request_id not in entry.get('request_id', ''):
                continue
            if module and entry.get('module', '').upper() != module.upper():
                continue
            if search and search.lower() not in entry.get('msg', '').lower():
                continue

            logs.append(entry)

        # Reverse to chronological order
        logs = list(reversed(logs))

        response = {
            "logs": logs,
            "count": len(logs),
            "filters_applied": {
                "level": level,
                "request_id": request_id,
                "module": module,
                "search": search,
                "since_minutes": since_minutes
            }
        }

        # Add summary if requested
        if include_summary and logs:
            response["summary"] = _generate_log_summary(logs)

        return response

    except Exception as e:
        logger.error(f"Failed to retrieve logs: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "logs": []}
        )


def _generate_log_summary(logs: List[dict]) -> dict:
    """Generate AI-friendly summary of logs"""
    level_counts = defaultdict(int)
    module_counts = defaultdict(int)
    request_ids = set()
    errors = []
    slow_operations = []

    for log in logs:
        level_counts[log.get('level', 'UNKNOWN')] += 1
        module_counts[log.get('module', 'UNKNOWN')] += 1

        if log.get('request_id') and log['request_id'] != '----':
            request_ids.add(log['request_id'])

        if log.get('level') == 'ERROR':
            errors.append({
                'ts': log.get('ts'),
                'msg': log.get('msg', '')[:200],
                'module': log.get('module'),
                'request_id': log.get('request_id'),
                'exception': log.get('exception', {}).get('type') if isinstance(log.get('exception'), dict) else None
            })

        # Find slow operations
        duration = log.get('duration_ms')
        if duration and duration > 1000:
            slow_operations.append({
                'ts': log.get('ts'),
                'operation': log.get('span_op'),
                'duration_ms': duration,
                'request_id': log.get('request_id')
            })

    return {
        "total_entries": len(logs),
        "level_distribution": dict(level_counts),
        "module_distribution": dict(module_counts),
        "unique_requests": len(request_ids),
        "error_count": len(errors),
        "recent_errors": errors[:5],
        "slow_operations": sorted(slow_operations, key=lambda x: x.get('duration_ms', 0), reverse=True)[:5],
        "time_range": {
            "oldest": logs[0].get('ts') if logs else None,
            "newest": logs[-1].get('ts') if logs else None
        }
    }


@app.get("/api/debug/request/{request_id}")
async def get_request_trace(request_id: str):
    """
    Get all logs for a specific request ID.
    Useful for tracing a complete request lifecycle.
    """
    json_log_path = get_json_log_path()

    if not json_log_path.exists():
        return {"logs": [], "request_id": request_id, "message": "No logs found"}

    logs = []

    try:
        with open(json_log_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if request_id in entry.get('request_id', ''):
                        logs.append(entry)
                except json.JSONDecodeError:
                    continue

        return {
            "request_id": request_id,
            "logs": logs,
            "count": len(logs),
            "modules_involved": list(set(log.get('module') for log in logs if log.get('module'))),
            "has_errors": any(log.get('level') == 'ERROR' for log in logs),
            "total_duration_ms": sum(log.get('duration_ms', 0) for log in logs if log.get('duration_ms'))
        }

    except Exception as e:
        logger.error(f"Failed to retrieve request trace: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "request_id": request_id}
        )
