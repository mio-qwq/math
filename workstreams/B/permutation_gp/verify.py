#!/usr/bin/env python3
"""Exact original-definition checker for the fixed Pe(6,3) certificate.

No constructor import or closed distance formula. Rebuilds the full 504-vertex
arc relation by comparing every ordered pair, then uses BFS and all selected
ordered triples. Both programs are authored by B; this is self-verification,
not a claim of review by a separate person/agent.
"""
import argparse
from collections import deque, Counter
import hashlib
from itertools import permutations
import json
from math import prod
from pathlib import Path
import platform
import sys

class Rejected(ValueError):
    pass

def verify(cert):
    d,k=cert.get('d'),cert.get('k')
    if type(d) is not int or type(k) is not int or (d,k)!=(6,3):
        raise Rejected('this exact checker is intentionally fixed to d=6,k=3')
    if not k>=3 or not d>=2*k:
        raise Rejected('outside original conjecture hypotheses')
    alphabet=cert.get('alphabet')
    if alphabet != list(range(d+k)) or any(type(x) is not int for x in alphabet):
        raise Rejected('wrong alphabet')
    raw=cert.get('selected_words')
    if not isinstance(raw,list):
        raise Rejected('selected_words must be a list')
    selected=[]
    for w in raw:
        if not isinstance(w,list) or len(w)!=k or any(type(x) is not int or x not in alphabet for x in w) or len(set(w))!=k:
            raise Rejected('selected word is not a vertex')
        selected.append(tuple(w))
    if len(set(selected))!=len(selected):
        raise Rejected('duplicate selected vertex')
    bound=2*prod(range(d,d+k-1))
    if cert.get('conjectured_value') != bound:
        raise Rejected('incorrect source-bound arithmetic')
    if len(selected)<=bound:
        raise Rejected('selected set does not strictly exceed conjectured value')
    # Original graph: all injective length-k words, not only selected ones.
    vertices=list(permutations(alphabet,k)); index={w:i for i,w in enumerate(vertices)}
    adjacency=[]
    for u in vertices:
        adjacency.append([j for j,v in enumerate(vertices)
                          if u[1:]==v[:-1] and v[-1] not in u])
    indegree=[0]*len(vertices)
    for row in adjacency:
        if len(row)!=d: raise Rejected('wrong out-degree in reconstructed graph')
        for v in row: indegree[v]+=1
    if any(x!=d for x in indegree): raise Rejected('wrong in-degree')
    ids=[index[w] for w in selected]
    distances={}
    pair_distribution=Counter()
    for source in ids:
        row=[-1]*len(vertices); row[source]=0; q=deque([source])
        while q:
            u=q.popleft()
            for v in adjacency[u]:
                if row[v]<0:
                    row[v]=row[u]+1; q.append(v)
        if any(x<0 for x in row): raise Rejected('unreachable vertex from selected source')
        distances[source]=row
        for target in ids:
            if target!=source: pair_distribution[row[target]]+=1
    triples=0
    for u,v,w in permutations(ids,3):
        triples+=1
        if distances[u][w]==distances[u][v]+distances[v][w]:
            raise Rejected('geodesic triple: '+repr((vertices[u],vertices[v],vertices[w])))
    return {'result':'PASS','d':d,'k':k,'graph_vertices':len(vertices),
            'graph_arcs':sum(map(len,adjacency)), 'in_degree':d,'out_degree':d,
            'conjectured_value':bound,'verified_gp_lower_bound':len(ids),
            'strict_excess':len(ids)-bound,'selected_ordered_pairs':len(ids)*(len(ids)-1),
            'selected_distance_distribution':dict(sorted(pair_distribution.items())),
            'selected_ordered_triples_checked':triples,
            'claim':'Original optimality conjecture is false; exact gp value is not determined.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificate',nargs='?',default=str(Path(__file__).with_name('certificate.json')))
    args=p.parse_args(); path=Path(args.certificate); raw=path.read_bytes()
    result=verify(json.loads(raw))
    result.update(certificate_sha256=hashlib.sha256(raw).hexdigest(),
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  python=sys.version,platform=platform.platform())
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
