import copy

print('hello world')


# STRINGS
def print_strings():
    s = 'digitale'
    print('value of s:', s, type(s), id(s))
    e = s
    print('value of e:', e, type(e), id(e))
    e = e + ' lexicographie'
    print('value of e:', e, type(e), id(e))


# LISTS
def print_lists():
    e = 'digitale lexicographie'
    list1 = []
    list1.append(e)
    list1.append('ws2018/2019')
    print(list1)
    list2 = copy.deepcopy(list1)
    print(list2)
    list1.append('hello_world')
    print(list1, list2)


# SETS
def print_sets():
    set1 = set()
    set1.add('hello')
    set1.add('world')
    set1.add('hello')
    print('set1', set1)
    set2 = set()
    set2.add('digitale')
    my_string = 'lexicographie'
    set2.add(my_string)
    set2.add('hello')
    print('set2', set2)
    set3 = set1.intersection(set2)
    print('set3', set3)
    set4 = set1.union(set2)
    print('set4', set4)


# TUPLES
def print_tuples():
    tuple1 = ('1', 1, True)
    print('tuple_first_object:', tuple1[0], type(tuple1[0]))
    tuple2 = tuple1[0:2]
    print('tuple2', tuple2)


# DICTS
def print_dicts():
    dict1 = {}
    dict1['digitale'] = 'lexicographie'
    dict1['digital'] = 'lexicography'
    dict1['lexicografía'] = 'digital'
    print('start looping')
    for k, v in dict1.items():
        print(k, v)

print_sets()
