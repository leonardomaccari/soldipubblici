#!/usr/bin/env python


# copyright 2014 leonardo maccari: mail@leonardo.ma


#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import soldipubblici
import json
from collections import defaultdict
from time import sleep
import sys

f = open("data/codici_comuni_ordinati.json",'r')

comuni_italiani_ordinati = json.load(f)
if len(sys.argv) != 3:
    print "Questo script restituisce la somma delle voci di costo "
    print "per una singola stringa di ricerca, per i primi X comuni "
    print "d'Italia, per l'anno 2013."
    print ""
    print "Leggete README.txt per capire i dettagli."
    print ""
    print "usage:"
    print "./test_crawler.py numero_comuni stringa_di_ricerca"
    sys.exit(1)

results = {}
numero_comuni = int(sys.argv[1])
stringa_ricerca = sys.argv[2]
s = soldipubblici.soldi_pubblici()
lista_comuni = []

print "Querying i", numero_comuni, \
    "comuni piu' popolosi d'italia per la keyword '"+stringa_ricerca+"'"

for c in comuni_italiani_ordinati[:numero_comuni]:
    print "Querying:",c[1]['nome']
    lista_comuni.append(c[1]['nome'])
    sleep(1)
    r = s.run_query(c[0].zfill(9), stringa_ricerca, 
            c[1]['nome'].replace(" ", "+"))
    if r:
        results[c[1]['nome']] = r

print ""

result_summary = defaultdict(int)

for k, d in results.items():
    for item in d['data']:
        if 'importo_2013' in item and item['importo_2013']:
            result_summary[item['descrizione_codice']] += \
                float(item['importo_2013'][:-2])

print "------------ Risultati ------------"
print "Per i comuni di:", ','.join(map(str,lista_comuni))
print "Ci sono le seguenti spese (anno 2013):"
for k,v in result_summary.items():
    print " - ", k, ":", "{:,}".format(v), "Euro" 
