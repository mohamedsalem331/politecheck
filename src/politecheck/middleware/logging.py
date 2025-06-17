import time
import logging
import json
import uuid
from contextvars import ContextVar
from typing import Any, Dict, Callable, List, Tuple
from pyramid.request import Request

# Create a context variable to store request-specific data
request_context: ContextVar[Dict[str, Any]] = ContextVar('request_context', default={})

class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger('request')

    def __call__(self, environ: Dict[str, Any], start_response: Callable) -> Any:
        # Create a request object from the WSGI environment
        request = Request(environ)
        
        # Initialize request context with all the data we want to track
        context = {
            'request_id': str(uuid.uuid4()),
            'start_time': time.time(),
            'request': {
                'method': request.method,
                'path': request.path,
                'query_string': request.query_string,
                'client_ip': request.client_addr,
                'user_agent': request.user_agent,
            },
            'meta': {},  # This will be populated by views
            'response': {
                'status_code': None,
                'duration_ms': None,
            }
        }
        
        # Set the context for this request
        token = request_context.set(context)

        # Create a wrapper for start_response to capture the status code
        def wrapped_start_response(status: str, headers: List[Tuple[str, str]], exc_info=None):
            # Extract status code from the status string (e.g., "200 OK" -> 200)
            try:
                status_code = int(status.split()[0])
                context['response']['status_code'] = status_code
            except (ValueError, IndexError):
                context['response']['status_code'] = 500

            return start_response(status, headers, exc_info)

        try:
            # Process the request through the WSGI application
            response = self.app(environ, wrapped_start_response)

            # Calculate request duration
            duration = time.time() - context['start_time']
            context['response']['duration_ms'] = round(duration * 1000, 2)
            
            # Log the complete request information
            self.logger.info('Request processed', extra={
                'structured': context
            })

            return response

        except Exception as e:
            # Update context with error information
            context['error'] = {
                'type': type(e).__name__,
                'message': str(e)
            }
            context['response']['status_code'] = 500
            
            # Log the error
            self.logger.error('Request failed', extra={
                'structured': context
            }, exc_info=True)
            raise
        finally:
            # Reset the context
            request_context.reset(token)

def get_request_context() -> Dict[str, Any]:
    """Get the current request context."""
    return request_context.get()

def add_meta_to_log(meta_data: Dict[str, Any]) -> None:
    """Add metadata to the current request's log context."""
    context = request_context.get()
    context['meta'].update(meta_data) 