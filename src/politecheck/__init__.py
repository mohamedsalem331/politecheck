from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.router import Router
from typing import Dict, Any, Type, TypeVar, Optional

from politecheck.middleware.logging import RequestLoggingMiddleware

T = TypeVar('T')

class Container:
    def __init__(self):
        self.services: Dict[str, Any] = {}

    def register(self, name: str, instance: Any) -> None:
        self.services[name] = instance

    def register_factory(self, name: str, factory: callable) -> None:
        """Register a factory function that will create the service instance."""
        self.services[name] = factory

    def resolve(self, name: str) -> Optional[Any]:
        service = self.services.get(name)
        if callable(service) and not isinstance(service, type):
            # If it's a factory function, call it
            return service()
        return service


container = Container()


def includeme(config: Configurator) -> None:
    """Pyramid includeme function to set up services."""
    # Register the container as a service
    config.registry.settings['container'] = container
    
    def get_container(request):
        return request.registry.settings['container']
    
    config.add_request_method(get_container, 'container', reify=True)

    # Include configuration and routes
    config.include('politecheck.config')
    config.include('politecheck.routes')
    
    # Scan for views in the resources directory
    config.scan('politecheck.resources')


def main(global_config: Dict[str, Any], **settings) -> Router:
    """This function returns a Pyramid WSGI application."""
    
    with Configurator(settings=settings) as config:
        config.include('pyramid_services')
        config.include(includeme)
        
        app = config.make_wsgi_app()
        app = RequestLoggingMiddleware(app)
        
        return app
