from functools import wraps
from django.http import JsonResponse
from rest_framework import status
from user import services as user_services
import jwt
from django.http import JsonResponse
from bson import ObjectId
import jwt
from django.conf import settings

def verify_auth(view_func):
  @wraps(view_func)
  def wrapper(request, *args, **kwargs):
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
      token = auth_header.split(' ')[1]
      try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

        user = user_services.find_specific_user(request.db, { '_id': ObjectId(decoded_token['user_id']), 'username': decoded_token['username'] })
        
        if not user:
          return JsonResponse({ 'error_message': 'Unauthorized' }, status=status.HTTP_401_UNAUTHORIZED)
        
        request.current_user = user

        return view_func(request, *args, **kwargs)
      except jwt.ExpiredSignatureError:
        return JsonResponse({'error_message': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
      except jwt.InvalidTokenError:
        return JsonResponse({'error_message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
      return JsonResponse({'error_message': 'Authorization header missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
  
  return wrapper