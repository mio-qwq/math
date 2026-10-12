#!/usr/bin/env python3
"""Bounded coordinate-only search for a support-12 base chart."""
import hashlib
import itertools
import json
from pathlib import Path
import time

SUPPORT = (10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57)
EQUATIONS = tuple(
    (t, sum(1 << i for i in (t, t - 2, t - 7, t - 15, t - 16)))
    for t in range(16, 64)
)
FULL = (1 << 64) - 1
SIZE5_TRIAL_BUDGET = 1_600_000


def propagate(anchors):
    known = sum(1 << i for i in anchors)
    order = []
    changed = True
    while changed:
        changed = False
        for t, mask in EQUATIONS:
            unknown = mask & ~known
            if unknown and not unknown & (unknown - 1):
                target = unknown.bit_length() - 1
                known |= unknown
                order.append([t, target])
                changed = True
    return known, order


def scan_size(size, limit=None):
    remaining = [i for i in range(64) if i not in SUPPORT]
    best = None
    histogram = {}
    trials = 0
    success = None
    for extra in itertools.combinations(remaining, size):
        if limit is not None and trials >= limit:
            break
        trials += 1
        known, order = propagate(set(SUPPORT) | set(extra))
        count = known.bit_count()
        histogram[count] = histogram.get(count, 0) + 1
        if best is None or count > best["known_count"]:
            best = {"anchors": list(extra), "known_count": count,
                    "order": order}
        if known == FULL:
            success = {"anchors": list(extra), "known_count": count,
                       "order": order,
                       "unused_equations": sorted(set(range(16, 64)) -
                                                  {t for t, _ in order})}
            break
    return {"anchor_count": size, "trials": trials,
            "histogram_final_known_coordinates": histogram,
            "best": best, "success": success}


def main():
    started = time.monotonic()
    scans = [scan_size(3), scan_size(4),
             scan_size(5, SIZE5_TRIAL_BUDGET)]
    assert scans[0]["trials"] == 20_825 and scans[0]["success"] is None
    assert scans[1]["trials"] == 249_900 and scans[1]["success"] is None
    success = scans[2]["success"]
    assert success is not None
    assert len(success["order"]) == 46
    assert len(success["unused_equations"]) == 2
    report = {
        "schema": "sha256-support12-base-lift-coordinate-search-v8",
        "status": "PASS",
        "support": SUPPORT,
        "size5_trial_budget": SIZE5_TRIAL_BUDGET,
        "scans": scans,
        "elapsed_seconds": time.monotonic() - started,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": ("coordinate-only reversible peeling; lower-size failure "
                  "does not imply failure of base completion"),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

