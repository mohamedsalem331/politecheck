import os
import yaml
from pyramid.config import Configurator
from pyramid.settings import asbool

def load_config(env: str):
    """Load configuration from YAML file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, 'config', f'{env}-config.yaml')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

def includeme(config: Configurator):
    """Include configuration in the Pyramid application."""
    env = os.environ.get('POLITECHECK_ENV', 'dev')
    app_config = load_config(env)
    
    # Register Tisane configuration
    config.registry.settings['tisane_config'] = app_config['tisane']
    
    def get_tisane_config(request):
        return request.registry.settings['tisane_config']
    
    config.add_request_method(get_tisane_config, 'tisane_config', reify=True)
    
    # Register Redis configuration
    config.registry.settings['redis_config'] = app_config['redis']
    
    def get_redis_config(request):
        return request.registry.settings['redis_config']
    
    config.add_request_method(get_redis_config, 'redis_config', reify=True) 