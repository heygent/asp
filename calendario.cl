% Aule

aule_per_materia(
    lettere,aula_lettere1;
    lettere,aula_lettere2;
    matematica,aula_matematica;
    scienze,lab_scienze;
    inglese,aula_inglese;
    spagnolo,aula_spagnolo;
    musica,aula_musica;
    tecnologia, aula_tecnologia;
    arte,lab_arte;
    ed_fisica,lab_ed_fisica;
    religione,aula_religione
).

% Docenti

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

% Le materie che i docenti sono abilitati ad insegnare.

% Ogni docente può insegnare la propria materia.
docente_puo_insegnare(Materia, Docente) :- docente(Materia, Docente).
% I docenti di matematica possono insegnare scienze.
docente_puo_insegnare(scienze, Docente) :- docente(matematica, Docente).

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

% Crea n fatti 'orario' per ogni n = numero di ore in ore_per_materia,
% associando informazioni sull'ora e il giorno.

OreMateria { 
    orario(Classe, Giorno, Ora, Materia, Aula) : 
    ora(Ora), giorno(Giorno), aule_per_materia(Materia,Aula)
} OreMateria :- classe(Classe), ore_per_materia(Materia, OreMateria).

% Per ogni possibile coppia (Classe, Materia) assegna un docente che può 
% insegnare quella materia.

1 { 
  classe_ha_docente(Classe, Materia, Docente)
  : docente_puo_insegnare(Materia, Docente) 
} 1 :- classe(Classe), materia(Materia).



%1 {aula_assegnata(Aula, Classe, Giorno, Ora, Materia) : aule_per_materia(Materia,Aula)} 1  
%:- orario(Classe, Giorno, Ora, Materia).



%% Vincoli

% La stessa classe non può avere due materie diverse nella stessa ora.

:- 
  orario(Classe, Giorno, Ora, Materia1,Aula),
  orario(Classe, Giorno, Ora, Materia2,Aula),
  Materia1 != Materia2.

% Lo stesso docente non può insegnare in due classi contemporaneamente.

:-
  orario(Classe1, Giorno, Ora, Materia1,Aula),
  orario(Classe2, Giorno, Ora, Materia2,Aula),
  Classe1 != Classe2,
  classe_ha_docente(Classe1, Materia1, Docente),
  classe_ha_docente(Classe2, Materia2, Docente).

% Tutti i docenti devono avere una classe assegnata.

:- docente(_, Docente), not classe_ha_docente(_, _, Docente).

%non possono esserci due lezioni nella stessa aula 
:-
orario(Aula, Classe1, Giorno, Ora, Materia),
orario(Aula, Classe2, Giorno, Ora, Materia),
Classe1 != Classe2.


#show orario/5.
#show classe_ha_docente/3.
