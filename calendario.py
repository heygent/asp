#!/usr/bin/env python3
"""
Esegue il parsing dell'output di clingo sul programma "calendario" e stampa in
forma tabellare il risultato.

Richiede la libreria `tabulate` (in Ubuntu: `sudo apt install python-tabulate`)
"""

import re
import sys
import argparse
from enum import IntEnum
from collections import namedtuple
from tabulate import tabulate

SYMBOL_RE = r"(?P<{}>\w[\d\w]*)"
NUMBER_RE = r"(?P<{}>\d+)"
STRING_RE = r'"(?P<{}>[^"]*)"'


class PredicateParser:
    def __init__(self, name, arglist):
        self.arglist = arglist
        args_re = r',\s*'.join(
            regex.format(name) for name, regex, *_ in arglist)
        self.re = re.compile(rf"{name}\({args_re}\)")
        self.result_tuple = namedtuple(name,
                                       [argname for argname, *_ in arglist])

    def parse(self, input_str):
        for match in self.re.finditer(input_str):
            parsed_args = match.groupdict()
            for argname, _, argtype in self.arglist:
                parsed_args[argname] = argtype(parsed_args[argname])

            yield self.result_tuple(**parsed_args)


class GiornoSettimana(IntEnum):
    lunedi = 1
    martedi = 2
    mercoledi = 3
    giovedi = 4
    venerdi = 5

    def __str__(self):
        return self.name


ORARIO_PARSER = PredicateParser('orario', [
    ('classe', SYMBOL_RE, str),
    ('giorno', SYMBOL_RE, GiornoSettimana.__getitem__),
    ('ora', NUMBER_RE, int),
    ('materia', SYMBOL_RE, str),
    ('aula', SYMBOL_RE, str),
])

CLASSE_HA_DOCENTE_PARSER = PredicateParser('classe_ha_docente', [
    ('classe', SYMBOL_RE, str),
    ('materia', SYMBOL_RE, str),
    ('docente', STRING_RE, str),
])


def make_orario_table_dicts(righe_orario):
    orario = {}

    for classe, giorno, ora, materia, aula, *_ in righe_orario:
        orario.setdefault(classe, {})
        orario[classe].setdefault(giorno, [None for _ in range(6)])
        orario[classe][giorno][ora - 1] = '\n'.join((materia, aula))

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


def print_summary(righe, docenti):
    orario = make_orario_table_dicts(righe)

    for classe, orario_dict in orario.items():
        print(f'\nClasse {classe}\n')
        print(
            tabulate(orario_dict,
                     tablefmt='grid',
                     headers='keys',
                     showindex=range(1, 7)))

    docenti, materie = make_docenti_table_dict(docenti)
    print('\nDocenti\n')
    print(tabulate(docenti, headers='keys', showindex=materie))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--tsv', action='store_true')
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        nargs='?',
                        default=sys.stdin)
    ns = parser.parse_args()

    with ns.infile:
        input_str = ns.infile.read()

    righe = sorted(ORARIO_PARSER.parse(input_str))
    docenti = sorted(CLASSE_HA_DOCENTE_PARSER.parse(input_str))

    if ns.tsv:
        print('\t'.join(ORARIO_PARSER.result_tuple._fields))
        for riga in righe:
            print('\t'.join(map(str, riga)))
    else:
        print_summary(righe, docenti)
