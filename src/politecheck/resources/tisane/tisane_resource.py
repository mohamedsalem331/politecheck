from pyramid.view import view_config
from pyramid.response import Response
from marshmallow import ValidationError
import json
import requests

from .schemas import TisaneRequestSchema
from politecheck.helpers.validation import get_request_data
from politecheck.services.tisane import TisaneService

class TisaneResource:
    def __init__(self, request):
        self.request = request
        self.request_schema = TisaneRequestSchema()
        self.tisane_service = request.find_service(TisaneService)

    @view_config(route_name='tisane', request_method='POST', renderer='json')
    def post(self):
        try:
            validated_data = get_request_data(self.request, self.request_schema)
            
            # Use the Tisane service to analyze the text
            response_data = self.tisane_service.analyze_text(validated_data)
            return response_data
            
        except Response as response:
            return response
        except requests.exceptions.RequestException as e:
            return Response(
                json.dumps({"error": f"Tisane API error: {str(e)}"}),
                status=500,
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type='application/json'
            )



