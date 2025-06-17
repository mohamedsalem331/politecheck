from pyramid.view import view_config

class HealthResource:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='health', request_method='GET', renderer='json')
    def get(self):
        return {
            "status": "healthy",
            "version": "1.0.0"
        } 