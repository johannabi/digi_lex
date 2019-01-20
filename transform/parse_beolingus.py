import re
from utils import input_output


def beolingus_as_list(file):
    lines = []
    with open(file, mode='r') as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith('#'):
                lines.append(line)
    return lines


def split_beolingus(lines):
    beo_dict = {}
    for i, line in enumerate(lines):
        i += 1
        line_dict = {}
        line = line.split('::')
        german = line[0]
        english = line[1]
        german = german.split('|')
        english = english.split('|')
        # if len(german) != len(english):
        #    print(line)
        for e, l in enumerate(german):
            line_dict[german[e]] = english[e]
        beo_dict[i] = line_dict
    return beo_dict


def pre_process_beo(beo_as_dict):
    # we need to replace all the ';' between brackets. we chose a '|' as replacement.
    desc_pattern = re.compile(r'(\((.*?)\))')
    for k1, v1 in beo_as_dict.items():
        for k2, v2 in v1.items():
            key_matches = desc_pattern.findall(str(k2))
            val_matches = desc_pattern.findall(str(v2))
            for match in key_matches:
                if ';' in match[1]:
                    rep = match[1].replace(';', '|')
                    k2 = str(k2).replace(match[1], rep)
                    k2 = k2.strip()
                    v1 = {k2: v2}
                    beo_as_dict[k1] = v1
            for match in val_matches:
                if ';' in match[1]:
                    rep = match[1].replace(';', '|')
                    v2 = str(v2).replace(match[1], rep)
                    v2 = v2.strip()
                    v1 = {k2: v2}
                    beo_as_dict[k1] = v1
    return beo_as_dict


def get_usg(beo_as_dict):
    usg_set = set()
    usg_pattern = re.compile(r'(\[(.*?)\])')
    for k, v in beo_as_dict.items():
        usg_matches = usg_pattern.findall(str(v))
        for match in usg_matches:
            usg_set.add(match[0])
    return usg_set


def get_gramm_info(beo_as_dict):
    gramm_set = set()
    gramm_pattern = re.compile(r'\{(.*?)\}')
    for k, v in beo_as_dict.items():
        usg_matches = gramm_pattern.findall(str(v))
        for match in usg_matches:
            gramm_set.add(match)
    return gramm_set


prepro = pre_process_beo(input_output.deserialize('data_to_process/splitted_beolingus.pickle'))
input_output.write_dict('data_to_process/splitted_beolingus_prepro.txt', prepro)
