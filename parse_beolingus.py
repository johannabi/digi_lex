import re

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


beo_list = beolingus_as_list('data/de-en.txt')
# beo_dict = split_beolingus(beo_list)
# write_dict('data/splitted_beolingus.txt', beo_dict)
# serialize('data/splitted_beolingus.pickle', beo_dict)
beo_dict = input_output.deserialize('data/splitted_beolingus.pickle')
pos_pattern = re.compile(r'\{\w+\}')
usg_pattern = re.compile(r'\[\w+\.?\]')
usg_set = set()
counter = 0
for k, v in beo_dict.items():
    # if counter < 10:
    usg_matches = usg_pattern.findall(str(v))
    for match in usg_matches:
        usg_set.add(match)
    counter += 1

usg_set = sorted(usg_set)

for e in usg_set:
    print(e)
