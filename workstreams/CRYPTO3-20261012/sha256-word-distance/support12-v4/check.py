#!/usr/bin/env python3
"""Definition-based finite proof replay, written separately by the author.

This is not an independent-agent review. Input classes are enumerated from
high quotients, output transitions from Boolean truth tables, and F2 rows
are eliminated from the low pivot with explicit XOR contradiction receipts.
It imports no discovery program and no SAT/SMT package.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
N=1<<32
MASK=N-1
WIDTH=96
COEFFICIENT=(1<<WIDTH)-1

def require(ok,message):
    if not ok: raise ValueError(message)

def rows(kind):
    a,b,s=((7,18,3),(17,19,10))[kind]
    return [(1<<((j+a)%32))^(1<<((j+b)%32))^
            ((1<<(j+s)) if j+s<32 else 0) for j in range(32)]

SIGMA_ROWS=[rows(0),rows(1)]

def image(mask,kind):
    return sum(((row&mask).bit_count()%2)<<j for j,row in enumerate(SIGMA_ROWS[kind]))

def input_classes(delta):
    k=(delta&-delta).bit_length()-1
    bits=32-k
    groups={}
    for q in range(1<<bits):
        x=q<<k
        alpha=x^((x+delta)&MASK)
        groups.setdefault(alpha,[]).append(q)
    result=[]
    for alpha,qs in sorted(groups.items()):
        eqs=[]
        for j in range(bits):
            vals={q>>j&1 for q in qs}
            if len(vals)==1:
                eqs.append((1<<(j+k),next(iter(vals))))
        # This verifies the *whole* cube, rather than assuming the constant
        # coordinates characterize a potentially non-affine class.
        require(len(qs)==1<<(bits-len(eqs)), 'input class cardinality')
        require(all(all(((q<<k)&r).bit_count()%2==v for r,v in eqs) for q in qs),
                'input cube assignments')
        result.append((alpha,eqs))
    require(sum(len(qs) for qs in groups.values())==1<<bits,'input quotient coverage')
    return result

def affine_equations(allowed,size):
    equations=[]
    for r in range(1,1<<size):
        rhs={(r&v).bit_count()%2 for v in allowed}
        if len(rhs)==1: equations.append((r,next(iter(rhs))))
    rebuilt=[v for v in range(1<<size)
             if all((r&v).bit_count()%2==b for r,b in equations)]
    require(rebuilt==allowed,'exact truth-table affine compression')
    return equations

def transitions(kind,alpha_left,alpha_right,left,right,constant,bit,carry):
    a=(image(alpha_left,kind)>>bit)&1
    b=(image(alpha_right,kind)>>bit)&1
    functions=[]
    if a: functions.append(SIGMA_ROWS[kind][bit]<<left)
    if b: functions.append(SIGMA_ROWS[kind][bit]<<right)
    groups={}
    for value in range(1<<len(functions)):
        u=(value&1) if a else 0
        v=((value>>a)&1) if b else 0
        # Two actual derivative bits: (u xor a)-u, (v xor b)-v.
        integer=carry+((v^b)-v)-((u^a)-u)-(constant>>bit&1)
        if integer%2==0:
            groups.setdefault(integer//2,[]).append(value)
    out=[]
    for nxt,allowed in sorted(groups.items()):
        eqs=[]
        for little,rhs in affine_equations(allowed,len(functions)):
            coeff=0
            for j,r in enumerate(functions):
                if little>>j&1: coeff^=r
            eqs.append((coeff,rhs))
        out.append((nxt,eqs))
    return out

def insert(basis,equations):
    basis=dict(basis)
    for coeff,rhs in equations:
        eq=(coeff,rhs)
        word=coeff|(rhs<<WIDTH)
        receipt=frozenset((eq,))
        while word&COEFFICIENT:
            p=((word&COEFFICIENT)&-(word&COEFFICIENT)).bit_length()-1
            if p in basis:
                old,old_receipt=basis[p]
                word^=old;receipt=receipt.symmetric_difference(old_receipt)
            else:
                basis[p]=(word,receipt)
                break
        if word==1<<WIDTH:
            selected=sorted(receipt)
            total=0
            for c,b in selected: total^=c|(b<<WIDTH)
            require(total==1<<WIDTH,'explicit XOR contradiction')
            return None,tuple(selected)
    return basis,None

class Rebuild:
    def __init__(self):
        self.bank=[]
        self.bank_ids={}
        self.stats=Counter()

    def bank_id(self,proof):
        if proof not in self.bank_ids:
            self.bank_ids[proof]=len(self.bank)
            self.bank.append(proof)
        return self.bank_ids[proof]

    def carry(self,bases,kind,alpha_left,alpha_right,left,right,constant):
        current=[(0,b) for b in bases]
        conflicts=[]
        for bit in range(32):
            following=[]
            for c,b in current:
                for nxt,eqs in transitions(kind,alpha_left,alpha_right,left,right,
                                           constant,bit,c):
                    self.stats['truth_table_edges']+=1
                    nb,receipt=insert(b,eqs)
                    if nb is None:
                        self.stats['F2_conflicts']+=1
                        conflicts.append(self.bank_id(receipt))
                    else: following.append((nxt,nb))
            current=following
        # Every final integer carry is discarded, exactly as required by
        # equality modulo 2^32. There is no no-wrap or final-zero condition.
        return [b for _,b in current],conflicts

def recurrence_core(supports):
    # Each target is supplied as an integer combination of original rows.
    # Therefore validation is valid over Z/(2^32) without division by 2.
    combinations={
        'd18-d11': {18:1},
        'd34-d18': {34:1},
        'd43+d34': {50:-1},
        'F34-F18': {33:1,42:-1,49:-1},
        'F43-F18': {33:1,42:-1,58:-1},
        'G34-G18-2d18': {20:1,27:2,18:-2,36:-1,29:-1},
        'G34-G43-d18': {36:-1,45:1,27:1,18:-1},
    }
    targets={
        'd18-d11': [('d',18,1),('d',11,-1)],
        'd34-d18': [('d',34,1),('d',18,-1)],
        'd43+d34': [('d',43,1),('d',34,1)],
        'F34-F18': [('f',34,1),('f',18,-1)],
        'F43-F18': [('f',43,1),('f',18,-1)],
        'G34-G18-2d18': [('g',34,1),('g',18,-1),('d',18,-2)],
        'G34-G43-d18': [('g',34,1),('g',43,-1),('d',18,-1)],
    }
    records=[]
    for index,shift in ((12,0),(6,1),(7,3),(13,2)):
        S=set(supports[index])
        require({18+shift,34+shift,43+shift}<=S,'active triple')
        eqs={}
        for t in range(16,64):
            eqs[t]={(k,i):c for k,i,c in [('d',t,1),('g',t-2,-1),
                    ('d',t-7,-1),('f',t-15,-1),('d',t-16,-1)] if i in S}
        for name,combo in combinations.items():
            sums=Counter()
            for t,c in combo.items():
                require(16<=t+shift<64,'original equation boundary')
                for v,a in eqs[t+shift].items(): sums[v]+=c*a
            got={v:c for v,c in sums.items() if c}
            wanted={(k,i+shift):c for k,i,c in targets[name]}
            require(got==wanted,'original recurrence row combination '+name)
            records.append({'support':index,'relation':name,'shift':shift,
                            'original_rows':{str(t+shift):c for t,c in combo.items()}})
    for j in range(22,32):
        require(SIGMA_ROWS[1][j]>>19==0,'sigma1 top-ten-bit locality')
    return records

def reconstruct():
    R=Rebuild();cases=[];classes_record={}
    for q in range(1,8):
        D=q<<19
        positive=input_classes(D)
        negative=input_classes((-D)&MASK) if q==5 else []
        classes_record[str(q)]=[{'alpha':f'{a:08x}',
                                'input_rows':[[f'{r:08x}',v] for r,v in eqs]}
                               for a,eqs in positive]
        subcases=[]
        for (ax,ex),(ay,ey) in itertools.product(positive,repeat=2):
            basis,receipt=insert({},ex+[(r<<32,v) for r,v in ey])
            require(receipt is None,'consistent input pair cube')
            f,fc=R.carry([basis],0,ax,ay,0,32,0)
            g,gc=R.carry(f,1,ax,ay,0,32,(2*D)&MASK)
            triple=[]
            if q!=5:
                require(not g,'excluded fixed-D twin core')
            else:
                for ordinal,b in enumerate(g):
                    for ar,er in negative:
                        rb,rc=insert(b,[(r<<64,v) for r,v in er])
                        if rb is None:
                            triple.append({'branch':ordinal,'alpha_r':f'{ar:08x}',
                                           'input_conflict':R.bank_id(rc)})
                            continue
                        rf,rfc=R.carry([rb],0,ay,ar,32,64,0)
                        rg,rgc=R.carry(rf,1,ar,ay,64,32,D)
                        require(not rg,'excluded fixed-D triple core')
                        triple.append({'branch':ordinal,'alpha_r':f'{ar:08x}',
                                       'f_leaves':len(rf),'g_leaves':len(rg),
                                       'f_conflicts':rfc,'g_conflicts':rgc})
            subcases.append({'alpha_x':f'{ax:08x}','alpha_y':f'{ay:08x}',
                             'f_leaves':len(f),'g_leaves':len(g),
                             'f_conflicts':fc,'g_conflicts':gc,'third_pair':triple})
        cases.append({'q':q,'delta':f'{D:08x}','mask_count':len(positive),
                      'mask_pairs':len(subcases),'cases':subcases})
    return {'schema':'CRYPTO3-support12-v4-finite-carry-certificate',
            'definition':{'bits':32,'lowest_divisibility_bit':19,
                          'f_rotations':[7,18],'f_shift':3,
                          'g_rotations':[17,19],'g_shift':10,
                          'final_carry':'discarded modulo 2^32'},
            'positive_input_classes':classes_record,'cases':cases,
            'conflict_row_bank':[[[f'{c:024x}',rhs] for c,rhs in proof] for proof in R.bank],
            'stats':dict(R.stats),
            'scope':'v2(D)<=18 for four specified support cores; not distance>=14'}

def direct_positive_control():
    x=0xffd80000;xp=0;y=0xffd80040;yp=0x40
    D=(xp-x)&MASK
    require(D==5<<19 and (yp-y)&MASK==D,'positive control differences')
    F=lambda a,b:(image(b,0)-image(a,0))&MASK
    G=lambda a,b:(image(b,1)-image(a,1))&MASK
    require(F(x,xp)==F(y,yp),'positive control common sigma0 derivative')
    require((G(y,yp)-G(x,xp))&MASK==(2*D)&MASK,'positive control sigma1 gap')
    return {'x':f'{x:08x}','xp':f'{xp:08x}','y':f'{y:08x}','yp':f'{yp:08x}',
            'D':f'{D:08x}','F':f'{F(x,xp):08x}',
            'G_x':f'{G(x,xp):08x}','G_y':f'{G(y,yp):08x}',
            'scope':'twin core only, no third pair or actual message blocks'}

def check(support_path,certificate_path):
    start=time.monotonic()
    stored=json.loads(certificate_path.read_text())
    supports=json.loads(support_path.read_text())['supports']
    original=recurrence_core(supports)
    rebuilt=reconstruct()
    require(stored==rebuilt,'certificate bytes do not match complete definition-based rebuild')
    for proof in stored['conflict_row_bank']:
        coeff=rhs=0
        for c,b in proof: coeff^=int(c,16);rhs^=b
        require(coeff==0 and rhs==1,'corrupt XOR row receipt')
    summary=[]
    for case in stored['cases']:
        summary.append({'q':case['q'],'mask_count':case['mask_count'],
                        'mask_pairs':case['mask_pairs'],
                        'twin_surviving_branches':sum(c['g_leaves'] for c in case['cases']),
                        'third_masks_checked':sum(len(c['third_pair']) for c in case['cases'])})
    return {'status':'PASS','certificate_sha256':hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
            'support_sha256':hashlib.sha256(support_path.read_bytes()).hexdigest(),
            'recurrence_combinations':len(original),'original_row_combinations':original,
            'summary':summary,'xor_conflict_proofs':len(stored['conflict_row_bank']),
            'stats':stored['stats'],'positive_control':direct_positive_control(),
            'seconds':time.monotonic()-start,
            'scope':'author finite proof replay, not independent-agent review or Lean formalization'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--supports',type=Path,default=HERE.parent/'supports-v2.json')
    p.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.json')
    p.add_argument('--output',type=Path)
    p.add_argument('--build',action='store_true')
    a=p.parse_args()
    if a.build:
        d=reconstruct();a.certificate.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
        result={'status':'BUILT','bytes':a.certificate.stat().st_size,
                'xor_conflict_proofs':len(d['conflict_row_bank']),'stats':d['stats']}
    else: result=check(a.supports,a.certificate)
    if a.output: a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
