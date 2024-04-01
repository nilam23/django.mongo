from datetime import datetime
from utils.app_exception import ApplicationException

class User:
  def __init__(self, username, password):
    self.username = username.strip()
    self.password = password
    self.blog_ids = []
    self.created_at = datetime.now()
    self.updated_at = datetime.now()

  def validate(self):
    if len(self.username) < 3:
      raise ApplicationException('username should have at least 3 characters')
    
    if len(self.blog_ids):
      raise ApplicationException('blog_ids should be an empty array')

  def save(self, db_instance):
    users_collection = db_instance['users']
    user_data = {
      'username': self.username,
      'password': self.password,
      'blog_ids': self.blog_ids,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }

    result = users_collection.insert_one(user_data)
    return result.inserted_id
