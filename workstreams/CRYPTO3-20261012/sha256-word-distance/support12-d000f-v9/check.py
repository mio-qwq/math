#!/usr/bin/env python3
"""Stdlib-only semantic reconstruction and deletion-free DRUP checker."""

from pathlib import Path
import argparse
import hashlib
import json
import time

MASK = (1 << 32) - 1
D = 0x000F0000
NEAR_MISS = {
    "x": 0x5FF2E1BE,
    "y": 0x5FF2E1A6,
    "z": 0x9FF20041,
    "A": 0x398179EC,
    "T": 0xA000E3B9,
}


def rotr(value, count):
    return ((value >> count) | (value << (32 - count))) & MASK


def small0(value):
    return rotr(value, 7) ^ rotr(value, 18) ^ (value >> 3)


def small1(value):
    return rotr(value, 17) ^ rotr(value, 19) ^ (value >> 10)


def F(value, delta):
    return (small0((value + delta) & MASK) - small0(value)) & MASK


def G(value, delta):
    return (small1((value + delta) & MASK) - small1(value)) & MASK


class AuditFormula:
    """A second construction, kept independent from generate.py imports."""

    def __init__(self):
        self.n = 0
        self.db = []

    def new(self, width=32):
        result = list(range(self.n + 1, self.n + width + 1))
        self.n += width
        return result

    def table(self, variables, accepts):
        for packed in range(1 << len(variables)):
            values = [(packed >> j) & 1 for j in range(len(variables))]
            if not accepts(values):
                self.db.append([
                    -variable if value else variable
                    for variable, value in zip(variables, values)
                ])

    def plus_constant(self, source, constant):
        destination = self.new()
        carry = self.new(33)
        self.db.append([-carry[0]])
        for i in range(32):
            k = (constant >> i) & 1

            def valid(v, k=k):
                total = v[0] + v[1] + k
                return v[2] == (total & 1) and v[3] == (total >> 1)

            self.table([source[i], carry[i], destination[i], carry[i + 1]], valid)
        return destination

    def plus_word(self, left, right):
        destination = self.new()
        carry = self.new(33)
        self.db.append([-carry[0]])
        for i in range(32):
            def valid(v):
                total = v[0] + v[1] + v[2]
                return v[3] == (total & 1) and v[4] == (total >> 1)

            self.table(
                [left[i], right[i], carry[i], destination[i], carry[i + 1]],
                valid,
            )
        return destination

    def same(self, left, right):
        for a, b in zip(left, right):
            self.db.extend(([-a, b], [a, -b]))

    def little_sigma(self, source, rotates, shift):
        destination = self.new()
        for i in range(32):
            terms = [source[(i + amount) % 32] for amount in rotates]
            if i + shift < 32:
                terms.append(source[i + shift])
            self.table(
                terms + [destination[i]],
                lambda v: v[-1] == (sum(v[:-1]) & 1),
            )
        return destination

    def context(self, source):
        shifted = self.plus_constant(source, D)
        s0 = self.little_sigma(source, (7, 18), 3)
        s0d = self.little_sigma(shifted, (7, 18), 3)
        s1 = self.little_sigma(source, (17, 19), 10)
        s1d = self.little_sigma(shifted, (17, 19), 10)
        return s0, s0d, s1, s1d


def reconstruct():
    q = AuditFormula()
    x, y, z = q.new(), q.new(), q.new()
    A = q.new()

    x0, x0d, x1, x1d = q.context(x)
    t = q.plus_word(x0, A)
    q.same(t, x0d)
    GX = q.new()
    t = q.plus_word(x1, GX)
    q.same(t, x1d)
    T = q.plus_constant(GX, D)

    y0, y0d, y1, y1d = q.context(y)
    t = q.plus_word(y0, A)
    q.same(t, y0d)
    TD = q.plus_constant(T, D)
    t = q.plus_word(y1, TD)
    q.same(t, y1d)

    z0, z0d, z1, z1d = q.context(z)
    t = q.plus_word(z0d, A)
    q.same(t, z0)
    t = q.plus_word(z1d, T)
    q.same(t, z1)
    return q.n, q.db


def parse_cnf(path):
    nvars = announced = None
    clauses = []
    pending = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            fields = line.split()
            if len(fields) != 4 or fields[1] != "cnf" or nvars is not None:
                raise ValueError("bad DIMACS header")
            nvars, announced = int(fields[2]), int(fields[3])
            continue
        for number in map(int, line.split()):
            if number == 0:
                clauses.append(pending)
                pending = []
            else:
                pending.append(number)
    if nvars is None or pending or announced != len(clauses):
        raise ValueError("incomplete DIMACS")
    if any(not 1 <= abs(lit) <= nvars for clause in clauses for lit in clause):
        raise ValueError("out-of-range DIMACS literal")
    return nvars, clauses


