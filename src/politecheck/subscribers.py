from .logging_context import get_log_context, set_log_context
import logging
import datetime


def add_logging_context(event):
    print("event", event)
    log_data = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "request": {
            "method": event.request.method,
            "path": event.request.path,
            "query_string": event.request.query_string,
            "remote_addr": event.request.remote_addr,
        },
        "meta": {},
    }
    set_log_context(log_data)


def clear_logging_context(event):
    log_data = get_log_context().copy()
    log_data["response"] = {
        "status": event.response.status,
        "content_type": event.response.content_type,
    }
    log_data["meta"]["user_agent"] = event.request.user_agent
    logger = logging.getLogger("request")
    logger.info("completed", extra={"structured": log_data})
