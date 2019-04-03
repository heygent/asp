%8 aule
aula(
  lettere1;
  lettere2;
  matematica;
  tecnologia;
  musica;
  inglese;
  spagnolo;
  religione
).

%3 lab
lab(arte; scienze; educazione_fisica).

%docenti
docente(
  doc_lettedre1; 
  doc_lettere2; 
  doc_mate_scienze1; 
  doc_mate_scienze2; 
  doc_mate_scienze3; 
  doc_mate_scienze4;
  doc_tecnologia; 
  doc_musica; 
  doc_inglese; 
  doc_spagnolo; 
  doc_religione
).

%materie
materia(lettere; matematica; tecnologia; musica; inglese; spagnolo; religione).

%tipi di classe
classe(a1; a2; b1; b2; c1; c2).

%giornisettimana
giorno(lunedi; martedi; mercoledi; giovedi; venerdi).

%ore
ora(1..6).

%ad ogni giorno della settimana  assegna  6 materie
%6 {assegna(P,T) : materia(P)} 6 :- giorno(T).

%ore per materia 
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

% Vincolo: La stessa classe non può avere due materie diverse nella stessa ora

:- 
  orario(Classe, Giorno, Ora, Materia1),
  orario(Classe, Giorno, Ora, Materia2),
  Materia1 != Materia2.

OreMateria { orario(Classe, Giorno, Ora, Materia) : ora(Ora), giorno(Giorno) } OreMateria 
:- classe(Classe), ore_per_materia(Materia, OreMateria).


#show orario/4.


