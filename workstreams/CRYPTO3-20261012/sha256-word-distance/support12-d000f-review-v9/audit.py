#!/usr/bin/env python3
"""Independent author-artifact audit for the fixed-D three-pair core."""

from __future__ import annotations

import hashlib
import json
import platform
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-d000f-v9"
MASK = (1 << 32) - 1
D = 0x000F0000


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def s0(x: int) -> int:
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def s1(x: int) -> int:
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def deriv(fn, x: int) -> int:
    return (fn((x + D) & MASK) - fn(x)) & MASK


class Reconstruction:
    """Clause reconstruction with no imports from the author package."""

    def __init__(self) -> None:
        self.top = 0
        self.clauses: list[list[int]] = []

    def block(self, count: int = 32) -> list[int]:
        ans = list(range(self.top + 1, self.top + count + 1))
        self.top += count
        return ans

    def truth_relation(self, variables: list[int], valid) -> None:
        for packed in range(1 << len(variables)):
            values = tuple((packed >> bit) & 1 for bit in range(len(variables)))
            if not valid(values):
                self.clauses.append([
                    -var if value else var
                    for var, value in zip(variables, values)
                ])

    def constant_add(self, source: list[int], constant: int) -> list[int]:
        out, carry = self.block(), self.block(33)
        self.clauses.append([-carry[0]])
        for bit in range(32):
            k = (constant >> bit) & 1
            self.truth_relation(
                [source[bit], carry[bit], out[bit], carry[bit + 1]],
                lambda v, k=k: (v[2] == ((v[0] + v[1] + k) & 1)
                                  and v[3] == ((v[0] + v[1] + k) >> 1)),
            )
        return out

    def word_add(self, left: list[int], right: list[int]) -> list[int]:
        out, carry = self.block(), self.block(33)
        self.clauses.append([-carry[0]])
        for bit in range(32):
            self.truth_relation(
                [left[bit], right[bit], carry[bit], out[bit], carry[bit + 1]],
                lambda v: (v[3] == ((v[0] + v[1] + v[2]) & 1)
                           and v[4] == ((v[0] + v[1] + v[2]) >> 1)),
            )
        return out

    def equivalent(self, left: list[int], right: list[int]) -> None:
        for a, b in zip(left, right):
            self.clauses += [[-a, b], [a, -b]]

    def sigma(self, source: list[int], rotations: tuple[int, int], shift: int) -> list[int]:
        out = self.block()
        for bit in range(32):
            inputs = [source[(bit + r) % 32] for r in rotations]
            if bit + shift < 32:
                inputs.append(source[bit + shift])
            self.truth_relation(
                inputs + [out[bit]],
                lambda v: v[-1] == (sum(v[:-1]) & 1),
            )
        return out

    def context(self, source: list[int]):
        shifted = self.constant_add(source, D)
        return (self.sigma(source, (7, 18), 3),
                self.sigma(shifted, (7, 18), 3),
                self.sigma(source, (17, 19), 10),
                self.sigma(shifted, (17, 19), 10))


def reconstruct() -> Reconstruction:
    q = Reconstruction()
    x, y, z, A = q.block(), q.block(), q.block(), q.block()
    x0, x0d, x1, x1d = q.context(x)
    q.equivalent(q.word_add(x0, A), x0d)
    gx = q.block()
    q.equivalent(q.word_add(x1, gx), x1d)
    T = q.constant_add(gx, D)
    y0, y0d, y1, y1d = q.context(y)
    q.equivalent(q.word_add(y0, A), y0d)
    TD = q.constant_add(T, D)
    q.equivalent(q.word_add(y1, TD), y1d)
    z0, z0d, z1, z1d = q.context(z)
    q.equivalent(q.word_add(z0d, A), z0)
    q.equivalent(q.word_add(z1d, T), z1)
    return q


def parse_cnf(path: Path) -> tuple[int, list[list[int]]]:
    nvars = expected = None
    clauses: list[list[int]] = []
    pending: list[int] = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            fields = line.split()
            if fields[:2] != ["p", "cnf"] or len(fields) != 4 or nvars is not None:
                raise ValueError("invalid or repeated DIMACS header")
            nvars, expected = map(int, fields[2:])
            continue
        if nvars is None:
            raise ValueError("clause precedes DIMACS header")
        for token in map(int, line.split()):
            if token:
                if abs(token) > nvars:
                    raise ValueError("out-of-range CNF literal")
                pending.append(token)
            else:
                clauses.append(pending)
                pending = []
    if nvars is None or pending or len(clauses) != expected:
        raise ValueError("incomplete CNF")
    return nvars, clauses


