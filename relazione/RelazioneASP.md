---
# vim: spell spelllang=it
title: Answer Set Programming
subtitle: Progetto di Intelligenze Artificiali e Laboratorio - Parte 1
author:
  - Emanuele Gentiletti
  - Alessandro Caputo
lang: it
titlepage: true
titlepage-color: a20021
titlepage-text-color: ededf4
titlepage-rule-color: ededf4
toc-own-page: true
listings-disable-line-numbers: true

---

# Introduzione

L'obiettivo di questa esercitazione è quello di creare un calendario accademico
attraverso l'applicativo Clingo. Parleremo di come abbiamo definito la base di
conoscenza, gli aggregati, i vincoli e di come abbiamo gestito l'output di
Clingo al fine di rendere la visualizzazione dei dati più agevole.

# Base di conoscenza 

Abbiamo scelto di codificare parte dei requisiti previsti dalla consegna come
parte della "base di conoscenza", e quindi di rappresentarli tramite termini
ground o regole comunque triviali.

> - ci sono otto aule: lettere (2 aule), matematica, tecnologia, musica, inglese,
>   spagnolo, religione
> 
> - ci sono tre laboratori: arte, scienze, educazione fisica (palestra)
> 
> - ci sono due docenti per ciascuno dei seguenti insegnamenti: lettere,
>   matematica, scienze
> 
> - vi è un unico docente per tutti gli altri insegnamenti
> 
> - 30 ore complessive, da distribuire in 5 giorni (da lunedì a venerdì), 6 ore
>   al giorno
> 
> - le classi sono: 1A, 1B, 2A, 2B, 3A, 3B
> 
> - ogni docente insegna una ed una sola materia, con l’eccezione di matematica
>   e scienze, ossia un docente incaricato di insegnare matematica risulterà
>   anche insegnante di scienze (non necessariamente per la stessa classe);

Per quanto riguarda le classi, i giorni della settimana e le ore di lezione, ci
è bastato enumerare ogni possibilità in diversi fatti. I fatti più complessi
sono invece:

- `ore_per_materia`, in cui abbiamo associato a ogni materia il numero di ore
  settimanali previsto.

  ```prolog
  ore_per_materia(
    lettere, 10; 
    matematica, 4;
    scienze, 2;
    ...
  ).
  ```

- `aule_per_materia`, in cui abbiamo associato a ogni materia le rispettive
  aule. Abbiamo scelto di trattare i laboratori come aule, dato che non si
  presentavano differenze a un livello di trattamento nella consegna.

  ```prolog
  aule_per_materia(
      lettere, aula_lettere1;
      lettere, aula_lettere2;
      scienze, lab_scienze;
      ...
  ).
  ```

- `docente`, che associa ad ogni materia i nomi dei docenti di loro competenza.

  ```prolog
  docente(
    lettere, "Lucia Lettere1"; 
    lettere, "Annalisa Lettere2"; 
    matematica, "Rob Matematica";
    ...
  ).
  ```

La regola `materia(X) :- ore_per_materia(X, _)` serve a consultare le materie
disponibili attraverso `materia(Materia)` piuttosto che
`ore_per_materia(Materia, _)`, semplificando la scrittura del codice.

Per rappresentare il fatto che i docenti di matematica possano insegnare
scienze, abbiamo creato una regola che permette di stabilire quali materie il
docente sia abilitato ad insegnare, oltre alla materia propriamente di sua
competenza.

```prolog
% Ogni docente può insegnare la propria materia.
docente_puo_insegnare(Materia, Docente) :- docente(Materia, Docente).
% I docenti di matematica possono insegnare scienze.
docente_puo_insegnare(scienze, Docente) :- docente(matematica, Docente).
```

La prima parte della regola stabilisce trivialmente che ogni docente può
insegnare la sua materia di competenza. Nella seconda parte permettiamo a tutti
i docenti di matematica di insegnare anche scienze.

# Aggregati 

Per costruire i fatti che rappresentano l'orario, abbiamo fatto uso di due
aggregati.

## `orario`

L'aggregato costruisce un fatto `orario` per ognuna delle ore da assegnare a
ciascuna materia.

```{.prolog}
OreMateria { 
    orario(Classe, Giorno, Ora, Materia, Aula) : 
    ora(Ora), giorno(Giorno), aule_per_materia(Materia, Aula)
} OreMateria :- classe(Classe), ore_per_materia(Materia, OreMateria).
```

L'intenzione nell'usare i termini `classe(Classe)` e `ore_per_materia(Materia,
OreMateria)` nel corpo della regola è di rendere vera la testa per ogni
possibile istanziazione della tripletta delle variabili, andando a fare
un'operazione analoga al prodotto cartesiano tra le possibili istanziazioni di
`Classe` e `(Materia, OreMateria)`. Per indicare che vogliamo avere un termine
`orario` per ogni ora da assegnare usiamo la variabile `OreMateria` nella
specifica della cardinalità minima e massima dell'aggregato. In questo modo, ci
saranno `OreMateria` fatti `orario` per ogni classe.

Nel resto dell'aggregato, facciamo assegnare arbitrariamente un'ora, un giorno e
un'aula alla classe tramite le corrispondenti variabili.

## `classe_ha_docente`

