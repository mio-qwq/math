"""Exact finite-threshold construction for compatible nonproduct pair costs.

Standard library only. The independent checker does not import this module.
One coordinate relation must be a disjoint union of complete bipartite blocks.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(raw):
    require(raw.get("format") == "compatible-pair-costs-v1", "unknown input format")
    dims = raw["sizes"]
    require(set(dims) == {"P", "I", "S", "J"}, "incorrect dimensions")
    require(all(type(v) is int and v >= 0 for v in dims.values()), "invalid size")
    shapes = {"E": ("P", "I"), "F": ("S", "J"), "R": ("P", "J"),
              "C": ("I", "S"), "H": ("P", "S"), "Z": ("I", "J")}
    sets = {}
    for name in ("E", "F", "R", "C"):
        data = raw[name]
        require(isinstance(data, list), "pairs must be arrays")
        a, b = shapes[name]
        for v in data:
            require(isinstance(v, list) and len(v) == 2 and
                    all(type(k) is int for k in v), "invalid pair")
            require(0 <= v[0] < dims[a] and 0 <= v[1] < dims[b], "pair out of domain")
        sets[name] = set(map(tuple, data))
        require(len(sets[name]) == len(data), "duplicate pair")
    require(set(raw["costs"]) == {"R", "C", "H", "Z"}, "incorrect cost keys")
    costs = {}
    for name in ("R", "C", "H", "Z"):
        a, b = shapes[name]
        mat = raw["costs"][name]
        require(isinstance(mat, list) and len(mat) == dims[a], "bad cost rows")
        require(all(isinstance(row, list) and len(row) == dims[b] for row in mat),
                "bad cost columns")
        require(all(type(v) is str for row in mat for v in row), "costs need rational strings")
        costs[name] = [[Q(v) for v in row] for row in mat]
        require(all(v >= 0 for row in costs[name] for v in row), "negative cost")
    return dims, sets, costs


def blocks(relation):
    """Return complete connected blocks, or None for an unsupported relation."""
    graph = {}
    for a, b in relation:
        u, v = (0, a), (1, b)
        graph.setdefault(u, set()).add(v)
        graph.setdefault(v, set()).add(u)
    remaining, result = set(graph), []
    while remaining:
        seed = min(remaining)
        component, pending = {seed}, [seed]
        while pending:
            u = pending.pop()
            for v in graph[u] - component:
                component.add(v)
                pending.append(v)
        remaining -= component
        left = {v for side, v in component if side == 0}
        right = {v for side, v in component if side == 1}
        if any((a, b) not in relation for a in left for b in right):
            return None
        result.append((left, right))
    return result


def vertex(tag, pair):
    return f"{tag}:{pair[0]}:{pair[1]}"


def corners(sets):
    E, F, R, C = (sets[k] for k in ("E", "F", "R", "C"))
    conflicts = [(r, c) for r in sorted(R) for c in sorted(C)
                 if (r[0], c[0]) in E and (c[1], r[1]) in F]
    H = {(r[0], c[1]) for r, c in conflicts}
    Z = {(c[0], r[1]) for r, c in conflicts}
    return conflicts, H, Z


def threshold_cover(sets, cost, block_list):
    conflicts, H, Z = corners(sets)
    for (p, j), (i, s) in conflicts:
        require(cost["R"][p][j] * cost["C"][i][s] <=
                cost["H"][p][s] * cost["Z"][i][j], "local product constraint failed")
    weights = {vertex(tag, pair): cost[tag][pair[0]][pair[1]]
               for tag in ("R", "C") for pair in sets[tag]}
    for z in Z:
        weights[vertex("ZL", z)] = weights[vertex("ZR", z)] = cost["Z"][z[0]][z[1]]
    cover, trace = set(), []
    for S0, J0 in block_list:
        rg = {p: {r for r in sets["R"] if r[0] == p and r[1] in J0}
              for p, j in sets["R"] if j in J0}
        cg = {i: {c for c in sets["C"] if c[0] == i and c[1] in S0}
              for i, s in sets["C"] if s in S0}
        edges = {(p, i) for p, i in sets["E"] if p in rg and i in cg}
        ps, indices = {p for p, i in edges}, {i for p, i in edges}
        hp = {p: sum((cost["H"][p][s] for pp, s in H if pp == p and s in S0), Q(0))
              for p in ps}
        zi = {i: {z for z in Z if z[0] == i and z[1] in J0} for i in indices}
        zcost = {i: sum((cost["Z"][a][j] for a, j in zi[i]), Q(0)) for i in indices}
        xp = {p: sum((cost["R"][a][j] for a, j in rg[p]), Q(0)) for p in ps}
        yi = {i: sum((cost["C"][a][s] for a, s in cg[i]), Q(0)) for i in indices}
        alpha = {p: Q(0) if xp[p] == 0 else None if hp[p] == 0 else xp[p] / hp[p]
                 for p in ps}  # None denotes positive infinity.
        thresholds = sorted({Q(1)} | {v for v in alpha.values() if v is not None and v > 1})
        candidates = []
        for t in thresholds:
            chosen_p = {p for p in ps if alpha[p] is not None and alpha[p] <= t}
            qset = {i for p, i in edges if p not in chosen_p}
            selected = {vertex("R", r) for p in chosen_p for r in rg[p]}
            for i in indices:
                if i in qset:
                    selected |= {vertex("C", c) for c in cg[i]}
                    selected |= {vertex("ZR", z) for z in zi[i]}
                elif yi[i] <= zcost[i]:
                    selected |= {vertex("C", c) for c in cg[i]}
                else:
                    selected |= {vertex("ZL", z) for z in zi[i]}
            amount = sum((weights[v] for v in selected), Q(0))
            candidates.append((amount, t, selected))
        amount, t, selected = min(candidates, key=lambda v: (v[0], v[1]))
        require(amount <= sum(hp.values(), Q(0)) + sum(zcost.values(), Q(0)),
                "threshold construction failed its bound")
        cover |= selected
        trace.append({"block_left": sorted(S0), "block_right": sorted(J0), "threshold": str(t),
                      "candidate_count": len(thresholds), "cover_cost": str(amount)})
    return cover, trace


def transpose(sets, cost):
    transposed = {"E": {(s, j) for s, j in sets["F"]},
                  "F": {(p, i) for p, i in sets["E"]},
                  "R": {(s, i) for i, s in sets["C"]},
                  "C": {(j, p) for p, j in sets["R"]}}
    # Explicit dimensions handle empty matrices without relying on zip(*matrix).
    def tr(mat, width):
        return [[mat[a][b] for a in range(len(mat))] for b in range(width)]
    return transposed, tr


def solve(raw):
    dims, sets, cost = load(raw)
    fblocks, eblocks = blocks(sets["F"]), blocks(sets["E"])
    require(fblocks is not None or eblocks is not None, "neither relation has complete blocks")
    if fblocks is not None:
        cover, trace = threshold_cover(sets, cost, fblocks)
        structured = "F"
    else:
        swapped, tr = transpose(sets, cost)
        scost = {"R": tr(cost["C"], dims["S"]), "C": tr(cost["R"], dims["J"]),
                 "H": tr(cost["H"], dims["S"]), "Z": tr(cost["Z"], dims["J"])}
        temp, trace = threshold_cover(swapped, scost, eblocks)
        tagmap = {"R": "C", "C": "R", "ZL": "ZR", "ZR": "ZL"}
        cover = set()
        for v in temp:
            tag, a, b = v.split(":")
            cover.add(f"{tagmap[tag]}:{b}:{a}")
        structured = "E"
    _, H, Z = corners(sets)
    keep_r = {r for r in sets["R"] if vertex("R", r) not in cover}
    keep_c = {c for c in sets["C"] if vertex("C", c) not in cover}
    uncovered = {z for z in Z if not any(r[1] == z[1] and (r[0], z[0]) in sets["E"] for r in keep_r)
                 and not any(c[0] == z[0] and (c[1], z[1]) in sets["F"] for c in keep_c)}
    def total(tag, points):
        return sum((cost[tag][a][b] for a, b in points), Q(0))
    deletion = total("R", sets["R"] - keep_r) + total("C", sets["C"] - keep_c)
    cover_amount = deletion + sum((cost["Z"][int(v.split(":")[1])][int(v.split(":")[2])]
                                   for v in cover if v.startswith(("ZL:", "ZR:"))), Q(0))
    return {"schema": "compatible-pair-costs-certificate-v1", "instance": raw,
            "structured_relation": structured, "cover": sorted(cover),
            "retained_R": [list(r) for r in sorted(keep_r)],
            "retained_C": [list(c) for c in sorted(keep_c)],
            "uncovered": [list(z) for z in sorted(uncovered)],
            "claims": {"H_mass": str(total("H", H)), "Z_mass": str(total("Z", Z)),
                       "cover_cost": str(cover_amount), "deletion_cost": str(deletion),
                       "uncovered_mass": str(total("Z", uncovered))},
            "construction_trace": trace}


def main():
    require(len(sys.argv) in (2, 3), "usage: compatible_pair_costs.py INPUT [OUTPUT]")
    with open(sys.argv[1], encoding="utf-8") as stream:
        raw = json.load(stream)
    if raw.get("format") == "compatible-pair-costs-example-suite-v1":
        result = {"format": raw["format"], "cases": [
            {"name": item["name"], "certificate": solve(item["certificate"]["instance"])}
            for item in raw["cases"]]}
    else:
        result = solve(raw)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if len(sys.argv) == 3:
        with open(sys.argv[2], "w", encoding="utf-8") as stream:
            stream.write(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
