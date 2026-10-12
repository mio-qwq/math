#!/usr/bin/env python3
"""Replay without replacing the frozen independent execution records."""
import argparse
import json
import check_independent
import controls_and_compare

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--part',choices=['all','core','controls'],default='all')
    a=p.parse_args();reports={}
    if a.part in ('all','core'):
        reports['core']=check_independent.run(list(range(1,16,2)))
        assert reports['core']['all_unsat']
    if a.part in ('all','controls'):
        reports['controls']=controls_and_compare.run()
        assert reports['controls']['status']=='PASS'
    print(json.dumps({'status':'PASS','readonly':True,'reports':reports}))
