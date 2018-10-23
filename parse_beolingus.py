def beolingus_as_list(file):
    lines = []
    with open(file, mode='r') as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith('#'):
                lines.append(line)
    return lines


lines = beolingus_as_list('data/de-en.txt')


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


beo_dict = split_beolingus(lines)

counter = 0
for k, v in beo_dict.items():
    if counter < 10:
        print(k, v)
    counter += 1
