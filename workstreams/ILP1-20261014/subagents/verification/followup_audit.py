"""Independent policy expectation/advice and compact resource-certificate audit."""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import random
import sys
from time import perf_counter

from constraint_solver import operational_check, solve


def chain_continuation(B, W, x, first):
    L = (B - W + W - 2) // (W - 1)
    n = B + L
    issued = set(first)
    schedule = [sorted(first)]
    if x not in issued:
        missed = {x}
        missed.update([j for j in range(B) if j not in issued and j != x][:W - 1])
        schedule.append(sorted(missed))
        issued.update(missed)
    for chain_job in range(B, n):
        roots = [j for j in range(B) if j not in issued][:W - 1]
        schedule.append(roots + [chain_job])
        issued.update(roots)
        issued.add(chain_job)
    assert issued == set(range(n))
    return schedule


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--primary-directory", required=True)
    p.add_argument("--output", default="followup_results.json")
    args = p.parse_args()
    start = perf_counter()
    report = {"utc_start": datetime.now(timezone.utc).isoformat(), "seed": 2026101402,
              "scope": "Independent finite checks and source review; no new Lean compilation.",
              "source_sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("constraint_solver.py", "followup_audit.py")}}

    policy_replays = advice_replays = parameter_pairs = 0
    examples = []
    for B in range(3, 13):
        for W in range(2, B):
            parameter_pairs += 1
            L = (B - W + W - 2) // (W - 1)
            n = B + L
            subsets = list(combinations(range(1, B), W - 1))
            expected_ratio = Fraction(1) + Fraction(B - W, (B - 1) * (L + 1))
            for x in range(1, B):
                total = hits = 0
                edges = [(x, B)] + [(j, j + 1) for j in range(B, n - 1)]
                for subset in subsets:
                    schedule = chain_continuation(B, W, x, {0, *subset})
                    assert operational_check(n, edges, B, W, schedule)
                    assert len(schedule) == (L + 1 if x in subset else L + 2)
                    total += len(schedule)
                    hits += x in subset
                    policy_replays += 1
                assert Fraction(hits, len(subsets)) == Fraction(W - 1, B - 1)
                assert Fraction(total, len(subsets) * (L + 1)) == expected_ratio

            # Explicit partition-based fixed-length advice, including padding.
            hidden = list(range(1, B))
            groups = [hidden[k:k+W-1] for k in range(0, len(hidden), W-1)]
            M = (B - 2 + W - 1) // (W - 1)
            assert len(groups) == M and (M - 1) * (W - 1) < B - 1
            for group in groups:
                first = {0, *group}
                first.update([j for j in range(B) if j not in first][:W-len(first)])
                for x in group:
                    edges = [(x, B)] + [(j, j + 1) for j in range(B, n - 1)]
                    schedule = chain_continuation(B, W, x, first)
                    assert len(schedule) == L+1
                    assert operational_check(n, edges, B, W, schedule)
                    advice_replays += 1
            examples.append({"B": B, "W": W, "L": L,
                             "number_first_subsets": comb(B-1, W-1),
                             "randomized_ratio": [expected_ratio.numerator, expected_ratio.denominator],
                             "advice_messages": M, "advice_bits": (M-1).bit_length()})
    report["chain_minimax_advice"] = {"B_range": [3, 12], "W_range": "2..B-1",
                                       "parameter_pairs": parameter_pairs,
                                       "policy_replays": policy_replays,
                                       "advice_replays": advice_replays,
                                       "instances": examples}

    primary = Path(args.primary_directory).resolve()
    sys.path.insert(0, str(primary))
    import resources
    import rob
    primary_hashes = {name: hashlib.sha256((primary / name).read_bytes()).hexdigest()
                      for name in ("resources.py", "rob.py", "checker.py")}
    rng = random.Random(report["seed"])
    checked = 0
    for _ in range(350):
        n = rng.randrange(6, 15)
        edges = tuple((i, j) for j in range(n)
                      for i in rng.sample(range(j), rng.randrange(min(2, j) + 1)))
        cert = resources.saturated_window(rob.Program(n, edges))
        assert resources.check_saturation_certificate(cert)["valid"]
        assert operational_check(n, edges, cert["B_sat"], n, cert["schedule"])
        original, _ = solve(n, edges, n, n)
        assert original == cert["cycles"]
        minimal = next(B for B in range(1, n+1) if solve(n, edges, B, n)[0] == original)
        assert cert["B_sat"] == minimal
        checked += 1

    good = resources.saturated_window(rob.Program(4, ((1, 3), (2, 3))))
    mutations = []
    def bad(name, field, value):
        cert = copy.deepcopy(good)
        cert[field] = value
        mutations.append((name, cert))
    bad("zero_window", "B_sat", 0)
    bad("too_large_window", "B_sat", 5)
    bad("nonstrict_integer_window", "B_sat", 3.5)
    bad("unsupported_width", "W", 2)
    bad("claimed_height_changed", "cycles", 3)
    bad("original_path_empty", "original_critical_chain", [])
    bad("original_path_repeated", "original_critical_chain", [1, 1])
    bad("original_path_backward", "original_critical_chain", [3, 1])
    bad("original_path_missing_edge", "original_critical_chain", [0, 3])
    bad("original_path_out_of_range", "original_critical_chain", [1, 4])
    bad("smaller_path_empty", "smaller_window_chain", [])
    bad("smaller_path_short", "smaller_window_chain", [1, 3])
    bad("smaller_path_repeated", "smaller_window_chain", [0, 0, 3])
    bad("smaller_path_backward", "smaller_window_chain", [3, 2, 0])
    bad("smaller_path_missing_edge", "smaller_window_chain", [0, 1, 3])
    bad("smaller_path_out_of_range", "smaller_window_chain", [0, 2, 4])
    bad("schedule_missing_job", "schedule", [[0, 1], [3]])
    bad("schedule_duplicate_job", "schedule", [[0, 1, 1, 2], [3]])
    bad("schedule_unready_job", "schedule", [[0, 1, 3], [2]])
    bad("schedule_unadmitted_job", "schedule", [[1, 2, 3], [0]])
    bad("schedule_trailing_cycle", "schedule", good["schedule"] + [[]])
    bad("dependency_backward", "edges", [[3, 1]])
    bad("dependency_out_of_range", "edges", [[1, 4]])
    b1 = resources.saturated_window(rob.Program(3, ((0, 1), (1, 2))))
    b1["smaller_window_chain"] = [0]
    mutations.append(("window_one_spurious_obstruction", b1))
    rejected = []
    for name, certificate in mutations:
        try:
            resources.check_saturation_certificate(certificate)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(("invalid certificate accepted", name, certificate))
    report["compact_resource_certificates"] = {
        "primary_source_sha256": primary_hashes, "random_instances": checked,
        "random_N_range": [6,14], "independent_solver": "constraint_solver.solve",
        "rejected_mathematical_tampers": rejected,
        "note": "Certificates bind their own embedded n/edges, not an external trusted instance.",
    }
    report["status"] = "PASS"
    report["elapsed_seconds"] = perf_counter()-start
    Path(args.output).write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "elapsed_seconds": report["elapsed_seconds"],
                      "chain_policy_replays": policy_replays, "advice_replays": advice_replays,
                      "resource_cases": checked, "mathematical_tampers_rejected": len(rejected)}))


if __name__ == "__main__":
    main()
