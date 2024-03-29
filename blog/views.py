from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from utils import helpers, decorators
from .models import Blog
from user import services as user_services
from datetime import datetime

@decorators.verify_auth
@csrf_exempt
@api_view(['POST'])
def create_blog(request):
  try:
    current_user = request.current_user
    db_instance = request.db
    title = request.data['title']
    content = request.data['content']
    author_id = current_user['_id']

    new_blog = Blog(title=title, content=content, author_id=ObjectId(author_id))
    new_blog_id = new_blog.save(db_instance)

    user_services.update_specific_user(
      db_instance,
      { '_id': ObjectId(current_user['_id']) },
      {
        '$addToSet': { 'blog_ids': ObjectId(new_blog_id) },
        '$set': {'updated_at': datetime.now()},
      },
    )

    return JsonResponse({ 'data': { 'title': title, 'content': content, 'author': current_user['username'] } }, status=status.HTTP_201_CREATED)
  except Exception as error:
    return helpers.handle_view_exception(error, 'Exception in create_blog view')