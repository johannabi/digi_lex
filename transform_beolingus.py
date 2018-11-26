import re
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

    usg_pattern = re.compile(r'\[\w+\.?\]')
    gramm_pattern = re.compile(r'\{\w+\.?\}')

    for k1, v1 in beo_as_dict.items():

        if len(v1) > 1:
            super_entry = etree.Element('superEntry')

        for k2, v2 in v1.items():

            entry = etree.Element('entry')

            splitted_forms = k2.split(';')
            splitted_senses = v2.split(';')

            for f in splitted_forms:
                form = etree.SubElement(entry, 'form')
                orth = etree.SubElement(form, 'orth')

                gramm_matches = gramm_pattern.findall(f)
                usg_matches = usg_pattern.findall(f)
                # we assume , and only allow one gram per form
                if len(gramm_matches) > 0:
                    grammGrp = etree.SubElement(form, 'gramGrp')
                    gramm = etree.SubElement(grammGrp, 'gram')
                    gramm.text = gramm_matches[0]
                    f = f.replace(gramm_matches[0], '')

                if len(usg_matches) > 0:
                    for match in usg_matches:
                        usg = etree.SubElement(form, 'usg')
                        usg.text = match
                        f = f.replace(match, '')

                f = f.strip()
                orth.text = f
            for s in splitted_senses:
                sense = etree.SubElement(entry, 'sense')
                usg_matches = usg_pattern.findall(s)
                if len(usg_matches) > 0:
                    for match in usg_matches:
                        usg = etree.SubElement(sense, 'usg')
                        usg.text = match
                        s = s.replace(match, '')

                definition = etree.SubElement(sense, 'def')
                s = s.strip()
                definition.text = s

            if len(v1) > 1:
                super_entry.append(entry)
                super_entry.attrib['n'] = str(k1)
                body.append(super_entry)

            else:
                entry.attrib['n'] = str(k1)
                body.append(entry)

    et = etree.ElementTree(root)
    return et


et = transform_in_tei(input_output.deserialize('data/splitted_beolingus.pickle'))
et.write('data/beolingus_tei_2.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
