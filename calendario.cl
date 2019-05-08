%% Base di conoscenza

% Classi

classe(a1; a2; b1; b2; c1; c2).

% Giorni della settimana

giorno(lunedi; martedi; mercoledi; giovedi; venerdi).

% Possibili ore di lezione

ora(1..6).

% Ore da assegnare nell'orario per ciascuna materia

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

% Le materie disponibili

materia(X) :- ore_per_materia(X, _).

% Aule

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

% Docenti

docente(
  lettere, doc_lettere1; 
  lettere, doc_lettere2; 
  matematica, doc_matematica1;
  matematica, doc_matematica2;
  scienze, doc_scienze1; 
  scienze, doc_scienze2; 
  inglese, doc_inglese; 
  spagnolo, doc_spagnolo; 
  musica, doc_musica; 
  tecnologia, doc_tecnologia; 
  arte, doc_arte;
  ed_fisica, doc_edfisica;
  religione, doc_religione 
).

% Le materie che i docenti sono abilitati ad insegnare.

% Ogni docente può insegnare la propria materia.
docente_puo_insegnare(Materia, Docente) :- docente(Materia, Docente).
% I docenti di matematica possono insegnare scienze.
docente_puo_insegnare(scienze, Docente) :- docente(matematica, Docente).

%% Aggregati

% Crea n fatti 'orario' per ogni n = numero di ore in ore_per_materia,
% associando informazioni sull'ora e il giorno.

OreMateria { 
    orario(Classe, Giorno, Ora, Materia, Aula) : 
    ora(Ora), giorno(Giorno), aule_per_materia(Materia, Aula)
} OreMateria :- classe(Classe), ore_per_materia(Materia, OreMateria).

% Per ogni possibile coppia (Classe, Materia) assegna un docente che può 
% insegnare quella materia.

1 { 
  classe_ha_docente(Classe, Materia, Docente) :
  docente_puo_insegnare(Materia, Docente) 
} 1 :- classe(Classe), materia(Materia).

%% Vincoli

% La stessa classe non può avere due materie diverse nella stessa ora.

:- 
  orario(Classe, Giorno, Ora, Materia1, _),
  orario(Classe, Giorno, Ora, Materia2, _),
  Materia1 != Materia2.

% Lo stesso docente non può insegnare in due classi contemporaneamente.

:-
  orario(Classe1, Giorno, Ora, Materia1, _),
  orario(Classe2, Giorno, Ora, Materia2, _),
  Classe1 != Classe2,
  classe_ha_docente(Classe1, Materia1, Docente),
  classe_ha_docente(Classe2, Materia2, Docente).

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


#show orario/5.
#show classe_ha_docente/3.