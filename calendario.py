#!/usr/bin/env python3

import clingo
from collections import defaultdict
from typing import NamedTuple
from tabulate import tabulate

c = clingo.Control()
c.load("calendario.cl")
c.ground(parts=[("base", [])])

HEADERS = ['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi']

with c.solve(yield_=True) as solve_handle:
  for model in solve_handle:
    model: clingo.Model
    symbols = model.symbols(shown=True)

    orario = {}

    for orario_symbol in filter(lambda s: s.name == 'orario', symbols):
      classe, giorno, ora, materia, *_ = map(str, orario_symbol.arguments)
      ora = int(ora)
      orario.setdefault(classe, {})
      orario[classe].setdefault(giorno, [None for _ in range(6)])
      orario[classe][giorno][ora - 1] = materia

    for classe, orario_classe in sorted(orario.items()):
      print(f'\nClasse {classe}\n')
      print(tabulate(orario_classe, headers=HEADERS, showindex=range(1,7)))