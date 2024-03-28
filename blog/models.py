from djangoPymongo import db_config
from datetime import datetime

class Blog:
  def __init__(self, title, content, author_id):
    self.title = title
    self.content = content
    self.author_id = author_id
    self.created_at = datetime.now()
    self.updated_at = datetime.now()

  def save(self, db_instance):
    blogs_collection = db_instance['blogs']
    blog_data = {
      'title': self.title,
      'content': self.content,
      'author_id': self.author_id,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }

    result = blogs_collection.insert_one(blog_data)
    return result.inserted_id