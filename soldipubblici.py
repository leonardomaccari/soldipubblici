#!/usr/bin/env python

import requests
import json


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
    header['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header['Accept-Language'] = 'en-US,en;q=0.5'
    header['Accept-Encoding'] = 'gzip, deflate'
    header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    session = None

    def __init__(self):
        self.session = requests.Session()
        r = self.session.get(self.URL1)

    def run_query(self, codiceente, cosa):
        p = self.payload.copy()
        p['codiceente'] = codiceente
        p['cosa'] = cosa
        r = self.session.post(self.URL2, data=p, headers=self.header)
        return r.json()
