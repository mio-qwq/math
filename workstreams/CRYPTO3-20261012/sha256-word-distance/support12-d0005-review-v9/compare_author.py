#!/usr/bin/env python3
"""Independent exact-formula, proof, metadata, and manifest audit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import independent as ind

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-d0005-v9"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ExactLayout:
    """Independent reconstruction using the author's published variable layout."""

    def __init__(self) -> None:
        self.nv = 0
        self.clauses: list[tuple[int, ...]] = []

    def alloc(self, count: int) -> list[int]:
        ans = list(range(self.nv + 1, self.nv + count + 1))
        self.nv += count
        return ans

    def relation(self, variables: list[int], predicate) -> None:
        for values in itertools.product((False, True), repeat=len(variables)):
            if not predicate(*values):
                self.clauses.append(tuple(v if not b else -v for v, b in zip(variables, values)))

    def add_constant(self, src: list[int], constant: int) -> list[int]:
        dst = self.alloc(32)
        carry = self.alloc(33)
        self.clauses.append((-carry[0],))
        for i in range(32):
            k = (constant >> i) & 1
            self.relation(
                [src[i], carry[i], dst[i], carry[i + 1]],
                lambda x, c, y, cn, k=k: y == ((x + c + k) & 1) and cn == ((x + c + k) >> 1),
            )
        return dst

    def sigma(self, src: list[int], rotations: tuple[int, int], shift: int) -> list[int]:
        dst = self.alloc(32)
        for i in range(32):
            inputs = [src[(i + r) % 32] for r in rotations]
            if i + shift < 32:
                inputs.append(src[i + shift])
            self.relation(inputs + [dst[i]], lambda *v: v[-1] == (sum(v[:-1]) & 1))
        return dst

    def equal(self, left: list[int], right: list[int]) -> None:
        for a, b in zip(left, right):
            self.clauses.extend(((-a, b), (a, -b)))


def expected_formula(kind: str) -> ExactLayout:
    c = ExactLayout()
    x = c.alloc(32)
    if kind == "reciprocal":
        y = c.add_constant(x, ind.A)
        fx = c.sigma(x, (7, 18), 3)
        fy = c.sigma(y, (7, 18), 3)
        c.equal(c.add_constant(fx, ind.D), fy)
    elif kind == "third_image":
        y = c.add_constant(x, ind.D)
        fx = c.sigma(x, (7, 18), 3)
        fy = c.sigma(y, (7, 18), 3)
        gx = c.sigma(x, (17, 19), 10)
        gy = c.sigma(y, (17, 19), 10)
        c.equal(c.add_constant(fx, (-ind.A) & ind.MASK), fy)
        c.equal(c.add_constant(gx, (-ind.T) & ind.MASK), gy)
    else:
        raise ValueError(kind)
    return c


def clause_multiset(clauses) -> Counter:
    return Counter(tuple(sorted(set(clause), key=lambda z: (abs(z), z < 0))) for clause in clauses)


def verify_manifest() -> dict:
    manifest = json.loads((AUTHOR / "SHA256.json").read_text())
    assert manifest["self_excluded"] == "SHA256.json"
    actual_names = sorted(p.name for p in AUTHOR.iterdir() if p.is_file() and p.name != "SHA256.json")
    assert actual_names == sorted(manifest["files"])
    for name, record in manifest["files"].items():
        path = AUTHOR / name
        assert path.stat().st_size == record["bytes"]
        assert digest(path) == record["sha256"]
    return {"files_checked": len(actual_names), "self_excluded": "SHA256.json", "all_hashes_and_sizes_match": True}


