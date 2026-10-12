#!/usr/bin/env python3
"""Independent standard-library replay of one fixed-D joint-fibre obstruction."""
import argparse
from collections import Counter
from functools import cache
import hashlib
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent

N=1<<32; MASK=N-1; WIDTH=64; COEFF=(1<<WIDTH)-1

def need(ok,msg):
    if not ok: raise ValueError(msg)

def rows(kind):
    a,b,s=((7,18,3),(17,19,10))[kind]
    return [(1<<((j+a)%32))^(1<<((j+b)%32))^
            ((1<<(j+s)) if j+s<32 else 0) for j in range(32)]
ROWS=(rows(0),rows(1))

def sigma(x,kind):
    return sum(((r&x).bit_count()&1)<<j for j,r in enumerate(ROWS[kind]))

@cache
def input_classes(delta):
    k=(delta&-delta).bit_length()-1; bits=32-k; groups={}
    for q in range(1<<bits):
        x=q<<k; alpha=x^((x+delta)&MASK)
        groups.setdefault(alpha,[]).append(q)
    out=[]
    for alpha,qs in sorted(groups.items()):
        eq=[]
        for j in range(bits):
            vals={q>>j&1 for q in qs}
            if len(vals)==1: eq.append((1<<(j+k),next(iter(vals))))
        need(len(qs)==1<<(bits-len(eq)),'non-cube input class')
        need(all(all(((q<<k)&r).bit_count()&1==v for r,v in eq) for q in qs),
             'bad input cube')
        out.append((alpha,tuple(eq)))
    need(sum(map(len,groups.values()))==1<<bits,'input quotient coverage')
    return tuple(out)

def affine(allowed,size):
    eq=[]
    for r in range(1,1<<size):
        vals={(r&v).bit_count()&1 for v in allowed}
        if len(vals)==1:eq.append((r,next(iter(vals))))
    need([v for v in range(1<<size)
          if all((r&v).bit_count()&1==b for r,b in eq)]==allowed,
         'truth-table compression')
    return eq

