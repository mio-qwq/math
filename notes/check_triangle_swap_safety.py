"""Exact, bounded check of a literal local-swap condition; no Tuza claim."""
from pathlib import Path
from itertools import combinations
from datetime import datetime, timezone
import hashlib, json

vertices = tuple('uvwxyzf')
edge_words = ('uv','uw','vw','vx','vy','xy','ux','uz','xz','uf','xf','wy')
edges = frozenset(frozenset(e) for e in edge_words)

def te(t):
    return frozenset(frozenset(e) for e in combinations(t, 2))

triangles = tuple(frozenset(t) for t in combinations(vertices, 3) if te(t) <= edges)

def packing(p):
    return all(te(a).isdisjoint(te(b)) for a,b in combinations(p,2))

def support(p):
    return frozenset().union(*p)

packings = [p for k in range(len(triangles)+1) for p in combinations(triangles,k) if packing(p)]
max_packing = max(map(len, packings))
max_support_at_max = max(len(support(p)) for p in packings if len(p)==max_packing)
old = tuple(frozenset(t) for t in ('uvw','vxy','uxz'))
old_local = old[:2]
new_local = tuple(frozenset(t) for t in ('uxf','vwy'))
outside = frozenset(vertices)-support(old)
new_global = new_local+old[2:]
assert len(vertices)==7 and len(edges)==12 and max_packing==3 and max_support_at_max==6
assert all(t in triangles for t in old+new_local) and packing(old) and packing(new_local)
assert support(new_local)<=outside|support(old_local)
assert len(support(new_local))>len(support(old_local))
assert not packing(new_global) and te(new_local[0]) & te(old[2]) == {frozenset('ux')}
assert frozenset().union(*(te(t) for t in triangles))==edges
assert all(any(v in t for t in triangles) for v in vertices)
assert not any(all(frozenset(e) in edges for e in combinations(q,2)) for q in combinations(vertices,4))
# Rule 4 cannot split a vertex: its incident-edge triangle link is connected.
links_connected = {}
for v in vertices:
    ns = {next(iter(e-{v})) for e in edges if v in e}
    seen = {next(iter(ns))}
    while True:
        nxt = seen | {b for a in seen for b in ns if frozenset((a,b)) in edges}
        if nxt==seen: break
        seen=nxt
    links_connected[v] = seen==ns
assert all(links_connected.values())
cover_number = next(k for k in range(len(edges)+1) if any(all(te(t)&set(c) for t in triangles) for c in combinations(edges,k)))
assert cover_number<=2*max_packing
def word(t): return ''.join(v for v in vertices if v in t)
receipt = {
    'checked_utc': datetime.now(timezone.utc).isoformat(),
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'vertices':list(vertices), 'edges':list(edge_words),
    'all_triangles':[word(t) for t in triangles],
    'packing_number':max_packing, 'max_support_at_maximum_packing':max_support_at_max,
    'cover_number':cover_number, 'old_packing':[word(t) for t in old],
    'old_pair':[word(t) for t in old_local], 'outside_vertices':word(outside),
    'new_pair':[word(t) for t in new_local],
    'old_pair_support':len(support(old_local)), 'new_pair_support':len(support(new_local)),
    'new_pair_is_packing':True, 'retained_triangle':word(old[2]),
    'replacement_is_global_packing':False, 'conflicting_edge':'ux',
    'all_edges_and_vertices_triangular':True, 'contains_K4':False,
    'vertex_triangle_links_connected':links_connected,
    'previous_rules_note':'For k=4, rules 1-5 do not terminate/reduce; maximum packing forbids 6/7. Rule8 literal local condition succeeds but global packing fails.',
    'claim_scope':'finite counterexample to an unqualified local-swap safety implication; NOT a Tuza counterexample or invalidation of all kernel/discharging conclusions',
    'sources':['https://arxiv.org/html/2308.16515v1','https://www.researchgate.net/publication/376376955_A_Discharging_Method_Improved_Kernels_for_Edge_Triangle_Packing_and_Covering']
}
print(json.dumps(receipt,ensure_ascii=False))
