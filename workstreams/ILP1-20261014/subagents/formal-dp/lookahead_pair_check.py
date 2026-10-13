#!/usr/bin/env python3
"""Small independent time-CSP checks of the fixed-lookahead obstruction.

The graph and witnesses are built here without importing the theory author's
implementation. The separately owned oracle assigns cycle variables and
independently replays the ROB. Finite checks do not prove arbitrary M or L.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import platform
import sys
import time

sys.dont_write_bytecode = True


def family(m, padding, side):
    a = [3] + [4 + 2 * j for j in range(m)]
    b = [2] + [5 + 2 * j for j in range(m)]
    n = 2 * m + 5 + padding
    z = n - 1
    edges = list(zip(a, a[1:])) + list(zip(b, b[1:]))
    edges.append(((a if side == "A" else b)[-1], z))
    extra = [2 * m + 4] if padding else []
    if side == "A":
        schedule = [[0, 1, a[0]]] + [[b[j - 1], a[j]] for j in range(1, m + 1)]
        schedule.append(sorted([b[-1], z] + extra))
    else:
        schedule = [[0, 1, b[0]]] + [[a[j - 1], b[j]] for j in range(1, m + 1)]
        schedule.append(sorted([a[-1], z] + extra))
    return n, edges, schedule


def run(oracle_path):
    began = time.monotonic()
    spec = importlib.util.spec_from_file_location("lookahead_review_csp", oracle_path)
    oracle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(oracle)
    actions = [tuple(j for j in range(4) if mask >> j & 1) for mask in range(16)]
    rows = []
    decisions = replays = observation_pairs = 0
    for m, padding in itertools.product(range(1, 4), (0, 1)):
        paired_edges = {}
        for side in ("A", "B"):
            n, edges, explicit = family(m, padding, side)
            paired_edges[side] = edges
            horizon = m + 2
            if not oracle.operational_check(n, edges, 4, 3, explicit):
                raise RuntimeError((m, padding, side, "explicit witness failed replay"))
            replays += 1
            if len(explicit) != horizon:
                raise RuntimeError("wrong witness horizon")
            wrong = family(m, padding, "B" if side == "A" else "A")[2]
            wrong[-1] = [job for job in wrong[-1] if job != n - 1]
            wrong.append([n - 1])
            if len(wrong) != horizon + 1 or not oracle.operational_check(n, edges, 4, 3, wrong):
                raise RuntimeError("wrong-leader one-cycle-loss witness failed")
            replays += 1
            if oracle.feasible(n, edges, 4, 3, horizon - 1) is not None:
                raise RuntimeError("critical-path lower bound violated")
            optimum_times = oracle.feasible(n, edges, 4, 3, horizon)
            decisions += 2
            if optimum_times is None:
                raise RuntimeError("target horizon infeasible")
            if not oracle.operational_check(n, edges, 4, 3, oracle.times_to_schedule(optimum_times)):
                raise RuntimeError("CSP witness failed operational replay")
            replays += 1
            successful = []
            for action in actions:
                times = oracle.feasible(n, edges, 4, 3, horizon, first_action=action)
                decisions += 1
                if times is not None:
                    successful.append(action)
                    if not oracle.operational_check(n, edges, 4, 3, oracle.times_to_schedule(times)):
                        raise RuntimeError("fixed-first-action witness failed replay")
                    replays += 1
            expected = [(0, 3), (0, 1, 3), (0, 2, 3)] if side == "A" else [(0, 1, 2)]
            if set(successful) != set(expected):
                raise RuntimeError((m, padding, side, successful, expected))
            rows.append({"M": m, "padding": padding, "side": side, "N": n,
                         "optimum": horizon, "optimal_first_actions": successful,
                         "explicit_schedule": explicit, "wrong_leader_schedule": wrong})
        # All L at or below the sharp visibility cutoff, including L=0.
        for lookahead in range(n - 4):
            exclusive = min(n, 4 + lookahead)
            if not exclusive <= n - 1:
                raise RuntimeError("hidden last job became visible")
            observed = [[tuple(u for u, v in paired_edges[side] if v == job)
                         for job in range(exclusive)] for side in ("A", "B")]
            if observed[0] != observed[1]:
                raise RuntimeError("initial observations differ")
            observation_pairs += 1
    return {"status": "PASS", "python": platform.python_version(),
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "M_values": [1, 2, 3], "padding_values": [0, 1],
            "programs": len(rows), "CSP_decisions": decisions,
            "direct_operational_replays": replays,
            "initial_observation_pair_checks": observation_pairs,
            "initial_action_scope": "All 16 root subsets: 15 capacity-valid subsets including empty, plus one over-width negative check.",
            "cases": rows,
            "oracle_sha256": hashlib.sha256(oracle_path.read_bytes()).hexdigest(),
            "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "elapsed_seconds": round(time.monotonic() - began, 6),
            "scope": "Finite boundary/CSP evidence, not a proof for arbitrary M, L, policies, or randomization."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = run(args.oracle)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {report['programs']} programs, {report['CSP_decisions']} CSP decisions, "
          f"{report['initial_observation_pair_checks']} initial observation pairs")
