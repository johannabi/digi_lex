import pickle
import pyuca


def sort_set(set_to_sort):
    coll = pyuca.Collator()
    set_to_sort = sorted(set_to_sort, key=coll.sort_key)
    return set_to_sort


def write_set(filename, set_to_write):
    with open(filename, mode='wt', encoding='utf-8') as f:
        for e in set_to_write:
            f.write(str(e) + '\n')


def write_dict(filename, dict_to_write):
    with open(filename, mode='wt', encoding='utf-8') as f:
        for k, v in dict_to_write.items():
            f.write(str(k) + '\t' + str(v) + '\n')


def serialize(filename, data):
    with open(filename, mode='wb') as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)


def deserialize(filename):
    with open(filename, mode='rb') as input:
        return pickle.load(input, encoding='utf-8')
