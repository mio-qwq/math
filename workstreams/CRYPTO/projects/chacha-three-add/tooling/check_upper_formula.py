#!/usr/bin/env python3
"""Check a separately derived upper-bit closed form against exact state sums.

This is a root-agent cross-check of the discovery-agent formula. It imports
the root's earlier evaluator, not the discovering agent's moment code.
"""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time

from exact_dp import correlation


def closed(r, q, k):
    a = -Fraction(1, 3 << r) + Fraction(4, 3 << (3*r + 2*q))
    b = -Fraction(1, 7 << q) - Fraction(1, 7 << (3*r + q))
    d = Fraction(2, 7 << (3*r + q))
    return a / (4**k) + b / (2**k) + d / (16**k)


def main():
    project = Path(__file__).resolve().parent.parent
    start = time.perf_counter()
    rows = []
    for r in range(1, 7):
        for q in range(1, 7):
            for k in range(q+1):
                i = r+q+k
                for n in (i+1, i+4):
                    actual = correlation(n, r, q, i)
                    expected = closed(r, q, k)
                    assert actual == expected, (n, r, q, k, actual, expected)
                    rows.append({"n": n, "r": r, "q": q, "k": k,
                                 "i": i, "correlation": str(actual)})
    assert len(rows) == 324
    standard = []
    for k in range(4):
        actual = correlation(32, 16, 12, 28+k)
        assert actual == closed(16, 12, k)
        standard.append({"i": 28+k, "correlation": str(actual)})
    actual = correlation(5, 1, 1, 4)
    extrapolated = closed(1, 1, 2)
    assert actual == Fraction(-7, 256)
    assert extrapolated == Fraction(-57, 2048)
    assert actual != extrapolated
    recurrence_checks = 0
    for r in range(1, 7):
        for q in range(3, 7):
            n = r+2*q+1
            values = [correlation(n, r, q, r+q+k) for k in range(q+1)]
            for k in range(q-2):
                rhs = Fraction(13,16)*values[k+2] - Fraction(11,64)*values[k+1] + Fraction(1,128)*values[k]
                assert values[k+3] == rhs
                recurrence_checks += 1
    result = {
        "status": "pass",
        "utc": datetime.now(timezone.utc).isoformat(),
        "command": [sys.executable, *sys.argv],
        "comparison_count": len(rows),
        "recurrence_comparisons": recurrence_checks,
        "standard": standard,
        "outside_domain_control": {"n":5,"r":1,"q":1,"k":2,"actual":str(actual),
                                   "incorrect_extrapolation":str(extrapolated),"separated":True},
        "source_sha256": {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (Path(__file__), Path(__file__).with_name("exact_dp.py"))},
        "randomness": "none",
        "elapsed_seconds": time.perf_counter()-start,
        "rows": rows,
        "evidence_limit": "finite cross-check of a supplied formula; general proof and novelty are separate",
    }
    output = project / "tooling/results/upper_formula_check.json"
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status":"pass","comparisons":len(rows),"recurrences":recurrence_checks,
                      "standard":standard,"output":str(output)}))


if __name__ == "__main__":
    main()
