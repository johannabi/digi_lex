import re


def group_forms(synlist, label):
    synset = set(synlist)
    already_grouped = set()
    forms = list()

    # group orthographic similar syns
    for i1, s1 in enumerate(synset):
        for i2, s2 in enumerate(synset):
            if s1 == s2:
                continue
            if (s1 in already_grouped) & (s2 in already_grouped):
                continue

            if is_same_form(s1, s2):
                # prüfen, ob es zu einem der beiden ein Tupel gibt
                if s1 in already_grouped:
                    for i, t in enumerate(forms):
                        if s1 in t:
                            index = i
                            break

                    prev_form = forms[index]
                    form = prev_form + (s2,)
                elif s2 in already_grouped:
                    for i, t in enumerate(forms):
                        if s2 in t:
                            index = i
                            break

                    prev_form = forms[index]
                    form = prev_form + (s1,)
                else:
                    form = (s1, s2)  # neues tupel erzeugen
                    index = len(forms)
                    forms.append(form)

                forms[index] = form

                # s1 und s2 als "bereits gruppiert" markieren
                already_grouped.add(s1)
                already_grouped.add(s2)

    not_grouped = synset - already_grouped
    for form in not_grouped:
        forms.append((form,))

    # put the tuple with synset label at first position
    for form in forms:
        if label in form:
            forms.remove(form)
            # change order of tuple
            form_list = list(form)
            form_list.remove(label)
            form_list.insert(0,label)
            form = tuple(form_list)
            # insert current form at first position

            forms.insert(0, form)
            break

    return forms


def is_same_form(s1,s2):

    s1 = s1.lower()
    s2 = s2.lower()

    pattern = '[-\/\\\.\s\:#!()\*]+'

    # replace chars by whitespace
    alt1 = re.sub(pattern, ' ', s1)
    alt2 = re.sub(pattern, ' ', s2)
    if alt1 == alt2:
        return True

    # replace chars by nothing
    alt1 = re.sub(pattern, '', s1)
    alt2 = re.sub(pattern, '', s2)
    if alt1 == alt2:
        return True

    # replace ph by f
    alt1 = re.sub('ph', 'f', s1)
    alt2 = re.sub('ph', 'f', s2)
    if alt1 == alt2:
        return True

    return False


def normalize_string(string):

    string = string.lower()  # alles kleinschreiben
    string = re.sub(r"[\s\-]+", '_', string)  # leerzeichen durch unterstrich ersetzen
    string = re.sub('\+', 'pl', string)
    string = re.sub('§', 'p', string)  # paragraph durch p ersetzen
    string = re.sub(r"[^\d\w]+", '', string)  # alles außer buchstaben und zahlen löschen
    string = re.sub('²', '2', string)
    return string
