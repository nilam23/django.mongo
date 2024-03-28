import pymongo
from django.conf import settings

def get_db_connection():
  client = pymongo.MongoClient(settings.MONGO_URI)
  db = client[settings.MONGO_DB]

  return db