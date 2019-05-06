#!/usr/bin/env python3

import sys
import sqlite3
import re
from calendario import ORARIO_PARSER, CLASSE_HA_DOCENTE_PARSER

ANSWER_RE = re.compile(r'Answer: (\d+)')

con = sqlite3.connect(sys.argv[1])

con.executescript('''
CREATE TABLE orario(answer_set, classe, giorno, ora, materia, aula);
CREATE TABLE docenti(classe, materia, docente);
''')

parse_next_line = False

for line in sys.stdin:
  match = ANSWER_RE.match(line)
  if match:
    answer_set = int(match.group(1))
    parse_next_line = True
    print(f'Match AS {answer_set}')
  elif parse_next_line:
    parse_next_line = False
    print(list(ORARIO_PARSER.parse(line)))
    print('Execute query')
    con.executemany(f'INSERT INTO orario(answer_set, classe, giorno, ora, materia, aula) VALUES ({answer_set}, ?, ?, ?, ?, ?)',
                      map(str, ORARIO_PARSER.parse(line)))

con.close()