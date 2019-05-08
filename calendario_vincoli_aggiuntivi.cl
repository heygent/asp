#include "calendario.cl".

% Se ci sono più ore di una materia in uno stesso giorno, devono essere
% consecutive.

:-
  orario(Classe, Giorno, Ora1, Materia, _),
  orario(Classe, Giorno, Ora2, Materia, _),
  Ora1 < Ora2,
  not orario(Classe, Giorno, Ora2 - 1, Materia, _).

% Non permettere cambi d'aula nel corso di una lezione.

:-
  orario(Classe, Giorno, Ora1, Materia, Aula1),
  orario(Classe, Giorno, Ora2, Materia, Aula2),
  Ora1 != Ora2,
  Aula1 != Aula2.
