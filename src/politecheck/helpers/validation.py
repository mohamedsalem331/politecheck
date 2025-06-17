from marshmallow import ValidationError
from pyramid.response import Response
import json

def get_request_data(request, schema):
    """
    Validate request data against a marshmallow schema.
    
    Args:
        request: The Pyramid request object
        schema: A marshmallow Schema instance to validate against
        
    Returns:
        dict: The validated and deserialized request data
        
    Raises:
        Response: A 400 Bad Request response if validation fails
    """
    try:
        validated_data = schema.load(request.json_body)
        return validated_data
        
    except ValidationError as err:
        raise Response(
            json.dumps({"error": err.messages}),
            status=400,
            content_type='application/json'
        )
    except json.JSONDecodeError:
        raise Response(
            json.dumps({"error": "Invalid JSON data"}),
            status=400,
            content_type='application/json'
        ) 