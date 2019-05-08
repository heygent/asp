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
from operator import attrgetter
from collections import defaultdict


def make_classe_table_dict(righe_orario, docenti, attr_names):
    orario = defaultdict(list)

    for riga_orario in righe_orario:
        data = [
            str(getattr(riga_orario, attr)) for attr in attr_names
            if attr != 'docente'
        ]

        if 'docente' in attr_names:
            docente_materia = next(docente
                                   for (classe, materia, docente) in docenti
                                   if riga_orario.classe == classe
                                   and riga_orario.materia == materia)

            data.append(docente_materia)

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


def print_model_summary(model, cell_data, doctable=False):
    righe, docenti, number = model
    print(f'## Answer Set {number}')

    for (classe, righe_classe), (_, docenti_classe) in zip(
            groupby(righe, attrgetter('classe')),
            groupby(docenti, attrgetter('classe'))):

        orario_classe = make_classe_table_dict(list(righe_classe),
                                               list(docenti_classe), cell_data)

        print()
        print(
            tabulate(orario_classe,
                     tablefmt='grid',
                     headers='keys',
                     showindex=range(1, 7)))
        print(f"""
Table: Orario della classe {classe} nell'Answer Set {number}

\pagebreak
        """
        )

    if doctable:
        docenti, materie = make_docenti_table_dict(docenti)
        print()
        print(
            tabulate(docenti,
                     headers='keys',
                     tablefmt='grid',
                     showindex=materie))
        print('\nTable: Assegnazione dei docenti\n')


def tsv_line_iter(model):
    docenti_dict = {(classe, materia): docente
                    for classe, materia, docente in model.classe_ha_docente}

    for riga_orario in model.orario:
        yield (model.number, *riga_orario, docenti_dict[(riga_orario.classe,
                                                         riga_orario.materia)])


def print_model_tsv(model):
    for row in tsv_line_iter(model):
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
    parser.add_argument('--doctable', action='store_true')
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
                print_model_summary(model, ns.cell_data, doctable=ns.doctable)
