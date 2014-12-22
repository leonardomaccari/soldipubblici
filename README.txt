Questo software interroga il sito http://soldipubblici.gov.it/
utilizzando una POST che ho reversato dal sito stesso. 

BIG DISCLAIMER: Non esiste una API documentata al momento, quindi i dati
vengono estratti secondo criteri di buon senso, potrebbero non essere
corretti ed il programma potrebbe smettere di funzionare prima o poi.

Questo codice è solo un hack, quindi non vi aspettate una gestione
dell'errore particolarmente solida. 

Come funziona:
 - ho raccolto i codici degli enti pubblici dal sito della ragioneria
   dello stato:
   http://www.rgs.mef.gov.it/VERSIONE-I/e-GOVERNME1/SIOPE/Codici-deg/

 - ho incrociato i codici con la popolazione dei comuni:
   http://www3.istat.it/strumenti/definizioni/comuni/archivo/elenco_comuni_italiani_30_giugno_2010.xls

 - ho creato il file di dati .json nella cartella dati/. il file viene 
   caricato ad ogni avvio. 

 - il crawler apre una sessione con il sito, e fa una query per i primi
   X comuni in ordine di popolazione per la stringa passata da riga di
   comando

 - per ciascun comune diverse voci vengono ritornate dal sito. Il
   valore di ciascuna voce viene raggruppato su tutte le citta' e
   stampato.
 
 - tra ciascuna query c'e' una pausa di un secondo per non essere troppo
   aggressivi


Esempio: la somma delle voci di spesa per la keyword "software" dei
primi 10 comuni più popolosi d'Italia:

> ./crawler.py 10 software


Querying i 10 comuni piu' popolosi d'italia per la keyword 'software'
Querying: COMUNE DI ROMA
Querying: COMUNE DI MILANO
Querying: COMUNE DI NAPOLI
Querying: COMUNE DI TORINO
Querying: COMUNE DI PALERMO
Querying: COMUNE DI GENOVA
Querying: COMUNE DI BOLOGNA
Querying: COMUNE DI FIRENZE
Querying: COMUNE DI BARI
Querying: COMUNE DI CATANIA

------------ Risultati ------------
Per i comuni di: COMUNE DI ROMA,COMUNE DI MILANO,COMUNE DI NAPOLI,COMUNE
DI TORINO,COMUNE DI PALERMO,COMUNE DI GENOVA,COMUNE DI BOLOGNA,COMUNE DI
FIRENZE,COMUNE DI BARI,COMUNE DI CATANIA
Ci sono le seguenti spese (anno 2013):
 -  Licenze software : 10,471,396.0 Euro
 -  Beni immateriali : 31,369.0 Euro
 -  Acquisizione o realizzazione software : 13,436,604.0 Euro
 -  Spese per liti (patrocinio legale) : 6,509,926.0 Euro
 -  Assistenza informatica e manutenzione software : 136,564,879.0 Euro

