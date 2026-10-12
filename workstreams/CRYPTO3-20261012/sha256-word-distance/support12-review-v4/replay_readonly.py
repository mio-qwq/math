#!/usr/bin/env python3
"""Replay the independent checks without replacing frozen evidence bytes."""
import argparse
import json
import check_independent
import negative_control
import compare_author

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--part',choices=['all','core','controls','comparison'],default='all')
    a=p.parse_args()
    reports={}
    if a.part in ('all','core'):
        reports['core']=check_independent.run(list(range(1,8)))
        assert reports['core']['all_unsat']
    if a.part in ('all','controls'):
        reports['controls']=negative_control.run()
        assert reports['controls']['status']=='PASS'
    if a.part in ('all','comparison'):
        reports['comparison']=compare_author.run()
        assert reports['comparison']['status']=='PASS'
    print(json.dumps({'status':'PASS','readonly':True,'reports':reports}))