def parse_proof(path: Path, nvars: int) -> list[list[int]]:
    additions = []
    for number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("d "):
            raise ValueError(f"deletion at proof line {number}")
        values = list(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise ValueError(f"malformed proof line {number}")
        if any(abs(x) > nvars for x in values[:-1]):
            raise ValueError(f"out-of-range proof literal at line {number}")
        additions.append(values[:-1])
    return additions


class WatchedRUP:
    """Independent two-watched-literal deletion-free RUP verifier."""

    def __init__(self, nvars: int, clauses: list[list[int]]) -> None:
        self.nvars = nvars
        self.clauses: list[tuple[int, ...]] = []
        self.watch_pos: list[list[int]] = []
        self.watch: dict[int, list[int]] = {}
        self.units: list[int] = []
        self.has_empty = False
        for clause in clauses:
            self.add(clause)

    def add(self, clause: list[int]) -> None:
        item = tuple(clause)
        ci = len(self.clauses)
        self.clauses.append(item)
        if not item:
            self.watch_pos.append([])
            self.has_empty = True
        elif len(item) == 1:
            self.watch_pos.append([0])
            self.units.append(item[0])
        else:
            self.watch_pos.append([0, 1])
            self.watch.setdefault(item[0], []).append(ci)
            self.watch.setdefault(item[1], []).append(ci)

    @staticmethod
    def lit_value(lit: int, values: list[int]) -> int:
        value = values[abs(lit)]
        return value if lit > 0 else -value

    def check(self, candidate: list[int]) -> bool:
        if self.has_empty:
            return True
        values = [0] * (self.nvars + 1)
        trail: list[int] = []

        def assign(lit: int) -> bool:
            want = 1 if lit > 0 else -1
            old = values[abs(lit)]
            if old == -want:
                return False
            if old == 0:
                values[abs(lit)] = want
                trail.append(lit)
            return True

        for lit in candidate:
            if not assign(-lit):
                return True
        for lit in self.units:
            if not assign(lit):
                return True

        head = 0
        while head < len(trail):
            falsified = -trail[head]
            head += 1
            bucket = self.watch.get(falsified, [])
            cursor = 0
            while cursor < len(bucket):
                ci = bucket[cursor]
                clause = self.clauses[ci]
                positions = self.watch_pos[ci]
                watched_slot = 0 if clause[positions[0]] == falsified else 1
                other_pos = positions[1 - watched_slot]
                other = clause[other_pos]
                if self.lit_value(other, values) == 1:
                    cursor += 1
                    continue
                replacement = None
                for pos, lit in enumerate(clause):
                    if pos not in positions and self.lit_value(lit, values) != -1:
                        replacement = pos
                        break
                if replacement is not None:
                    positions[watched_slot] = replacement
                    bucket[cursor] = bucket[-1]
                    bucket.pop()
                    self.watch.setdefault(clause[replacement], []).append(ci)
                    continue
                if self.lit_value(other, values) == -1:
                    return True
                if not assign(other):
                    return True
                cursor += 1
        return False


def check_witness(values: dict[str, int]) -> dict[str, bool | str]:
    x, y, z, A, T = (values[k] for k in ("x", "y", "z", "A", "T"))
    equations = {
        "A=F_D(x)": A == deriv(s0, x),
        "T=G_D(x)+D": T == ((deriv(s1, x) + D) & MASK),
        "F_D(y)=A": deriv(s0, y) == A,
        "G_D(y)=T+D": deriv(s1, y) == ((T + D) & MASK),
        "F_D(z)=-A": deriv(s0, z) == ((-A) & MASK),
        "G_D(z)=-T": deriv(s1, z) == ((-T) & MASK),
    }
    return {**equations, "G_D(z)": f"{deriv(s1, z):08x}",
            "-T": f"{(-T) & MASK:08x}"}


def main() -> None:
    cnf_path, proof_path = AUTHOR / "fourpair.cnf", AUTHOR / "fourpair.drup"
    manifest = json.loads((AUTHOR / "SHA256.json").read_text())
    manifest_ok = all(sha(AUTHOR / name) == digest
                      for name, digest in manifest["files"].items())
    nvars, clauses = parse_cnf(cnf_path)
    rebuilt = reconstruct()
    exact_reconstruction = nvars == rebuilt.top and clauses == rebuilt.clauses
    if not manifest_ok or not exact_reconstruction:
        raise AssertionError("manifest or independent clause reconstruction failed")

    proof = parse_proof(proof_path, nvars)
    if not proof or proof[-1] or any(not clause for clause in proof[:-1]):
        raise AssertionError("proof does not have one final empty clause")
    damaged = proof[0].copy()
    damaged[5] = -damaged[5]
    damaged_addition_rejected = not WatchedRUP(nvars, clauses).check(damaged)
    truncated_rejected = not any(not clause for clause in proof[:-1])
    if not damaged_addition_rejected or not truncated_rejected:
        raise AssertionError("proof negative control failed")
    started = time.monotonic()
    checker = WatchedRUP(nvars, clauses)
    for index, clause in enumerate(proof, 1):
        if not checker.check(clause):
            raise AssertionError(f"proof addition {index} is not RUP")
        checker.add(clause)
    proof_seconds = time.monotonic() - started

    author_witness = {"x": 0x5FF2E1BE, "y": 0x5FF2E1A6,
                      "z": 0x9FF20041, "A": 0x398179EC, "T": 0xA000E3B9}
    independent_witness = {"x": 0x3FFEB7FF, "y": 0x3FFEB7E7,
                           "z": 0x3FF28BDF, "A": 0x46FE9924, "T": 0xE00FC3BD}
    controls = {
        "author": check_witness(author_witness),
        "independent": check_witness(independent_witness),
    }
    for result in controls.values():
        if not all(result[name] for name in list(result)[:5]) or result["G_D(z)=-T"]:
            raise AssertionError("near-miss control failed")

    report = {
        "status": "ACCEPT",
        "scope": "fixed D=000f0000 selected local three-pair UNSAT only",
        "environment": {"python": platform.python_version()},
        "manifest_all_files_match": manifest_ok,
        "cnf": {"variables": nvars, "clauses": len(clauses),
                "sha256": sha(cnf_path), "exact_independent_reconstruction": exact_reconstruction},
        "proof": {"format": "deletion-free DRUP", "additions": len(proof),
                  "only_final_clause_empty": True, "all_additions_rup": True,
                  "sha256": sha(proof_path), "seconds": proof_seconds,
                  "checker": "independent two-watched-literal Python verifier",
                  "negative_controls": {
                      "truncated_before_final_empty_rejected": truncated_rejected,
                      "first_addition_literal_6_flipped_rejected": damaged_addition_rejected,
                  }},
        "near_miss_controls": controls,
        "limitations": ["no full support-12 inference", "no message-pair inference",
                        "no distance-14 inference"],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
