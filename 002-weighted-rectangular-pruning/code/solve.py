"""Exact product-weighted rectangular cover and pruning certificates.

Standard library only. This is a search program, not the independent checker.
"""

from __future__ import annotations

import json
import math
import sys
from collections import deque
from fractions import Fraction


def load_instance(raw):
    sizes = raw["sizes"]
    if set(sizes) != {"P", "I", "S", "J"}:
        raise ValueError("sizes must specify exactly P, I, S, J")
    for size in sizes.values():
        if type(size) is not int or size < 0:
            raise ValueError("coordinate sizes must be nonnegative integers")
    shape = {"E": ("P", "I"), "F": ("S", "J"),
             "R": ("P", "J"), "C": ("I", "S")}
    sets = {}
    for name, (first, second) in shape.items():
        pairs = raw[name]
        if not isinstance(pairs, list):
            raise ValueError(f"{name} must be an array")
        for pair in pairs:
            if not isinstance(pair, list) or len(pair) != 2:
                raise ValueError(f"bad pair in {name}")
            if any(type(x) is not int for x in pair):
                raise ValueError("coordinates must be integers")
            if not (0 <= pair[0] < sizes[first] and
                    0 <= pair[1] < sizes[second]):
                raise ValueError(f"out-of-domain pair in {name}")
        sets[name] = set(map(tuple, pairs))
        if len(sets[name]) != len(pairs):
            raise ValueError(f"duplicate pair in {name}")
    weights = {}
    for name, domain in zip("abcd", ("P", "I", "S", "J")):
        entries = raw["weights"][name]
        if len(entries) != sizes[domain] or any(type(x) is not str for x in entries):
            raise ValueError("weight arrays must contain rational strings")
        weights[name] = [Fraction(x) for x in entries]
        if any(x < 0 for x in weights[name]):
            raise ValueError("weights must be nonnegative")
    return sets, weights


def name(tag, pair):
    return f"{tag}:{pair[0]}:{pair[1]}"


def prepare(raw):
    sets, weights = load_instance(raw)
    E, F, R, C = (sets[x] for x in ("E", "F", "R", "C"))
    conflicts = [(r, c) for r in sorted(R) for c in sorted(C)
                 if (r[0], c[0]) in E and (c[1], r[1]) in F]
    Z = {(c[0], r[1]) for r, c in conflicts}
    H = {(r[0], c[1]) for r, c in conflicts}
    a, b, c, d = (weights[x] for x in "abcd")
    cost = {name("R", (p, j)): a[p] * d[j] for p, j in R}
    cost.update({name("C", (i, s)): b[i] * c[s] for i, s in C})
    for z in Z:
        for tag in ("ZL", "ZR"):
            cost[name(tag, z)] = b[z[0]] * d[z[1]]
    left = sorted([name("R", r) for r in R] + [name("ZL", z) for z in Z])
    right = sorted([name("C", cc) for cc in C] + [name("ZR", z) for z in Z])
    edges = [(name("R", r), name("C", cc)) for r, cc in conflicts]
    edges.extend((name("R", r), name("ZR", z))
                 for r in sorted(R) for z in sorted(Z)
                 if r[1] == z[1] and (r[0], z[0]) in E)
    edges.extend((name("ZL", z), name("C", cc))
                 for z in sorted(Z) for cc in sorted(C)
                 if z[0] == cc[0] and (cc[1], z[1]) in F)
    scale = 1
    for w in cost.values():
        scale = math.lcm(scale, w.denominator)
    total = sum(cost.values(), Fraction(0)) * scale
    assert total.denominator == 1
    large = total.numerator + 1
    arcs = [("_source", v, int(cost[v] * scale)) for v in left]
    arcs += [(v, "_sink", int(cost[v] * scale)) for v in right]
    arcs += [(u, v, large) for u, v in sorted(edges)]
    return sets, weights, Z, H, left, right, edges, cost, scale, arcs


