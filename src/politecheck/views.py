import logging
from pyramid.view import view_config
from .logging_context import get_log_context, set_log_context

logger = logging.getLogger("request")


class HelloWorldView:
    def __init__(self, request):
        self.request = request

    @view_config(route_name="hello", renderer="json")
    def get(self):
        context = get_log_context().copy()
        context["meta"]["action"] = "say_hello"
        set_log_context(context)
        logger.info(
            "Request completed",
            extra={"structured": {"user": "alice", "action": "login"}},
        )
        return {"message": "Hello, World"}