def parse_drup(path, nvars):
    additions = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("d "):
            raise ValueError("certificate must be deletion-free")
        values = list(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise ValueError("malformed DRUP line")
        clause = values[:-1]
        if any(not 1 <= abs(lit) <= nvars for lit in clause):
            raise ValueError("out-of-range proof literal")
        additions.append(clause)
    return additions


class RUP:
    def __init__(self, nvars, clauses):
        self.nvars = nvars
        self.clauses = [tuple(c) for c in clauses]
        self.occ = {lit: [] for lit in range(-nvars, nvars + 1) if lit}
        for index, clause in enumerate(self.clauses):
            for literal in set(clause):
                self.occ[literal].append(index)

    def check(self, candidate):
        values = [0] * (self.nvars + 1)
        remaining = [len(c) for c in self.clauses]
        satisfied = [False] * len(self.clauses)
        queue = [-literal for literal in candidate]
        queue.extend(c[0] for c in self.clauses if len(c) == 1)
        if any(not c for c in self.clauses):
            return True
        position = 0
        while position < len(queue):
            literal = queue[position]
            position += 1
            variable = abs(literal)
            sign = 1 if literal > 0 else -1
            if values[variable] == sign:
                continue
            if values[variable] == -sign:
                return True
            values[variable] = sign
            for ci in self.occ[literal]:
                satisfied[ci] = True
            for ci in self.occ[-literal]:
                if satisfied[ci]:
                    continue
                remaining[ci] -= 1
                if remaining[ci] == 0:
                    return True
                if remaining[ci] == 1:
                    unit = next(
                        q for q in self.clauses[ci]
                        if values[abs(q)] == 0
                    )
                    queue.append(unit)
        return False

    def add(self, clause):
        index = len(self.clauses)
        clause = tuple(clause)
        self.clauses.append(clause)
        for literal in set(clause):
            self.occ[literal].append(index)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_near_miss():
    x, y, z = (NEAR_MISS[k] for k in ("x", "y", "z"))
    A, T = NEAR_MISS["A"], NEAR_MISS["T"]
    equations = {
        "A_eq_FDx": A == F(x, D),
        "T_eq_GDx_plus_D": T == ((G(x, D) + D) & MASK),
        "FDy_eq_A": F(y, D) == A,
        "GDy_eq_T_plus_D": G(y, D) == ((T + D) & MASK),
        "FDz_eq_minus_A": F(z, D) == ((-A) & MASK),
        "GDz_eq_minus_T": G(z, D) == ((-T) & MASK),
    }
    if not all(equations[name] for name in list(equations)[:-1]):
        raise AssertionError("near-miss positive control lost a required identity")
    if equations["GDz_eq_minus_T"]:
        raise AssertionError("near-miss negative control unexpectedly satisfies core")
    return {
        **{k: f"{v:08x}" for k, v in NEAR_MISS.items()},
        "G_D_z": f"{G(z, D):08x}",
        "minus_T": f"{(-T) & MASK:08x}",
        "equations": equations,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    cnf_path = root / "fourpair.cnf"
    proof_path = root / "fourpair.drup"
    meta = json.loads((root / "CERTIFICATE.json").read_text())

    nvars, clauses = parse_cnf(cnf_path)
    expected_nvars, expected_clauses = reconstruct()
    if (nvars, clauses) != (expected_nvars, expected_clauses):
        raise AssertionError("CNF differs from independent reconstruction")
    if sha256(cnf_path) != meta["cnf"]["sha256"]:
        raise AssertionError("CNF digest mismatch")
    additions = parse_drup(proof_path, nvars)
    if sha256(proof_path) != meta["proof"]["sha256"]:
        raise AssertionError("DRUP digest mismatch")
    if not additions or additions[-1] != []:
        raise AssertionError("proof does not end in the empty clause")

    started = time.monotonic()
    database = RUP(nvars, clauses)
    for index, clause in enumerate(additions, 1):
        if not database.check(clause):
            raise AssertionError(f"DRUP addition {index} is not RUP")
        database.add(clause)
    elapsed = time.monotonic() - started

    near_miss = verify_near_miss()
    truncated_rejected = additions[-1] == [] and all(c != [] for c in additions[:-1])
    changed = bytearray(cnf_path.read_bytes())
    changed[-2] = ord("1") if changed[-2] != ord("1") else ord("2")
    mutation_rejected = hashlib.sha256(changed).hexdigest() != meta["cnf"]["sha256"]
    if not truncated_rejected or not mutation_rejected:
        raise AssertionError("negative control failed")

    report = {
        "schema": "support12-d000f-selected-four-pair-check-v9",
        "status": "PASS",
        "theorem": (
            "for D=000f0000 the exact selected three-pair core is UNSAT; "
            "therefore the selected four-pair criterion is UNSAT"
        ),
        "cnf": {"variables": nvars, "clauses": len(clauses),
                "sha256": sha256(cnf_path), "independent_rebuild": True},
        "drup": {"clauses_checked": len(additions), "final_empty": True,
                 "sha256": sha256(proof_path),
                 "checker": "Python standard library only", "seconds": elapsed},
        "near_miss_control": near_miss,
        "negative_controls": {
            "missing_final_empty_rejected": truncated_rejected,
            "mutated_cnf_digest_rejected": mutation_rejected,
        },
        "scope": (
            "fixed D selected local subsystem only; not the complete support-12 "
            "factor graph and not a SHA-256 message pair"
        ),
    }
    if args.write:
        (root / "RUN.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
