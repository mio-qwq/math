"""Independent original-definition check of the fixed 11 x 29 counterexample.

Standard library only. Reads no author program, JSON, certificate, or data file.
All graph distances come from the adjacency predicates below. In particular the
Cartesian sum formula is tested after, not used in, the product BFS computation.
GP means no three DISTINCT vertices on a shortest path; maximal means inclusion.
This is a fixed-object verifier, not a counterexample or graph-order search.
"""
from collections import Counter, deque
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations
import json
import platform
import sys
import time


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def g_adj(x, y):
    return x != y and (x == 0 or y == 0 or ((x <= 5) == (y <= 5)))


def h_adj(x, y):
    if x == y:
        return False
    if x > y:
        x, y = y, x
    if y < 5:
        return x == 2 or y == 2 or (x < 2 and y >= 3)
    if x >= 5:
        return (x - 5) // 6 == (y - 5) // 6
    i, j = divmod((y - 5) // 6, 2)
    return x in (i, 2, 3 + j)


def adjacency(n, pred):
    ans = [[] for _ in range(n)]
    for x, y in combinations(range(n), 2):
        require(pred(x, y) == pred(y, x), 'non-symmetric predicate')
        if pred(x, y):
            ans[x].append(y)
            ans[y].append(x)
    require(all(not pred(x, x) for x in range(n)), 'loop')
    return ans


def all_bfs(adj):
    distances, parents = [], []
    for source in range(len(adj)):
        dist = [-1] * len(adj)
        parent = [-1] * len(adj)
        dist[source] = 0
        queue = deque([source])
        while queue:
            x = queue.popleft()
            for y in adj[x]:
                if dist[y] < 0:
                    dist[y] = dist[x] + 1
                    parent[y] = x
                    queue.append(y)
        require(min(dist) == 0, 'graph disconnected')
        distances.append(dist)
        parents.append(parent)
    return distances, parents


def floyd(adj):
    n = len(adj)
    ans = [[0 if x == y else 1 if y in adj[x] else n + 1
            for y in range(n)] for x in range(n)]
    for k in range(n):
        for x in range(n):
            for y in range(n):
                ans[x][y] = min(ans[x][y], ans[x][k] + ans[k][y])
    return ans


def collinear(dist, x, y, z):
    require(len({x, y, z}) == 3, 'non-distinct GP triple')
    a, b, c = sorted((dist[x][y], dist[y][z], dist[z][x]))
    return a + b == c


def is_gp(dist, selected):
    if len(set(selected)) != len(selected):
        return False
    return all(not collinear(dist, *t) for t in combinations(selected, 3))


def extension(dist, selected):
    pairs = list(combinations(selected, 2))
    used = set(selected)
    for x in range(len(dist)):
        if x not in used and all(not collinear(dist, a, b, x) for a, b in pairs):
            return x
    return None


def low_sets(dist, bound):
    counts, gp_counts = [], []
    evidence = sha256()
    for k in range(bound + 1):
        total = good = 0
        for selected in combinations(range(len(dist)), k):
            total += 1
            if is_gp(dist, selected):
                good += 1
                x = extension(dist, selected)
                require(x is not None, f'factor maximal GP below 6: {selected}')
                require(is_gp(dist, selected + (x,)), 'extension recheck')
                evidence.update(json.dumps([selected, x], separators=(',', ':')).encode())
                evidence.update(b'\n')
        counts.append(total)
        gp_counts.append(good)
    return {'all_subsets_by_size': counts, 'gp_subsets_by_size': gp_counts,
            'extension_certificate_sha256': evidence.hexdigest()}


def path(parents, source, target):
    out = [target]
    while out[-1] != source:
        out.append(parents[source][out[-1]])
        require(out[-1] >= 0, 'no BFS path')
    return list(reversed(out))


def blocker(dist, selected, x):
    for a, b in combinations(selected, 2):
        for left, middle, right in ((x, a, b), (a, x, b), (a, b, x)):
            if dist[left][middle] + dist[middle][right] == dist[left][right]:
                return left, middle, right
    return None


def bad_claim_rejected(thunk):
    try:
        thunk()
    except AssertionError:
        return True
    raise AssertionError('negative control was accepted')


def digest(obj):
    return sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def main():
    started = datetime.now(timezone.utc).isoformat()
    tick = time.perf_counter_ns()
    ga, ha = adjacency(11, g_adj), adjacency(29, h_adj)
    gd, gp = all_bfs(ga)
    hd, hp = all_bfs(ha)
    require(gd == floyd(ga), 'G BFS/Floyd disagree')
    require(hd == floyd(ha), 'H BFS/Floyd disagree')
    require(sum(map(len, ga)) // 2 == 30, 'G edge count')
    require(sum(map(len, ha)) // 2 == 140, 'H edge count')
    require(max(map(max, gd)) == max(map(max, hd)) == 2, 'diameter 2')

    # Direct construction over all unordered actual pairs; no distance shortcut.
    vertices = [(g, h) for g in range(11) for h in range(29)]
    def padj(x, y):
        g, h = vertices[x]
        gg, hh = vertices[y]
        return (g == gg and h_adj(h, hh)) or (h == hh and g_adj(g, gg))
    pa = adjacency(len(vertices), padj)
    pd, pp = all_bfs(pa)
    require(sum(map(len, pa)) // 2 == 2410, 'Cartesian edge count')
    require(max(map(max, pd)) == 4, 'Cartesian diameter')
    for x, (g, h) in enumerate(vertices):
        for y, (gg, hh) in enumerate(vertices):
            require(pd[x][y] == gd[g][gg] + hd[h][hh], 'distance additivity')

    selected_pairs = [(1, 0), (1, 1), (0, 2), (6, 3), (6, 4)]
    selected = tuple(vertices.index(p) for p in selected_pairs)
    require(is_gp(pd, selected), 'proposed five-set fails GP')
    witness_hash = sha256()
    role_counts, length_counts = Counter(), Counter()
    witness_count = 0
    for x in range(len(vertices)):
        if x in selected:
            continue
        witness = blocker(pd, selected, x)
        require(witness is not None, f'unblocked outside vertex {vertices[x]}')
        left, middle, right = witness
        route = path(pp, left, middle) + path(pp, middle, right)[1:]
        require(len(route) == len(set(route)), 'shortest witness repeats vertex')
        require(all(v in pa[u] for u, v in zip(route, route[1:])), 'nonedge in path')
        require(len(route) - 1 == pd[left][right], 'witness path not shortest')
        require({x, middle} <= set(route), 'missing point in witness path')
        require(len(set(route) & set(selected)) >= 2, 'missing two selected vertices')
        role_counts['outside_middle' if middle == x else 'outside_endpoint'] += 1
        length_counts[len(route) - 1] += 1
        witness_count += 1
        witness_hash.update(json.dumps([x, witness, route], separators=(',', ':')).encode())
        witness_hash.update(b'\n')
    require(witness_count == 314, 'not every outside point handled')
    require(extension(pd, selected) is None, 'maximality independent recheck')

    factors = {'G': low_sets(gd, 5), 'H': low_sets(hd, 5)}
    maximal_g = []
    for k in range(6, 12):
        for t in combinations(range(11), k):
            if is_gp(gd, t) and extension(gd, t) is None:
                maximal_g.append(t)
    require(maximal_g == [tuple(range(6)), (0, 6, 7, 8, 9, 10), tuple(range(1, 11))],
            'G maximal-set classification')

    # Independent quotient check after checking literal true-twin neighborhoods.
    # The accompanying paper proof establishes saturation, hence completeness.
    classes = [(i,) for i in range(5)] + [tuple(range(5+6*q, 11+6*q)) for q in range(4)]
    for twin_class in classes[5:]:
        require(all(set(ha[x]) | {x} == set(ha[twin_class[0]]) | {twin_class[0]}
                    for x in twin_class), 'not true twins')
    maximal_h_saturated = []
    for mask in range(1 << len(classes)):
        t = tuple(x for i, c in enumerate(classes) if mask >> i & 1 for x in c)
        if is_gp(hd, t) and extension(hd, t) is None:
            maximal_h_saturated.append(t)
    require(min(map(len, maximal_h_saturated)) >= 6, 'saturated H lower bound')

    # Real bad mathematical claims, not unconditional deliberate exceptions.
    controls = {
        'four_point_subset_is_maximal': bad_claim_rejected(
            lambda: require(extension(pd, selected[:-1]) is None, 'four-set extends')),
        'six_point_superset_is_GP': bad_claim_rejected(
            lambda: require(is_gp(pd, selected + (0,)), 'outside vertex blocked')),
        'G_lower_number_at_least_7': bad_claim_rejected(
            lambda: require(not (is_gp(gd, tuple(range(6))) and
                                extension(gd, tuple(range(6))) is None), 'maximal K6')),
        'G_cross_block_triple_is_GP': bad_claim_rejected(
            lambda: require(is_gp(gd, (1, 0, 6)), 'a-c-b shortest path')),
    }
    answer = {
        'status': 'PASS', 'started_utc': started,
        'finished_utc': datetime.now(timezone.utc).isoformat(),
        'elapsed_ns': time.perf_counter_ns() - tick,
        'python': sys.version, 'platform': platform.platform(),
        'graphs': {'orders': [11, 29, 319], 'edges': [30, 140, 2410], 'diameters': [2, 2, 4]},
        'factor_distance_checks': 'BFS and independent Floyd matrices equal',
        'product_BFS_distance_entries': 319**2,
        'adjacency_sha256': {'G': digest(ga), 'H': digest(ha), 'product': digest(pa)},
        'distance_sha256': {'G': digest(gd), 'H': digest(hd), 'product': digest(pd)},
        'selected_coordinates': selected_pairs,
        'selected_distance_matrix': [[pd[x][y] for y in selected] for x in selected],
        'selected_unordered_triples_checked': 10,
        'outside_vertices_with_actual_shortest_path': witness_count,
        'outside_roles': dict(role_counts), 'blocking_path_lengths': dict(length_counts),
        'blocker_paths_sha256': witness_hash.hexdigest(),
        'small_factor_subsets': factors,
        'G_all_maximal_GP_sets': maximal_g,
        'H_saturated_maximal_GP_size_counts': dict(sorted(Counter(map(len, maximal_h_saturated)).items())),
        'negative_controls_rejected': controls,
        'conclusion': 'gpminus(G)=6; gpminus(H)>=6; gpminus(G Cartesian H)<=5',
        'independence': 'No author code/data read at runtime; no universal-min5 dependency; no Lean claim',
    }
    print(json.dumps(answer, indent=2))


if __name__ == '__main__':
    main()
