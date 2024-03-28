def find_specific_user(db_instance, filter_query):
  user_doc = db_instance.users.find_one(filter_query)

  return user_doc

def update_specific_user(db_instance, filter_query, update_query):
  result = db_instance.users.update_one(filter_query, update_query)
  
  return result.modified_count