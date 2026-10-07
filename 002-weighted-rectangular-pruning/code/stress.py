"""Finite exact stress tests; their ranges do not assert the general theorem."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
from check_certificate import check
from solve import prepare, solve


def subset(mask, pairs):
    return [list(pair) for bit, pair in enumerate(pairs) if (mask >> bit) & 1]


def brute_cover_cost(raw):
    *_, edges, cost, _, _ = prepare(raw)
    nodes = sorted(cost)
    best = sum(cost.values(), Fraction(0))
    for mask in range(1 << len(nodes)):
        selected = {node for bit, node in enumerate(nodes) if (mask >> bit) & 1}
        if all(u in selected or v in selected for u, v in edges):
            best = min(best, sum((cost[node] for node in selected), Fraction(0)))
    return best


def exercise(raw, brute=False):
    cert = solve(raw)
    totals = check(cert)
    if brute:
        assert Fraction(totals["cover_cost"]) == brute_cover_cost(raw)
    return cert


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--small", action="store_true", help="skip exhaustive two-element inputs")
    options = parser.parse_args()
    counts = {}
    one = [(0, 0)]
    count = 0
    for masks in itertools.product(range(2), repeat=4):
        for values in itertools.product(range(3), repeat=4):
            raw = {"sizes": dict.fromkeys(("P", "I", "S", "J"), 1),
                   **{key: subset(mask, one) for key, mask in zip(("E", "F", "R", "C"), masks)},
                   "weights": {key: [str(value)] for key, value in zip("abcd", values)}}
            exercise(raw, brute=True)
            count += 1
    counts["all_one_element_relations_and_weights_0_1_2"] = count

    # Every one of the four 2-by-2 relation/family matrices is unrestricted.
    if not options.small:
        two = list(itertools.product(range(2), repeat=2))
        count = 0
        for masks in itertools.product(range(16), repeat=4):
            raw = {"sizes": dict.fromkeys(("P", "I", "S", "J"), 2),
                   **{key: subset(mask, two) for key, mask in zip(("E", "F", "R", "C"), masks)},
                   "weights": {key: ["1", "1"] for key in "abcd"}}
            exercise(raw)
            count += 1
        counts["all_two_element_relations_unit_weights"] = count

    rng = random.Random(20261008)
    for _ in range(300):
        dimensions = {key: rng.randrange(4) for key in ("P", "I", "S", "J")}
        raw = {"sizes": dimensions}
        for key, domains in {"E": ("P", "I"), "F": ("S", "J"),
                             "R": ("P", "J"), "C": ("I", "S")}.items():
            raw[key] = [list(pair) for pair in itertools.product(*(range(dimensions[d]) for d in domains))
                        if rng.randrange(2)]
        raw["weights"] = {key: [str(Fraction(rng.randrange(6), rng.randrange(1, 6)))
                                for _ in range(dimensions[domain])]
                          for key, domain in zip("abcd", ("P", "I", "S", "J"))}
        exercise(raw)
    counts["fixed_seed_rational_and_empty_domain_inputs"] = 300

    sharp = {"sizes": dict.fromkeys(("P", "I", "S", "J"), 1),
             **{key: [[0, 0]] for key in ("E", "F", "R", "C")},
             "weights": {key: ["1"] for key in "abcd"}}
    valid = exercise(sharp, brute=True)
    invalid = []
    changed = copy.deepcopy(valid)
    changed["cover"] = []
    invalid.append(changed)
    changed = copy.deepcopy(valid)
    changed["flow"] = changed["flow"][:-1]
    invalid.append(changed)
    changed = copy.deepcopy(valid)
    changed["flow"][0]["flow"] = changed["flow"][0]["capacity"] + 1
    invalid.append(changed)
    changed = copy.deepcopy(valid)
    changed["instance"]["weights"]["a"][0] = "-1"
    invalid.append(changed)
    changed = copy.deepcopy(valid)
    changed["H"] = []
    invalid.append(changed)
    changed = copy.deepcopy(valid)
    changed["retained_R"] = [] if changed["retained_R"] else [[0, 0]]
    invalid.append(changed)
    changed = copy.deepcopy(valid)
    changed["totals"]["cover_cost"] = "123"
    invalid.append(changed)
    changed = copy.deepcopy(valid)
    changed["scale"] = 0
    invalid.append(changed)
    for bad in invalid:
        try:
            check(bad)
        except (ValueError, KeyError, TypeError, ZeroDivisionError):
            continue
        raise AssertionError("checker accepted a mutated certificate")
    counts["mutated_certificates_rejected"] = len(invalid)
    print(json.dumps({"status": "PASS", "counts": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
