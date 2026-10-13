"""Bounded independent audit controls. Does not execute MET5 or Lean."""
from pathlib import Path
from itertools import combinations, product
from collections import deque
from fractions import Fraction
from functools import reduce
from math import gcd
import ast
import hashlib
import json
import random
from datetime import datetime, timezone

REPO = Path(r"C:\Users\Administrator\Desktop\math\research")
WRITTEN = REPO / "workstreams/ROOT/distributed-written-proofs/B/lower_gp_product"
FIXED = REPO / "workstreams/ROOT/lower-gp-product319-counterexample"
OUT = Path(__file__).resolve().parent


def rank(rows, dimension):
    a = [[Fraction(x) for x in row] for row in rows]
    p = 0
    for c in range(dimension):
        pivot = next((i for i in range(p, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[p], a[pivot] = a[pivot], a[p]
        s = a[p][c]
        a[p] = [x / s for x in a[p]]
        for i in range(len(a)):
            if i != p and a[i][c]:
                s = a[i][c]
                a[i] = [x - s * y for x, y in zip(a[i], a[p])]
        p += 1
    return p


def extract_function(path, name):
    source = path.read_text(encoding="utf-8")
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name)
    return ast.get_source_segment(source, node)


def reduced_cone_controls():
    source = extract_function(WRITTEN / "verify_metric_rays.py", "extreme_metric_rays")
    adjacency_line = "if any(k not in (i,j) and z&common==common for k,(r,z) in enumerate(rays)):continue"
    assert source.count(adjacency_line) == 1
    instrument = """third=any(k not in (i,j) and z&common==common for k,(r,z) in enumerate(rays))
    coordinate_rows=[tuple(int(a==b) for a in range(dimension)) for b in range(dimension)]
    active=[h for b,h in enumerate(coordinate_rows+constraints[:step]) if common>>b&1]
    adjacent_by_rank=(rank(active,dimension)==dimension-2)
    assert (not third)==adjacent_by_rank
    stats[n]['adjacency_pairs']+=1
    if third:continue"""
    source = source.replace(adjacency_line, instrument)
    # The production routine has a fixed MET5 count. This control intentionally
    # replaces only that count to exercise dimensions 3 and 4, never dimension 5.
    assert source.count("assert len(result)==25") == 1
    source = source.replace("assert len(result)==25", "assert len(result)==(1<<(n-1))-1")
    stats = {n: {"adjacency_pairs": 0} for n in (3, 4)}
    scope = dict(combinations=combinations, reduce=reduce, gcd=gcd, json=json, rank=rank, stats=stats)
    exec(compile(source, "<reduced-dimension-production-ray-function>", "exec"), scope)
    for n in (3, 4):
        edges, triangle_rows, rays, stages = scope["extreme_metric_rays"](n)
        cuts = set()
        for s in range(1, 1 << n):
            if s & 1 and s != (1 << n) - 1:
                cuts.add(tuple(int(bool(s >> a & 1) != bool(s >> b & 1)) for a, b in edges))
        assert set(rays) == cuts
        rows = [tuple(int(a == b) for a in range(len(edges))) for b in range(len(edges))] + triangle_rows

        def zero_pattern(v):
            return sum(int(sum(x * y for x, y in zip(h, v)) == 0) << j for j, h in enumerate(rows))

        all_bits = (1 << len(rows)) - 1
        closure = {all_bits: (0,) * len(edges)}
        queue = deque([all_bits])
        while queue:
            z = queue.popleft()
            for ray in rays:
                w = z & zero_pattern(ray)
                if w not in closure:
                    v = tuple(a + b for a, b in zip(closure[z], ray))
                    assert zero_pattern(v) == w
                    closure[w] = v
                    queue.append(w)
        subsets = set()
        for mask in range(1 << len(rays)):
            v = tuple(sum(rays[i][j] for i in range(len(rays)) if mask >> i & 1) for j in range(len(edges)))
            subsets.add(zero_pattern(v))
        assert subsets == set(closure)
        stats[n].update(extreme_rays=len(rays), zero_patterns=len(closure), stage_counts=stages)
    return stats


def distances(adjacency):
    ans = []
    for start in range(len(adjacency)):
        d = [-1] * len(adjacency)
        d[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if d[v] == -1:
                    d[v] = d[u] + 1
                    queue.append(v)
        assert all(x >= 0 for x in d)
        ans.append(d)
    return ans


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return distances(adj)


def gp(d, selected):
    for a, b, c in combinations(selected, 3):
        u, v, w = d[a][b], d[a][c], d[b][c]
        if u + v == w or u + w == v or v + w == u:
            return False
    return True


def lower_gp(d):
    for size in range(len(d) + 1):
        for selected in combinations(range(len(d)), size):
            if gp(d, selected) and all(not gp(d, selected + (x,)) for x in range(len(d)) if x not in selected):
                return size
    raise AssertionError("finite maximality missing")


def profile(d, landmarks, x):
    bits = []
    for a, b in combinations(landmarks, 2):
        bits.extend((d[a][x] + d[x][b] == d[a][b],
                     d[x][a] + d[a][b] == d[x][b],
                     d[x][b] + d[b][a] == d[x][a]))
    zeros = sum(int(d[x][a] == 0) << i for i, a in enumerate(landmarks))
    return sum(int(v) << i for i, v in enumerate(bits)), zeros


def metric_profile_controls():
    k3 = graph(3, combinations(range(3), 2))
    path3 = graph(3, [(0, 1), (1, 2)])
    diamond = graph(4, [e for e in combinations(range(4), 2) if e != (2, 3)])
    bowtie = graph(5, list(combinations((0, 1, 2), 2)) + list(combinations((0, 3, 4), 2)))
    cycle4 = graph(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    singleton = graph(1, [])
    stats = dict(fixtures=0, gp_sets=0, extension_tests=0, repeated_projection_sets=0, factor_demands=0)
    for dg, dh in ((path3, k3), (diamond, bowtie), (cycle4, diamond), (singleton, k3), (k3, k3)):
        lg, lh = lower_gp(dg), lower_gp(dh)
        vertices = list(product(range(len(dg)), range(len(dh))))
        dp = [[dg[a][c] + dh[b][e] for c, e in vertices] for a, b in vertices]
        stats["fixtures"] += 1
        for size in range(1, min(4, len(vertices)) + 1):
            for selected in combinations(range(len(vertices)), size):
                if not gp(dp, selected):
                    continue
                stats["gp_sets"] += 1
                ag = tuple(vertices[i][0] for i in selected)
                ah = tuple(vertices[i][1] for i in selected)
                if len(set(ag)) < size or len(set(ah)) < size:
                    stats["repeated_projection_sets"] += 1
                for x, (a, b) in enumerate(vertices):
                    p, z = profile(dg, ag, a)
                    q, w = profile(dh, ah, b)
                    compatible = not (p & q) and not (z & w)
                    genuine_extension = x not in selected and gp(dp, selected + (x,))
                    assert compatible == genuine_extension
                    stats["extension_tests"] += 1
                for d, landmarks, low in ((dg, ag, lg), (dh, ah, lh)):
                    if size >= low:
                        continue
                    distinct = tuple(dict.fromkeys(landmarks))
                    for tsize in range(1, len(distinct) + 1):
                        for t in combinations(distinct, tsize):
                            if not gp(d, t) or any(gp(d, t + (u,)) for u in distinct if u not in t):
                                continue
                            assert any(gp(d, t + (x,)) for x in range(len(d)) if x not in distinct)
                            stats["factor_demands"] += 1
    return stats


def compatible(p, z, q, w):
    return not (p & q) and not (z & w)


def brute_infeasible(g, h):
    for xm in range(1 << len(g["P"])):
        if any(not (d & xm) for d in g["demands"]):
            continue
        gx = g["known"] + [(p, 0) for i, p in enumerate(g["P"]) if xm >> i & 1]
        for ym in range(1 << len(h["P"])):
            if any(not (d & ym) for d in h["demands"]):
                continue
            hy = h["known"] + [(q, 0) for i, q in enumerate(h["P"]) if ym >> i & 1]
            if all(not compatible(p, z, q, w) for p, z in gx for q, w in hy):
                return False
    return True


def search_controls():
    source = extract_function(WRITTEN / "verify_arbitrary_four.py", "infeasible")
    scope = dict(nodes=0, digest=hashlib.sha256())
    exec(compile(source, "<isolated-production-search-function>", "exec"), scope)
    rng = random.Random(20261012)

    def model():
        p = sorted(rng.sample(range(8), rng.randrange(1, 5)))
        return dict(P=p,
                    demands=[rng.randrange(1 << len(p)) for _ in range(rng.randrange(4))],
                    known=[(rng.randrange(8), rng.randrange(8)) for _ in range(rng.randrange(3))])

    for _ in range(2000):
        g, h = model(), model()
        wanted = brute_infeasible(g, h)
        assert scope["infeasible"](g, h) == wanted
        assert scope["infeasible"](h, g) == wanted
    return dict(synthetic_systems=2000, both_factor_orders_checked=True, production_states=scope["nodes"])


def hash_sources():
    paths = [FIXED / name for name in ("PROOF.md", "FAMILY_PROOF.md", "LowerGPProduct319.lean", "lean-audit.json", "lean-audit.log")]
    paths += [WRITTEN / name for name in ("UNIVERSAL_FIVE_PROOF.md", "UNBOUNDED_GAP_PROOF.md", "verify_metric_rays.py", "verify_arbitrary_four.py", "verify_universal_five.py", "metric_faces.json", "metric_rays_verified.json")]
    return {str(p.relative_to(REPO)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


if __name__ == "__main__":
    before = hash_sources()
    result = dict(status="PASS", utc=datetime.now(timezone.utc).isoformat(),
                  scope="Independent bounded controls only: MET3/MET4, small graph profiles and artificial Boolean systems. No MET5 full replay, no Lean compilation.",
                  reduced_cones=reduced_cone_controls(),
                  graph_profiles=metric_profile_controls(),
                  synthetic_search=search_controls(), source_sha256=before)
    assert hash_sources() == before
    result["source_unchanged_during_controls"] = True
    target = OUT / "independent_small_controls.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "source_sha256"}, indent=2))
