from django.utils.deprecation import MiddlewareMixin
from djangoPymongo import db_config

class PyMongoMiddleware(MiddlewareMixin):
  def process_request(self, request):
    request.db = db_config.get_db_connection()