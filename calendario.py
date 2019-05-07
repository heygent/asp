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


def print_model_summary(model, cell_data):
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


def join_with_docente(model):
    docenti_dict = {(classe, materia): docente
                    for classe, materia, docente in model.classe_ha_docente}

    for riga_orario in model.orario:
        yield (model.number, *riga_orario, docenti_dict[(riga_orario.classe,
                                                         riga_orario.materia)])


def print_model_tsv(model):
    for row in join_with_docente(model):
        print('\t'.join(map(str, row)))


if __name__ == '__main__':

    class Split(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, values.split(','))

    parser = argparse.ArgumentParser()
    parser.add_argument('--tsv', action='store_true')
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        nargs='?',
                        default=sys.stdin)
    parser.add_argument('--cell-data',
                        action=Split,
                        default=['materia', 'aula'])
    parser.add_argument('--solve', action='store', type=int)
    ns = parser.parse_args()

    with ns.infile:
        if ns.solve:
            from lib.calendario_solver import CalendarioSolver
            model_iter = CalendarioSolver([ns.solve])
        else:
            from lib.calendario_output_parser import parse_clingo_output
            model_iter = parse_clingo_output(ns.infile)

        for model in model_iter:
            if ns.tsv:
                print_model_tsv(model)
            else:
                print_model_summary(model, ns.cell_data)
