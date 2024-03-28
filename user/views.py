from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from user import services as user_services
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from utils import helpers
  
@csrf_exempt
@api_view(['POST'])
def register(request):
  try:
    db_instance = request.db
    username = request.data['username']
    password = request.data['password']
    hashedPassword = make_password(password)

    user_doc = user_services.find_specific_user(db_instance, { 'username': username })

    if user_doc:
      return JsonResponse({ 'error_message': f'User already exists with the username {username}' }, status=status.HTTP_409_CONFLICT)

    new_user = User(username=username, password=hashedPassword)
    user_id = new_user.save(db_instance)

    jwt_payload = {
      'user_id': str(user_id),
      'username': username,
    }

    jwt_token = helpers.generate_jwt_token(jwt_payload)

    return JsonResponse({ 'data': jwt_token }, status=status.HTTP_201_CREATED)
  except Exception as error:
    return helpers.handle_view_exception(error, 'Exception in register view')

@csrf_exempt
@api_view(['POST'])
def login(request):
  try:
    db_instance = request.db
    username = request.data['username']
    password = request.data['password']
    
    user_doc = user_services.find_specific_user(db_instance, { 'username': username })

    if not user_doc:
      return JsonResponse({ 'error_message': f'User does not exist with the username {username}' }, status=status.HTTP_404_NOT_FOUND)
    
    password_check = check_password(password, user_doc['password'])

    if not password_check:
      return JsonResponse({ 'error_message': 'Password is incorrect' }, status=status.HTTP_400_BAD_REQUEST)
    
    jwt_payload = {
      'user_id': str(user_doc['_id']),
      'username': username,
    }

    jwt_token = helpers.generate_jwt_token(jwt_payload)

    return JsonResponse({ 'data': jwt_token }, status=status.HTTP_200_OK)
  except Exception as error:
    return helpers.handle_view_exception(error, 'Exception in login view')
