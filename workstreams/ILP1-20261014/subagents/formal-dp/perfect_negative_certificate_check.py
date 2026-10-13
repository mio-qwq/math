#!/usr/bin/env python3
"""Independent true-edge checker for perfect-saturation rejection witnesses.

The validator does not import the producer or compute macro legality flags.
The CLI runs small, deterministic parser/tampering checks; it is not a
replacement for the arbitrary-size odd-interval proof in the review.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time

sys.dont_write_bytecode = True


def _integers(value, length):
    return (isinstance(value, (list, tuple)) and len(value) == length
            and all(type(x) is int for x in value))


def validate_negative(n, width, edges, certificate):
    """Return True only for a complete isolated odd-interval certificate.

    Graph input uses zero-based forward edges. After O(|E|) membership-set
    preprocessing, witness validation takes O(k), where k=N/W. Internal
    double-macro flags and maximality of the interval are never inspected.
    """
    if type(n) is not int or type(width) is not int or n < 0 or width <= 0:
        return False
    if n % width:
        return False
    graph = set()
    try:
        for edge in edges:
            if not _integers(edge, 2):
                return False
            u, v = edge
            if not 0 <= u < v < n:
                return False
            graph.add((u, v))
    except TypeError:
        return False
    keys = {"first_block", "past_last_block", "forbidden_singletons",
            "left_boundary", "right_boundary"}
    if not isinstance(certificate, dict) or set(certificate) != keys:
        return False
    lo, hi = certificate["first_block"], certificate["past_last_block"]
    blocks = n // width
    if type(lo) is not int or type(hi) is not int:
        return False
    if not 0 <= lo < hi <= blocks or (hi - lo) % 2 != 1:
        return False
    witnesses = certificate["forbidden_singletons"]
    if not isinstance(witnesses, (list, tuple)):
        return False
    if len(witnesses) != (hi - lo + 1) // 2:
        return False
    for expected, witness in zip(range(lo, hi, 2), witnesses):
        if not _integers(witness, 3):
            return False
        block, u, v = witness
        if block != expected or (u, v) not in graph:
            return False
        if not block * width <= u < v < (block + 1) * width:
            return False

    def blocks_boundary(witness, expected):
        if expected is None:
            return witness is None
        if not _integers(witness, 3):
            return False
        block, u, v = witness
        if block != expected or (u, v) not in graph:
            return False
        if not block * width <= u < v < (block + 2) * width:
            return False

        def phase(job):
            local = job - block * width
            first = local < width - 1 or local == width
            return 0 if first else 1

        return phase(u) >= phase(v)

    return (blocks_boundary(certificate["left_boundary"], None if lo == 0 else lo - 1)
            and blocks_boundary(certificate["right_boundary"], None if hi == blocks else hi - 1))


def run_checks(producer_path):
    """Use producer only to obtain witnesses, never inside the validator."""
    began = time.monotonic()
    spec = importlib.util.spec_from_file_location("reviewed_saturation_producer", producer_path)
    producer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(producer)
    results = []

    def check(name, actual, expected):
        if actual != expected:
            raise RuntimeError(f"{name}: got {actual!r}, expected {expected!r}")
        results.append({"case": name, "accepted": actual})

    graph = [(1, 2), (2, 3), (3, 4)]
    cert = producer.analyse_edges(6, graph, 2)["negative_certificate"]
    check("producer interior one-block witness", validate_negative(6, 2, graph, cert), True)
    for field, value, name in [
        ("first_block", -1, "negative lower endpoint"),
        ("first_block", 2, "empty interval"),
        ("past_last_block", 4, "upper endpoint beyond program"),
        ("past_last_block", 3, "even interval"),
        ("first_block", True, "boolean lower endpoint"),
        ("forbidden_singletons", (), "missing singleton witness"),
        ("forbidden_singletons", ((1, 2, 3), (1, 2, 3)), "duplicate singleton witness"),
        ("forbidden_singletons", ((0, 2, 3),), "wrong singleton position"),
        ("forbidden_singletons", ((1, 1, 2),), "cross-block singleton edge"),
        ("forbidden_singletons", ((1, 2, 2),), "non-edge singleton witness"),
        ("left_boundary", None, "missing interior left barrier"),
        ("left_boundary", (1, 1, 2), "wrong left boundary index"),
        ("left_boundary", (0, 3, 4), "left witness outside its two-block interval"),
        ("left_boundary", (0, 2, 3), "nonviolating left true edge"),
        ("right_boundary", None, "missing interior right barrier"),
        ("right_boundary", (0, 3, 4), "wrong right boundary index"),
        ("right_boundary", (1, 2, 3), "nonviolating right true edge"),
    ]:
        bad = deepcopy(cert)
        bad[field] = value
        check(name, validate_negative(6, 2, graph, bad), False)
    missing = deepcopy(cert)
    del missing["left_boundary"]
    check("missing required field", validate_negative(6, 2, graph, missing), False)
    check("witness edge deleted from graph", validate_negative(6, 2, [(1, 2), (3, 4)], cert), False)
    check("zero-width input", validate_negative(6, 0, graph, cert), False)
    check("nondivisible input", validate_negative(7, 2, graph, cert), False)
    check("invalid true edge", validate_negative(6, 2, graph + [(4, 3)], cert), False)

    # This interval contains two forbidden internal double macros. It is not
    # a connected component of the legal-double path, but remains a proof.
    chain = [(j, j + 1) for j in range(5)]
    noncomponent = {"first_block": 0, "past_last_block": 3,
                    "forbidden_singletons": ((0, 0, 1), (2, 4, 5)),
                    "left_boundary": None, "right_boundary": None}
    check("valid noncomponent odd interval", validate_negative(6, 2, chain, noncomponent), True)
    spurious = deepcopy(noncomponent)
    spurious["left_boundary"] = (-1, 0, 1)
    check("spurious endpoint boundary", validate_negative(6, 2, chain, spurious), False)

    one = producer.analyse_edges(2, [(0, 1)], 2)["negative_certificate"]
    check("single-block program", validate_negative(2, 2, [(0, 1)], one), True)
    check("false certificate on independent program", validate_negative(2, 2, [], one), False)
    empty = {"first_block": 0, "past_last_block": 0,
             "forbidden_singletons": (), "left_boundary": None, "right_boundary": None}
    check("no rejection certificate for empty program", validate_negative(0, 2, [], empty), False)
    check("no width-one singleton true edge", validate_negative(2, 1, [(0, 1)], one), False)
    return {"status": "PASS", "python": platform.python_version(),
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "deterministic_checks": len(results), "results": results,
            "producer_sha256": hashlib.sha256(producer_path.read_bytes()).hexdigest(),
            "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "elapsed_seconds": round(time.monotonic() - began, 6),
            "scope": "Targeted witness/parser checks only; no new scheduling enumeration or Lean claim."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    report = run_checks(arguments.producer)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {report['deterministic_checks']} targeted negative-certificate checks")
