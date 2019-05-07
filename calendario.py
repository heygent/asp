#!/usr/bin/env python3
"""
Esegue il parsing dell'output di clingo sul programma "calendario" e stampa in
forma tabellare il risultato.

Richiede la libreria `tabulate` (in Ubuntu: `sudo apt install python-tabulate`)
"""

import re
import sys
import argparse
from itertools import groupby
from tabulate import tabulate
from collections import defaultdict
from lib.calendario_output_parser import parse_clingo_output

def make_classe_table_dict(righe_orario, attr_names):
    orario = defaultdict(list)

    for riga_orario in righe_orario:
        data = map(lambda attrname: str(getattr(riga_orario, attrname)),
                   attr_names)
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


def print_summary(model, cell_data):
    righe, docenti, number = model
    print(f'Answer Set: {number}')

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

    with ns.infile as infile:
        for model in parse_clingo_output(infile):
            if ns.tsv:
                print('\t'.join(ORARIO_PARSER.result_tuple._fields))
                for riga in righe:
                    print('\t'.join(map(str, riga)))
            else:
                print_summary(model, ns.cell_data)
