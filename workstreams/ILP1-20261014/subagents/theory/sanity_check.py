#!/usr/bin/env python3
"""Independent finite sanity checks for the theory note; no external packages.

This script is a test, not a proof for unbounded N. It deliberately does not
import either of the main research branch's exact solvers.
"""

from functools import lru_cache
from fractions import Fraction
from itertools import combinations, product
from math import comb
import hashlib
import json
from pathlib import Path
import platform
import time


def all_graphs(n):
    pairs = [(i, j) for j in range(n) for i in range(j)]
    for bits in range(1 << len(pairs)):
        deps = [0] * n
        for k, (i, j) in enumerate(pairs):
            if bits >> k & 1:
                deps[j] |= 1 << i
        yield tuple(deps)


def solve_rob(deps, b, w):
    n = len(deps)
    full = (1 << n) - 1

    @lru_cache(None)
    def rec(done):
        if done == full:
            return 0, ()
        r = 0
        while done >> r & 1:
            r += 1
        ready = [j for j in range(r, min(n, r + b))
                 if not (done >> j & 1) and not (deps[j] & ~done)]
        assert ready
        best = (n + 1, ())
        for size in range(1, min(w, len(ready)) + 1):
            for action in combinations(ready, size):
                nxt = done | sum(1 << j for j in action)
                cost, tail = rec(nxt)
                if cost + 1 < best[0]:
                    best = cost + 1, (action,) + tail
        return best

    answer = rec(0)
    assert rec.cache_info().currsize <= 1 + n * (1 << max(0, b - 1))
    return answer


def earliest(deps, b):
    n = len(deps)
    e, prefix = [], [0]
    for j in range(n):
        dep_max = max((e[i] for i in range(j) if deps[j] >> i & 1), default=0)
        window_max = prefix[max(0, j - b + 1)]
        e.append(1 + max(dep_max, window_max))
        prefix.append(max(prefix[-1], e[-1]))
    return e


def worst_nondelay(deps, b, w):
    n = len(deps)
    full = (1 << n) - 1

    @lru_cache(None)
    def rec(done):
        if done == full:
            return 0
        r = 0
        while done >> r & 1:
            r += 1
        ready = [j for j in range(r, min(n, r + b))
                 if not (done >> j & 1) and not (deps[j] & ~done)]
        return 1 + max(rec(done | sum(1 << j for j in chosen))
                       for chosen in combinations(ready, min(w, len(ready))))

    return rec(0)


def replay(deps, b, w, times):
    n = len(deps)
    done = 0
    for c in range(1, max(times, default=0) + 1):
        r = 0
        while r < n and done >> r & 1:
            r += 1
        action = [j for j in range(n) if times[j] == c]
        if len(action) > w:
            return False
        if any(not (r <= j < min(n, r + b)) or deps[j] & ~done for j in action):
            return False
        done |= sum(1 << j for j in action)
    return done == (1 << n) - 1


def footprint(times):
    return max((j - i + 1 for j in range(len(times)) for i in range(j + 1)
                if times[i] >= times[j]), default=0)


def two_window_matching(deps):
    n = len(deps)
    j, matched = 0, 0
    while j + 1 < n:
        if not (deps[j + 1] >> j & 1):
            matched += 1
            j += 2
        else:
            j += 1
    return n - matched


def bottleneck_window(deps):
    n = len(deps)
    h = max(earliest(deps, max(1, n)), default=0)
    threshold = 0
    for seq in combinations(range(n), h + 1):
        gaps = [j - i for i, j in zip(seq, seq[1:]) if not (deps[j] >> i & 1)]
        assert gaps
        threshold = max(threshold, min(gaps))
    return threshold + 1


