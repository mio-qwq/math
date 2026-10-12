#!/usr/bin/env python3
"""Exact semantic checks for ENDPOINT_SUPPORT_AND_INDEPENDENT_CODES.md.
The universal proofs are in the note; no optimizer is used here.
"""
from collections import deque
from itertools import product, combinations
from pathlib import Path
import hashlib, json, random, time

def direct_strict(code, alphabet):
    for w in product(alphabet, repeat=8):
        if sum(w[i:i+4] in code for i in range(5)) > 2:
            return False, w
    return True, None

def supports(code):
    return ({r: {w[:r] for w in code} for r in (1,2,3)},
            {r: {w[-r:] for w in code} for r in (1,2,3)})

def support_criterion(code, alphabet):
    pairs=list(product(alphabet,repeat=2))
    edges={p:set() for p in pairs}
    for w in code: edges[w[:2]].add(w[2:])
    for a in pairs:
        for b in edges[a]:
            for c in edges[b]:
                if edges[c]: return False
    P,Q=supports(code)
    for u in code:
        for v in code:
            if u[1:] == v[:3]:
                if any(u[:r] in Q[r] or v[-r:] in P[r] for r in (1,2,3)):
                    return False
    return True

def graph(m):
    words=[w for w in product(range(m),repeat=4)
           if all(w[i] != w[i+1] for i in range(3))]
    index={w:i for i,w in enumerate(words)}
    adjacency=[[index[w[1:]+(a,) ] for a in range(m) if a!=w[-1]] for w in words]
    distances=[]
    for start in range(len(words)):
        ds=[-1]*len(words);ds[start]=0;queue=deque([start])
        while queue:
            u=queue.popleft()
            for v in adjacency[u]:
                if ds[v]<0: ds[v]=ds[u]+1;queue.append(v)
        distances.append(ds)
    return words,index,adjacency,distances

def overlap_distance(u,v):
    if u==v: return 0
    for k in (3,2,1):
        if u[-k:]==v[:k]: return 4-k
    return 4

def gp_witness(selected, distances):
    for x in selected:
        for y in selected:
            if y==x: continue
            for z in selected:
                if z==x or z==y: continue
                if distances[x][y]+distances[y][z]==distances[x][z]:
                    return (x,y,z)
    return None

def lift_check(q, expected_m=None, damaged=False):
    m=2*q
    if expected_m is not None:
        assert expected_m==m, 'alphabet binding mismatch'
    words,index,adjacency,distances=graph(m)
    assert all(distances[i][j]==overlap_distance(u,v)
               for i,u in enumerate(words) for j,v in enumerate(words))
    patterns={(0,0,0,1),(0,0,1,1)}
    if damaged: patterns.add((0,1,0,1))
    selected={i for i,w in enumerate(words) if tuple(a//q for a in w) in patterns}
    witness=gp_witness(selected,distances)
    if damaged:
        assert witness is not None
        return {'q':q,'damaged_code_gp_witness':[words[i] for i in witness]}
    assert witness is None
    expected=q*q*(q-1)*(q-1)
    assert len(selected)==2*expected
    components=[];covered=set()
    for b in range(q):
        for c in range(q):
            if b==c: continue
            for d in range(q,m):
                left={index[(a,b,c,d)] for a in range(q) if a!=b}
                right={index[(b,c,d,e)] for e in range(q,m) if e!=d}
                assert len(left)==len(right)==q-1
                assert not ((left|right)&covered)
                covered.update(left|right)
                for u in left:
                    assert set(adjacency[u])&selected==right
                for v in right:
                    assert not (set(adjacency[v])&selected)
                # A perfect matching gives |left| disjoint adjacency constraints;
                # choosing either whole side attains the resulting exact bound.
                matching=list(zip(sorted(left),sorted(right)))
                assert len(matching)==q-1
                assert all(v in adjacency[u] for u,v in matching)
                components.append({'triple':[b,c,d],
                                   'left':[words[i] for i in sorted(left)],
                                   'right':[words[i] for i in sorted(right)]})
    assert covered==selected
    assert len(components)==q*q*(q-1)
    max_independent=len(components)*(q-1)
    assert max_independent==expected
    return {'q':q,'m':m,'vertices':len(words),'selected':len(selected),
            'component_count':len(components),'part_size':q-1,
            'exact_max_independent_subset':max_independent,
            'exact_minimum_deletion':expected,'components':components}

def main():
    started=time.monotonic();D={(0,0,0,1),(0,0,1,1)}
    codes=[set(),{(0,0,0,1)},{(0,0,1,1)},D,
           D|{(0,1,0,1)},D|{(0,1,1,1)}]
    binary=[]
    for C in codes:
        direct,witness=direct_strict(C,(0,1))
        assert direct==support_criterion(C,(0,1))
        binary.append({'code':sorted(C),'strict':direct,'counterexample':witness})
    assert direct_strict(D,(0,1))[0]
    assert not direct_strict(D|{(0,1,0,1)},(0,1))[0]
    # Independent samples of the saturation theorem; direct window enumeration
    # is independent of the support/level argument.
    rng=random.Random(20261012);A=(0,1,2);quadruples=list(product(A,repeat=4))
    saturated=[]
    for trial in range(20):
        ell={p:rng.randrange(3) for p in product(A,repeat=2)}
        tau={t:rng.randrange(2) for t in product(A,repeat=3)}
        C={w for w in quadruples if ell[w[:2]]<ell[w[2:]]
           and tau[w[:3]]==1 and tau[w[1:]]==0}
        assert direct_strict(C,A)[0]
        P,Q=supports(C);assert not(P[3]&Q[3])
        assert support_criterion(C,A)
        saturated.append({'trial':trial,'size':len(C),'ell':[[list(k),v] for k,v in ell.items()],
                          'tau':[[list(k),v] for k,v in tau.items()]})
    lifts=[lift_check(q) for q in (2,3)]
    damaged=lift_check(2,damaged=True)
    try:
        lift_check(2,expected_m=5)
    except AssertionError:
        binding_negative=True
    else: raise AssertionError('damaged alphabet binding was accepted')
    words,_,_,ds=graph(4)
    broken=[row[:] for row in ds];broken[0][1]+=1
    assert any(broken[i][j]!=overlap_distance(u,v)
               for i,u in enumerate(words) for j,v in enumerate(words))
    report={'status':'finite semantic checks passed; universal mathematics is written',
            'binary_codes':binary,'saturated_samples':saturated,'actual_kautz_lifts':lifts,
            'negative_controls':{'damaged_code':damaged,'damaged_distance_rejected':True,
                                 'damaged_parameter_binding_rejected':binding_negative},
            'seconds':time.monotonic()-started}
    here=Path(__file__).resolve().parent
    proof=here/'ENDPOINT_SUPPORT_AND_INDEPENDENT_CODES.md'
    report['proof_sha256']=hashlib.sha256(proof.read_bytes()).hexdigest()
    report['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    target=here/'endpoint_structure_verification.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','seconds','proof_sha256','checker_sha256')},indent=2))
    print('Actual lift checks:',[(x['q'],x['selected'],x['exact_max_independent_subset']) for x in lifts])
    print('Negative controls passed: damaged code, distance, alphabet binding.')
if __name__=='__main__':main()
