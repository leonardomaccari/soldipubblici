#!/usr/bin/env python

import requests, json
import soldipubblici

s = soldipubblici.soldi_pubblici()

r = s.run_query("800000013", "software")
print r

