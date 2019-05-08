import re
from collections import namedtuple
from enum import IntEnum
from itertools import tee

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
    ('docente', SYMBOL_RE, str),
])

calendario_model = namedtuple('calendario_model',
                              'orario classe_ha_docente number')


def pairwise(iter):
    a, b = tee(iter)
    next(b)
    return zip(a, b)


ANSWER_RE = re.compile(r'Answer: (\d+)')


def parse_clingo_output(line_iter):
    for answer_str, model_str in pairwise(line_iter):
        answer_match = ANSWER_RE.match(answer_str)
        if answer_match:
            model_number = answer_match.group(1)
            yield calendario_model(
                number=model_number,
                orario=sorted(ORARIO_PARSER.parse(model_str)),
                classe_ha_docente=sorted(
                    CLASSE_HA_DOCENTE_PARSER.parse(model_str)),
            )
