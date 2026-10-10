"""Original full-digraph BFS validation, independent of the support-search code."""
from itertools import product,permutations,combinations
from collections import deque
import json,platform
W=[w for w in product(range(4),repeat=4) if all(w[i]!=w[i+1] for i in range(3))]
idx={w:i for i,w in enumerate(W)}
A=[[idx[w[1:]+(x,)] for x in range(4) if x!=w[-1]] for w in W]
D=[]
for s in range(len(W)):
    d=[-1]*len(W);d[s]=0;q=deque([s])
    while q:
        u=q.popleft()
        for v in A[u]:
            if d[v]<0:d[v]=d[u]+1;q.append(v)
    assert min(d)>=0;D.append(d)
P=list(permutations(range(4)))
def odd(w):return sum(w[i]>w[j] for i in range(4) for j in range(i+1,4))%2==1
S=[idx[w] for w in P if odd(w)]
def gp(ids):return all(D[u][v]+D[v][w]!=D[u][w] for u,v,w in permutations(ids,3))
assert len(S)==12 and gp(S)
orbits={min(w[i:]+w[:i] for i in range(4)) for w in P}
assert len(orbits)==6
triples=0
for w in orbits:
    vs=[idx[w[i:]+w[:i]] for i in range(4)]
    for i,j in permutations(range(4),2):assert D[vs[i]][vs[j]]==(j-i)%4
    for t in combinations(vs,3):assert not gp(t);triples+=1
bad=S+[next(idx[w] for w in P if not odd(w))]
assert not gp(bad)
print(json.dumps(dict(status='PASS',python=platform.python_version(),full_vertices=len(W),bfs_distance_pairs=len(W)**2,odd_witness_size=len(S),selected_ordered_triples=12*11*10,rotation_orbits=6,upper_bound_triples=triples,negative_controls=1,scope='exact four-letter-support maximum12; no original full gp formula'),sort_keys=True))
