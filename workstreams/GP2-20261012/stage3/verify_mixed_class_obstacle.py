#!/usr/bin/env python3
"""Exact reconstruction of the omitted mixed-class witness and local colors."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def require(ok, message):
    if not ok:raise ValueError(message)


def verify(data):
    levels=data['levels'];n=data['alphabet_size']
    require(type(n) is int and n==4, 'alphabet binding')
    require(levels==[[2,0,2,2],[2,2,1,2],[2,2,2,0],[1,2,2,2]], 'level binding')
    require(data['uniform_weights']==['1/4']*4, 'weight binding')
    e=g=0;missing=[]
    for a,b,c,d in product(range(n),repeat=4):
        event=levels[a][b]==levels[c][d] and levels[b][c]==levels[d][a]
        cs=[tuple(sorted((levels[x][y],levels[y][x]))) for x,y in [(a,b),(a,d),(c,b),(c,d)]]
        hit=event and len(set(cs))==1
        e+=event;g+=hit
        if event and not hit:missing.append([a,b,c,d])
    require(data['E']==str(F(e,n**4)) and data['G']==str(F(g,n**4)), 'event totals')
    require(data['missing']==str(F(e-g,n**4)), 'omitted total')
    require(data['all_missing_tuples']==missing and data['witness'] in missing, 'explicit omitted witnesses')
    # Four independent unordered cross pairs have eight directed colors.
    ee=gg=0
    for z in product(range(3),repeat=8):
        event=z[0]==z[6] and z[5]==z[3]
        cs=[tuple(sorted(z[i:i+2])) for i in (0,2,4,6)]
        ee+=event;gg+=event and len(set(cs))==1
    require(ee==729 and gg==15, 'eight-color exact counts')
    require(data['limiting_random_E']==str(F(ee,6561)), 'random E binding')
    require(data['limiting_random_G']==str(F(gg,6561)), 'random G binding')
    require(data['limiting_random_captured_ratio']==str(F(gg,ee)), 'captured ratio')
    return {'E':str(F(e,256)),'G':str(F(g,256)),'omitted_tuples':len(missing),
            'independent_color_assignments':6561,'color_E_hits':ee,'color_G_hits':gg}


def main():
    data=json.loads((Path(__file__).resolve().parent/'mixed_class_witness.json').read_text())
    result=verify(data);negative=[]
    for field,badvalue in [('G','3/8'),('missing','0'),('limiting_random_G','1/9')]:
        damaged=dict(data);damaged[field]=badvalue
        try:verify(damaged)
        except ValueError as error:negative.append({'field':field,'rejected':str(error)})
        else:raise RuntimeError('Altered witness accepted')
    print(json.dumps({'status':'PASS','result':result,'negative_controls':negative,
                     'scope':'Mechanism omission, not strict-code optimality'},indent=2))


if __name__=='__main__':main()
