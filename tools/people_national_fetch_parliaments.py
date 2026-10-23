#!/usr/bin/env python3
"""Download Wikipedia HTML+wikitext for the 50th-54th NZ Parliament articles (raw/people/national/parliaments/)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people_national_wiki import api
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'people', 'national', 'parliaments')
for n in range(50, 55):
    if os.path.exists(os.path.join(OUT, f'{n}.html')): continue
    d = api({'action': 'parse', 'page': {50:'50th',51:'51st',52:'52nd',53:'53rd',54:'54th'}[n] + ' New Zealand Parliament', 'prop': 'text|wikitext', 'redirects': 1})
    open(os.path.join(OUT, f'{n}.html'), 'w').write(d['parse']['text']['*'])
    open(os.path.join(OUT, f'{n}.wikitext'), 'w').write(d['parse']['wikitext']['*'])
    print(n)
