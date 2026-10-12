#!/usr/bin/env python3
"""Check all thirty original recurrence substitutions, with damage controls."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE_HASH='02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf'
LOCATIONS=[(0,30),(1,31),(2,32),(4,33),(8,29),(9,29)]


def check(certificate,raw):
    assert hashlib.sha256(raw).hexdigest()==SOURCE_HASH,'support source hash'
    supports=json.loads(raw)['supports']
    assert certificate['schema']=='crypto3-coupled-bridges-v1'
    assert [(r['support'],r['u']) for r in certificate['rows']]==LOCATIONS,'coverage'
    checked=0
    for row in certificate['rows']:
        u=row['u']; p=u+7; q=u+14; r=u+22
        assert (row['p'],row['q'],row['r'])==(p,q,r),'coordinates'
        S=set(supports[row['support']])
        assert {u,p,q,r}<=S,'nonzero premises'
        expected=[
            [('d',p,1),('d',u,-1)],
            [('d',q,1),('d',p,-1)],
            [('g',q,-1),('d',u,-1)],
            [('d',r,1),('f',p,-1)],
            [('d',r,-1),('f',q,-1)],
        ]
        assert [e['t'] for e in row['recurrences']]==[p,q,u+16,r,u+29],'equation locations'
        for equation,want in zip(row['recurrences'],expected):
            t=equation['t']
            assert 16<=t<64,'recurrence range'
            full=[('d',t,1),('g',t-2,-1),('d',t-7,-1),('f',t-15,-1),('d',t-16,-1)]
            actual=[x for x in full if x[1] in S]
            assert actual==want,'original recurrence reduction'
            assert [tuple(x) for x in equation['terms']]==want,'certificate equation'
            checked+=1
    return checked


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--negative',action='store_true')
    args=parser.parse_args()
    data=json.loads((HERE/'bridges.json').read_text())
    raw=(HERE.parent/'supports-v2.json').read_bytes()
    count=check(data,raw)
    controls=[]
    if args.negative:
        changed=copy.deepcopy(data); changed['rows'].pop()
        cases=[('omit support',changed,raw)]
        changed=copy.deepcopy(data); changed['rows'][0]['q']+=1
        cases.append(('wrong shared pair',changed,raw))
        changed=copy.deepcopy(data); changed['rows'][0]['recurrences'][-1]['terms'][0][2]=1
        cases.append(('wrong sigma0 cancellation sign',changed,raw))
        changed=copy.deepcopy(data); changed['rows'][0]['recurrences'][0]['t']=15
        cases.append(('invalid recurrence boundary',changed,raw))
        cases.append(('alter frozen support bytes',data,raw+b' '))
        for name,bad,badraw in cases:
            try:
                check(bad,badraw)
            except (AssertionError,ValueError,KeyError) as e:
                controls.append({'case':name,'rejected':True,'reason':str(e)})
            else:
                raise AssertionError('accepted damage: '+name)
    print(json.dumps({'status':'PASS','recurrences':count,'supports':len(LOCATIONS),
                      'negative_controls':controls},sort_keys=True))


if __name__=='__main__':
    main()
