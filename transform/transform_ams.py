from lxml import etree
from utils import input_output
from utils import util


def transform_in_tei(fl_groups):
    root = etree.Element('TEI', attrib={"xmlns": 'http://www.tei-c.org/ns/1.0'})

    # #HEADER
    header = etree.SubElement(root, 'teiHeader')

    file_desc = etree.SubElement(header, 'fileDesc')
    title_stmt = etree.SubElement(file_desc, 'titleStmt')
    title = etree.SubElement(title_stmt, 'title')
    title.text = 'TEI Version of AMS Kompetenzen'

    publication_stmt = etree.SubElement(file_desc, 'publicationStmt')
    p_publication_stmt = etree.SubElement(publication_stmt, 'p')
    p_publication_stmt.text = 'Original Data: AMS Kompetenzen'

    source_desc = etree.SubElement(file_desc, 'sourceDesc')
    p_source_desc = etree.SubElement(source_desc, 'p')
    p_source_desc.text = 'Digi_Lex - TEI Version'

    # #TEXT
    text = etree.SubElement(root, 'text')
    body = etree.SubElement(text, 'body')

    fl_index = 0
    for fl_label, fl_list in fl_groups.items():
        fl_index += 1
        div_fl = etree.SubElement(body, 'div')
        div_fl.attrib['{http://www.w3.org/XML/1998/namespace}id'] = 'first_level_' + str(fl_index)
        div_fl.attrib['label'] = fl_label
        sl_groups = group_competences(fl_list, 'sl')
        sl_index = 0
        for sl_label, sl_list in sl_groups.items():
            sl_index += 1
            div_sl = etree.SubElement(div_fl, 'div')
            div_sl.attrib['{http://www.w3.org/XML/1998/namespace}id'] = 'second_level_' \
                                                                        + str(fl_index) + '_' \
                                                                        + str(sl_index)
            div_sl.attrib['label'] = sl_label
            tl_groups = group_competences(sl_list, 'tl')
            tl_index = 0
            for tl_label, tl_list in tl_groups.items():
                tl_index += 1
                super_entry = etree.SubElement(div_sl, 'superEntry')
                super_entry.attrib['{http://www.w3.org/XML/1998/namespace}id'] = 'se_' \
                                                                                 + str(fl_index) + '_' \
                                                                                 + str(sl_index) + '_' \
                                                                                 + str(tl_index)
                super_entry.attrib['label'] = tl_label
                entry_list = group_syns(tl_list, tl_label)

                for e_index, entry in enumerate(entry_list):
                    tei_entry = etree.SubElement(super_entry, 'entry')

                    forms = util.group_forms(entry, tl_label)
                    # forms enthält nun alle synonyme gruppiert nach orthographischer Aehnlichkeit
                    curr_label = forms[0][0]
                    normalized_id = util.normalize_string(curr_label)
                    id = str(fl_index) + '_' + str(sl_index) + '_' + str(tl_index) + '_' + normalized_id
                    tei_entry.attrib['{http://www.w3.org/XML/1998/namespace}id'] = 'e_' + id
                    tei_entry.attrib['label'] = curr_label
                    for f_index, form in enumerate(forms):

                        normalized_id = util.normalize_string(form[0])
                        id = str(fl_index) + '_' + str(sl_index) + '_' + str(tl_index) + '_' + normalized_id
                        tei_form = etree.SubElement(tei_entry, 'form')
                        tei_form.attrib['{http://www.w3.org/XML/1998/namespace}id'] = 'f_' + id
                        tei_form.attrib['label'] = form[0]

                        for o_index, orth in enumerate(form):

                            if orth == tl_label:  # TODO
                                tei_form.attrib['type'] = 'standard'

                            tei_orth = etree.SubElement(tei_form, 'orth')
                            tei_orth.text = orth
                            tei_orth.attrib[
                                '{http://www.w3.org/XML/1998/namespace}id'] = 'o_' + id + '_' + str(o_index)
                            tei_orth.attrib['source'] = 'ams'
                            tei_orth.attrib['valid'] = 'true'


    et = etree.ElementTree(root)
    return et


# groups competence objects according to their synonyms
def group_syns(entrys, label):
    all_competences = [] #contains all strings that are already listed in grouped_entries
    grouped_entries = []
    main_entry = [] #synset that contains the label of the hypersynset
    for c in entrys:
        token = c.token
        syns = c.syn_array
        already_listed = False
        for s in syns:
            if s in all_competences:
                already_listed = True
                break
        if not already_listed:
            entry = []
            is_main_entry = False
            for s in syns:
                entry.append(s)
                all_competences.append(s)
            entry.append(token)
            all_competences.append(token)

            if label in entry:
                is_main_entry = True
            entry = sorted(entry)
            if not is_main_entry:
                grouped_entries.append(entry)
            else:
                main_entry = entry

    grouped_entries.insert(0, main_entry)
    return grouped_entries


def group_competences(comps, level):
    groups = {}
    for v in comps:
        if level == 'fl':
            curr_group = v.fl
        elif level == 'sl':
            curr_group = v.sl
        elif level == 'tl':
            curr_group = v.tl
        first_level_list = []
        f = groups.get(curr_group)
        if f is not None:
            first_level_list = f
        first_level_list.append(v)
        groups[curr_group] = first_level_list
    return groups


def validate(tei_file, rng_schema):
    parser = etree.XMLParser(recover=True)
    tei_parsed = etree.parse(tei_file, parser)
    rng_parsed = etree.parse(rng_schema)
    rng_validator = etree.RelaxNG(rng_parsed)
    validation_rng = rng_validator.validate(tei_parsed)
    return validation_rng


all_competences = input_output.read_competences('../data_to_process/CategorizedCompetences.db')
et = transform_in_tei(group_competences(all_competences,'fl'))
# TODO add xml model (relaxNG) to et
et.write('../data_to_publish/compdict.tei', pretty_print=True, xml_declaration=True, encoding='utf-8')

val = validate('../data_to_publish/compdict.tei','../data_to_publish/out/compdict.rng')
print('TEI-Document is valid: ', val)