def max_flow(arcs):
    graph = {}
    original = []

    def add(u, v, cap):
        graph.setdefault(u, [])
        graph.setdefault(v, [])
        forward = [v, cap, len(graph[v])]
        backward = [u, 0, len(graph[u])]
        graph[u].append(forward)
        graph[v].append(backward)
        original.append((u, len(graph[u]) - 1, cap))

    graph.setdefault("_source", [])
    graph.setdefault("_sink", [])
    for u, v, cap in arcs:
        add(u, v, cap)
    value = 0
    while True:
        parent = {"_source": None}
        queue = deque(["_source"])
        while queue and "_sink" not in parent:
            u = queue.popleft()
            for index, (v, cap, _) in enumerate(graph[u]):
                if cap > 0 and v not in parent:
                    parent[v] = (u, index)
                    queue.append(v)
        if "_sink" not in parent:
            reached = set(parent)
            break
        cap = None
        v = "_sink"
        while parent[v] is not None:
            u, index = parent[v]
            residual = graph[u][index][1]
            cap = residual if cap is None else min(cap, residual)
            v = u
        v = "_sink"
        while parent[v] is not None:
            u, index = parent[v]
            reverse = graph[u][index][2]
            graph[u][index][1] -= cap
            graph[v][reverse][1] += cap
            v = u
        value += cap
    flows = [cap - graph[u][index][1] for u, index, cap in original]
    return value, reached, flows


def solve(raw):
    (sets, weights, Z, H, left, right, edges, cost,
     scale, arcs) = prepare(raw)
    value, reached, flows = max_flow(arcs)
    incident = {v for edge in edges for v in edge}
    cover = ({v for v in left if v not in reached} |
             {v for v in right if v in reached}) & incident
    R_keep = {r for r in sets["R"] if name("R", r) not in cover}
    C_keep = {cc for cc in sets["C"] if name("C", cc) not in cover}
    uncovered = {z for z in Z
                 if not any(r[1] == z[1] and (r[0], z[0]) in sets["E"]
                            for r in R_keep)
                 and not any(cc[0] == z[0] and (cc[1], z[1]) in sets["F"]
                             for cc in C_keep)}
    a, b, c, d = (weights[x] for x in "abcd")
    h_mass = sum((a[p] * c[s] for p, s in H), Fraction(0))
    z_mass = sum((b[i] * d[j] for i, j in Z), Fraction(0))
    u_mass = sum((b[i] * d[j] for i, j in uncovered), Fraction(0))
    cover_cost = sum((cost[v] for v in cover), Fraction(0))
    deletion = sum((cost[name("R", r)] for r in sets["R"] - R_keep), Fraction(0))
    deletion += sum((cost[name("C", cc)] for cc in sets["C"] - C_keep), Fraction(0))
    assert cover_cost == Fraction(value, scale)
    assert cover_cost <= h_mass + z_mass
    assert deletion <= h_mass + u_mass
    return {
        "schema": 1, "instance": raw, "scale": scale,
        "cover": sorted(cover),
        "retained_R": [list(x) for x in sorted(R_keep)],
        "retained_C": [list(x) for x in sorted(C_keep)],
        "H": [list(x) for x in sorted(H)],
        "Z": [list(x) for x in sorted(Z)],
        "uncovered_Z": [list(x) for x in sorted(uncovered)],
        "flow": [{"u": u, "v": v, "capacity": cap, "flow": flow}
                 for (u, v, cap), flow in zip(arcs, flows)],
        "totals": {"cover_cost": str(cover_cost), "H_mass": str(h_mass),
                   "Z_mass": str(z_mass), "deletion_cost": str(deletion),
                   "uncovered_mass": str(u_mass), "flow_value": str(Fraction(value, scale))},
    }


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python solve.py INPUT.json CERTIFICATE.json")
    with open(sys.argv[1], encoding="utf-8") as handle:
        certificate = solve(json.load(handle))
    with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as handle:
        json.dump(certificate, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(certificate["totals"], sort_keys=True))


if __name__ == "__main__":
    main()
