import sqlite3 as sql
from transform import competence


def read_competences(file):
    print(file)
    con = sql.connect(file)
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Categories")

    rows = cur.fetchall()
    # competences = {}
    competences = []
    for r in rows:
        comp_lemma = r["Competence"]
        fl = r["FirstLevelCategory"]
        sl = r["SecondLevelCategory"]
        tl = r["ThirdLevelCategory"]
        syn = r["Synonyms"]
        syn_array = process_syns(syn)
        token = r["Orig_String"]
        c = competence.Competence(lemma=comp_lemma, fl=fl, sl=sl, tl=tl, syn_array=syn_array, token=token)
        competences.append(c)
    return competences


def process_syns(syn):
    if syn is None:
        return ''
    syn_array = syn.split(' | ')
    return syn_array

