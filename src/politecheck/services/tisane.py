from typing import Dict, Any
import requests
from pyramid.request import Request

class TisaneService:
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config['api_key']
        self.base_url = config['base_url']
        
    def _get_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': self.api_key
        }
        
    def analyze_text(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze text using the Tisane API.
        
        Args:
            data: The request data containing language, content, and settings
            
        Returns:
            Dict containing the analysis results
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.post(
            self.base_url,
            headers=self._get_headers(),
            json=data
        )
        
        response.raise_for_status()
        return response.json()

def includeme(config):
    """Register the Tisane service."""
    def get_tisane_service(request: Request) -> TisaneService:
        return TisaneService(request.tisane_config)
    
    config.register_service_factory(
        get_tisane_service,
        iface=TisaneService
    ) 