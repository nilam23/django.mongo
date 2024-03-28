from djangoPymongo import db_config
from datetime import datetime

class User:
  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.blog_ids = []
    self.created_at = datetime.now()
    self.updated_at = datetime.now()

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
