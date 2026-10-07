"""Exact, standalone checker of the positive nonproduct boundary example."""

from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(raw):
    require(raw.get("format") == "nonproduct-single-rectangle-v1", "unexpected format")
    systems = raw["coordinate_weight_systems"]
    require(isinstance(systems, list) and len(systems) == 2, "expected two product systems")
    summed = dict.fromkeys(("R", "C", "H", "Z"), Fraction(0))
    for component in systems:
        require(set(component) == set("abcd"), "invalid coordinate weights")
        require(all(type(x) is str for x in component.values()), "weights must be rational strings")
        a, b, c, d = (Fraction(component[key]) for key in "abcd")
        require(min(a, b, c, d) > 0, "component weights must be strictly positive")
        pairs = {"R": a * d, "C": b * c, "H": a * c, "Z": b * d}
        for key, value in pairs.items():
            summed[key] += value
        require(min(pairs["R"] + pairs["C"], pairs["R"] + pairs["Z"],
                    pairs["C"] + pairs["Z"]) <= pairs["H"] + pairs["Z"],
                "component does not satisfy cover bound")
    require({key: str(value) for key, value in summed.items()} == raw["claimed_pair_costs"],
            "claimed pair costs disagree with the two product systems")
    cost = {"r": summed["R"], "c": summed["C"], "zl": summed["Z"], "zr": summed["Z"]}
    edges = {("r", "c"), ("r", "zr"), ("zl", "c")}
    nodes = ("r", "c", "zl", "zr")
    covers = []
    for flags in itertools.product((False, True), repeat=4):
        selected = {node for node, flag in zip(nodes, flags) if flag}
        if all(u in selected or v in selected for u, v in edges):
            amount = sum((cost[node] for node in selected), Fraction(0))
            covers.append({"cover": sorted(selected), "cost": str(amount)})
    minimum = min(Fraction(entry["cost"]) for entry in covers)
    proposed_cover_bound = summed["H"] + summed["Z"]
    threshold = min(summed["R"], summed["C"], summed["R"] + summed["C"] - summed["Z"])
    require(summed["H"] < threshold, "single-conflict classification predicts feasibility")
    require(minimum - summed["Z"] == threshold, "cover/pruning classification mismatch")
    require(minimum == Fraction(121, 100), "unexpected minimum cover value")
    require(proposed_cover_bound == Fraction(2, 5) and minimum > proposed_cover_bound,
            "cover obstruction failed")

    large = sum(cost.values(), Fraction(0)) + 1
    capacity = {"source->r": cost["r"], "source->zl": cost["zl"],
                "c->sink": cost["c"], "zr->sink": cost["zr"],
                "r->c": large, "r->zr": large, "zl->c": large}
    require(set(raw["flow"]) == set(capacity), "flow has unexpected or missing arcs")
    balance = dict.fromkeys((*nodes, "source", "sink"), Fraction(0))
    for arc, limit in capacity.items():
        require(type(raw["flow"][arc]) is str, "flows must be rational strings")
        amount = Fraction(raw["flow"][arc])
        require(0 <= amount <= limit, "flow outside capacity")
        u, v = arc.split("->")
        balance[u] -= amount
        balance[v] += amount
    require(all(balance[node] == 0 for node in nodes), "flow conservation failed")
    require(balance["sink"] == -balance["source"] == minimum, "incorrect flow value")

    prunings = []
    for delete_r, delete_c in itertools.product((False, True), repeat=2):
        if not (delete_r or delete_c):
            continue  # the original conflict survives
        deletion = (cost["r"] if delete_r else 0) + (cost["c"] if delete_c else 0)
        uncovered = delete_r and delete_c
        bound = summed["H"] + (summed["Z"] if uncovered else 0)
        require(deletion > bound, "a feasible pruning satisfies the proposed bound")
        prunings.append({"deleted": [node for node, flag in (("r", delete_r), ("c", delete_c)) if flag],
                         "deletion_cost": str(deletion), "uncovered": uncovered, "bound": str(bound)})
    require(len(prunings) == 3, "incomplete pruning enumeration")
    return {"status": "PASS", "minimum_cover": str(minimum),
            "flow_value": str(balance["sink"]), "proposed_cover_bound": str(proposed_cover_bound),
            "single_conflict_H_threshold": str(threshold),
            "all_covers": covers, "all_feasible_prunings": prunings}


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python check_nonproduct.py NONPRODUCT.json")
    try:
        with open(sys.argv[1], encoding="utf-8") as handle:
            result = check(json.load(handle))
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as error:
        raise SystemExit(f"REJECT: {error}") from error
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
