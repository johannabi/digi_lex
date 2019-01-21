import requests


def test_simple_query(query, query_type, field):
    r = requests.get('http://localhost:5000/v1/search',
                     params={'q': query, 'query_type': query_type, 'field': field})
    print(r.url)
    return r


test_simple_query('Hochwasserabfluss', 'term', 'form')
test_simple_query('.*luss', 'regexp', 'form')
test_simple_query('discharge', 'match', 'sense')
