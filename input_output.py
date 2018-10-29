import pickle


def write_dict(filename, beolingus_dict):
    with open(filename, mode='w', encoding='utf-8') as f:
        for k, v in beolingus_dict.items():
            f.write(str(k) + '\t' + str(v) + '\n')


def serialize(filename, data):
    with open(filename, mode='wb') as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)


def deserialize(filename):
    with open(filename, mode='rb') as input:
        return pickle.load(input, encoding='utf-8')
