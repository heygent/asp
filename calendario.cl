materia(lettere; matematica; scienze; inglese; spagnolo;
  musica; tecnologia; arte; ed_fisica; religione).

docenti(lettere, 2).
docenti(matematica, 2).
docenti(scienze, 2).
docenti(X, 1) :- materia(X), not docenti(X, 2).

aule(lettere, 2).
aule(X, 1) :- materia(X), not aule(X, 2).

docente_puo_insegnare(matematica, scienze).
docente_puo_insegnare(X, X) :- materia(X).

classe(a1; a2; a3; b1; b2; b3).

giorno(lun; mar; mer; gio; ven).
ora(1..6).

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


OreMateria {
   orario(Classe, Giorno, Ora, Materia) : ora(Ora), giorno(Giorno) 
} OreMateria :- classe(Classe), ore_per_materia(Materia, OreMateria).

% conflitto :- 
%   materia(M),
%   materia(N),
%   M != N,
%   orario(A, S, G, O, M),
%   orario(A, S, G, O, M).

% :- conflitto.

#show orario/4.