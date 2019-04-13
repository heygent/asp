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


SYMBOL_RE = r"\w[\d\w]*"
NUMBER_RE = r"\d+"
STRING_RE = r'"[^"]*"'

ORARIO_ARGS = [
    ('classe', SYMBOL_RE),
    ('giorno', SYMBOL_RE),
    ('ora', NUMBER_RE),
    ('materia', SYMBOL_RE),
]

ORARIO_ARGS_RE = r',\s*'.join(
    r"(?P<{}>{})".format(name, regex) for name, regex in ORARIO_ARGS
)

ORARIO_RE = re.compile(rf"orario\({ORARIO_ARGS_RE}\)")


def parse_orario(text):
    for match in ORARIO_RE.finditer(text):
        groupdict = match.groupdict()
        groupdict['ora'] = int(groupdict['ora'])
        groupdict['giorno'] = GiornoSettimana[groupdict['giorno']]

        yield RigaOrario(**groupdict)


def transform_for_tabulate(righe_orario: List[RigaOrario]):
    orario = {}

    for classe, giorno, ora, materia, *_ in righe_orario:
        giorno = giorno.name
        orario.setdefault(classe, {})
        orario[classe].setdefault(giorno, [None for _ in range(6)])
        orario[classe][giorno][ora - 1] = materia

    return orario


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
    orario = transform_for_tabulate(righe)

    for classe, orario_classe in orario.items():
        print(f'\nClasse {classe}\n')
        print(tabulate(orario_classe, headers='keys', showindex=range(1, 7)))