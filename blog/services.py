def find_all_blogs(db_instance, filter_query):
  blogs = db_instance.blogs.aggregate(filter_query)

  return list(blogs)