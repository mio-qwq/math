#!/usr/bin/env python3
"""Independent boundary replay that never replaces frozen evidence files."""
import argparse
import json
import check_independent
import compare_fixture

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--part',choices=['all','core','comparison'],default='all')
    a=p.parse_args();reports={}
    if a.part in ('all','core'):
        reports['core']=check_independent.run()
        assert reports['core']['status']=='PASS'
    if a.part in ('all','comparison'):
        reports['comparison']=compare_fixture.run()
        assert reports['comparison']['status']=='PASS'
    print(json.dumps({'status':'PASS','readonly':True,'reports':reports}))
