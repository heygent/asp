import clingo
from collections import namedtuple
from enum import IntEnum
from pathlib import Path


class GiornoSettimana(IntEnum):
    lunedi = 1
    martedi = 2
    mercoledi = 3
    giovedi = 4
    venerdi = 5

    def __str__(self):
        return self.name


orario = namedtuple('orario', 'classe giorno ora materia aula')
classe_ha_docente = namedtuple('classe_ha_docente', 'classe materia docente')
calendario_model = namedtuple('calendario_model',
                              'orario classe_ha_docente number')

CALENDARIO_FILE_PATH = str(Path(__file__).parent.parent / 'calendario.cl')

class CalendarioSolver:
    def __init__(self, arguments):
        self.control = clingo.Control(arguments=arguments)
        self.control.load(CALENDARIO_FILE_PATH)
        self.control.ground(parts=[("base", [])])

    def _extract_data(self, clingo_model):
        model = calendario_model([], [], clingo_model.number)

        for symbol in clingo_model.symbols(shown=True):
            args = symbol.arguments

            if symbol.name == 'orario':

                model.orario.append(
                    orario(args[0].name, GiornoSettimana[args[1].name],
                           args[2].number, args[3].name, args[4].name))

            elif symbol.name == 'classe_ha_docente':

                model.classe_ha_docente.append(
                    classe_ha_docente(args[0].name, args[1].name,
                                      args[2].name))

        model.orario.sort()
        model.classe_ha_docente.sort()
        return model

    def __iter__(self):

        with self.control.solve(yield_=True) as solve_handle:
            for model in solve_handle:
                yield self._extract_data(model)
