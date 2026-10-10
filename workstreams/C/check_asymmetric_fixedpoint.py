#!/usr/bin/env python3
"""Exact independent certificate checker for C's fixed-point TF example.

The graph is rebuilt from its separately listed edges.  No graph library,
no discovery-script imports and no numerical eigensolver are used.
The universal proof in mizzi_v3_asymmetric_theorem.md stands separately.
"""
import argparse
from collections import Counter, deque
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import platform


def build_matrix(document):
    n = document['n']
    assert type(n) is int and 1 <= n <= 80
    A = [[False] * n for _ in range(n)]
    used = set()
    for raw in document['edges']:
        assert type(raw) is list and len(raw) == 2
        u, v = raw
        assert type(u) is type(v) is int and 0 <= u < v < n
        assert (u, v) not in used, 'repeated undirected edge'
        used.add((u, v))
        A[u][v] = A[v][u] = True
    assert all(not A[i][i] for i in range(n))
    return A


def components_and_bipartite(A):
    n = len(A)
    seen = [-1] * n
    components = 0
    is_bip = True
    for root in range(n):
        if seen[root] >= 0:
            continue
        components += 1
        seen[root] = 0
        todo = deque([root])
        while todo:
            u = todo.popleft()
            for v in range(n):
                if not A[u][v]:
                    continue
                if seen[v] == -1:
                    seen[v] = seen[u] ^ 1
                    todo.append(v)
                elif seen[v] == seen[u]:
                    is_bip = False
    return components, is_bip


def stable_vertex_colors(A):
    n = len(A)
    degrees = [sum(row) for row in A]
    triangles = [sum(A[i][j] and A[j][k] and A[k][i]
                     for j in range(n) for k in range(j+1,n)) for i in range(n)]
    sig = [(degrees[i], triangles[i]) for i in range(n)]
    while True:
        # Only graph invariants: degrees, triangles, and multisets of
        # neighbours' previous invariant colours. Equality preserves all.
        keys = [(sig[i], tuple(sorted(sig[j] for j in range(n) if A[i][j])))
                for i in range(n)]
        mapping = {key: i for i, key in enumerate(sorted(set(keys)))}
        refined = [mapping[key] for key in keys]
        same_partition = all((refined[i] == refined[j]) == (sig[i] == sig[j])
                             for i in range(n) for j in range(n))
        sig = refined
        if same_partition:
            return sig


def has_nontrivial_automorphism(A):
    """Complete (not heuristic) backtracking on labelled adjacency matrices.

    Vertex invariants only prune the bijection search. Every bijection
    satisfying the raw adjacency relation is represented and checked.
    """
    n = len(A)
    colors = stable_vertex_colors(A)
    candidates = [[v for v in range(n) if colors[v] == colors[u]]
                  for u in range(n)]
    mapping = [-1] * n
    inverse = [-1] * n
    steps = 0
    def backtrack(remaining, nonidentity):
        nonlocal steps
        steps += 1
        if not remaining:
            return nonidentity
        best_options = None
        best_u = None
        # Use the smallest remaining candidate set for exhaustive pruning.
        for u in remaining:
            poss = []
            for v in candidates[u]:
                if inverse[v] >= 0:
                    continue
                if all(A[u][w] == A[v][mapping[w]]
                       for w in range(n) if mapping[w] >= 0):
                    poss.append(v)
            if best_options is None or len(poss) < len(best_options):
                best_u = u
                best_options = poss
        if not best_options:
            return False
        for v in best_options:
            mapping[best_u] = v
            inverse[v] = best_u
            if backtrack(tuple(u for u in remaining if u != best_u),
                         nonidentity or v != best_u):
                return True
            mapping[best_u] = -1
            inverse[v] = -1
        return False
    answer = backtrack(tuple(range(n)), False)
    return answer, steps, len(set(colors))


def permutation_orbits(p):
    n = len(p)
    assert type(p) is list and len(p) == n
    assert all(type(a) is int for a in p) and sorted(p) == list(range(n))
    unseen = set(range(n))
    out = []
    while unseen:
        seed = min(unseen)
        cyc = []
        v = seed
        while v in unseen:
            unseen.remove(v)
            cyc.append(v)
            v = p[v]
        assert v == seed
        out.append(cyc)
    return out


