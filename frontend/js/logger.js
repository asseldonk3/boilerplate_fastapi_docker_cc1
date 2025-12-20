/**
 * Frontend Error Logging - Centralized JavaScript Error Handler
 * Automatically logs JavaScript errors, API failures, and promise rejections
 * Includes session tracking for correlating user journeys
 */
(function() {
    'use strict';

    // Session ID for correlating user journey across requests
    const SESSION_ID = sessionStorage.getItem('debug_session_id') || (() => {
        const id = crypto.randomUUID ? crypto.randomUUID() :
            'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
                const r = Math.random() * 16 | 0;
                return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
            });
        sessionStorage.setItem('debug_session_id', id);
        return id;
    })();

    // Page view counter for sequence tracking
    let pageViewCount = parseInt(sessionStorage.getItem('page_view_count') || '0') + 1;
    sessionStorage.setItem('page_view_count', pageViewCount.toString());

    // Log to server function
    async function logToServer(level, message, context = {}) {
        try {
            // Add session and page context
            context.session_id = SESSION_ID;
            context.page_sequence = pageViewCount;
            context.url = window.location.href;
            context.timestamp = new Date().toISOString();
            context.userAgent = navigator.userAgent;
            context.viewport = {
                width: window.innerWidth,
                height: window.innerHeight
            };

            await fetch('/api/log/frontend', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    level: level,
                    message: message,
                    context: context,
                    url: window.location.href,
                    user_agent: navigator.userAgent,
                    session_id: SESSION_ID,
                    timestamp: new Date().toISOString()
                })
            });
        } catch (err) {
            console.error('[Logger] Failed to log to server:', err);
        }
    }

    // 1. Global Error Handler
    window.addEventListener('error', function(event) {
        const context = {
            filename: event.filename,
            lineno: event.lineno,
            colno: event.colno,
            stack: event.error?.stack || 'No stack trace',
            error_type: event.error?.name || 'Error'
        };

        console.error('[Frontend Error]', event.message, context);
        logToServer('error', `JavaScript Error: ${event.message}`, context);
        return false;
    });

    // 2. Unhandled Promise Rejection Handler
    window.addEventListener('unhandledrejection', function(event) {
        const reason = event.reason?.toString() || 'Unknown rejection';
        const context = {
            reason: reason,
            stack: event.reason?.stack || 'No stack trace',
            promise: event.promise?.toString()
        };

        console.error('[Unhandled Promise Rejection]', reason);
        logToServer('error', `Unhandled Promise Rejection: ${reason}`, context);
        return false;
    });

    // 3. Enhanced Fetch Error Logging
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        const url = typeof args[0] === 'string' ? args[0] : args[0]?.url || 'unknown';
        const method = args[1]?.method || 'GET';
        const startTime = Date.now();

        return originalFetch.apply(this, args)
            .then(response => {
                const duration = Date.now() - startTime;
                const requestId = response.headers.get('X-Request-ID');

                // Log failed API calls
                if (!response.ok) {
                    logToServer('error', 'API Request Failed', {
                        endpoint: url,
                        method: method,
                        status: response.status,
                        statusText: response.statusText,
                        duration_ms: duration,
                        request_id: requestId
                    });
                }

                // Log slow API calls (> 5 seconds)
                if (duration > 5000) {
                    logToServer('warning', 'Slow API Request', {
                        endpoint: url,
                        method: method,
                        duration_ms: duration,
                        request_id: requestId
                    });
                }

                return response;
            })
            .catch(error => {
                logToServer('error', 'API Request Exception', {
                    endpoint: url,
                    method: method,
                    error: error.message,
                    error_type: error.name,
                    duration_ms: Date.now() - startTime
                });
                throw error;
            });
    };

    // 4. Expose global logger for manual logging
    window.frontendLogger = {
        error: (message, context) => logToServer('error', message, context || {}),
        warning: (message, context) => logToServer('warning', message, context || {}),
        info: (message, context) => logToServer('info', message, context || {}),
        debug: (message, context) => logToServer('debug', message, context || {}),

        // Get session ID for debugging
        getSessionId: () => SESSION_ID,

        // Manual span tracking for frontend operations
        startSpan: (operation, context = {}) => {
            const spanId = crypto.randomUUID ? crypto.randomUUID().slice(0, 8) :
                Math.random().toString(36).slice(2, 10);
            const startTime = Date.now();
            logToServer('info', `SPAN_START:${operation}`, { span_id: spanId, ...context });
            return {
                end: (extraContext = {}) => {
                    const duration = Date.now() - startTime;
                    logToServer('info', `SPAN_END:${operation}`, {
                        span_id: spanId,
                        duration_ms: duration,
                        ...context,
                        ...extraContext
                    });
                },
                error: (error, extraContext = {}) => {
                    const duration = Date.now() - startTime;
                    logToServer('error', `SPAN_ERROR:${operation}`, {
                        span_id: spanId,
                        duration_ms: duration,
                        error: error.message || error,
                        ...context,
                        ...extraContext
                    });
                }
            };
        }
    };

    // Legacy compatibility
    window.logError = (message, context) => logToServer('error', message, context);
    window.logWarning = (message, context) => logToServer('warning', message, context);
    window.logInfo = (message, context) => logToServer('info', message, context);

    console.log('Frontend logger initialized | Session:', SESSION_ID);
})();
