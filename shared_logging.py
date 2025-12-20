"""
Centralized logging configuration for the entire project
Optimized for AI debugger agents with JSON output and operation tracing

Usage:
    from shared_logging import get_logger, log_span, log_exception_context
    logger = get_logger(__name__, module='MY_MODULE')
    logger.info("Processing...")

    # Trace complex operations
    with log_span("process_order", order_id=123):
        do_work()

    # Log exceptions with context
    try:
        risky_operation()
    except Exception as e:
        log_exception_context(logger, e, "Failed to process")
"""
import logging
import sys
import json
import time
import uuid
import traceback
import inspect
from pathlib import Path
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from contextlib import contextmanager
from typing import Optional, Any, Dict

# Central log directory at project root
PROJECT_ROOT = Path(__file__).parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log format with module tag and request_id
DETAILED_FORMAT = '%(asctime)s | %(levelname)-8s | [%(module_tag)s] | %(request_id)s | %(name)s:%(lineno)d | %(message)s'
SIMPLE_FORMAT = '%(asctime)s | %(levelname)-8s | [%(module_tag)s] | %(request_id)s | %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Track if logging has been initialized
_initialized = False
_loggers = {}

# JSON log file path
JSON_LOG_FILE = LOG_DIR / "application.jsonl"


class ModuleTagFilter(logging.Filter):
    """Add module tag to log records"""
    def __init__(self, module_tag='MAIN'):
        super().__init__()
        self.module_tag = module_tag

    def filter(self, record):
        record.module_tag = self.module_tag
        return True


class RequestIDFilter(logging.Filter):
    """Add request_id to log records from context"""
    def filter(self, record):
        # Try to get request ID from context (set by middleware)
        try:
            from backend.middleware.request_id import get_request_id
            record.request_id = get_request_id()
        except:
            # If not in request context, use placeholder
            record.request_id = '----'
        return True


class JSONLineHandler(logging.Handler):
    """
    Handler that writes logs as JSON lines for AI parsing.
    Each line is a complete JSON object for easy machine processing.
    """
    def __init__(self, filename: Path):
        super().__init__()
        self.filename = filename

    def emit(self, record):
        try:
            log_entry = {
                "ts": datetime.utcnow().isoformat() + "Z",
                "unix_ts": record.created,
                "level": record.levelname,
                "module": getattr(record, 'module_tag', 'MAIN'),
                "request_id": getattr(record, 'request_id', None),
                "logger": record.name,
                "file": record.filename,
                "line": record.lineno,
                "func": record.funcName,
                "msg": record.getMessage(),
                # Include extra fields if present
                "span_id": getattr(record, 'span_id', None),
                "span_op": getattr(record, 'span_op', None),
                "duration_ms": getattr(record, 'duration_ms', None),
                "context": getattr(record, 'log_context', None),
            }

            # Add exception info if present
            if record.exc_info:
                log_entry["exception"] = {
                    "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                    "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                    "traceback": self.formatException(record.exc_info)
                }

            # Remove None values to keep logs clean
            log_entry = {k: v for k, v in log_entry.items() if v is not None}

            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, default=str) + '\n')

        except Exception:
            self.handleError(record)


def setup_centralized_logging(
    log_level: str = "INFO",
    console_output: bool = True
):
    """Setup centralized logging for the entire project"""
    global _initialized

    if _initialized:
        return

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(DETAILED_FORMAT, datefmt=DATE_FORMAT)
    simple_formatter = logging.Formatter(SIMPLE_FORMAT, datefmt=DATE_FORMAT)

    # Create Request ID filter (applied to all handlers)
    request_id_filter = RequestIDFilter()

    # 1. Console Handler (for development)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(simple_formatter)
        console_handler.addFilter(request_id_filter)
        root_logger.addHandler(console_handler)

    # 2. Main Application Log (all modules combined)
    main_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / "application.log",
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    main_handler.suffix = "%Y-%m-%d"
    main_handler.setLevel(logging.INFO)
    main_handler.setFormatter(detailed_formatter)
    main_handler.addFilter(request_id_filter)
    root_logger.addHandler(main_handler)

    # 3. Error Log (all errors from all modules)
    error_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / "application_errors.log",
        when='midnight',
        interval=1,
        backupCount=90,
        encoding='utf-8'
    )
    error_handler.suffix = "%Y-%m-%d"
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    error_handler.addFilter(request_id_filter)
    root_logger.addHandler(error_handler)

    # 4. JSON Line Handler (for AI parsing)
    json_handler = JSONLineHandler(JSON_LOG_FILE)
    json_handler.setLevel(logging.INFO)
    json_handler.addFilter(request_id_filter)
    root_logger.addHandler(json_handler)

    # Reduce noise from external libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)

    _initialized = True

    print(f"Centralized logging initialized (with AI debug features) | Log directory: {LOG_DIR}")


