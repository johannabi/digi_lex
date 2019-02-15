from lxml import etree
from elasticsearch import Elasticsearch
from elasticsearch_dsl import document, field, InnerDoc, analyzer, connections, Index
from datetime import datetime
from bs4 import BeautifulSoup

namespaces = {'ns': 'http://www.tei-c.org/tei/1.0'} # key ursprünglich ns

html_strip = analyzer('html_strip',
                      tokenizer="standard",
                      filter=["standard", "lowercase"],
                      char_filter=["html_strip"])

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])
client = Elasticsearch()


class Form(InnerDoc):
    form_id = field.Text()
    orth = field.Keyword(fields={'raw': field.Keyword()})


class Entry(document.Document):
    forms = field.Nested(Form)
    created = field.Date()
    superentry = field.Text()

    def save(self, **kwargs):
        return super(Entry, self).save(**kwargs)

    def is_published(self):
        return datetime.now() > self.created


def get_tei_entries(comp_tei):
    handler = open(comp_tei).read() # TODO utf8 encoding
    soup = BeautifulSoup(handler, 'lxml-xml')
    superentries = soup.find_all('superEntry')
    return(superentries)


def index_entries(superentries, index_name):
    for i, e in enumerate(superentries):

        # meta bezieht sich auf elastic search
        se_index = e.get('xml:id') # index of superEntry
        entries = e.find_all('entry')
        for entry in entries:
            entry_to_index = Entry(meta={'id': entry.get('xml:id'), 'index': index_name})
            tei_forms = e.find_all('form')

            forms = []

            for form in tei_forms:
                form_id = form.get('xml:id')
                new_form = Form()
                new_form.form_id = form_id

                # TODO multiple orthographies
                tei_orths = form.find_all('orth')
                # provisorisch wird nur die erste Orth aufgenommen
                new_form.orth = tei_orths[0].text
                forms.append(new_form)

            entry_to_index.forms = forms

            entry_to_index.created = datetime.now()
            entry_to_index.save()


def delete_index(index_name):
    to_del = Index(index_name)
    # delete the index, ignore if it doesn't exist
    to_del.delete(ignore=404)


def index_file(index_name, tei_file):
    Entry.init(index_name)
    # entries = get_tei_entries(tei_file)
    entries = get_tei_entries(tei_file)
    index_entries(entries, index_name)
    print('done with it')


def del_and_re_index(index_name, tei_to_index):
    print('deleting index:  ', index_name)
    delete_index(index_name)
    print('creating index:  ', index_name)
    index_file(index_name, tei_to_index)


del_and_re_index('comp', '../data_to_publish/compdict_clean.tei')
# get_tei_entries('../data_to_publish/compdict.tei')
