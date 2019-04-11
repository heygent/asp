% Aule

aula(
  aula_lettere1;
  aula_lettere2;
  aula_matematica;
  aula_tecnologia;
  aula_musica;
  aula_inglese;
  aula_spagnolo;
  aula_religione;
  lab_arte;
  lab_scienze;
  lab_ed_fisica
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
  ed_fisica, "Pantani Michele EdFisica";
  religione, "SanGiuseppe religione"
).

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

% Crea n fatti 'orario' per ogni n := numero di ore in ore_per_materia,
% associando informazioni sull'ora, il giorno e il docente.

OreMateria { orario(Classe, Giorno, Ora, Materia, Docente) : ora(Ora), giorno(Giorno), docente(Materia, Docente) } OreMateria 
:- classe(Classe), ore_per_materia(Materia, OreMateria).

% Vincolo: La stessa classe non può avere due materie diverse nella stessa ora

:- 
  orario(Classe, Giorno, Ora, Materia1, _),
  orario(Classe, Giorno, Ora, Materia2, _),
  Materia1 != Materia2.

#show orario/5.
