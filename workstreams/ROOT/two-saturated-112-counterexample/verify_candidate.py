"""Independent exhaustive original-definition verifier; no discovery imports."""
import itertools,json,collections
from pathlib import Path

def verify(data):
    n=data['n'];edges=data['edges'];assert n==7
    assert len(edges)==len({tuple(sorted(e)) for e in edges})
    adj=[set() for _ in range(n)]
    for u,v in edges:
        assert 0<=u<n and 0<=v<n and u!=v
        adj[u].add(v);adj[v].add(u)
    degrees=[len(a) for a in adj]
    assert max(degrees)<=3
    assert all(sum(degrees[v]==3 for v in adj[u])<=2 for u in range(n) if degrees[u]==3)
    distances=[]
    for root in range(n):
        d=[n+1]*n;d[root]=0;q=collections.deque([root])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if d[v]>d[u]+1:d[v]=d[u]+1;q.append(v)
        assert max(d)<=n
        distances.append(d)
    good=[]
    for colors in itertools.product(range(3),repeat=n):
        if all(colors[u]!=colors[v] or distances[u][v]>(1,1,2)[colors[u]] for u in range(n) for v in range(u+1,n)):
            good.append(colors)
    assert not good,good[:1]
    # Explicit short proof: triangle 0,1,3; each possible third-colored
    # triangle vertex sees all vertices within two. Deleting it leaves odd cycle.
    cycles={0:[1,3,5,2,4],1:[0,3,5,2,6],3:[0,1,4,2,6]}
    for u,cycle in cycles.items():
        assert max(distances[u])==2
        assert u not in cycle and len(set(cycle))==5
        assert all(b in adj[a] for a,b in zip(cycle,cycle[1:]+cycle[:1]))
    return {'vertices':n,'edges':len(edges),'degrees':degrees,'assignments':3**n,'valid_colorings':0,'diameter':max(map(max,distances)),'triangle_cases':3}
if __name__=='__main__':
    data=json.loads(Path(__file__).with_name('candidate.json').read_text())
    print(json.dumps(verify(data),sort_keys=True))
    bad=json.loads(json.dumps(data));bad['edges'].append([0,2])
    try:verify(bad)
    except AssertionError: print('PASS rejected degree-four corrupted graph')
    else:raise AssertionError('negative control accepted')
    bad=json.loads(json.dumps(data));bad['edges'].remove([0,1])
    try:verify(bad)
    except AssertionError:print('PASS rejected colorable edge-deleted graph / wrong UNSAT claim')
    else:raise AssertionError('negative control accepted')
