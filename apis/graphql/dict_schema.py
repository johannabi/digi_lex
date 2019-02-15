import graphene
import json
from collections import namedtuple
from elasticsearch import Elasticsearch
import urllib.parse

client = Elasticsearch()


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    as_python = json.loads(data, object_hook=_json_object_hook)
    return as_python


class Form(graphene.ObjectType):
    form_id = graphene.String()
    orth = graphene.String()
    # gram = graphene.String()
    # usgs = graphene.List(graphene.String)


#class Sense(graphene.ObjectType):
#    sense_id = graphene.String()
#    definition = graphene.String()
#    usgs = graphene.List(graphene.String)


class DictEntry(graphene.ObjectType):
    id = graphene.String()
    forms = graphene.List(Form)
    superentry = graphene.String()
    #senses = graphene.List(Sense)


def select_from_elastic_response(elastic_raw):
    from_elastic = []
    for e in elastic_raw:
        elastic_result = {}
        elastic_result['id'] = e['_id']
        elastic_result['forms'] = e['_source']['forms']
        # elastic_result['senses'] = e['_source']['senses']
        from_elastic.append(elastic_result)
    return from_elastic


def get_from_elastic(dict_id, query, query_type, field):
    query = urllib.parse.unquote(query)
    query_type = urllib.parse.unquote(query_type)
    field = urllib.parse.unquote(field)

    res = ''

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


class DictQuery(graphene.ObjectType):
    entries = graphene.List(DictEntry, dict_id=graphene.String(), query=graphene.String(), query_type=graphene.String(),
                            field=graphene.String())

    def resolve_entries(self, info, query, query_type, field):
        res = get_from_elastic('comp', query=query, query_type=query_type, field=field)
        parsed_results = select_from_elastic_response(res['hits']['hits'])
        return json2obj(json.dumps(parsed_results))
