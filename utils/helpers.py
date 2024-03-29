import jwt
from django.conf import settings
import json
from django.http import JsonResponse
from rest_framework import status
import datetime

def generate_jwt_token(payload):
  payload = {
    **payload,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600),
  }

  token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

  return token

def handle_view_exception(exception, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
  error_data = {
    'type': type(exception).__name__,
    'message': str(exception),
  }
  json_error = json.dumps(error_data)

  return JsonResponse({ 'error_message': message, 'error_meta_data': json_error }, status=status_code)