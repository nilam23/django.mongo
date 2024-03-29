def aggregation_query_for_blogs(filter_query = {}, sort_query = { 'created_at': -1 }, skip = 0, limit = 100):
  query = [
    { '$match': filter_query },
    { '$sort': sort_query },
    { '$skip': skip },
    { '$limit': limit },
    {
      '$lookup': {
        'from': 'users', 
        'localField': 'author_id', 
        'foreignField': '_id', 
        'pipeline': [
            { '$project': { '_id': 0,  'username': 1 } }
        ], 
        'as': 'author_details'
      }
    },
    { '$unwind': '$author_details' },
    {
      '$project': {
        '_id': { '$toString': '$_id' }, 
        'title': 1, 
        'content': 1, 
        'author': '$author_details.username', 
        'created_at': 1
      }
    }
  ]

  return query