def verify_one(stem: str, cert: dict) -> dict:
    cnf_path = AUTHOR / f"{stem}.cnf"
    proof_path = AUTHOR / f"{stem}.drup"
    nv, clauses = ind.parse_dimacs(cnf_path)
    rebuilt = expected_formula(stem)
    assert nv == rebuilt.nv
    assert clause_multiset(clauses) == clause_multiset(rebuilt.clauses)

    proof = proof_path.read_text(encoding="ascii").splitlines()
    proof_check = ind.DRUPChecker(nv, clauses).run(proof)
    assert proof and proof[-1].strip() == "0"
    assert len(proof) == cert["proof"]["added_clauses"]
    assert nv == cert["cnf"]["variables"] and len(clauses) == cert["cnf"]["clauses"]
    assert digest(cnf_path) == cert["cnf"]["sha256"]
    assert digest(proof_path) == cert["proof"]["sha256"]

    truncated_rejected = flipped_first_rejected = False
    try:
        ind.DRUPChecker(nv, clauses).run(proof[:-1])
    except (AssertionError, ValueError):
        truncated_rejected = True
    first = [int(x) for x in proof[0].split()[:-1]]
    damaged = [-first[0]] + first[1:]
    flipped_first_rejected = not ind.DRUPChecker(nv, clauses).rup(damaged)
    assert truncated_rejected and flipped_first_rejected

    return {
        "variables": nv,
        "clauses": len(clauses),
        "cnf_sha256": digest(cnf_path),
        "exact_independent_clause_multiset_rebuild": True,
        "drup_sha256": digest(proof_path),
        "drup": proof_check,
        "negative_controls": {
            "truncated_final_empty_rejected": truncated_rejected,
            "flipped_first_proof_literal_rejected": flipped_first_rejected,
        },
    }


def orientation() -> dict:
    q = 0x0FFB000E
    q1 = (q + ind.D) & ind.MASK
    q_forward = (ind.D, ind.derivative(ind.f, q, ind.D), ind.derivative(ind.g, q, ind.D))
    q_reverse = tuple((-v) & ind.MASK for v in q_forward)
    required_negative = ((-ind.D) & ind.MASK, ind.A, ind.T)
    required_forward = (ind.D, (-ind.A) & ind.MASK, (-ind.T) & ind.MASK)
    assert q_forward == (ind.D, ind.A, ind.T)
    assert q_reverse == ((-ind.D) & ind.MASK, (-ind.A) & ind.MASK, (-ind.T) & ind.MASK)
    assert q_reverse != required_negative
    return {
        "Q_words": [f"{q:08x}", f"{q1:08x}"],
        "Q_forward": [f"{v:08x}" for v in q_forward],
        "Q_reverse": [f"{v:08x}" for v in q_reverse],
        "required_R_orientation": [f"{v:08x}" for v in required_negative],
        "equivalent_required_forward_image": [f"{v:08x}" for v in required_forward],
        "candidate_sign_correction": "ACCEPT",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    cert = json.loads((AUTHOR / "CERTIFICATE.json").read_text())
    assert cert["constants"] == {"A": "40406e02", "D": "00050000", "T": "1ffd913e"}
    result = {
        "schema": "support12-d0005-author-comparison-v9",
        "author_manifest": verify_manifest(),
        "orientation": orientation(),
        "author_artifacts": {
            "third_image": verify_one("third_image", cert["claims"]["third_image"]),
            "reciprocal": verify_one("reciprocal", cert["claims"]["reciprocal"]),
        },
        "independent_rebuild": json.loads((HERE / "INDEPENDENT_RUN.json").read_text()),
        "verdicts": {
            "candidate_sign_correction": "ACCEPT",
            "fixed_third_image_UNSAT": "ACCEPT",
            "fixed_reciprocal_UNSAT": "ACCEPT",
        },
        "scope_exclusions": ["other q=5 A", "full support", "message", "distance14"],
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    path = HERE / "COMPARISON.json"
    if args.write:
        path.write_text(encoded, encoding="utf-8", newline="\n")
    else:
        assert path.read_text(encoding="utf-8") == encoded
    print(encoded, end="")


if __name__ == "__main__":
    main()
