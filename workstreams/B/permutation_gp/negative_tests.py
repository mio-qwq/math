#!/usr/bin/env python3
"""Deliberately reject malformed and mathematically invalid witnesses."""
import copy
import json
from pathlib import Path
from verify import verify, Rejected
base=json.loads(Path(__file__).with_name('certificate.json').read_text())
tests=[]
c=copy.deepcopy(base); c['selected_words']=c['selected_words'][:84]; tests.append(('not_strictly_larger',c))
c=copy.deepcopy(base); c['selected_words'].append(c['selected_words'][0]); tests.append(('duplicate_word',c))
c=copy.deepcopy(base); c['selected_words'][0]=[0,0,6]; tests.append(('noninjective_word',c))
c=copy.deepcopy(base); c['conjectured_value']=83; tests.append(('wrong_bound',c))
c=copy.deepcopy(base); c['selected_words'].extend([[1,6,2],[6,2,3]]); tests.append(('actual_geodesic_triple',c))
results=[]
for name,c in tests:
    try: verify(c)
    except Rejected as e: results.append({'name':name,'rejected':True,'reason':str(e)})
    else: raise AssertionError('negative control accepted: '+name)
print(json.dumps({'negative_controls':results,'all_rejected':True},indent=2))
