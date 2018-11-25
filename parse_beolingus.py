import re
import unicodedata
import input_output


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


def get_usg(beo_as_dict):
    usg_set = set()
    usg_pattern = re.compile(r'\[\w+\.?\]')
    counter = 0
    for k, v in beo_as_dict.items():
        # if counter < 10:
        usg_matches = usg_pattern.findall(str(v))
        for match in usg_matches:
            usg_set.add(match)
        counter += 1
    return usg_set


def get_pos(beo_as_dict):
    pos_set = set()
    pos_pattern = re.compile(r'\{\w+\.?\}')
    counter = 0
    for k, v in beo_as_dict.items():
        # if counter < 10:
        usg_matches = pos_pattern.findall(str(v))
        for match in usg_matches:
            pos_set.add(match)
        counter += 1
    return pos_set


pos = get_pos(input_output.deserialize('data/splitted_beolingus.pickle'))
for e in pos:
    print(e)
