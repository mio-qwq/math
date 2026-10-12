#!/usr/bin/env python3
"""Independent V6 replay without replacing frozen evidence files."""
import argparse
import json
import check_independent
import controls_and_compare

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--part',choices=['all','core','controls'],default='all')
    p.add_argument('--q',type=int,nargs='+',default=list(range(1,32,2)))
    p.add_argument('--h',type=int,nargs='+',default=[0,1])
    a=p.parse_args()
    assert all(q in range(1,32,2) for q in a.q) and all(h in (0,1) for h in a.h)
    reports={}
    if a.part in ('all','core'):
        reports['core']=check_independent.run(a.q,a.h)
        assert reports['core']['all_unsat']
    if a.part in ('all','controls'):
        reports['controls']=controls_and_compare.run()
        assert reports['controls']['status']=='PASS'
    print(json.dumps({'status':'PASS','readonly':True,'reports':reports}))
