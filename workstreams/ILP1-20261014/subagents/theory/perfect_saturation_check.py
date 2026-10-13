#!/usr/bin/env python3
"""Cross-check perfect saturation against full completed-set optimization."""

from pathlib import Path
import hashlib
import json
import platform
import random
import time

from perfect_saturation import analyse, analyse_edges
from sanity_check import replay, solve_rob
from wider_policy_search import local_graph


def check(deps, width):
    result = analyse(deps, width)
    optimum, _ = solve_rob(deps, width + 1, width)
    assert result["feasible"] == (optimum * width == len(deps))
    if result["feasible"]:
        times = [0] * len(deps)
        for cycle, action in enumerate(result["schedule"], 1):
            assert len(action) == width
            for job in action:
                assert times[job] == 0
                times[job] = cycle
        assert len(result["schedule"]) == len(deps) // width
        assert replay(deps, width + 1, width, times)
    else:
        lo, hi = result["obstruction_component"]
        assert (hi - lo) % 2 == 1
        assert lo == 0 or not result["double_legal"][lo - 1]
        assert hi == len(result["single_legal"]) or not result["double_legal"][hi - 1]
        assert all(result["double_legal"][j] for j in range(lo, hi - 1))
        assert all(not result["single_legal"][j] for j in range(lo, hi, 2))
        cert = result["negative_certificate"]
        assert cert["first_block"] == lo and cert["past_last_block"] == hi
        assert [j for j, _, _ in cert["forbidden_singletons"]] == list(range(lo, hi, 2))
        for j, u, v in cert["forbidden_singletons"]:
            assert deps[v] >> u & 1 and u // width == j == v // width
        for side, expected in (("left_boundary", None if lo == 0 else lo - 1),
                               ("right_boundary", None if hi * width == len(deps) else hi - 1)):
            witness = cert[side]
            if expected is None:
                assert witness is None
            else:
                j, u, v = witness
                assert j == expected and deps[v] >> u & 1
                first = list(range(j * width, (j + 1) * width))
                second = list(range((j + 1) * width, (j + 2) * width))
                first[-1], second[0] = second[0], first[-1]
                issue_cycle = {x: c for c, action in enumerate((first, second)) for x in action}
                assert issue_cycle[u] >= issue_cycle[v]
    return result["feasible"]


def run():
    start = time.perf_counter()
    seed = 20261014
    rng = random.Random(seed)
    cases = []
    total = positives = 0
    for n in range(1, 7):
        for width in range(2, n + 1):
            if n % width:
                continue
            bits = sum(min(j, width) for j in range(n))
            count = 0
            for mask in range(1 << bits):
                deps = local_graph(n, mask, width + 1)
                positives += check(deps, width)
                total += 1
                count += 1
            cases.append({"N": n, "W": width, "effective_graphs": count})

    boundary = 0
    for width in range(1, 8):
        assert check((), width)
        boundary += 1
    for n in range(1, 13):
        assert check(tuple(0 for _ in range(n)), 1)
        assert check(tuple(0 if j == 0 else 1 << (j - 1) for j in range(n)), 1)
        boundary += 2

    random_cases = 0
    for width in range(2, 7):
        for blocks in (2, 3, 4):
            for probability in (0.1, 0.3, 0.6):
                for _ in range(2):
                    n = width * blocks
                    deps = tuple(sum(1 << i for i in range(j)
                                     if rng.random() < probability) for j in range(n))
                    check(deps, width)
                    edges = [(i, j) for j in range(n) for i in range(j) if deps[j] >> i & 1]
                    assert analyse_edges(n, edges, width) == analyse(deps, width)
                    random_cases += 1

    # Force a legal double macro while both individual blocks are illegal.
    forced_swaps = 0
    for width in range(2, 21):
        n = 2 * width
        deps = [0] * n
        deps[width - 1] = 1
        deps[2 * width - 1] = 1 << width
        result = analyse(deps, width)
        assert result["feasible"] and result["tiles"] == ((0, 2),)
        times = [0] * n
        for cycle, action in enumerate(result["schedule"], 1):
            for j in action:
                times[j] = cycle
        assert replay(deps, width + 1, width, times)
        forced_swaps += 1

    errors = 0
    for deps, width in (((0, 0, 0), 2), ((0,), 0), ((1,), 1)):
        try:
            analyse(deps, width)
        except ValueError:
            errors += 1
        else:
            raise AssertionError("invalid theorem input was not rejected")
    return {
        "status": "PASS", "python": platform.python_version(), "seed": seed,
        "complete_effective_graph_ranges": cases,
        "complete_graph_cases": total, "complete_graph_positive_certificates": positives,
        "boundary_cases": boundary, "seeded_random_cases": random_cases,
        "forced_swap_cases": forced_swaps, "invalid_input_rejections": errors,
        "oracle": "full completed-set optimization, independently encoded in sanity_check.solve_rob",
        "positive_check": "operational ROB replay of every returned schedule",
        "implementation_sha256": hashlib.sha256(Path(__file__).with_name("perfect_saturation.py").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "scope": "Finite implementation checks; arbitrary-size correctness is the written tiling/component proof."
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
