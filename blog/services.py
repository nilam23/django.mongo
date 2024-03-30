def find_all_blogs(db_instance, filter_query):
  blogs = db_instance.blogs.aggregate(filter_query)

  return list(blogs)

def update_specific_blog(db_instance, filter_query, update_query):
  result = db_instance.blogs.update_one(filter_query, update_query)

  return result.modified_count

def delete_specific_blog(db_instance, filter_query):
  result = db_instance.blogs.delete_one(filter_query)

  return result.deleted_count