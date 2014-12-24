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

    def clean_data(self, xlabel, y):
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
        #fig.subplots_adjust(bottom=0.2)
        plt.bar(x, y, width=w)
        ax.set_title(title)
        ax.set_ylabel("Milioni di Euro")
        plt.tight_layout()
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

    def run_multiple_queries(self):
        comuni_dict = {}
        results = {}

        print "Querying i", self.numero_comuni, \
            "comuni piu' popolosi d'italia per la keyword '"+self.stringa_ricerca+"'"

        #a = filter( lambda x: x[1]['popolazione'] > 50000, comuni_italiani_ordinati)
        for c in self.comuni[:self.numero_comuni]:
            print "Querying:",c[1]['nome']
            comuni_dict[c[1]['nome']] = c[1]
            sleep(1)
            r = self.session.run_query(c[0].zfill(9), self.stringa_ricerca, 
                    c[1]['nome'].replace(" ", "+"))
            if r:
                results[c[1]['nome']] = r
        return results, comuni_dict


    def cumulative_query(self):
        results, comuni_dict = self.run_multiple_queries()
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
        print "Per i comuni di:", ','.join(map(str, comuni_dict.keys()))
        print "Ci sono le seguenti spese (anno 2013):"
        for k,v in result_summary.items():
            print " - ", k, ":", "{:,}".format(v), "M Euro" 
            graphX.append(textwrap.fill(k,15))
            graphY.append(v)
        self.clean_data(graphX, graphY)
        self.plot_data(graphX, graphY, 
            self.stringa_ricerca + ": top " + str(self.numero_comuni) + \
            " comuni")

    def classifica_comuni(self, procapite=True):
        results = self.query_and_purge()
        graph_y = defaultdict(float)
        graph_title = ""
        #graph_title = set(["Classifica spese per:\n"])
        
        for city, query_data in results.items():
            for item in query_data['data']:
                try:
                    graph_y[city] += float(item['importo_2013'])/1000000
                except TypeError:
                    # some fields are None
                    pass
                graph_title += " " + item['codice_siope']
        if procapite:
            for (city, value) in graph_y.items():
                for city_id, data in self.comuni:
                    if city == data["nome"]:
                        people = float(data["popolazione"])
                graph_y[city] = value/people
            
            t = "Primi 10 comuni sui " + str(self.numero_comuni) +\
                    " piu' abitati per spesa procapite in \n" + \
                    " voci relative a " + self.stringa_ricerca 
                    #" (codici siope:\n"
            graph_title = t #+ textwrap.fill(graph_title, 80) + ")"
        else:
            t = "Primi 10 comuni sui " + str(self.numero_comuni) +\
                    " piu' abitati per spesa totale in \n" + \
                    " voci relative a " + self.stringa_ricerca 
                    #" (codici siope:\n"
            graph_title = t #+ textwrap.fill(graph_title, 80) + ")"

        sorted_values = sorted(graph_y.items(), key = lambda x: x[1], reverse=True)
        graph_x = [textwrap.fill(k, 10) for k in zip(*sorted_values)[0]]
        graph_y = zip(*sorted_values)[1]
        self.plot_data(graph_x[:9], graph_y[0:9], graph_title)

        
    def query_and_purge(self):
        results, comuni_dict = self.run_multiple_queries()
        returned_keys = set()
        for k, d in results.items():
            for item in d['data']:
                returned_keys.add(item['descrizione_codice'])
        key_list = list(returned_keys)
        self.clean_data(key_list, range(len(returned_keys)))
        for city, query_data in results.items():
            for i in reversed(range(len(query_data['data']))):
                if query_data['data'][i]['descrizione_codice'] not in key_list:
                    del results[city]['data'][i]
            if not query_data['data']:
                    del results[city]
        return results
        #print "Per i comuni di:", ','.join(map(str, comuni_dict.keys()))
        #print "Ci sono le seguenti spese (anno 2013):"
        #for k,v in result_summary.items():
        #    print " - ", k, ":", "{:,}".format(v), "M Euro" 
        #    graphX.append(textwrap.fill(k,15))
        #    graphY.append(v)
        #self.plot_data(graphX, graphY, 
        #    self.stringa_ricerca + ": top " + str(self.numero_comuni) + \
        #    " comuni")


if __name__ == '__main__':
    c = crawler()
    c.parse_args()
    c.classifica_comuni()
    #c.cumulative_query()