def get_logger(name: str, module: str = 'MAIN'):
    """Get a logger instance for a specific module"""
    if not _initialized:
        setup_centralized_logging()

    logger_key = f"{module}:{name}"
    if logger_key in _loggers:
        return _loggers[logger_key]

    logger = logging.getLogger(name)

    # Add module tag filter
    tag_filter = ModuleTagFilter(module)
    logger.addFilter(tag_filter)

    # Cache logger
    _loggers[logger_key] = logger

    return logger


def get_frontend_logger(name: str):
    """Get logger for frontend browser errors"""
    return get_logger(name, module='FRONTEND')


# =============================================================================
# OPERATION SPANS - Trace complex operations with timing
# =============================================================================

@contextmanager
def log_span(operation: str, logger: Optional[logging.Logger] = None, **context):
    """
    Context manager to trace operation duration and context for debugging.

    Usage:
        with log_span("process_order", order_id=123):
            validate_order()
            save_to_db()

    Logs SPAN_START at entry and SPAN_END with duration at exit.
    On exception, logs SPAN_ERROR before re-raising.
    """
    if logger is None:
        logger = get_logger(__name__, module='SPAN')

    span_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    # Create extra dict for structured logging
    extra = {'span_id': span_id, 'span_op': operation, 'log_context': context if context else None}

    logger.info(f"SPAN_START:{operation} | context={json.dumps(context, default=str)}", extra=extra)

    try:
        yield span_id
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        extra['duration_ms'] = duration_ms
        extra['log_context'] = {**context, 'error': str(e), 'error_type': type(e).__name__}
        logger.error(f"SPAN_ERROR:{operation} | duration={duration_ms:.2f}ms | error={e}", extra=extra)
        raise
    else:
        duration_ms = (time.time() - start_time) * 1000
        extra['duration_ms'] = duration_ms
        logger.info(f"SPAN_END:{operation} | duration={duration_ms:.2f}ms", extra=extra)


# =============================================================================
# ENHANCED EXCEPTION LOGGING - Capture local variables and context
# =============================================================================

def log_exception_context(
    logger: logging.Logger,
    exc: Exception,
    message: str = "Exception occurred",
    include_locals: bool = True,
    max_local_repr: int = 200
):
    """
    Log exception with local variables and call context for debugging.

    Usage:
        try:
            risky_operation(order_id=123)
        except Exception as e:
            log_exception_context(logger, e, "Failed to process order")

    Captures:
    - Exception type and message
    - Full traceback
    - Local variables from the calling frame (sanitized)
    - Call location
    """
    # Get the calling frame
    frame = inspect.currentframe()
    if frame is not None:
        frame = frame.f_back

    # Extract local variables (sanitized)
    locals_safe = {}
    if include_locals and frame is not None:
        sensitive_patterns = ['password', 'token', 'key', 'secret', 'credential', 'auth']
        for k, v in frame.f_locals.items():
            # Skip private/dunder variables
            if k.startswith('_'):
                continue
            # Skip sensitive data
            if any(pattern in k.lower() for pattern in sensitive_patterns):
                locals_safe[k] = '[REDACTED]'
                continue
            # Truncate long representations
            try:
                repr_val = repr(v)
                if len(repr_val) > max_local_repr:
                    repr_val = repr_val[:max_local_repr] + '...[truncated]'
                locals_safe[k] = repr_val
            except:
                locals_safe[k] = '[repr failed]'

    # Build context for JSON log
    context = {
        'exception_type': type(exc).__name__,
        'exception_message': str(exc),
        'locals': locals_safe if locals_safe else None,
        'traceback': traceback.format_exc()
    }

    # Log with extra context
    extra = {'log_context': context}
    logger.error(
        f"{message} | {type(exc).__name__}: {exc}",
        extra=extra,
        exc_info=True
    )


def get_json_log_path() -> Path:
    """Return path to JSON log file for external tools"""
    return JSON_LOG_FILE
