def includeme(config):
    config.add_route("health", "/health")
    config.add_route("tisane", "/api/v1/tisane")
