#!/usr/bin/env python3
"""Controls for the independently frozen carry engine; no author imports."""
import collections
import datetime
import hashlib
import itertools
import json
import pathlib
import check_independent as own

HERE=pathlib.Path(__file__).resolve().parent

def twin_possible(k,a,b,base_words=None):
    fa,fb=a[3],b[3]
    ga,gb=a[4],b[4]
    D=k<<19
    if ga+gb<2*D:return False
    dummy=(0,0,0,0,0)
    basis=own.fixed_input_basis((a,b,dummy))
    if base_words is not None:
        for word,value in enumerate(base_words):
            for bit in range(32):
                if not own.insert(basis,1<<(word*32+bit),value>>bit&1):return False
    eqs=[own.equation_templates(fa,fb,((fa-fb)//2)&((1<<31)-1),-1,
                               own.FR,[r<<32 for r in own.FR]),
         own.equation_templates(gb,ga,((gb-ga-2*D)//2)&((1<<31)-1),-1,
                               [r<<32 for r in own.GR],own.GR)]
    stack=[(0,(0,0),basis)]
    while stack:
        step,cs,bs=stack.pop()
        if step==62:return True
        bit,which=divmod(step,2)
        for nxt,rows in eqs[which][bit][cs[which]]:
            nb=bs.copy()
            if not all(own.insert(nb,r,v) for r,v in rows):continue
            nc=list(cs);nc[which]=nxt
            stack.append((step+1,tuple(nc),nb))
    return False

def run():
    controls={}
    # Check every compressed carry group against a second direct truth table.
    checked=0
    for p,q,t,op,carry in itertools.product((0,1),(0,1),(0,1),(-1,1),(-1,0,1)):
        table=own.equation_templates(p,q,t,op,[1]*31,[2]*31)[0][carry]
        rebuilt={}
        for nxt,rows in table:
            allowed=[(u,v) for u,v in itertools.product((0,1),repeat=2)
                     if all(((u|(v<<1))&r).bit_count()%2==b for r,b in rows)]
            rebuilt[nxt]=allowed
        direct={}
        for u,v in itertools.product((0,1),repeat=2):
            value=carry+p*u+op*q*v-t
            if value%2==0:direct.setdefault(value//2,[]).append((u,v))
        assert rebuilt==direct
        checked+=1
    controls['all_local_carry_groups_exact']={'PASS':True,'groups_checked':checked}
    x=0xffd80000;xp=0;y=0xffd80040;yp=0x40
    D=5<<19
    F=lambda a,b:(own.sigma0(b)-own.sigma0(a))&own.M
    G=lambda a,b:(own.sigma1(b)-own.sigma1(a))&own.M
    assert (xp-x)&own.M==D and (yp-y)&own.M==D
    assert F(x,xp)==F(y,yp)
    assert (G(y,yp)-G(x,xp))&own.M==2*D
    control_case=next(c for c in own.masks(5) if c[0]==x^xp)
    assert control_case[1]>>31==0
    assert twin_possible(5,control_case,control_case,(x,y))
    assert not twin_possible(5,control_case,control_case,(x,y^1))
    controls['wrapped_positive_twin']={'PASS':True,'x':hex(x),'xp':hex(xp),
        'y':hex(y),'yp':hex(yp),'D':hex(D),'f':hex(F(x,xp)),
        'gx':hex(G(x,xp)),'gy':hex(G(y,yp)),
        'controls':'exact carry model accepts genuine wraparound pair, rejects y xor 1 mutation'}
    # This demonstrates why sigma0 must act as an XOR-linear map on masks,
    # never as an ordinary-addition-linear map on derivatives.
    assert F(x,xp)!=own.sigma0(D)
    controls['sigma0_addition_linearity_rejected']={'PASS':True,
        'actual_F':hex(F(x,xp)),'invalid_sigma0_D':hex(own.sigma0(D))}
    summary=[]
    for k in range(1,8):
        cases=own.masks(k)
        survivors=[]
        for a,b in itertools.product(cases,repeat=2):
            if twin_possible(k,a,b):survivors.append([hex(a[0]),hex(b[0])])
        assert survivors==([['0xffd80000','0xffd80000']] if k==5 else [])
        assert all(c[3]<(1<<29) and c[4]<(1<<22) for c in cases)
        summary.append({'k':k,'mask_pairs':len(cases)**2,'surviving_mask_pairs':survivors})
    controls['complete_twin_classification']=summary
    # Exact binary elimination detects a contradictory original row.
    bs={}
    assert own.insert(bs,1,0)
    assert not own.insert(bs,1,1)
    controls['linear_row_contradiction']={'PASS':True,'rows':['a0=0','a0=1']}
    return {'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'controls':controls,'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    data=run()
    (HERE/'NEGATIVE_CONTROL_RUN.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data))
