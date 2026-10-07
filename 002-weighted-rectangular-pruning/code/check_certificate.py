"""Independent exact checker. Does not import the solver or run a flow search."""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pair_array(value, shape=None):
    require(isinstance(value, list), "pair array must be a list")
    pairs = []
    for item in value:
        require(isinstance(item, list) and len(item) == 2, "invalid pair")
        require(all(type(x) is int for x in item), "pair entries must be integers")
        if shape is not None:
            require(0 <= item[0] < shape[0] and 0 <= item[1] < shape[1], "pair outside domain")
        pairs.append(tuple(item))
    require(len(set(pairs)) == len(pairs), "duplicate pair")
    return set(pairs)


def vertex(tag, x, y):
    return f"{tag}:{x}:{y}"


def check(cert):
    require(cert.get("schema") == 1, "unknown certificate schema")
    raw = cert["instance"]
    dims = raw["sizes"]
    require(set(dims) == {"P", "I", "S", "J"}, "incorrect dimensions")
    require(all(type(n) is int and n >= 0 for n in dims.values()), "invalid dimensions")
    e_pairs = pair_array(raw["E"], (dims["P"], dims["I"]))
    f_pairs = pair_array(raw["F"], (dims["S"], dims["J"]))
    r_pairs = pair_array(raw["R"], (dims["P"], dims["J"]))
    c_pairs = pair_array(raw["C"], (dims["I"], dims["S"]))
    wt = {}
    for letter, domain in (("a", "P"), ("b", "I"), ("c", "S"), ("d", "J")):
        arr = raw["weights"][letter]
        require(isinstance(arr, list) and len(arr) == dims[domain], "bad weight array")
        require(all(type(x) is str for x in arr), "weights must be rational strings")
        wt[letter] = [Fraction(x) for x in arr]
        require(all(x >= 0 for x in wt[letter]), "negative weight")

    # Derive all corners and graph edges from raw relations, not certificate lists.
    z_points, h_points, graph_edges = set(), set(), set()
    conflicting_r, conflicting_c = set(), set()
    for p, j in r_pairs:
        for i, s in c_pairs:
            if (p, i) in e_pairs and (s, j) in f_pairs:
                z_points.add((i, j))
                h_points.add((p, s))
                conflicting_r.add((p, j))
                conflicting_c.add((i, s))
                graph_edges.add((vertex("R", p, j), vertex("C", i, s)))
    for i, j in z_points:
        for p, jj in r_pairs:
            if jj == j and (p, i) in e_pairs:
                graph_edges.add((vertex("R", p, j), vertex("ZR", i, j)))
        for ii, s in c_pairs:
            if ii == i and (s, j) in f_pairs:
                graph_edges.add((vertex("ZL", i, j), vertex("C", i, s)))
    require(pair_array(cert["H"]) == h_points, "incorrect H")
    require(pair_array(cert["Z"]) == z_points, "incorrect Z")

    costs = {}
    left, right = set(), set()
    for p, j in r_pairs:
        node = vertex("R", p, j)
        left.add(node)
        costs[node] = wt["a"][p] * wt["d"][j]
    for i, s in c_pairs:
        node = vertex("C", i, s)
        right.add(node)
        costs[node] = wt["b"][i] * wt["c"][s]
    for i, j in z_points:
        lv, rv = vertex("ZL", i, j), vertex("ZR", i, j)
        left.add(lv)
        right.add(rv)
        costs[lv] = costs[rv] = wt["b"][i] * wt["d"][j]
    scale = 1
    for amount in costs.values():
        scale = math.lcm(scale, amount.denominator)
    require(type(cert["scale"]) is int and cert["scale"] == scale, "incorrect scale")
    large_capacity = int(sum(costs.values(), Fraction(0)) * scale) + 1
    network = {("_source", node): int(costs[node] * scale) for node in left}
    network.update({(node, "_sink"): int(costs[node] * scale) for node in right})
    network.update({edge: large_capacity for edge in graph_edges})

    require(isinstance(cert["cover"], list) and all(type(x) is str for x in cert["cover"]), "invalid cover")
    cover = set(cert["cover"])
    require(len(cover) == len(cert["cover"]) and cover <= set(costs), "invalid or duplicate cover vertex")
    incident = {node for edge in graph_edges for node in edge}
    require(cover <= incident, "isolated vertex in cover")
    require(all(u in cover or v in cover for u, v in graph_edges), "uncovered graph edge")
    cover_cost = sum((costs[node] for node in cover), Fraction(0))

    # Independently check a feasible flow and the matching upper/lower certificates.
    require(isinstance(cert["flow"], list), "flow must be an array")
    seen = set()
    balance = {node: 0 for node in set(costs) | {"_source", "_sink"}}
    for arc in cert["flow"]:
        edge = (arc["u"], arc["v"])
        require(edge in network and edge not in seen, "unexpected or duplicate network arc")
        require(type(arc["capacity"]) is int and arc["capacity"] == network[edge], "incorrect capacity")
        amount = arc["flow"]
        require(type(amount) is int and 0 <= amount <= network[edge], "flow outside capacity")
        seen.add(edge)
        balance[edge[0]] -= amount
        balance[edge[1]] += amount
    require(seen == set(network), "missing network arc")
    require(all(balance[node] == 0 for node in costs), "flow conservation failed")
    flow_value = balance["_sink"]
    require(flow_value >= 0 and balance["_source"] == -flow_value, "bad terminal balance")
    require(Fraction(flow_value, scale) == cover_cost, "flow value differs from cover cost")

    kept_r = {(p, j) for p, j in r_pairs if vertex("R", p, j) not in cover}
    kept_c = {(i, s) for i, s in c_pairs if vertex("C", i, s) not in cover}
    require(pair_array(cert["retained_R"]) == kept_r, "incorrect retained R")
    require(pair_array(cert["retained_C"]) == kept_c, "incorrect retained C")
    require(r_pairs - conflicting_r <= kept_r and c_pairs - conflicting_c <= kept_c,
            "initially conflict-free member was removed")
    require(not any((p, i) in e_pairs and (s, j) in f_pairs
                    for p, j in kept_r for i, s in kept_c), "conflict survives")
    uncovered = set()
    for i, j in z_points:
        covered = any(jj == j and (p, i) in e_pairs for p, jj in kept_r)
        covered |= any(ii == i and (s, j) in f_pairs for ii, s in kept_c)
        if not covered:
            uncovered.add((i, j))
    require(pair_array(cert["uncovered_Z"]) == uncovered, "incorrect uncovered set")
    h_mass = sum((wt["a"][p] * wt["c"][s] for p, s in h_points), Fraction(0))
    z_mass = sum((wt["b"][i] * wt["d"][j] for i, j in z_points), Fraction(0))
    u_mass = sum((wt["b"][i] * wt["d"][j] for i, j in uncovered), Fraction(0))
    deletion = sum((wt["a"][p] * wt["d"][j] for p, j in r_pairs - kept_r), Fraction(0))
    deletion += sum((wt["b"][i] * wt["c"][s] for i, s in c_pairs - kept_c), Fraction(0))
    require(cover_cost <= h_mass + z_mass, "weighted cover bound failed")
    require(deletion <= h_mass + u_mass, "weighted pruning bound failed")
    calculated = {"cover_cost": str(cover_cost), "H_mass": str(h_mass),
                  "Z_mass": str(z_mass), "deletion_cost": str(deletion),
                  "uncovered_mass": str(u_mass), "flow_value": str(Fraction(flow_value, scale))}
    require(cert["totals"] == calculated, "incorrect printed totals")
    return calculated


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python check_certificate.py CERTIFICATE.json")
    try:
        with open(sys.argv[1], encoding="utf-8") as handle:
            totals = check(json.load(handle))
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as error:
        raise SystemExit(f"REJECT: {error}") from error
    print("ACCEPT: exact feasible flow, equal-cost cover, cover and pruning bounds")
    print(json.dumps(totals, sort_keys=True))


if __name__ == "__main__":
    main()
