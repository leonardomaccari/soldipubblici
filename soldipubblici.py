#!/usr/bin/env python

import requests
import sys
import simplejson


class soldi_pubblici():
    URL1 = "http://soldipubblici.gov.it/"
    URL2 = "http://soldipubblici.gov.it/it/ricerca"
    payload = {'codicecomparto': 'PRO', 'codiceente': '', 
        'chi':'', 'cosa':''}

    header = {}
    header['Host']='soldipubblici.gov.it'
    header['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'
    header['X-Requested-With']='XMLHttpRequest'
    header['Referer']='http://soldipubblici.gov.it/it/home'
    header['Accept'] = 'application/json'
    header['Accept-Language'] = 'en-US,en;q=0.5'
    header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    header['Origin'] = 'http://soldipubblici.gov.it/it/home'
    #header['Accept-Encoding'] = 'gzip, deflate'
    #header['Accept'] = 'application/json, text/javascript, */*; q=0.01'

    session = None

    def __init__(self):
        self.session = requests.Session()
        try:
            r = self.session.get(self.URL1)
        except requests.exceptions.ConnectionError:
            print "Website", self.URL1, "does not respond"
            sys.exit(1)

    def run_query(self, codiceente, cosa, chi):
        p = self.payload.copy()
        p['codiceente'] = codiceente
        p['cosa'] = cosa
        p['chi'] = chi
        try:
            r = self.session.post(self.URL2, data=p, headers=self.header)
        except requests.exceptions.ConnectionError:
            print "Website", self.URL2, "does not respond"
        try:
            j = r.json()
        except simplejson.scanner.JSONDecodeError:
            print "There was an error in the answer, or an empty answer:"
            print r.text
            return {}
        return j

    def close_connection(self):
        r = requests.post(self.URL1, headers={'Connection':'close'})

