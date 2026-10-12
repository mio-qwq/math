#!/usr/bin/env python3
"""Separately written finite checker; same author, not independent review.

Input carry classes are rebuilt from all 2^11 high quotients. Output
transitions are rebuilt from tiny Boolean truth tables and propagated
breadth-first using low-pivot F2 elimination. The discovery traversal,
rotation implementation and transition formula are not imported.
"""
import argparse
import copy
from collections import Counter
import json
from pathlib import Path

N=1<<32
ALL=(1<<64)-1


def need(ok,msg):
    if not ok:
        raise ValueError(msg)


def output_rows(kind):
    a,b,s=((7,18,3),(17,19,10))[kind]
    rows=[]
    for j in range(32):
        row=(1<<((j+a)%32))^(1<<((j+b)%32))
        if j+s<32:
            row ^= 1<<(j+s)
        rows.append(row)
    return rows


ROWS=[output_rows(k) for k in (0,1)]


def image(mask,kind):
    return sum(((mask&row).bit_count()%2)<<j for j,row in enumerate(ROWS[kind]))


def extend(basis,equations):
    basis=dict(basis)
    for coeff,rhs in equations:
        word=coeff|(rhs<<64)
        while word&ALL:
            pivot=((word&ALL)&-(word&ALL)).bit_length()-1
            if pivot in basis:
                word ^= basis[pivot]
            else:
                basis[pivot]=word
                break
        if word==1<<64:
            return None
    return basis


def input_classes():
    grouped={}
    for q in range(1<<11):
        alpha=(q^((q+1)%(1<<11)))<<21
        grouped.setdefault(alpha,[]).append(q)
    classes=[]
    for alpha,values in sorted(grouped.items()):
        constraints=[]
        for j in range(11):
            bits={q>>j&1 for q in values}
            if len(bits)==1:
                constraints.append((1<<(j+21),next(iter(bits))))
        need(len(values)==1<<(11-len(constraints)),'input class is full affine cube')
        for q in values:
            need(all(((q<<21)&row).bit_count()%2==rhs for row,rhs in constraints),
                 'input class constraints')
        classes.append((alpha,constraints))
    need(len(classes)==11 and sum(len(v) for v in grouped.values())==2048,
         'complete input carry classes')
    return classes


def affine_constraints(allowed,m):
    # Determine every constant F2 functional on the small permitted set.
    # Verify by truth table that the resulting equations describe exactly
    # the permitted set, so compression cannot add or remove assignments.
    eqs=[]
    for row in range(1,1<<m):
        values={(row&v).bit_count()%2 for v in allowed}
        if len(values)==1:
            eqs.append((row,next(iter(values))))
    rebuilt={v for v in range(1<<m)
             if all((row&v).bit_count()%2==rhs for row,rhs in eqs)}
    need(rebuilt==set(allowed),'exact affine transition compression')
    return eqs


