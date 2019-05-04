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

Abbiamo fatto ricorso agli aggregati per l'assegnazione delle ore di studio alle
classi e per l'assegnazione delle classi ai professori. Abbiamo scelto di
separare l'assegnazione delle materie alle classi da quelle dei docenti
partendo dal presupposto che ogni classe avesse sempre lo stesso docente per una
determinata materia. Se si parte da questo assunto, sono necessarie meno
assegnazioni di docenti che di ore.

Un'alternativa sarebbe potuta essere assegnare il docente e le ore in un unico
aggregato, per poi stabilire che la materia dovesse essere insegnata sempre
dallo stesso docente usando un vincolo. Abbiamo preferito l'approccio usato
perché rende più esplicita la cardinalità delle assegnazioni al docente, e
perché permette di ridurre la complessità degli aggregati separando le due
problematiche.

```prolog
OreMateria { 
    orario(Classe, Giorno, Ora, Materia, Aula) : 
    ora(Ora), giorno(Giorno), aule_per_materia(Materia, Aula)
} OreMateria :- classe(Classe), ore_per_materia(Materia, OreMateria).
```

L'intenzione nell'usare i termini `classe(Classe)` e `ore_per_materia(Materia,
OreMateria)` nel corpo della regola è di rendere vera la testa per ogni
possibile istanziazione della tripletta delle variabili, andando a fare
un'operazione analoga al prodotto cartesiano. 

Nella base di conoscenza abbiamo incluso informazioni sulle ore che vogliamo far
assegnare a ciascuna classe per ogni singola materia nel termine
`ore_per_materia(Materia, OreMateria)`. Possiamo quindi usare la variabile
`OreMateria` per stabilire quante volte creare il termine `orario`, in modo che
ce ne sia uno per ogni ora che vogliamo assegnare.

In `orario`, andiamo ad assegnare anche le 


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