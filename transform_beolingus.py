from lxml import etree
import input_output


def transform_in_tei(beo_as_dict):
    root = etree.Element('TEI', attrib={"xmlns": 'http://www.tei-c.org/ns/1.0'})

    ##HEADER
    header = etree.SubElement(root, 'teiHeader')

    fileDesc = etree.SubElement(header, 'fileDesc')
    titleStmt = etree.SubElement(fileDesc, 'titleStmt')
    title = etree.SubElement(titleStmt, 'title')
    title.text = 'TEI Version of Beolingus DE-EN'

    publicationStmt = etree.SubElement(fileDesc, 'publicationStmt')
    p_publicationStmt = etree.SubElement(publicationStmt, 'p')
    p_publicationStmt.text = 'Original Data: Copyright (c) :: Frank Richter <frank.richter.tu-chemnitz.de>'

    sourceDesc = etree.SubElement(fileDesc, 'sourceDesc')
    p_sourceDesc = etree.SubElement(sourceDesc, 'p')
    p_sourceDesc.text = 'Digi_Lex - TEI Version'

    ##TEXT
    text = etree.SubElement(root, 'text')
    body = etree.SubElement(text, 'body')

    for k1, v1 in beo_as_dict.items():
        entry = etree.Element('entry')
        for k2, v2 in v1.items():

            splitted_forms = k2.split(';')
            splitted_senses = v2.split(';')

            for f in splitted_forms:
                form = etree.SubElement(entry, 'form')
                orth = etree.SubElement(form, 'orth')
                orth.text = f
            for s in splitted_senses:
                sense = etree.SubElement(entry, 'sense')
                sense.text = s

        body.append(entry)

    et = etree.ElementTree(root)
    return et


et = transform_in_tei(input_output.deserialize('data/splitted_beolingus.pickle'))
et.write('data/beolingus_tei_2.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
