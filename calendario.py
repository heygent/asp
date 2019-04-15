#!/usr/bin/env python3
"""
Esegue il parsing dell'output di clingo sul programma "calendario" e stampa in
forma tabellare il risultato.

Richiede la libreria `tabulate` (in Ubuntu: `sudo apt install python-tabulate`)
"""

import re
import sys
from enum import IntEnum, auto
from typing import List, NamedTuple
from tabulate import tabulate


class GiornoSettimana(IntEnum):
    lunedi = auto() 
    martedi = auto()
    mercoledi = auto() 
    giovedi = auto()
    venerdi = auto()


class RigaOrario(NamedTuple):
    classe: str
    giorno: GiornoSettimana
    ora: int
    materia: str
    aula: str


SYMBOL_RE = r"(?P<{}>\w[\d\w]*)"
NUMBER_RE = r"(?P<{}>\d+)"
STRING_RE = r'"(?P<{}>[^"]*)"'


def make_predicate_re(name, arglist):
    args_re = r',\s*'.join(
        regex.format(name) for name, regex in arglist
    )
    return re.compile(rf"{name}\({args_re}\)")


ORARIO_RE = make_predicate_re('orario', [
    ('classe', SYMBOL_RE),
    ('giorno', SYMBOL_RE),
    ('ora', NUMBER_RE),
    ('materia', SYMBOL_RE),
    ('aula', SYMBOL_RE),
])

CLASSE_HA_DOCENTE_RE = make_predicate_re('classe_ha_docente', [
    ('classe', SYMBOL_RE),
    ('materia', SYMBOL_RE),
    ('docente', STRING_RE),
])


def parse_orario(text):
    for match in ORARIO_RE.finditer(text):
        groupdict = match.groupdict()
        groupdict['ora'] = int(groupdict['ora'])
        groupdict['giorno'] = GiornoSettimana[groupdict['giorno']]

        yield RigaOrario(**groupdict)


def parse_classe_ha_docente(text):
    for match in CLASSE_HA_DOCENTE_RE.finditer(text):
        yield match.groups()


def make_orario_table_dicts(righe_orario: List[RigaOrario]):
    orario = {}

    for classe, giorno, ora, materia, aula, *_ in righe_orario:
        giorno = giorno.name
        orario.setdefault(classe, {})
        orario[classe].setdefault(giorno, [None for _ in range(6)])
        orario[classe][giorno][ora - 1] = (materia, aula)

    return orario

def make_docenti_table_dict(pred_tuples):
    pred_tuples = sorted(pred_tuples)

    docenti = {}
    for classe, _, docente in pred_tuples:
        docenti.setdefault(classe, [])
        docenti[classe].append(docente)
    
    materie = []
    for _, materia, _ in pred_tuples:
        if materia in materie:
            break
        materie.append(materia)

    return docenti, materie

if __name__ == '__main__':

    if len(sys.argv) > 2:
        print(f"USAGE: {sys.argv[0]} [FILENAME or -]")
        exit(1)

    if len(sys.argv) < 2 or sys.argv[1] == '-':
        input_file = sys.stdin
    else:
        input_file = open(sys.argv[1])

    with input_file as input_stream:
        input_str = input_stream.read()

    righe = list(parse_orario(input_str))
    righe.sort()
    orario = make_orario_table_dicts(righe)

    for classe, orario_dict in orario.items():
        print(f'\nClasse {classe}\n')
        print(tabulate(orario_dict, headers='keys', showindex=range(1, 7)))

    docenti = list(parse_classe_ha_docente(input_str))
    docenti, materie = make_docenti_table_dict(docenti)
    print('\nDocenti\n')
    print(tabulate(docenti, headers='keys', showindex=materie)) 
