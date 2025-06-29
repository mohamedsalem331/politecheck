from pyramid.view import view_config
from pyramid.response import Response
from marshmallow import ValidationError
import json
import requests

from .schemas import TisaneRequestSchema
from politecheck.helpers.validation import get_request_data
from politecheck.services.tisane import TisaneService
from politecheck.services.redis_service import RedisService

class TisaneResource:
    def __init__(self, request):
        self.request = request
        self.request_schema = TisaneRequestSchema()
        self.tisane_service = request.find_service(TisaneService)
        self.redis_service = request.find_service(RedisService)


    @view_config(route_name='tisane', request_method='POST', renderer='json')
    def post(self):
        try:
            validated_data = get_request_data(self.request, self.request_schema)
            user_id = validated_data.get('user_id')
            cached_data = self.redis_service.exists(user_id)
     
            # Use the Tisane service to analyze the text
            response_data = self.tisane_service.analyze_text(validated_data)
            # if cached_data is not none and any object.severity == high in abuse list raise error 400
            if cached_data and any(obj.get('severity') == 'high' for obj in cached_data):
                return Response(
                    json.dumps({"error": "User abuse polarity is high in a span of 30 seconds"}),
                    status=400,
                    content_type='application/json'
                )
            
            # set the user_id in redis with the response_data
            self.redis_service.set(user_id, response_data)
            
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



