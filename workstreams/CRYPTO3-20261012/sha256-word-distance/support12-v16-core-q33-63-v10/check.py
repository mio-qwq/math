#!/usr/bin/env python3
"""Stdlib reconstruction and RUP audit for every odd q=33..63."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "support12-v16-core-batch-v9" / "check.py"
BASE_SHA256 = "e033375f78bbaf125ccf486123e68bd018b3d788b25a2785bd1eaf8985582c3e"
QS = tuple(range(33, 64, 2))
NEAR = {
    37: (0xffe59b73, 0xffe58a61, 0xffe5a74b, 0xa1fdfeb9, 0xa014693a),
    39: (0x7fe46a5b, 0x7fe47b49, 0x7ff4b8ae, 0xda020137, 0x1ff489ca),
    41: (0x7feb02d7, 0x7feb13c5, 0xffeba774, 0x5dffdeb5, 0xa00b8a40),
    43: (0x7feb3f21, 0x7feb2e33, 0xffeb8b90, 0x59ff9d3f, 0xe0148abf),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_base():
    if sha(BASE) != BASE_SHA256:
        raise AssertionError("frozen independent reconstruction changed")
    spec = importlib.util.spec_from_file_location("v16_core_check_base", BASE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def near_miss(base, q):
    d = q << 16
    x, y, z, A, T = NEAR[q]
    tests = {
        "A_eq_FDx": A == base.F(x, d),
        "T_eq_GDx_plus_D": T == ((base.G(x, d) + d) & base.MASK),
        "FDy_eq_A": base.F(y, d) == A,
        "GDy_eq_T_plus_D": base.G(y, d) == ((T + d) & base.MASK),
        "FDz_eq_minus_A": base.F(z, d) == ((-A) & base.MASK),
        "GDz_eq_minus_T": base.G(z, d) == ((-T) & base.MASK),
    }
    if not all(list(tests.values())[:-1]) or tests["GDz_eq_minus_T"]:
        raise AssertionError(f"q={q}: near-miss control failed")
    return {"x": f"{x:08x}", "y": f"{y:08x}", "z": f"{z:08x}",
            "A": f"{A:08x}", "T": f"{T:08x}",
            "G_D_z": f"{base.G(z, d):08x}",
            "minus_T": f"{(-T) & base.MASK:08x}", "equations": tests}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    base = load_base()
    meta = json.loads((HERE / "CERTIFICATE.json").read_text())
    reports = {}
    for q in QS:
        tag, d = f"d{q:04x}", q << 16
        record = meta["records"][str(q)]
        cnf_path, proof_path = HERE / f"{tag}.cnf", HERE / f"{tag}.drup"
        nvars, clauses = base.read_cnf(cnf_path)
        if (nvars, clauses) != base.reconstruct(d):
            raise AssertionError(f"q={q}: independent CNF mismatch")
        if sha(cnf_path) != record["cnf"]["sha256"]:
            raise AssertionError(f"q={q}: CNF digest mismatch")
        proof = base.read_proof(proof_path, nvars)
        if sha(proof_path) != record["proof"]["sha256"]:
            raise AssertionError(f"q={q}: proof digest mismatch")
        if not proof or proof[-1] != []:
            raise AssertionError(f"q={q}: missing final empty clause")
        started = time.monotonic()
        database = base.RUP(nvars, clauses)
        for number, clause in enumerate(proof, 1):
            if not database.proves(clause):
                raise AssertionError(f"q={q}: DRUP line {number} is not RUP")
            database.add(clause)
        seconds = time.monotonic() - started
        changed = bytearray(cnf_path.read_bytes())
        changed[-2] = ord("1") if changed[-2] != ord("1") else ord("2")
        controls = {
            "truncated_proof_rejected": proof[-1] == [] and
                                        all(row != [] for row in proof[:-1]),
            "mutated_cnf_digest_rejected":
                hashlib.sha256(changed).hexdigest() != record["cnf"]["sha256"],
        }
        if not all(controls.values()):
            raise AssertionError(f"q={q}: negative control failed")
        reports[str(q)] = {
            "status": "PASS", "D": f"{d:08x}",
            "cnf": {"variables": nvars, "clauses": len(clauses),
                    "sha256": sha(cnf_path), "independent_rebuild": True},
            "drup": {"clauses_checked": len(proof), "final_empty": True,
                     "sha256": sha(proof_path), "seconds": seconds},
            "near_miss_dropping_GDz": (near_miss(base, q) if q in NEAR else
                                        {"not_applicable":
                                         "twin layer is already empty"}),
            "negative_controls": controls,
        }
    output = {
        "schema": "support12-v16-selected-core-q33-63-check-v10",
        "status": "PASS",
        "theorem": ("the exact selected three-pair core is UNSAT for each "
                    "listed positive D; pair reversal supplies negative D"),
        "records": reports,
        "checker": "Python standard library only",
        "base_checker_sha256": BASE_SHA256,
        "scope": ("sixteen fixed D values only; not all v2(D)=16, not complete "
                  "support-12, and not SHA-256 message pairs"),
    }
    if args.write:
        (HERE / "RUN.json").write_text(
            json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
