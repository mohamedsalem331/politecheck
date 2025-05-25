from pyramid.config import Configurator
import structlog

# structlog.configure(
#     processors=[
#         structlog.contextvars.merge_contextvars,
#         structlog.processors.add_log_level,
#         structlog.processors.TimeStamper(fmt="iso"),
#         structlog.processors.JSONRenderer(),
#     ],
#     context_class=dict,
#     logger_factory=structlog.stdlib.LoggerFactory(),
#     wrapper_class=structlog.stdlib.BoundLogger,
#     cache_logger_on_first_use=True,
# )


class Container:
    def __init__(self):
        self.services = {}

    def register(self, name, instance):
        self.services[name] = instance

    def resolve(self, name):
        return self.services.get(name)


container = Container()


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include(".routes")
    config.scan(".views")
    config.add_subscriber(
        "politecheck.subscribers.add_logging_context", "pyramid.events.NewRequest"
    )
    config.add_subscriber(
        "politecheck.subscribers.clear_logging_context",
        "pyramid.events.NewResponse",
    )
    return config.make_wsgi_app()
