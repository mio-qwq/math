#!/usr/bin/env python3
"""Bounded coordinate-only elimination test described in PROJECTION.md."""
import hashlib
import itertools
import json
from pathlib import Path
import time

SUPPORT = (2, 9, 10, 16, 23, 24, 30, 37, 38, 44, 51, 52, 58)
EQUATIONS = [(t, sum(1 << i for i in (t, t - 2, t - 7, t - 15, t - 16)))
             for t in range(16, 64)]
FULL = (1 << 64) - 1


def propagate(anchors):
    known = sum(1 << i for i in anchors)
    order = []
    changed = True
    while changed:
        changed = False
        for t, mask in EQUATIONS:
            unknown = mask & ~known
            if unknown and not unknown & (unknown - 1):
                position = unknown.bit_length() - 1
                order.append([t, position])
                known |= unknown
                changed = True
    return known, order


def main():
    started = time.monotonic()
    remaining = [i for i in range(64) if i not in SUPPORT]
    initial = set(SUPPORT)
    trials = 0
    best = None
    histogram = {}
    for extra in itertools.combinations(remaining, 3):
        trials += 1
        known, order = propagate(initial | set(extra))
        count = known.bit_count()
        histogram[count] = histogram.get(count, 0) + 1
        if best is None or count > best["known_count"]:
            best = {"additional_anchors": list(extra), "known_count": count,
                    "elimination_order": order,
                    "unresolved": [i for i in range(64) if not (known >> i) & 1]}
        if known == FULL:
            assert len(order) == 48
            assert len({t for t, _ in order}) == 48
            break
    result = {"schema": "sha256-support0-coordinate-elimination-v1",
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "support": SUPPORT, "extra_anchor_count": 3, "tested_anchor_sets": trials,
              "completion_found": best["known_count"] == 64,
              "histogram_final_known_coordinates": histogram, "best": best,
              "elapsed_seconds": time.monotonic() - started,
              "scope": "Coordinate peeling only; failure does not disprove projection surjectivity"}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
