import json
import flask
import urllib
from elasticsearch import Elasticsearch
from flask import make_response
from werkzeug.routing import Map, Rule

client = Elasticsearch()

app = flask.Flask(__name__)


def make_json_response(obj):
    resp = flask.Response(json.dumps(obj, indent=2, ensure_ascii=False), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers["Content-Type"] = "application/json; charset=utf-8"
    return resp


def select_from_elastic_response(elastic_raw):
    data = {}
    from_elastic = []
    for e in elastic_raw:
        print(e)
        elastic_result = {}
        elastic_result['id'] = e['_id']
        elastic_result['forms'] = e['_source']['forms']
        #elastic_result['senses'] = e['_source']['senses']
        from_elastic.append(elastic_result)
    data['data'] = from_elastic
    return data


def get_from_elastic(dict_id, query, query_type, field):
    query = urllib.parse.unquote(query)
    query_type = urllib.parse.unquote(query_type)
    field = urllib.parse.unquote(field)
    if field == 'form':
        res = client.search(index=dict_id,
                            body={
                                "query": {
                                    "nested": {
                                        "path": "forms",
                                        "query": {
                                            query_type: {
                                                "forms.orth": query
                                            }
                                        }
                                    }
                                }})

    return res


@app.errorhandler(404)
def not_found(error):
    return make_response(flask.jsonify({'error': 'Not found'}), 404)


@app.endpoint('info')
def api_root():
    info = {
        'name': app.config['APPLICATION_NAME'],
    }
    return make_json_response(info)


@app.endpoint('search')
def search():
    query = flask.request.args.get("q")
    field = flask.request.args.get("field")
    query_type = flask.request.args.get("query_type")

    if query:
        if query_type is None:
            query_type = 'term'
        elastics_response = get_from_elastic('comp', query, query_type, field)
        resp = make_json_response(
            select_from_elastic_response(elastics_response['hits']['hits']))
    else:
        elastics_response = {
            'you need to use this path for searching': ':',
            'paramaters': ':',
            'q': 'your_query',
            'field': 'form|sense',
            'query_type': '(term, prefix ...) for more see elastic docs',
        }
        resp = make_json_response(elastics_response)

    return resp


app.url_map = Map([
    Rule('/v1', endpoint='info'),
    Rule('/v1/search', endpoint='search')
])

app_name = app.config["APPLICATION_NAME"] = 'COMP_REST_API'
app_port = app.config.get('APPLICATION_PORT', 5000)


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', app_port, app)
