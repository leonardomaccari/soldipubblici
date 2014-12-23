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
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import textwrap

class crawler():

    def __init__(self):
        self.comuni = self.load_data()
        self.session = soldipubblici.soldi_pubblici()
        self.numero_comuni, self.stringa_ricerca = self.parse_args()

    def clean_data(self, xlabel,y):
        del_index = []
        for i in range(len(xlabel)):
           unicode_string = xlabel[i].replace(u"\n",' ').encode('utf-8', 'ignore')
           print "Vuoi plottare la colonna:\n    " \
                + unicode_string,
           inputString = " [y/n]? :"
           user_input = raw_input(inputString)
           if user_input == 'n':
                del_index.append(i)
        for i in sorted(del_index, reverse=True):
            del xlabel[i]
            del y[i]

    def plot_data(self, xlabel, y, title):
        w = 0.8
        x = range(len(y))
        fig, ax = plt.subplots()
        ax.set_xticks([p+w/2 for p in x])
        ax.set_xticklabels(xlabel)
        fig.subplots_adjust(bottom=0.2)
        plt.bar(x, y, width=w)
        ax.set_title(title)
        ax.set_ylabel("Milioni di Euro")
        plt.show()
        fig.savefig("/tmp/graph.png")

    def load_data(self):
        f = open("data/codici_comuni_ordinati.json",'r')
        comuni_italiani_ordinati = json.load(f)
        return comuni_italiani_ordinati


    def parse_args(self):
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

        numero_comuni = int(sys.argv[1])
        stringa_ricerca = sys.argv[2]
        return numero_comuni, stringa_ricerca

    def cumulative_query(self):
        lista_comuni = []
        results = {}

        print "Querying i", self.numero_comuni, \
            "comuni piu' popolosi d'italia per la keyword '"+self.stringa_ricerca+"'"

        #a = filter( lambda x: x[1]['popolazione'] > 50000, comuni_italiani_ordinati)
        for c in self.comuni[:self.numero_comuni]:
            print "Querying:",c[1]['nome']
            lista_comuni.append(c[1]['nome'])
            sleep(1)
            r = self.session.run_query(c[0].zfill(9), self.stringa_ricerca, 
                    c[1]['nome'].replace(" ", "+"))
            if r:
                results[c[1]['nome']] = r
        print ""
        result_summary = defaultdict(int)
        graphX = []
        graphY = []
        for k, d in results.items():
            for item in d['data']:
                if 'importo_2013' in item and item['importo_2013']:
                    result_summary[item['descrizione_codice']] += \
                        float(item['importo_2013'][:-2])/1000000
        print "------------ Risultati ------------"
        print "Per i comuni di:", ','.join(map(str,lista_comuni))
        print "Ci sono le seguenti spese (anno 2013):"
        for k,v in result_summary.items():
            print " - ", k, ":", "{:,}".format(v), "M Euro" 
            graphX.append(textwrap.fill(k,15))
            graphY.append(v)
        self.clean_data(graphX, graphY)
        self.plot_data(graphX, graphY, 
            self.stringa_ricerca + ": top " + str(self.numero_comuni) + \
            " comuni")


if __name__ == '__main__':
    c = crawler()
    c.parse_args()
    c.cumulative_query()
