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

l'obiettivo di questa esercitazione è quello di creare un calendario accademico
attraverso l'applicativo Clingo, parleremo di come abbiamo definito la base di
conoscenza, gli aggregati, i vincoli e di come abbiamo gestito l'output di
Clingo al fine di rendere la visualizzazione dei dati più agevole.

## Base di conoscenza 

- *ci sono otto aule: lettere (2 aule), matematica, tecnologia, musica, inglese,
  spagnolo, religione*

- *ci sono tre laboratori: arte, scienze, educazione fisica (palestra)*

- *ci sono due docenti per ciascuno dei seguenti insegnamenti: lettere,
  matematica, scienze*

- *vi è un unico docente per tutti gli altri insegnamenti*

- *30 ore complessive, da distribuire in 5 giorni (da lunedì a venerdì), 6 ore
  al giorno*

- *le classi sono: 1A,1B, 2A, 2B, 3A, 3B*

Per quanto riguarda le classi, i giorni della settimana e le ore di lezione, ci
è bastato inserire fatti diversi per ognuno di essi elencando rispettivamente
tutte le classi i giorni e le ore. I fatti più complessi sono invece
`ore_per_materia` in cui abbiamo associato ad ogni materia il numero di ore
settimanali previsto, `aule_per_materia` in cui abbiamo associato ad ogni
materia la rispettiva aula  e `docente` associando ad ogni materia il nome del
docente di sua competenza. La regola `materia(X) :- ore_per_materia(X, _)` serve a
poter richiamare materia attraverso `materia(Materia)` piuttosto che
`ore_per_materia(Materia,_)` semplificando la scrittura del codice.
<!--serve a creare dei fatti di
sole materie a partire dai fatti `ore_per_materia` tutto ciò al solo fine poter
richiamare le materie con `materia(Materia)` senza utilizzare
`ore_per_materia(Materia,_)`. -->
```prolog
% Ore assegnate a ciascuna materia

ore_per_materia(
  lettere, 10; 
  matematica, 4;
  scienze, 2;
  inglese, 3;
  spagnolo, 2;
  musica, 2; 
  tecnologia, 2;
  arte, 2;
  ed_fisica, 2;
  religione, 1
).

% Scorciatoia

materia(X) :- ore_per_materia(X, _).

% Aula assegnata a ciascuna materia

aule_per_materia(
    lettere, aula_lettere1;
    lettere, aula_lettere2;
    matematica, aula_matematica;
    scienze, lab_scienze;
    inglese, aula_inglese;
    spagnolo, aula_spagnolo;
    musica, aula_musica;
    tecnologia, aula_tecnologia;
    arte, lab_arte;
    ed_fisica, lab_ed_fisica;
    religione, aula_religione
).

% Nome assegnato a ciascun docente

docente(
  lettere, "Lucia Lettere1"; 
  lettere, "Annalisa Lettere2"; 
  matematica, "Pozzo Matematica";
  scienze, "Paolo Scienze1"; 
  scienze, "Andrea Scienze2"; 
  scienze, "Luca Scienze3"; 
  scienze, "Gianni Scienze4";
  inglese, "Michele inglese"; 
  spagnolo, "Pierpaolo spagnolo"; 
  musica, "Ernesto musica"; 
  tecnologia, "Tecna Tecnologia"; 
  arte, "Picassa Arte";
  ed_fisica, "Pantani EdFisica";
  religione, "SanPeppe religione"
).

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

            yield self.result_tuple(`parsed_args)
```

## Conclusioni