```{.prolog}
1 { 
  classe_ha_docente(Classe, Materia, Docente) :
  docente_puo_insegnare(Materia, Docente) 
} 1 :- classe(Classe), materia(Materia).
```

L'aggregato serve a creare un fatto `classe_ha_docente` per ogni classe e
materia. Analogamente a quanto fatto in `orario`, abbiamo specificato
`classe(Classe)` e `materia(Materia)` nel corpo della regola, per enumerare
le possibili combinazioni delle variabili.

In `classe_ha_docente`, lasciamo che venga assegnato in `Docente` un docente tra
quelli abilitati a insegnare la materia di riferimento. Manteniamo anche
l'informazione sulla materia che il docente insegna alla classe, dato che il
requisito per cui i professori di matematica possono anche insegnare scienze
potrebbe lasciare spazio ad ambiguità. In particolare, sarebbe impossibile
stabilire senza contesto se un professore di matematica insegni matematica o
scienze a una determinata classe.

Abbiamo scelto di separare le assegnazioni delle ore di lezione dalle
assegnazioni dei docenti, partendo dal presupposto che per ogni classe una
materia venga sempre insegnata dallo stesso docente. Con questa base di
partenza, sono necessarie meno assegnazioni di docenti che di ore, e servono
meno informazioni per assegnare un docente alla classe che per assegnare un'ora
di lezione, rendendo questa separazione naturale. Un'alternativa che abbiamo
considerato è stata assegnare i docenti direttamente tramite `orario`, per poi
imporre che la materia sia sempre insegnata dallo stesso docente tramite un
vincolo.

\newpage

# Vincoli

Per andare incontro al resto dei requisiti, e per creare delle situazioni che
fossero accettabili dal punto di vista del senso comune, abbiamo fatto
ricorso a diversi vincoli:

* Abbiamo impedito che una classe potesse avere due lezioni in una stessa ora.

  ```{.prolog}
  :- 
    orario(Classe, Giorno, Ora, Materia1, _),
    orario(Classe, Giorno, Ora, Materia2, _),
    Materia1 != Materia2.
  ```

* Abbiamo stabilito che un docente possa insegnare solo in una classe per volta.
  Per farlo, abbiamo indicato che non ci possano essere situazioni in cui il
  docente insegna a classi diverse nello stesso giorno e nella stessa ora.

  ```prolog
  :-
    orario(Classe1, Giorno, Ora, Materia1, _),
    orario(Classe2, Giorno, Ora, Materia2, _),
    Classe1 != Classe2,
    classe_ha_docente(Classe1, Materia1, Docente),
    classe_ha_docente(Classe2, Materia2, Docente).
  ```

* Abbiamo indicato che tutti i docenti dovessero avere una classe assegnata.

  ```prolog
  :- docente(_, Docente), not classe_ha_docente(_, _, Docente).
  ```

* Abbiamo impedito che una classe potesse avere lezione in aule diverse in una
  stessa ora.

  ```prolog
  :- 
    orario(Classe, Giorno, Ora, _, Aula1),
    orario(Classe, Giorno, Ora, _, Aula2),
    Aula1 != Aula2.
  ```

* Infine, abbiamo stabilito che non ci possano essere due lezioni diverse in una
  stessa aula.

  ```prolog
  :-
    orario(Classe1, Giorno, Ora, _, Aula),
    orario(Classe2, Giorno, Ora, _, Aula),
    Classe1 != Classe2.
  ```


Inoltre, abbiamo creato anche un programma alternativo che estende quello
principale con alcuni vincoli che tengono conto di alcune considerazioni di
senso comune. I vincoli aggiunti sono:

* Far sì che tutte le ore di una materia in una giornata siano consecutive.

  ```prolog
  :-
    orario(Classe, Giorno, Ora1, Materia, _),
    orario(Classe, Giorno, Ora2, Materia, _),
    Ora1 < Ora2,
    not orario(Classe, Giorno, Ora2 - 1, Materia, _).
  ```

* Non permettere cambi d'aula nel corso di una stessa lezione.

  ```prolog
  :-
    orario(Classe, Giorno, Ora1, Materia, Aula1),
    orario(Classe, Giorno, Ora2, Materia, Aula2),
    Ora1 != Ora2,
    Aula1 != Aula2.
  ```

# Risultati

Nel programma principale, siamo riusciti a far generare a Clingo circa due
miliardi e mezzo di Answer Set possibili. La ricerca di soluzioni non è stata
esaustiva, ma è stata interrotta per ragioni di tempo.

Per permettere una visualizzazione più agevole dei risultati abbiamo scritto un
programma Python. Il programma può fare il parsing dell'output di Clingo e
stampare i dati contenuti negli Answer Set in forma di tabelle ASCII, o
convertirli in formato Tab Separated Values. Se il modulo Python ufficiale di
Clingo è presente nel sistema, è possibile anche far eseguire il solver
direttamente allo script.

```sh
# Esempi d'uso dello script calendario.py
./calendario.py --solve 1
clingo calendario.cl | ./calendario.py
```

In appendice, alleghiamo il primo Answer Set prodotto da Clingo, il cui markup
per la visualizzazione in questo documento è generato direttamente dal
programma Python.

\pagebreak

# Appendice

