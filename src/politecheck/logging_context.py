import logging
import contextvars

request_context_logger = contextvars.ContextVar("request_context_logger")


def get_log_context():
    return request_context_logger.get()


def set_log_context(data):
    request_context_logger.set(data)