def transitions(alpha_x,alpha_y,constant,j,carry,kind):
    bx=alpha_x>>j&1
    by=alpha_y>>j&1
    rows=[]
    if bx:
        rows.append(ROWS[kind][j])
    if by:
        rows.append(ROWS[kind][j]<<32)
    m=len(rows)
    groups={}
    for values in range(1<<m):
        where=0
        u=(values>>where)&1 if bx else 0
        where+=bx
        v=(values>>where)&1 if by else 0
        up=u^bx;vp=v^by
        total=carry+(vp-v)-(up-u)-(constant>>j&1)
        if total%2==0:
            groups.setdefault(total//2,[]).append(values)
    result=[]
    for nxt,allowed in groups.items():
        eqs=[]
        for little,rhs in affine_constraints(allowed,m):
            coeff=0
            for k,row in enumerate(rows):
                if little>>k&1:
                    coeff^=row
            eqs.append((coeff,rhs))
        result.append((nxt,eqs))
    return result


def verify_case(cx,cy):
    ax,ex=cx;ay,ey=cy
    basis=extend({},ex+[(row<<32,rhs) for row,rhs in ey])
    frontier=[basis]
    counts=Counter()
    for kind,constant in ((0,0),(1,1<<22)):
        beta_x=image(ax,kind);beta_y=image(ay,kind)
        current=[(0,b) for b in frontier]
        for j in range(32):
            following=[]
            for carry,b in current:
                for nxt,eqs in transitions(beta_x,beta_y,constant,j,carry,kind):
                    counts['truth_table_transitions']+=1
                    following_basis=extend(b,eqs)
                    if following_basis is not None:
                        following.append((nxt,following_basis))
                    else:
                        counts['linear_conflicts']+=1
            current=following
        frontier=[b for _,b in current]
    return len(frontier),dict(counts)


def verify_recurrences(supports):
    expected=[
        (19,[('d',19,1),('d',12,-1)]),
        (28,[('d',21,-1),('d',12,-1)]),
        (35,[('d',35,1),('d',19,-1)]),
        (21,[('d',21,1),('g',19,-1),('d',14,-1)]),
        (30,[('d',30,1),('d',14,-1)]),
        (37,[('g',35,-1),('d',30,-1),('d',21,-1)]),
        (46,[('g',44,-1),('d',30,-1)]),
        (51,[('d',44,-1),('d',35,-1)]),
        (34,[('d',27,-1),('f',19,-1)]),
        (43,[('d',43,1),('d',27,-1)]),
        (50,[('d',43,-1),('f',35,-1)]),
    ]
    checked=0
    for idx,shift in ((6,0),(7,2),(12,-1),(13,1)):
        active=set(supports[idx])
        need({19+shift,35+shift,44+shift}<=active,'nonzero core coordinates')
        for time,terms in expected:
            t=time+shift
            need(16<=t<64,'valid recurrence boundary')
            actual=[(kind,i,sign) for kind,i,sign in
                    [('d',t,1),('g',t-2,-1),('d',t-7,-1),('f',t-15,-1),('d',t-16,-1)]
                    if i in active]
            shifted=[(kind,i+shift,sign) for kind,i,sign in terms]
            need(sorted(actual)==sorted(shifted),'recurrence substitution')
            checked+=1
    return checked


def check(cert,supports):
    need(cert['bits']==32 and cert['k']==21 and cert['half'] is False,'fixed object')
    need(cert['delta']==1<<21 and cert['case_count']==121 and cert['sat_cases']==0,
         'certificate conclusion')
    classes=input_classes()
    indexed={(c['alpha_x'],c['alpha_y']):c for c in cert['cases']}
    expected={(ax,ay) for ax,_ in classes for ay,_ in classes}
    need(len(cert['cases'])==len(indexed)==121 and set(indexed)==expected,
         'complete supplied case list')
    need(all(c['witness'] is None for c in cert['cases']),'no supplied SAT case')
    for j in range(22,32):
        need(ROWS[1][j]>>21==0,'sigma1 high-output locality')
    totals=Counter()
    for cx in classes:
        for cy in classes:
            count,stats=verify_case(cx,cy)
            need(count==0,'fixed-difference twin exclusion')
            totals.update(stats)
    substitutions=verify_recurrences(supports)
    return {'all_case_pairs':121,'surviving_branches':0,
            'independently_rebuilt_input_quotients':2048,
            'recurrence_substitutions':substitutions,**dict(totals),
            'claim':'v2(D)<=20 in four stated support cores, pending external review',
            'scope':'written reduction plus finite computation; no full support exclusion'}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('supports',type=Path)
    p.add_argument('--certificate',type=Path,default=Path(__file__).with_name('TWIN-V21-CARRY.json'))
    p.add_argument('--negative',action='store_true')
    a=p.parse_args()
    cert=json.loads(a.certificate.read_text())
    supports=json.loads(a.supports.read_text())['supports']
    result=check(cert,supports)
    if a.negative:
        bad=[]
        c=copy.deepcopy(cert);c['cases'].pop();bad.append((c,supports))
        c=copy.deepcopy(cert);c['delta']^=1;bad.append((c,supports))
        c=copy.deepcopy(cert);c['cases'][0]['alpha_x']^=1;bad.append((c,supports))
        c=copy.deepcopy(cert);c['cases'][0]['witness']={};bad.append((c,supports))
        rejected=[]
        for c,s in bad:
            try:
                check(c,s)
            except ValueError as e:
                rejected.append(str(e))
            else:
                raise ValueError('corrupted certificate accepted')
        result['rejected_controls']=rejected
    print(json.dumps(result,sort_keys=True))
