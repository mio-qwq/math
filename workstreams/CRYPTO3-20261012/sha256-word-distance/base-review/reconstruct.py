#!/usr/bin/env python3
"""Independent SHA-256 interpolation chart reconstruction; stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path

MODULUS=1<<32
WORD_MASK=MODULUS-1
S=(2,9,10,16,23,24,30,37,38,44,51,52,58)
P=(0,1,3,4,5,7,8,11,12,15,29,43,57)
EXPECTED_T=(28,29,35,36,42,43,49,50,56,57)


def rows(kind):
    a,b,s=((7,18,3),(17,19,10))[kind]
    result=[]
    for j in range(32):
        r=(1<<((j+a)%32))^(1<<((j+b)%32))
        if j+s<32:
            r ^= 1<<(j+s)
        result.append(r)
    return result


def apply_rows(matrix,value):
    return sum(((r&value).bit_count()%2)<<j for j,r in enumerate(matrix))


def inverse_rows(matrix):
    augmented=[r|(1<<(32+i)) for i,r in enumerate(matrix)]
    for col in range(32):
        pivot=next((i for i in range(col,32) if augmented[i]>>col&1),None)
        if pivot is None:
            raise ValueError('sigma output matrix is singular')
        augmented[col],augmented[pivot]=augmented[pivot],augmented[col]
        for i in range(32):
            if i!=col and augmented[i]>>col&1:
                augmented[i] ^= augmented[col]
    if [r&WORD_MASK for r in augmented] != [1<<i for i in range(32)]:
        raise ValueError('inverse elimination did not reach identity')
    inverse=[r>>32 for r in augmented]
    for i in range(32):
        x=1<<i
        if apply_rows(matrix,apply_rows(inverse,x))!=x:
            raise ValueError('inverse basis composition')
        if apply_rows(inverse,apply_rows(matrix,x))!=x:
            raise ValueError('forward basis composition')
    return inverse


FORWARD=[rows(0),rows(1)]
INVERSE=[inverse_rows(m) for m in FORWARD]


def transform(kind,value):
    return value if kind=='identity' else apply_rows(FORWARD[int(kind[-1])],value)


def invert(kind,value):
    return value if kind=='identity' else apply_rows(INVERSE[int(kind[-1])],value)


def terms(t):
    return [(t,'identity',1),(t-2,'sigma1',-1),(t-7,'identity',-1),
            (t-15,'sigma0',-1),(t-16,'identity',-1)]


def chart():
    known=set(S)|set(P)
    if len(S)!=13 or len(P)!=13 or set(S)&set(P):
        raise ValueError('interpolation coordinate sets')
    unused=set(range(16,64));steps=[]
    while len(known)<64:
        choices=[]
        # T is the specified residual set; only its complement is solved.
        # An unrestricted elimination order can produce a different chart.
        for t in sorted(unused-set(EXPECTED_T)):
            unknown=[(i,k,c) for i,k,c in terms(t) if i not in known]
            if len(unknown)==1:
                choices.append((t,*unknown[0]))
        if not choices:
            raise ValueError('single-unknown closure stopped early')
        t,i,kind,c=choices[0]
        steps.append({'recurrence':t,'new_coordinate':i,'transform':kind,
                      'coefficient':c,'known_coordinates':sorted(j for j,_,_ in terms(t) if j!=i)})
        unused.remove(t);known.add(i)
    if len(steps)!=38 or sorted(unused)!=list(EXPECTED_T):
        raise ValueError('reconstructed equation complement differs')
    return steps,sorted(unused)


def fill(values,steps):
    expected=set(S)|set(P)
    if set(values)!=expected:
        raise ValueError('exact interpolation coordinate keys')
    if not all(type(v) is int and 0<=v<MODULUS for v in values.values()):
        raise ValueError('unsigned word range')
    w=dict(values)
    for step in steps:
        t=step['recurrence'];unknown=step['new_coordinate']
        missing=[i for i,_,_ in terms(t) if i not in w]
        if missing!=[unknown]:
            raise ValueError('one-new-coordinate invariant')
        row=next((k,c) for i,k,c in terms(t) if i==unknown)
        known_sum=sum(c*transform(k,w[i]) for i,k,c in terms(t) if i!=unknown)%MODULUS
        kind,coefficient=row
        w[unknown]=invert(kind,(-coefficient*known_sum)%MODULUS)
        if residual(w,t):
            raise ValueError('solved recurrence is not zero')
    if set(w)!=set(range(64)):
        raise ValueError('incomplete expansion coordinates')
    return [w[i] for i in range(64)]


def residual(w,t):
    return sum(c*transform(k,w[i]) for i,k,c in terms(t))%MODULUS


def expand(initial):
    if len(initial)!=16:
        raise ValueError('sixteen input words required')
    w=list(initial)
    for t in range(16,64):
        w.append((transform('sigma1',w[t-2])+w[t-7]+transform('sigma0',w[t-15])+w[t-16])%MODULUS)
    return w


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    steps,residuals=chart()
    result={'schema':'independent-sha256-coordinate-reconstruction-v1',
            'source_read_before_author_proof':True,
            'support':S,'free_inactive_coordinates':P,'known_initially':sorted(set(S)|set(P)),
            'steps':steps,'remaining_recurrences':residuals,
            'inverse_rows':INVERSE,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'assignments':len(steps),'residuals':residuals,
                      'solved_coordinate_order':[r['new_coordinate'] for r in steps],
                      'solved_equation_order':[r['recurrence'] for r in steps],
                      'sigma_inverse_basis_compositions':128},sort_keys=True))