def tf_relation(A, alpha):
    n = len(A)
    inverse = [0]*n
    for i, j in enumerate(alpha):
        inverse[j] = i
    return all(A[i][j] == A[alpha[i]][inverse[j]]
               for i in range(n) for j in range(n))


def raw_cdc_automorphism(A, alpha):
    """Independently check the 2n-vertex canonical-cover adjacency relation."""
    n = len(A)
    inverse = [0]*n
    for i, j in enumerate(alpha): inverse[j] = i
    def image(u):
        v, layer = divmod(u, 2)
        return 2*(alpha[v] if layer == 0 else inverse[v]) + layer
    for u in range(2*n):
        for v in range(2*n):
            a, x = divmod(u, 2)
            b, y = divmod(v, 2)
            old = x != y and A[a][b]
            pp, xx = divmod(image(u), 2)
            qq, yy = divmod(image(v), 2)
            new = xx != yy and A[pp][qq]
            if old != new:
                return False
    return True


def valid_cycle(A, values, length):
    n = len(A)
    return (isinstance(values, list) and len(values) == length
            and len(set(values)) == length
            and all(type(v) is int and 0 <= v < n for v in values)
            and all(A[values[i]][values[(i+1) % length]]
                    for i in range(length)))


def verify(doc):
    A = build_matrix(doc)
    n = len(A)
    assert n == 13 and sum(map(sum, A)) == 2 * 39
    components, bipartite = components_and_bipartite(A)
    assert components == 1 and not bipartite, 'source conditions incorrect'
    assert len({tuple(row) for row in A}) == n, 'not vertex determining'
    has_auto, steps, num_colors = has_nontrivial_automorphism(A)
    assert not has_auto, 'ordinary graph is not asymmetric'
    alpha = doc['alpha']
    orbits = permutation_orbits(alpha)
    assert [len(c) for c in orbits] == [1, 3, 3, 3, 3]
    assert alpha != list(range(n))
    assert tf_relation(A, alpha), 'TF condition violated'
    assert raw_cdc_automorphism(A, alpha), '26-vertex CDC isomorphism failed'
    k = len(doc['odd_cycle'])
    assert k >= 3 and k % 2 == 1
    assert valid_cycle(A, doc['odd_cycle'], k)
    assert valid_cycle(A, doc['double_cycle'], 2*k)
    assert set(doc['odd_cycle']).isdisjoint(doc['double_cycle'])
    return {'nodes':n,'edges':sum(map(sum,A))//2,
            'connected':True,'nonbipartite':True,'vertex_determining':True,
            'asymmetric':True,'tf_orbits':list(map(len,orbits)),
            'disjoint_cycle_lengths':[k,2*k],
            'asym_search_states':steps,'refinement_colors':num_colors}


def mutation_tests(doc):
    tests = []
    broken = deepcopy(doc)
    broken['edges'].remove([0, 4])
    tests.append(('removed_TF_edge',broken))
    broken = deepcopy(doc)
    broken['alpha'][1], broken['alpha'][4] = broken['alpha'][4], broken['alpha'][1]
    tests.append(('wrong_TF_permutation',broken))
    broken = deepcopy(doc)
    broken['double_cycle'][-1] = broken['double_cycle'][0]
    tests.append(('repeated_cycle_vertex',broken))
    broken = deepcopy(doc)
    broken['edges'].append([1,1])
    tests.append(('illegal_graph_loop',broken))
    for title, altered in tests:
        try:
            verify(altered)
        except (AssertionError,ValueError):
            continue
        raise RuntimeError('NEGATIVE TEST ACCEPTED: '+title)
    return [name for name,_ in tests]


def main():
    pa = argparse.ArgumentParser()
    pa.add_argument('certificate', nargs='?', default=str(Path(__file__).with_name('asymmetric_fixedpoint_certificate.json')))
    opts = pa.parse_args()
    p = Path(opts.certificate)
    data = json.loads(p.read_text(encoding='utf-8'))
    answer = verify(data)
    negative = mutation_tests(data)
    print('PASS: independent exact graph/cover/cycle/asymmetry checks')
    print('version:',platform.python_version())
    print('witness:',answer)
    print('negative controls rejected:',', '.join(negative))
    print('source SHA256:',sha256(Path(__file__).read_bytes()).hexdigest())
    print('input SHA256:',sha256(p.read_bytes()).hexdigest())


if __name__ == '__main__': main()