def run():
    start = time.perf_counter()
    counts = {"graphs": 0, "resource_cases": 0, "schedule_equivalence_cases": 0,
              "binomial_programs": 0, "binomial_actions": 0,
              "dichotomy_programs": 0, "chain_family_first_actions": 0,
              "worst_nondelay_resource_cases": 0,
              "large_window_drop_resource_cases": 0,
              "large_width_drop_resource_cases": 0,
              "chain_suffix_resource_cases": 0,
              "epsilon_threshold_cases": 0}
    for n in range(6):
        for deps in all_graphs(n):
            counts["graphs"] += 1
            heights = []
            for b in range(1, max(1, n) + 1):
                e = earliest(deps, b)
                height = max(e, default=0)
                heights.append(height)
                for w in range(1, max(1, n) + 1):
                    val, actions = solve_rob(deps, b, w)
                    times = [0] * n
                    for c, action in enumerate(actions, 1):
                        for j in action:
                            times[j] = c
                    assert replay(deps, b, w, times)
                    assert footprint(times) <= b
                    assert val >= height
                    if w >= b:
                        assert val == height
                    if b == 2 and w >= 2:
                        assert val == two_window_matching(deps)
                    worst = worst_nondelay(deps, b, w)
                    assert w * worst <= n + (w - 1) * height
                    assert w * worst <= (2 * w - 1) * val
                    counts["worst_nondelay_resource_cases"] += 1
                    counts["resource_cases"] += 1
            if n:
                bsat = next(b for b, h in enumerate(heights, 1) if h == heights[-1])
                assert bsat == bottleneck_window(deps)
            if n <= 4:
                for times in product(range(1, n + 1), repeat=n):
                    data_ok = all(times[i] < times[j] for j in range(n)
                                  for i in range(j) if deps[j] >> i & 1)
                    for b in range(1, max(1, n) + 1):
                        expected = data_ok and footprint(times) <= b
                        assert replay(deps, b, max(1, n), times) == expected
                        counts["schedule_equivalence_cases"] += 1

    barrier_values = []
    for m in range(1, 8):
        deps = [0] * (3 * m)
        for k in range(1, m):
            deps[3 * k] = (1 << (3 * k - 2)) | (1 << (3 * k - 1))
            deps[3 * k + 1] = 1 << (3 * k - 1)
        values = [solve_rob(tuple(deps), 3, w)[0] for w in (1, 2, 3)]
        assert values == [3 * m, 2 * m, m]
        barrier_values.append({"m": m, "makespans_width_1_2_3": values})

    binomial = []
    for q in range(1, 4):
        n, b, w = 4 * q, 3 * q, 2 * q
        prefix = set(range(q))
        candidates = list(combinations(range(q, 3 * q), q))
        for chosen in candidates:
            deps = [0] * n
            for r, pred in enumerate(chosen):
                deps[3 * q + r] = 1 << pred
            optimum, _ = solve_rob(tuple(deps), b, w)
            assert optimum == 2
            for guessed in candidates:
                action1 = prefix | set(guessed)
                times = [0] * n
                for j in action1:
                    times[j] = 1
                for j in range(3 * q):
                    if not times[j]:
                        times[j] = 2
                for r, pred in enumerate(chosen):
                    times[3 * q + r] = 2 if pred in action1 else 3
                assert replay(tuple(deps), b, w, times)
                assert max(times) == (2 if guessed == chosen else 3)
                counts["binomial_actions"] += 1
            counts["binomial_programs"] += 1
        binomial.append({"q": q, "programs": len(candidates),
                         "expected_makespan_numerator": 3 * comb(2 * q, q) - 1,
                         "expected_makespan_denominator": comb(2 * q, q)})

    for b in range(3, 21):
        for w in range(2, b):
            for hidden in range(1, b):
                length = (b - w + w - 2) // (w - 1)
                deps = [0] * (b + length)
                deps[b] = 1 << hidden
                for j in range(b + 1, b + length):
                    deps[j] = 1 << (j - 1)
                times = [0] * (b + length)
                first = set(range(w - 1)) | {hidden}
                if len(first) < w:
                    first.add(w - 1)
                assert len(first) == w
                for j in first:
                    times[j] = 1
                remaining = [j for j in range(b) if not times[j]]
                for k in range(length):
                    cycle = k + 2
                    times[b + k] = cycle
                    for _ in range(min(w - 1, len(remaining))):
                        times[remaining.pop(0)] = cycle
                assert replay(tuple(deps), b, w, times)
                assert max(times) == length + 1
                counts["dichotomy_programs"] += 1
                if b <= 10:
                    for selected in combinations(range(1, b), w - 1):
                        action1 = {0} | set(selected)
                        delayed = hidden not in action1
                        times = [0] * (b + length)
                        for j in action1:
                            times[j] = 1
                        remaining = [j for j in range(b) if not times[j]]
                        if delayed:
                            remaining.remove(hidden)
                            times[hidden] = 2
                            for _ in range(min(w - 1, len(remaining))):
                                times[remaining.pop(0)] = 2
                        for k in range(length):
                            cycle = k + 2 + delayed
                            times[b + k] = cycle
                            for _ in range(min(w - 1, len(remaining))):
                                times[remaining.pop(0)] = cycle
                        assert replay(tuple(deps), b, w, times)
                        assert max(times) == length + 1 + delayed
                        counts["chain_family_first_actions"] += 1

    saturation_deps = (0, 0, 0, (1 << 1) | (1 << 2))
    table = [[solve_rob(saturation_deps, b, w)[0] for w in range(1, 5)]
             for b in range(1, 5)]
    assert table == [[4, 4, 4, 4], [4, 3, 3, 3], [4, 3, 2, 2], [4, 2, 2, 2]]
    window_drop = []
    for height in range(2, 13):
        n = 2 * height
        deps = [0] * n
        layers = [[2 * k - 1, 2 * k] for k in range(1, height)] + [[n - 1]]
        for before, after in zip(layers, layers[1:]):
            for j in after:
                deps[j] = sum(1 << i for i in before)
        for b in range(1, n + 1):
            for w in range(1, 5):
                actual = solve_rob(tuple(deps), b, w)[0]
                if b == 1 or w == 1:
                    expected = n
                elif b == 2 or (w == 2 and b < n):
                    expected = height + 1
                else:
                    expected = height
                assert actual == expected
                counts["large_window_drop_resource_cases"] += 1
        window_drop.append({"height": height, "n": n,
                            "B_sat_width2": n, "B_sat_width3": 3})
    width_drop = []
    for m in range(2, 6):
        for r in range(1, m // 2 + 1):
            n = 2 * m
            deps = [0] * n
            required = list(range(r, r + m))
            parts = [required[2 * k:2 * k + 2] for k in range(r)]
            parts += [[j] for j in required[2 * r:]]
            for j, part in enumerate(parts, r + m):
                deps[j] = sum(1 << i for i in part)
            for b in range(m + r, n + 1):
                threshold = m + min(r, n - b)
                for w in range(1, b + 1):
                    actual = solve_rob(tuple(deps), b, w)[0]
                    assert (actual == 2) == (w >= threshold)
                    counts["large_width_drop_resource_cases"] += 1
            for s in range(r + 2):
                w = m + s
                threshold = n - s if s < r else m + r
                for b in range(1, n + 1):
                    actual = solve_rob(tuple(deps), b, w)[0]
                    assert (actual == 2) == (b >= threshold)
                    counts["large_width_drop_resource_cases"] += 1
            width_drop.append({"m": m, "r": r,
                               "width_at_window_m_plus_r": m + r,
                               "width_at_window_2m": m})
    epsilon_family = []
    tolerances = [Fraction(0), Fraction(1, 10), Fraction(1, 4), Fraction(1, 3),
                  Fraction(1, 2), Fraction(3, 4), Fraction(9, 10),
                  Fraction(1), Fraction(3, 2)]
    for k in range(1, 9):
        n = 2 * k
        deps = tuple(0 if j == 0 or j >= k else 1 << (j - 1) for j in range(n))
        for w in range(2, 6):
            optimum = {}
            for b in range(1, n + 1):
                value = solve_rob(deps, b, w)[0]
                remaining = max(0, k - b + 1)
                effective = min(b, w)
                expected = k + (remaining + effective - 1) // effective
                assert value == expected
                optimum[b] = value
                counts["chain_suffix_resource_cases"] += 1
            for epsilon in tolerances:
                d = (epsilon.numerator * k) // epsilon.denominator
                predicted = max((k + d + 1) // (d + 1), k + 1 - d * w)
                actual = min(b for b, value in optimum.items()
                             if value <= (1 + epsilon) * k)
                assert predicted == actual
                if w == 2:
                    simplified = max(2, k + 1 - 2 * d) if epsilon < 1 else 1
                    assert predicted == simplified
                counts["epsilon_threshold_cases"] += 1
        epsilon_family.append({"k": k, "n": n,
                               "B_sat_all_widths_ge_2": k + 1,
                               "B_epsilon_width2_tolerance_1_10":
                               max(2, k + 1 - 2 * (k // 10))})
    report = {"status": "PASS", "scope": "finite sanity tests only",
              "python": platform.python_version(), "platform": platform.platform(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "randomness": "none; exhaustive or deterministic stated families",
              "counts": counts, "all_forward_graphs_max_n": 5,
              "all_cycle_assignments_max_n": 4,
              "barrier_family": barrier_values, "binomial_family": binomial,
              "saturation_counterexample": table,
              "large_window_drop_family": window_drop,
              "large_width_drop_family": width_drop,
              "chain_suffix_epsilon_family": epsilon_family,
              "elapsed_seconds": round(time.perf_counter() - start, 6)}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()
