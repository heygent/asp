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
from itertools import groupby
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


def make_classe_table_dict(righe_orario, attr_names):
    orario = { giorno: [] for giorno in GiornoSettimana }

    for riga_orario in righe_orario:
        data = map(lambda attrname: str(getattr(riga_orario, attrname)), attr_names)
        orario[riga_orario.giorno].append('\n\n'.join(data))

    return orario


def make_docenti_table_dict(pred_tuples):
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


def print_summary(righe, docenti, cell_data):
    for classe, righe_classe in groupby(righe, lambda r: r.classe):
        orario_classe = make_classe_table_dict(righe_classe, cell_data)

        print()
        print(
            tabulate(orario_classe,
                     tablefmt='grid',
                     headers='keys',
                     showindex=range(1, 7)))
        print(f'\nTable: Orario della classe {classe}\n')

    docenti, materie = make_docenti_table_dict(docenti)
    print()
    print(tabulate(docenti, headers='keys', showindex=materie))
    print('\nTable: Assegnazione dei docenti\n')


if __name__ == '__main__':

    class Split(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, values.split(','))

    parser = argparse.ArgumentParser()
    parser.add_argument('--tsv', action='store_true')
    parser.add_argument('--clingo-output', action='store_true')
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        nargs='?',
                        default=sys.stdin)
    parser.add_argument('--cell-data', action=Split, default=['materia', 'aula'])
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
        if ns.clingo_output:
            print(input_str)
        print_summary(righe, docenti, ns.cell_data)
