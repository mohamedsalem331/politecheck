from typing import Dict, Any, Optional
import redis
from pyramid.request import Request
import json

class RedisService:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Redis service with configuration.
        
        Args:
            config: Dictionary containing Redis configuration
                   Expected keys: host, port, db, password (optional)
        """
        self.redis_client = redis.Redis(
            host=config.get('host', 'localhost'),
            port=config.get('port', 6379),
            db=config.get('db', 0),
            password=config.get('password'),
            decode_responses=True  # Automatically decode bytes to strings
        )
        
    def set(self, key: str, value: Any, expire: Optional[int] = 30) -> bool:
        try:
            # Serialize non-string values to JSON
            if not isinstance(value, str):
                value = json.dumps(value)
                
            result = self.redis_client.set(key, value, ex=expire)
            return result
        except redis.RedisError as e:
            raise redis.RedisError(f"Failed to set key '{key}': {str(e)}")
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
                
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except redis.RedisError as e:
            raise redis.RedisError(f"Failed to get key '{key}': {str(e)}")
    
    def exists(self, key: str) -> bool:
        try:
            return bool(self.redis_client.exists(key))
        except redis.RedisError as e:
            raise redis.RedisError(f"Failed to check existence of key '{key}': {str(e)}")

def includeme(config):
    """Register the Redis service."""
    def get_redis_service(request: Request) -> RedisService:
        return RedisService(request.redis_config)
    
    config.register_service_factory(
        get_redis_service,
        iface=RedisService
    ) 