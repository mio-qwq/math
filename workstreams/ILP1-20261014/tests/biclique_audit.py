"""Finite audit of the explicit biclique-to-ROB reduction; not a proof."""
from pathlib import Path
import hashlib
import itertools
import json
import platform
import random
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "subagents/verification")]
from biclique_reduction import construct, three_cycle_witness, four_cycle_witness
from constraint_solver import feasible, operational_check, times_to_schedule


def biclique(n, m, edges, k):
    for us in itertools.combinations(range(n), k):
        common = [v for v in range(m) if all((u, v) in edges for u in us)]
        if len(common) >= k:
            return us, common[:k]
    return None


def main():
    start = time.perf_counter()
    counts = {"cases": 0, "yes": 0, "no": 0, "CSP_witness_replays": 0,
              "constructed_witness_replays": 0, "window_edge_checks": 0}
    ranges = []

    def check(n, m, edges, k):
        expected = biclique(n, m, edges, k)
        p = construct(n, m, edges, k)
        N, dep, B, W = p["n"], p["edges"], p["B"], p["W"]
        assert B-W == k and N == 2*B and 2*W < N <= 3*W
        assert all(u < B <= v for u, v in dep)
        ds = set(dep)
        for v in range(N):
            for u in range(v-B+1):
                assert (u, v) in ds
                counts["window_edge_checks"] += 1
        got = feasible(N, dep, B, W, 3)
        assert (got is not None) == (expected is not None), (n, m, k, edges)
        if got is not None:
            assert operational_check(N, dep, B, W, times_to_schedule(got))
            counts["CSP_witness_replays"] += 1
        assert operational_check(N, dep, B, W, four_cycle_witness(p))
        counts["constructed_witness_replays"] += 1
        if expected is not None:
            assert operational_check(N, dep, B, W, three_cycle_witness(p, *expected))
            counts["constructed_witness_replays"] += 1
        counts["cases"] += 1
        counts["yes" if expected is not None else "no"] += 1

    for n in range(1, 4):
        for m in range(1, 4):
            before = counts["cases"]
            pairs = list(itertools.product(range(n), range(m)))
            for mask in range(1 << len(pairs)):
                edges = {edge for i, edge in enumerate(pairs) if mask >> i & 1}
                for k in range(1, min(n, m)+1):
                    check(n, m, edges, k)
            ranges.append({"left": n, "right": m, "graphs": 1 << (n*m),
                           "cases": counts["cases"]-before})
            print("checked bipartition", n, m, "cumulative cases", counts["cases"], flush=True)
    rng = random.Random(2026101414)
    for _ in range(40):
        n, m = rng.randint(3, 6), rng.randint(3, 6)
        k = rng.randint(1, min(3, n, m))
        density = rng.choice([0.1, 0.35, 0.6, 0.9])
        edges = {(u, v) for u in range(n) for v in range(m) if rng.random() < density}
        check(n, m, edges, k)
    out = {"status": "PASS", "completed_utc": datetime.now(timezone.utc).isoformat(),
           "python": platform.python_version(), "elapsed_seconds": time.perf_counter()-start,
           "counts": counts, "exhaustive_bipartition_ranges": ranges,
           "random": {"cases": 40, "seed": 2026101414, "left_right": "3..6", "k": "1..min(3,n,m)"},
           "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in [ROOT/"src/biclique_reduction.py", Path(__file__), ROOT/"subagents/verification/constraint_solver.py"]},
           "scope": "Root construction compared with independent time-variable CSP; finite tests are not the general proof. Unbounded true fan-in only."}
    (ROOT/"evidence/biclique-root.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({"status": out["status"], **counts, "seconds": out["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
