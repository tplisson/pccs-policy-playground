def parse_query_string(query_string):
    query = {}
    if query_string:
        for q in query_string.split(','):
            query[q.split('=')[0]] = q.split('=')[1]
    return query
