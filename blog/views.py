from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from utils import helpers, decorators
from .models import Blog
from user import services as user_services
from datetime import datetime
from blog import services as blog_services
from blog import queries

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

@api_view(['GET'])
def get_all_blogs(request):
  try:
    db_instance = request.db
    aggregation_query = queries.aggregation_query_for_blogs()
    
    blogs = blog_services.find_all_blogs(db_instance, aggregation_query)

    return JsonResponse({ 'data': blogs }, status=status.HTTP_200_OK)
  except Exception as error:
    return helpers.handle_view_exception(error, 'Exception in get_all_blogs view')
  
@api_view(['GET'])
def get_specific_blog(request, blog_id):
  try:
    db_instance = request.db
    aggregation_query = queries.aggregation_query_for_blogs({ '_id': ObjectId(blog_id) })

    blogs = blog_services.find_all_blogs(db_instance, aggregation_query)

    if not len(blogs):
      return JsonResponse({ 'error_message': f'Blog with id {blog_id} not found' }, status=status.HTTP_404_NOT_FOUND)
    
    return JsonResponse({ 'data': blogs[0] }, status=status.HTTP_200_OK)
  except Exception as error:
    return helpers.handle_view_exception(error, 'Exception in get_specific_blog view')
  
@decorators.verify_auth
@csrf_exempt
@api_view(['PATCH'])
def update_specific_blog(request, blog_id):
  try:
    if not len(request.data.keys()):
      return JsonResponse({ 'error_message': 'Data to be updated missing' }, status=status.HTTP_400_BAD_REQUEST)

    current_user = request.current_user
    db_instance = request.db
    filter_query = { '_id': ObjectId(blog_id), 'author_id': ObjectId(current_user['_id']) }
    update_query = {
      '$set': {
        'updated_at': datetime.now(),
      }
    }
    for data_field in list(request.data.keys()):
      update_query['$set'][data_field] = request.data[data_field]

    updated_count = blog_services.update_specific_blog(db_instance, filter_query, update_query)

    if not updated_count:
      return JsonResponse({ 'error_message': f'Blog with id {blog_id} not found' }, status=status.HTTP_404_NOT_FOUND)
    
    aggregation_query = queries.aggregation_query_for_blogs({ '_id': ObjectId(blog_id) })

    blogs = blog_services.find_all_blogs(db_instance, aggregation_query)
    updated_blog = blogs[0]

    return JsonResponse({ 'data': updated_blog }, status=status.HTTP_200_OK)
  except Exception as error:
    return helpers.handle_view_exception(error, 'Exception in update_specific_blog view')
  
@decorators.verify_auth
@csrf_exempt
@api_view(['DELETE'])
def delete_specific_blog(request, blog_id):
  try:
    current_user = request.current_user
    db_instance = request.db
    blog_filter_query = { '_id': ObjectId(blog_id), 'author_id': ObjectId(current_user['_id']) }
    deleted_count = blog_services.delete_specific_blog(db_instance, blog_filter_query)

    if not deleted_count:
      return JsonResponse({ 'error_message': f'Blog with id {blog_id} not found' }, status=status.HTTP_404_NOT_FOUND)
    
    user_filter_query = { '_id': ObjectId(current_user['_id']) }
    user_update_query = {
      '$pull': {
        'blog_ids': ObjectId(blog_id),
      },
      '$set': {
        'updated_at': datetime.now(),
      }
    }

    user_services.update_specific_user(db_instance, user_filter_query, user_update_query)

    return JsonResponse({ 'message': 'Success' }, status=status.HTTP_200_OK)
  except Exception as error:
    return helpers.handle_view_exception(error, 'Exception in delete_specific_blog view')