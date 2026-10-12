#!/usr/bin/env python3
"""Original-equation check of support 5, including the reversed pair."""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PIN='02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf'
EXPECTED={
    24:[('d',17,-1),('d',8,-1)],
    19:[('d',19,1),('g',17,-1)],
    26:[('d',26,1),('d',19,-1)],
    33:[('d',26,-1),('d',17,-1)],
    23:[('d',16,-1),('f',8,-1)],
    32:[('f',17,-1),('d',16,-1)],
}


def check(raw,orientation=(-1,-1),expected=EXPECTED):
    assert hashlib.sha256(raw).hexdigest()==PIN,'source pin'
    S=set(json.loads(raw)['supports'][5])
    assert S=={2,8,14,16,17,19,26,28,29,34,42,43,57},'exact support'
    assert set(expected)=={24,19,26,33,23,32},'equation coverage'
    for t,want in expected.items():
        terms=[('d',t,1),('g',t-2,-1),('d',t-7,-1),('f',t-15,-1),('d',t-16,-1)]
        assert [e for e in terms if e[1] in S]==want,'recurrence reduction'
    assert orientation==(-1,-1),'both derivatives reverse'
    # Reversing a pair negates its two differences in every additive group.
    for D,F in [(1,2),(0x887b6c5b,0x410c6383),(0x80000000,0xffffffff)]:
        d8=(-D)&0xffffffff; F8=F
        dp=(orientation[0]*d8)&0xffffffff
        Fp=(orientation[1]*F8)&0xffffffff
        assert dp==D and (Fp+F)&0xffffffff==0,'orientation check'
    return 6


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--negative',action='store_true')
    args=parser.parse_args()
    raw=(HERE.parent/'supports-v2.json').read_bytes()
    count=check(raw)
    bad_equations=dict(EXPECTED); bad_equations.pop(24)
    controls=[]
    if args.negative:
        for name,r,o,e in [('bad support bytes',raw+b' ',(-1,-1),EXPECTED),
                           ('only input reversed',raw,(-1,1),EXPECTED),
                           ('only sigma reversed',raw,(1,-1),EXPECTED),
                           ('missing early equation',raw,(-1,-1),bad_equations)]:
            try:
                check(r,o,e)
            except AssertionError as err:
                controls.append({'case':name,'rejected':True,'reason':str(err)})
            else:
                raise AssertionError('accepted damage')
    print(json.dumps({'status':'PASS','recurrences':count,'support':5,'negative_controls':controls},sort_keys=True))


if __name__=='__main__':
    main()
