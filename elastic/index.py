from lxml import etree
from elasticsearch import Elasticsearch
from elasticsearch_dsl import document, field, InnerDoc, analyzer, connections, Index
from datetime import datetime

namespaces = {'ns': 'http://www.tei-c.org/ns/1.0'}

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
    gram = field.Text(analyzer='standard')
    usgs = field.Text(analyzer='standard')


class Sense(InnerDoc):
    sense_id = field.Text()
    definition = field.Text(analyzer='standard')
    usgs = field.Text(analyzer='standard')


class Entry(document.Document):
    forms = field.Nested(Form)
    senses = field.Nested(Sense)
    created = field.Date()

    def save(self, **kwargs):
        return super(Entry, self).save(**kwargs)

    def is_published(self):
        return datetime.now() > self.created


def get_tei_entries(beo_tei):
    tree = etree.parse(beo_tei)
    entries = tree.xpath('//ns:entry', namespaces=namespaces)
    print('len_entries', len(entries))
    return entries


def index_entries(entries, index_name):
    for i, e in enumerate(entries):

        # get each form
        entry_to_index = Entry(meta={'id': e.attrib['{http://www.w3.org/XML/1998/namespace}id'], 'index': index_name})

        tei_forms = e.xpath('./ns:form', namespaces=namespaces)

        forms = []

        for form in tei_forms:
            form_id = form.attrib['{http://www.w3.org/XML/1998/namespace}id']
            new_form = Form()
            new_form.form_id = form_id
            orths = form.xpath('./ns:orth', namespaces=namespaces)
            new_form.orth = orths[0].text
            grams = form.xpath('./ns:gramGrp/ns:gram', namespaces=namespaces)
            if len(grams) > 0:
                new_form.gram = grams[0].text
            form_usgs = form.xpath('./ns:usg', namespaces=namespaces)
            if len(form_usgs) > 0:
                form_usgs_text = []
                for usg in form_usgs:
                    form_usgs_text.append(usg.text)
                new_form.usgs = form_usgs_text
            forms.append(new_form)

        entry_to_index.forms = forms

        tei_senses = e.xpath('./ns:sense', namespaces=namespaces)

        senses = []
        for sense in tei_senses:
            sense_id = sense.attrib['{http://www.w3.org/XML/1998/namespace}id']
            new_sense = Sense()
            new_sense.sense_id = sense_id
            defs = sense.xpath('./ns:def', namespaces=namespaces)
            new_sense.definition = defs[0].text
            sense_usgs = form.xpath('./ns:usg', namespaces=namespaces)
            if len(sense_usgs) > 0:
                sense_usgs_text = []
                for usg in sense_usgs:
                    sense_usgs_text.append(usg.text)
                new_sense.usgs = sense_usgs_text
            senses.append(new_sense)

        entry_to_index.senses = senses

        entry_to_index.created = datetime.now()
        entry_to_index.save()


def delete_index(index_name):
    to_del = Index(index_name)
    # delete the index, ignore if it doesn't exist
    to_del.delete(ignore=404)


def index_file(index_name, tei_file):
    Entry.init(index_name)
    entries = get_tei_entries(tei_file)
    index_entries(entries, index_name)
    print('done with it')


def del_and_re_index(index_name, tei_to_index):
    print('deleting index:  ', index_name)
    delete_index(index_name)
    print('creating index:  ', index_name)
    index_file(index_name, tei_to_index)


del_and_re_index('beo', 'data_to_publish/beo_en_de_short.tei')

# get_tei_entries('data_to_publish/beo_en_de_short.tei')
