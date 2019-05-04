---
title: Answer Set Programming
subtitle: Progetto di Intelligenze Artificiali e Laboratorio - Parte 1
author:
  - Emanuele Gentiletti
  - Alessandro Caputo
lang: it
titlepage: true
toc-own-page: true
---

# Introduzione

L'esercitazione prevedeva la creazione di un calendario scolastico secondo vari
requisiti, tramite l'uso dell'applicativo clingo. In seguito spieghiamo come
abbiamo soddisfatto i requisiti richiesti, spiegando mano a mano il codice che
abbiamo usato.

## Base di conoscenza 

Per codificare la situazione iniziale, abbiamo usato vari

```prolog
% Tutti i docenti devono avere una classe assegnata.

:- docente(_, Docente), not classe_ha_docente(_, _, Docente).

% La stessa classe non può avere lezione nella stessa ora in due aule diverse.

:- 
  orario(Classe, Giorno, Ora, _, Aula1),
  orario(Classe, Giorno, Ora, _, Aula2),
  Aula1 != Aula2.

% Non possono esserci due lezioni nella stessa aula.

:-
  orario(Classe1, Giorno, Ora, _, Aula),
  orario(Classe2, Giorno, Ora, _, Aula),
  Classe1 != Classe2.
```

## Aggregati 

## Vincoli 

## Output

```python
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
```

## Conclusioni