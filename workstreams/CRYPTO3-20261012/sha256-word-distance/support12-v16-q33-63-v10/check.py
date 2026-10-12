#!/usr/bin/env python3
"""Exact q=33..63 continuation of the frozen valuation-16 classifier."""

import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import importlib.util
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "support12-v16-general-v9" / "check.py"
BASE_SHA256 = "a58fc79b82edce8c82d8838a0d197bdd77b9dc42a4d91c4250b0d3ae4d6d1d60"
QS = tuple(range(33, 64, 2))


def need(ok, message):
    if not ok:
        raise AssertionError(message)


def load_base():
    need(hashlib.sha256(BASE.read_bytes()).hexdigest() == BASE_SHA256,
         "frozen classifier dependency changed")
    spec = importlib.util.spec_from_file_location("support12_v16_base", BASE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def classify_one(q):
    return load_base().classify(q)


def comparable(output):
    output = dict(output)
    output.pop("elapsed_seconds", None)
    output.pop("checker_sha256", None)
    return output


def run(jobs, negative):
    start = time.monotonic()
    base = load_base()
    for kind in (0, 1):
        for bit in range(32):
            need(base.sigma_rows(1 << bit, kind) ==
                 base.sigma_direct(1 << bit, kind),
                 "row construction differs from direct sigma")
    if jobs == 1:
        cases = [base.classify(q) for q in QS]
    else:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            cases = list(pool.map(classify_one, QS))
    cases.sort(key=lambda row: row["q"])
    excluded = [row["q"] for row in cases
                if row["full32_twin_leaves"] == 0]
    surviving = [row["q"] for row in cases
                 if row["full32_twin_leaves"] != 0]
    controls = {"basis_rows_checked": 64,
                "base_checker_sha256": BASE_SHA256}
    if negative:
        controls["damaged_fixture_fields_rejected"] = sum(
            base.damaged_fixture_rejected(row["q"], fixture)
            for row in cases for fixture in row["unique_recovered_fixtures"])
        controls["excluded_with_low31_frontier"] = [
            row["q"] for row in cases
            if row["low31_twin_leaves"] and
            not row["full32_twin_leaves"]]
    return {
        "schema": "CRYPTO3-support12-v16-q33-63-v10",
        "status": "PASS",
        "q_domain": list(QS),
        "cases": cases,
        "excluded_positive_q": excluded,
        "surviving_positive_q": surviving,
        "negative_orientation":
            "pair reversal gives the same classification for -D",
        "controls": controls,
        "scope": ("selected twin core only; survivors are local pair "
                  "fixtures, not three-pair cores, complete supports, or "
                  "message pairs"),
        "elapsed_seconds": time.monotonic() - start,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--negative", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    need(1 <= args.jobs <= 16, "jobs out of range")
    output = run(args.jobs, args.negative)
    certificate = HERE / "CERTIFICATE.json"
    if args.write_certificate:
        certificate.write_text(json.dumps(comparable(output), indent=2,
                                          sort_keys=True) + "\n")
    else:
        need(json.loads(certificate.read_text()) == comparable(output),
             "frozen certificate mismatch")
    print(json.dumps({
        "status": output["status"],
        "excluded_positive_q": output["excluded_positive_q"],
        "surviving_positive_q": output["surviving_positive_q"],
        "controls": output["controls"],
        "elapsed_seconds": output["elapsed_seconds"],
        "certificate_sha256": hashlib.sha256(certificate.read_bytes()).hexdigest(),
        "checker_sha256": output["checker_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
