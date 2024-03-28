from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from utils import helpers
from .models import Blog
from user import services as user_services
from datetime import datetime

@csrf_exempt
@api_view(['POST'])
def create_blog(request):
  try:
    auth_header = request.META['HTTP_AUTHORIZATION']
    
    if not auth_header:
      return JsonResponse({ 'error_message': 'Auth header is missing' }, status=status.HTTP_400_BAD_REQUEST)
    
    token = auth_header.split('Bearer ')[1]
    decoded_token = helpers.verify_jwt_token(token)

    if 'status_code' in decoded_token and decoded_token.status_code == 400:
      return JsonResponse({ 'error_message': 'Incorrect token' }, status=status.HTTP_400_BAD_REQUEST)

    db_instance = request.db
    title = request.data['title']
    content = request.data['content']
    author_id = decoded_token['user_id']

    new_blog = Blog(title=title, content=content, author_id=ObjectId(author_id))
    new_blog_id = new_blog.save(db_instance)

    user_services.update_specific_user(
      db_instance,
      { '_id': ObjectId(decoded_token['user_id']) },
      {
        '$addToSet': { 'blog_ids': ObjectId(new_blog_id) },
        '$set': {'updated_at': datetime.now()},
      },
    )

    return JsonResponse({ 'data': { 'title': title, 'content': content, 'author': decoded_token['username'] } }, status=status.HTTP_201_CREATED)
  except Exception as error:
    return helpers.handle_view_exception(error, 'Exception in create_blog view')