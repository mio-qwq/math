"""Bounded definition-first publication replay. No coloring enumeration.

This checker does not import the historical discovery/verifier code.
It reconstructs graphs, checks the exact mathematical certificate fields,
and tests actual full-graph distances and frozen positive controls.
The all-odd-k proof is the manuscript, not these finite fixtures.
"""
from collections import deque
from itertools import combinations
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json, platform

HERE = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def reconstruct(k):
    require(type(k) is int and k >= 3, 'ring length must be an integer >= 3')
    core = [set() for _ in range(4*k)]
    for i in range(k):
        a,b,p,q = (4*i+j for j in range(4))
        for u,v in [(a,b),(a,p),(a,q),(b,p),(b,q),(q,4*((i+1)%k)+2)]:
            require(u != v and v not in core[u], 'loop or repeated core edge')
            core[u].add(v); core[v].add(u)
    labels = [(v,w) for v in range(4*k) for w in sorted(core[v])]
    index = {vw:i for i,vw in enumerate(labels)}
    blocks = [[index[v,w] for w in sorted(core[v])] for v in range(4*k)]
    expanded = [set() for _ in labels]
    for v, block in enumerate(blocks):
        for x,y in combinations(block,2):
            expanded[x].add(y); expanded[y].add(x)
    for x,(v,w) in enumerate(labels):
        expanded[x].add(index[w,v])
    return core, labels, index, blocks, expanded

def all_distances(adj):
    result=[]
    for start in range(len(adj)):
        distances=[None]*len(adj); distances[start]=0; queue=deque([start])
        while queue:
            v=queue.popleft()
            for w in adj[v]:
                if distances[w] is None:
                    distances[w]=distances[v]+1; queue.append(w)
        require(all(d is not None for d in distances), 'disconnected graph')
        result.append(distances)
    return result

def edge_list(adj):
    return [[v,w] for v in range(len(adj)) for w in sorted(adj[v]) if v<w]

def check_certificate(data):
    core,labels,index,blocks,adj=reconstruct(3)
    for field,width in [('edges',2),('core_edges',2),('labels',2)]:
        values=data.get(field)
        require(type(values) is list and all(type(pair) is list and len(pair)==width and
                all(type(x) is int for x in pair) for pair in values), 'invalid '+field+' types')
    require(type(data.get('n')) is int and data['n']==36, 'incorrect graph order')
    require(type(data.get('palette')) is list and all(type(x) is int for x in data['palette'])
            and data['palette']==[1,1,3,3,4], 'incorrect palette')
    require(data['edges']==edge_list(adj), 'incorrect expanded edges')
    require(data['core_edges']==edge_list(core), 'incorrect core edges')
    require(data['labels']==[list(vw) for vw in labels], 'incorrect incidence labels')
    return core,labels,index,blocks,adj

def valid_coloring(distances, colors, radii):
    n=len(distances)
    if len(colors)!=n or any(type(c) is not int or not 0<=c<len(radii) for c in colors):
        return False
    return all(colors[x]!=colors[y] or distances[x][y]>radii[colors[x]]
               for x,y in combinations(range(n),2))

def inspect_fixture(k):
    core,labels,index,blocks,adj=reconstruct(k)
    require(len(adj)==12*k and len(edge_list(adj))==18*k, 'order/size mismatch')
    require(all(len(ns)==3 and v not in ns and all(v in adj[w] for w in ns)
                for v,ns in enumerate(adj)), 'not a simple cubic graph')
    require(all(any(y in adj[x] for x,y in combinations(ns,2)) for ns in adj), 'induced claw')
    triangles={tuple(sorted((x,y,z))) for x in range(len(adj))
               for y,z in combinations(adj[x],2) if z in adj[y]}
    require(triangles=={tuple(block) for block in blocks}, 'unexpected triangle')
    distances=all_distances(adj)
    adjacent_pairs=0
    for v,w in edge_list(core):
        for x in blocks[v]:
            for y in blocks[w]:
                require(distances[x][y]<=3, 'adjacent-core metric bound fails')
                adjacent_pairs+=1
    port_pairs=0
    for x,(v,w) in enumerate(labels):
        for u in core[w]-{v}:
            for y in blocks[u]:
                walk=[x,index[w,v],index[w,u],index[u,w]]
                if y!=walk[-1]: walk.append(y)
                require(all(b in adj[a] for a,b in zip(walk,walk[1:])), 'invalid four-step walk')
                require(len(walk)-1<=4 and distances[x][y]<=4, 'port metric bound fails')
                port_pairs+=1
    # The exact neighbor formulas used to exhaust private-neighbor candidates.
    for i in range(k):
        require(core[4*i+2]=={4*i,4*i+1,4*((i-1)%k)+3}, 'p-neighbor formula')
        require(core[4*i+3]=={4*i,4*i+1,4*((i+1)%k)+2}, 'q-neighbor formula')
    return dict(k=k,n=len(adj),m=len(edge_list(adj)),bfs_rows=len(distances),
                replacement_triangles=len(triangles),adjacent_core_pairs=adjacent_pairs,
                port_four_walk_pairs=port_pairs,connected_simple_cubic_clawfree_diamondfree=True)

def run():
    certificate_path=HERE/'frozen/counterexample.json'
    certificate=json.loads(certificate_path.read_text(encoding='utf-8'))
    _,_,_,blocks,adj=check_certificate(certificate)
    fixtures=[inspect_fixture(k) for k in [3,4,5,7,9]]
    negative=[]
    for label,mutator in [
        ('missing-edge',lambda d:d['edges'].pop()),
        ('corrupt-incidence',lambda d:d['labels'][0].__setitem__(1,11)),
        ('changed-palette',lambda d:d['palette'].__setitem__(4,3)),
        ('bool-for-integer',lambda d:d['palette'].__setitem__(0,True)),
    ]:
        broken=copy.deepcopy(certificate); mutator(broken)
        try: check_certificate(broken)
        except ValueError as error: negative.append(dict(control=label,rejected=str(error)))
        else: raise ValueError('Accepted damaged certificate: '+label)
    # Positive witnesses are frozen data, independently rechecked against fresh BFS.
    historical=json.loads((HERE/'frozen/verifier-author-run.json').read_text(encoding='utf-8'))
    distances=all_distances(adj)
    weaker=historical['weaker_11333_coloring']
    require(valid_coloring(distances,weaker,[1,1,3,3,3]), 'weaker positive control fails')
    require(not valid_coloring(distances,weaker,[1,1,3,3,4]), 'radius-four control must fail')
    damaged=weaker.copy(); damaged[blocks[0][0]]=damaged[blocks[0][1]]=0
    require(not valid_coloring(distances,damaged,[1,1,3,3,3]), 'bad low-color control accepted')
    _,_,_,_,even_adj=reconstruct(4)
    require(valid_coloring(all_distances(even_adj),historical['even_ring_11334_coloring'],[1,1,3,3,4]),
            'even-ring positive control fails')
    result=dict(status='PASS',completed_utc=datetime.now(timezone.utc).isoformat(),
                python=platform.python_version(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                certificate_sha256=hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
                historical_positive_witness_sha256=hashlib.sha256((HERE/'frozen/verifier-author-run.json').read_bytes()).hexdigest(),
                fixtures=fixtures,negative_controls=negative,invalid_coloring_rejected=True,
                weaker_positive_control=True,even_ring_positive_control=True,
                scope='Bounded object/metric/positive-control replay. No 531441-coloring enumeration, no all-odd-k computational proof.')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    run()