def transitions(kind,al,ar,left,right,constant,bit,carry):
    a=(sigma(al,kind)>>bit)&1; b=(sigma(ar,kind)>>bit)&1
    funcs=[]
    if a:funcs.append(ROWS[kind][bit]<<left)
    if b:funcs.append(ROWS[kind][bit]<<right)
    groups={}
    for value in range(1<<len(funcs)):
        u=(value&1) if a else 0
        v=((value>>a)&1) if b else 0
        integer=carry+((v^b)-v)-((u^a)-u)-((constant>>bit)&1)
        if integer%2==0:groups.setdefault(integer//2,[]).append(value)
    out=[]
    for nxt,allowed in sorted(groups.items()):
        eq=[]
        for little,rhs in affine(allowed,len(funcs)):
            coeff=0
            for j,r in enumerate(funcs):
                if little>>j&1:coeff^=r
            eq.append((coeff,rhs))
        out.append((nxt,eq))
    return out

def insert(basis,equations):
    basis=dict(basis)
    for coeff,rhs in equations:
        atom=(coeff,rhs); word=coeff|(rhs<<WIDTH); receipt=frozenset((atom,))
        while word&COEFF:
            p=((word&COEFF)&-(word&COEFF)).bit_length()-1
            if p in basis:
                old,oldrec=basis[p];word^=old;receipt=receipt.symmetric_difference(oldrec)
            else:
                basis[p]=(word,receipt);break
        if word==1<<WIDTH:
            rec=tuple(sorted(receipt)); total=0
            for c,b in rec:total^=c|(b<<WIDTH)
            need(total==1<<WIDTH,'invalid XOR contradiction')
            return None,rec
    return basis,None

def carry(bases,kind,al,ar,left,right,constant,bits,stats,receipts):
    cur=[(0,b) for b in bases]
    for bit in range(bits):
        follow=[]
        for c,basis in cur:
            for nxt,eq in transitions(kind,al,ar,left,right,constant,bit,c):
                stats['truth_edges']+=1
                nb,rec=insert(basis,eq)
                if nb is None:
                    stats['contradictions']+=1;receipts.add(rec)
                else:follow.append((nxt,nb))
        cur=follow
    return [b for _,b in cur]

def recover(basis):
    word=0
    for p,(eq,_) in sorted(basis.items(),reverse=True):
        rhs=eq>>WIDTH; coeff=eq&COEFF
        if (word&coeff).bit_count()&1!=rhs:word|=1<<p
    return word

def enumerate_twins(fbits,gbits,gap,save_first=False):
    D=1<<16; stats=Counter();receipts=set();fcount=gcount=0;first=None
    classes=input_classes(D)
    for ax,ex in classes:
      for ay,ey in classes:
        basis,rec=insert({},ex+tuple((r<<32,v) for r,v in ey))
        need(basis is not None,'disjoint input cubes conflict')
        fs=carry([basis],0,ax,ay,0,32,0,fbits,stats,receipts);fcount+=len(fs)
        gs=carry(fs,1,ax,ay,0,32,gap,gbits,stats,receipts);gcount+=len(gs)
        if save_first and first is None and gs:first=(ax,ay,recover(gs[0]))
    # Every stored leaf is an exact affine solution; every pruned branch has
    # an explicit XOR of original affine rows equal to 0=1.
    for rec in receipts:
        total=0
        for c,b in rec:total^=c|(b<<WIDTH)
        need(total==1<<WIDTH,'damaged contradiction receipt')
    return {'f_leaves':fcount,'g_leaves':gcount,'stats':dict(stats),
            'distinct_xor_receipts':len(receipts)},first

def bit30_frontier():
    """Classify every branch after the exact low-30-bit gap check."""
    D=1<<16;groups=Counter()
    for ax,ex in input_classes(D):
      for ay,ey in input_classes(D):
        basis,_=insert({},ex+tuple((r<<32,v) for r,v in ey))
        fs=carry([basis],0,ax,ay,0,32,0,32,Counter(),set())
        cur=[(0,b) for b in fs]
        for bit in range(30):
            follow=[]
            for cy,basis in cur:
                for nxt,eq in transitions(1,ax,ay,0,32,2*D,bit,cy):
                    nb,_=insert(basis,eq)
                    if nb is not None:follow.append((nxt,nb))
            cur=follow
        for cy,_ in cur:
            groups[(ax,ay,(sigma(ax,1)>>30)&1,
                    (sigma(ay,1)>>30)&1,cy)]+=1
    return [{'xor_x':ax,'xor_y':ay,'gx30':gx,'gy30':gy,
             'incoming_carry':cy,'leaves':n}
            for (ax,ay,gx,gy,cy),n in sorted(groups.items())]

def direct_boundary(w):
    D=1<<16;x=w['x'];y=w['y'];xp=w['xp'];yp=w['yp']
    need((xp-x)&MASK==D and (yp-y)&MASK==D,'input differences')
    fx=(sigma(xp,0)-sigma(x,0))&MASK;fy=(sigma(yp,0)-sigma(y,0))&MASK
    gx=(sigma(xp,1)-sigma(x,1))&MASK;gy=(sigma(yp,1)-sigma(y,1))&MASK
    need(fx==fy==w['F'],'full sigma0 equality')
    gap=(gy-gx)&MASK
    need(gap==w['G_gap'],'recorded sigma1 gap')
    need(gap%(1<<30)==2*D and gap%(1<<31)!=2*D,
         'bit30 boundary control')

def check_frozen_certificate(frontier,witness,theorem,trunc):
    cert=json.loads((HERE/'CERTIFICATE.json').read_text())
    need(cert['schema']=='CRYPTO3-support12-fixed-D-joint-fibre-v8','certificate schema')
    c=cert['claim']
    need(c=={'D':'00010000','orientation_partner':'ffff0000','modulus_bits':31,
             'input_class_count':len(input_classes(1<<16)),'mask_pair_count':256,
             'full_sigma0_affine_leaves':theorem['f_leaves'],
             'low30_sigma1_gap_leaves':trunc['g_leaves'],
             'low31_sigma1_gap_leaves':theorem['g_leaves']},'certificate counts')
    regroup=[]
    for m in (0x07ff0000,0x0fff0000,0x1fff0000,0x3fff0000,0x7fff0000):
        rows=[r for r in frontier if r['xor_x']==r['xor_y']==m]
        regroup.append({'xor_mask':f'{m:08x}',
          'incoming_carries':{str(r['incoming_carry']):r['leaves'] for r in rows},
          'sigma1_mask_bit30':1})
    need(cert['bit30_frontier']==regroup,'certificate frontier')
    bw=cert['boundary_control']
    actual={'x':f"{witness['x']:08x}",'x_plus_D':f"{witness['xp']:08x}",
            'y':f"{witness['y']:08x}",'y_plus_D':f"{witness['yp']:08x}",
            'xor_mask_x':f"{witness['xor_x']:08x}",'xor_mask_y':f"{witness['xor_y']:08x}",
            'common_sigma0_derivative':f"{witness['F']:08x}",
            'sigma1_derivative_gap_mod_2_32':f"{witness['G_gap']:08x}",
            'sigma1_gap_mod_2_30':f"{witness['G_gap']%(1<<30):08x}",
            'sigma1_gap_mod_2_31':f"{witness['G_gap']%(1<<31):08x}"}
    need(bw==actual,'certificate boundary witness')
    need('not all valuation-16' in cert['scope'],'certificate scope')
    return hashlib.sha256((HERE/'CERTIFICATE.json').read_bytes()).hexdigest()

def run(negative):
    start=time.monotonic();D=1<<16
    theorem,_=enumerate_twins(32,31,2*D)
    need(theorem['f_leaves']==414 and theorem['g_leaves']==0,
         'fixed-D obstruction failed')
    trunc,first=enumerate_twins(32,30,2*D,True)
    shortf,_=enumerate_twins(31,31,2*D)
    zerogap,_=enumerate_twins(32,31,0)
    need((trunc['f_leaves'],trunc['g_leaves'])==(414,20),'30-bit control')
    need((shortf['f_leaves'],shortf['g_leaves'])==(408,20),'31-bit F control')
    need((zerogap['f_leaves'],zerogap['g_leaves'])==(414,58),'zero-gap control')
    frontier=bit30_frontier()
    masks=[0x07ff0000,0x0fff0000,0x1fff0000,0x3fff0000,0x7fff0000]
    wanted=[{'xor_x':m,'xor_y':m,'gx30':1,'gy30':1,
             'incoming_carry':c,'leaves':2} for m in masks for c in (-1,1)]
    need(frontier==wanted,'unexpected bit30 frontier')
    # At bit30 each toggled derivative bit is 1-2u, hence odd.  Their
    # difference is even; adding the recorded odd carry can never be even,
    # so the next carry transition does not exist.
    ax,ay,packed=first;x=packed&MASK;y=(packed>>32)&MASK
    witness={'x':x,'xp':(x+D)&MASK,'y':y,'yp':(y+D)&MASK,
             'xor_x':ax,'xor_y':ay,
             'F':(sigma((x+D)&MASK,0)-sigma(x,0))&MASK,
             'G_gap':((sigma((y+D)&MASK,1)-sigma(y,1))-
                       (sigma((x+D)&MASK,1)-sigma(x,1)))&MASK}
    direct_boundary(witness)
    certificate_sha256=check_frozen_certificate(frontier,witness,theorem,trunc)
    theorem['bit30_frontier']=frontier
    controls={'truncate_G_to_30_bits':trunc,'truncate_F_to_31_bits':shortf,
              'replace_gap_by_zero':zerogap,'boundary_witness':witness}
    if negative:
        rejected=0
        for key in ('xp','yp','F','G_gap'):
            bad=dict(witness);bad[key]^=1
            try:direct_boundary(bad)
            except ValueError:rejected+=1
        need(rejected==4,'negative controls not rejected')
        controls['damaged_witnesses_rejected']=rejected
    return {'status':'PASS','claim':{'D':D,'modulus':1<<31,
             'statement':'no two actual D-pairs have equal sigma0 derivative and sigma1-derivative gap 2D modulo 2^31'},
            'theorem':theorem,'controls':controls,
            'elapsed_seconds':time.monotonic()-start,
            'certificate_sha256':certificate_sha256,
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'one fixed numerical D; selected twin core only; not a message pair'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--negative',action='store_true')
    p.add_argument('--output',type=Path);a=p.parse_args();result=run(a.negative)
    if a.output:a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
