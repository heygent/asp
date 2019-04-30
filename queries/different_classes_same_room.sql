SELECT o1.classe, o2.classe, o1.giorno, o1.ora, o1.aula FROM - o1 
JOIN - o2 
ON o1.classe != o2.classe 
AND o1.giorno = o2.giorno 
AND o1.ora = o2.ora 
AND o1.aula = o2.aula