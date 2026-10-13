#!/usr/bin/env python3
"""Finite independent-state checks for the prefix-macro optimizer."""

import hashlib
import json
from pathlib import Path
import platform
import random
import time

from forced_segment_dp import solve, solve_edges
from sanity_check import all_graphs, replay, solve_rob


def check(deps, width, oracle=True, all_suffixes=False):
    result = solve(deps, width)
    n = len(deps)
    if oracle:
        optimum, _ = solve_rob(deps, width + 1, width)
        assert result["cycles"] == optimum
    times = [0] * n
    for cycle, action in enumerate(result["schedule"], 1):
        for job in action:
            assert times[job] == 0
            times[job] = cycle
    assert replay(deps, width + 1, width, times)
    assert result["stats"]["macro_arcs"] <= n * min(n, width + 1)
    assert result["stats"]["longest_macro"] <= n
    assert len(result["prefix_values"]) == n + 1
    assert result["prefix_values"][-1] == 0
    if all_suffixes:
        for i in range(n + 1):
            suffix = tuple(mask >> i for mask in deps[i:])
            assert result["prefix_values"][i] == solve_rob(suffix, width + 1, width)[0]
    return result


def run():
    started = time.perf_counter()
    complete_cases = 0
    complete_graphs = 0
    ranges = []
    for n in range(6):
        graph_count = 0
        for deps in all_graphs(n):
            graph_count += 1
            for width in range(1, n + 3):
                check(deps, width)
                complete_cases += 1
        complete_graphs += graph_count
        ranges.append({"N": n, "graphs": graph_count, "W_min": 1, "W_max": n + 2})

    seed = 20261014
    rng = random.Random(seed)
    random_cases = 0
    for n in (6, 8, 10, 12):
        for width in range(2, min(6, n) + 1):
            for probability in (0.1, 0.4, 0.8):
                deps = []
                for j in range(n):
                    selected = [i for i in range(j) if rng.random() < probability]
                    rng.shuffle(selected)
                    deps.append(sum(1 << i for i in selected[:2]))
                check(tuple(deps), width, all_suffixes=True)
                random_cases += 1

    # A forced segment can propagate a completed hole through several
    # windows; it is not always a two-cycle macro as at B=3,W=2.
    deps = (0, 0, 0, 0, 1 << 2, 0, 1 << 4, 0)
    propagated = check(deps, 3, all_suffixes=True)
    assert propagated["stats"]["longest_macro"] >= 4

    large_boundaries = []
    for width in (1, 2, 3, 17, 10 ** 12):
        n = 200
        independent = check((0,) * n, width, oracle=False)
        serial = check(tuple(0 if j == 0 else 1 << (j - 1) for j in range(n)),
                       width, oracle=False)
        assert independent["cycles"] == (n + width - 1) // width
        assert serial["cycles"] == n
        large_boundaries.append({"N": n, "W": width,
                                 "independent_cycles": independent["cycles"],
                                 "serial_cycles": serial["cycles"]})

    duplicate_edges = solve_edges(5, [(0, 3), (0, 3), (1, 4)], 3)
    simple_edges = solve_edges(5, [(0, 3), (1, 4)], 3)
    assert duplicate_edges["cycles"] == simple_edges["cycles"]
    invalid = 0
    for n, edges, width in ((-1, [], 2), (2, [], 0), (2, [(1, 0)], 1),
                             (2, [(0, 2)], 1), (1, [(0, 0)], 1)):
        try:
            solve_edges(n, edges, width)
        except ValueError:
            invalid += 1
        else:
            raise AssertionError("invalid problem was accepted")
    return {
        "status": "PASS", "python": platform.python_version(), "seed": seed,
        "complete_graph_ranges": ranges, "complete_graphs": complete_graphs,
        "complete_resource_cases": complete_cases,
        "random_binary_input_cases_with_all_suffix_values": random_cases,
        "long_forced_segment": {"deps": deps, "W": 3,
                                "cycles": propagated["cycles"],
                                "longest_macro": propagated["stats"]["longest_macro"]},
        "large_boundary_cases": large_boundaries,
        "duplicate_edge_check": "PASS", "invalid_input_rejections": invalid,
        "oracle": "independent full completed-state recursion over every nonempty ready subset",
        "certificates": "every returned schedule operationally replayed",
        "implementation_sha256": hashlib.sha256(Path(__file__).with_name("forced_segment_dp.py").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope": "finite implementation checks, separate from the arbitrary-size written proof"
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
