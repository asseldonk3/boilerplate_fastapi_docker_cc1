"""Request ID Middleware - Add unique IDs to all requests for tracing"""
import uuid
import contextvars
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Thread-safe storage for request ID
_request_id_context = contextvars.ContextVar('request_id', default=None)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add unique request IDs to all requests"""

    async def dispatch(self, request: Request, call_next):
        # Generate or extract request ID
        request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))

        # Store in context for logging
        _request_id_context.set(request_id)

        # Process request
        response = await call_next(request)

        # Add request ID to response headers
        response.headers['X-Request-ID'] = request_id

        return response


def get_request_id() -> str:
    """Get the current request ID from context"""
    return _request_id_context.get() or 'no-request-id'
