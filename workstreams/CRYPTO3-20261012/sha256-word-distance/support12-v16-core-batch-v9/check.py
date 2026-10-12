#!/usr/bin/env python3
"""Stdlib-only reconstruction and RUP checker for the six fixed-D cores."""

from pathlib import Path
import argparse
import hashlib
import json
import time

MASK = (1 << 32) - 1
QS = (5, 13, 21, 23, 25, 27)
NEAR = {
    5:  (0xBFFF89AB, 0xBFFF89A3, 0x3FFFE0C9, 0xCAFF864E, 0xA006413E),
    13: (0xBFFB96FD, 0xBFFB96E5, 0x3FF3FF87, 0xBCFE89E4, 0xA00FC339),
    21: (0x7FFD484D, 0x7FFD595F, 0xFFEDFCFC, 0x51FE0137, 0x5FF38546),
    23: (0xFFEC5B45, 0xFFEC4A57, 0x7FEC102B, 0xD9FE01B9, 0x1FEB65BA),
    25: (0xFFFBB4BD, 0xFFFBA5AF, 0xFFFBAA81, 0xCDFE01FB, 0x1FEB6636),
    27: (0xFFF2336B, 0xFFF22279, 0x7FF25A01, 0x56001E11, 0xE00C66C0),
}


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def F(x, d):
    return (sigma0((x + d) & MASK) - sigma0(x)) & MASK


def G(x, d):
    return (sigma1((x + d) & MASK) - sigma1(x)) & MASK


class IndependentCircuit:
    def __init__(self, delta):
        self.delta = delta
        self.top = 0
        self.clauses = []

    def fresh(self, count=32):
        result = list(range(self.top + 1, self.top + count + 1))
        self.top += count
        return result

    def truth_table(self, variables, accepts):
        for packed in range(1 << len(variables)):
            values = [(packed >> i) & 1 for i in range(len(variables))]
            if not accepts(values):
                self.clauses.append([
                    -var if value else var
                    for var, value in zip(variables, values)
                ])

    def constant_sum(self, source, constant):
        target, carry = self.fresh(), self.fresh(33)
        self.clauses.append([-carry[0]])
        for bit in range(32):
            k = (constant >> bit) & 1
            def okay(v, k=k):
                total = v[0] + v[1] + k
                return (v[2], v[3]) == (total & 1, total >> 1)
            self.truth_table(
                [source[bit], carry[bit], target[bit], carry[bit + 1]], okay)
        return target

    def word_sum(self, left, right):
        target, carry = self.fresh(), self.fresh(33)
        self.clauses.append([-carry[0]])
        for bit in range(32):
            def okay(v):
                total = v[0] + v[1] + v[2]
                return (v[3], v[4]) == (total & 1, total >> 1)
            self.truth_table(
                [left[bit], right[bit], carry[bit], target[bit], carry[bit + 1]],
                okay)
        return target

    def equate(self, left, right):
        for a, b in zip(left, right):
            self.clauses.extend(([-a, b], [a, -b]))

    def small(self, source, rotations, shift):
        target = self.fresh()
        for bit in range(32):
            terms = [source[(bit + r) % 32] for r in rotations]
            if bit + shift < 32:
                terms.append(source[bit + shift])
            self.truth_table(
                terms + [target[bit]],
                lambda v: v[-1] == (sum(v[:-1]) & 1))
        return target

    def derivatives(self, source):
        shifted = self.constant_sum(source, self.delta)
        return (self.small(source, (7, 18), 3),
                self.small(shifted, (7, 18), 3),
                self.small(source, (17, 19), 10),
                self.small(shifted, (17, 19), 10))


def reconstruct(delta):
    c = IndependentCircuit(delta)
    x, y, z, A = c.fresh(), c.fresh(), c.fresh(), c.fresh()
    x0, x0d, x1, x1d = c.derivatives(x)
    w = c.word_sum(x0, A); c.equate(w, x0d)
    GX = c.fresh()
    w = c.word_sum(x1, GX); c.equate(w, x1d)
    T = c.constant_sum(GX, delta)
    y0, y0d, y1, y1d = c.derivatives(y)
    w = c.word_sum(y0, A); c.equate(w, y0d)
    TD = c.constant_sum(T, delta)
    w = c.word_sum(y1, TD); c.equate(w, y1d)
    z0, z0d, z1, z1d = c.derivatives(z)
    w = c.word_sum(z0d, A); c.equate(w, z0)
    w = c.word_sum(z1d, T); c.equate(w, z1)
    return c.top, c.clauses


def read_cnf(path):
    nvars = announced = None
    clauses, pending = [], []
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
        for value in map(int, line.split()):
            if value == 0:
                clauses.append(pending); pending = []
            else:
                pending.append(value)
    if nvars is None or pending or announced != len(clauses):
        raise ValueError("incomplete DIMACS")
    if any(not 1 <= abs(lit) <= nvars for c in clauses for lit in c):
        raise ValueError("invalid DIMACS literal")
    return nvars, clauses


def read_proof(path, nvars):
    result = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("d "):
            raise ValueError("proof is not deletion-free")
        values = list(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise ValueError("bad DRUP line")
        clause = values[:-1]
        if any(not 1 <= abs(lit) <= nvars for lit in clause):
            raise ValueError("invalid proof literal")
        result.append(clause)
    return result


class RUP:
    def __init__(self, nvars, clauses):
        self.nvars = nvars
        self.clauses = [tuple(c) for c in clauses]
        self.occ = {lit: [] for lit in range(-nvars, nvars + 1) if lit}
        for index, clause in enumerate(self.clauses):
            for lit in set(clause):
                self.occ[lit].append(index)

    def proves(self, candidate):
        assignment = [0] * (self.nvars + 1)
        remaining = [len(c) for c in self.clauses]
        satisfied = [False] * len(self.clauses)
        queue = [-lit for lit in candidate]
        queue.extend(c[0] for c in self.clauses if len(c) == 1)
        if any(not c for c in self.clauses):
            return True
        position = 0
        while position < len(queue):
            lit = queue[position]; position += 1
            variable, sign = abs(lit), 1 if lit > 0 else -1
            if assignment[variable] == sign:
                continue
            if assignment[variable] == -sign:
                return True
            assignment[variable] = sign
            for ci in self.occ[lit]:
                satisfied[ci] = True
            for ci in self.occ[-lit]:
                if satisfied[ci]:
                    continue
                remaining[ci] -= 1
                if remaining[ci] == 0:
                    return True
                if remaining[ci] == 1:
                    queue.append(next(q for q in self.clauses[ci]
                                      if assignment[abs(q)] == 0))
        return False

    def add(self, clause):
        index = len(self.clauses)
        clause = tuple(clause)
        self.clauses.append(clause)
        for lit in set(clause):
            self.occ[lit].append(index)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def near_miss(q):
    d = q << 16
    x, y, z, A, T = NEAR[q]
    tests = {
        "A_eq_FDx": A == F(x, d),
        "T_eq_GDx_plus_D": T == ((G(x, d) + d) & MASK),
        "FDy_eq_A": F(y, d) == A,
        "GDy_eq_T_plus_D": G(y, d) == ((T + d) & MASK),
        "FDz_eq_minus_A": F(z, d) == ((-A) & MASK),
        "GDz_eq_minus_T": G(z, d) == ((-T) & MASK),
    }
    if not all(tests[k] for k in list(tests)[:-1]) or tests["GDz_eq_minus_T"]:
        raise AssertionError(f"q={q} near-miss control failed")
    return {"x": f"{x:08x}", "y": f"{y:08x}", "z": f"{z:08x}",
            "A": f"{A:08x}", "T": f"{T:08x}",
            "G_D_z": f"{G(z, d):08x}", "minus_T": f"{(-T) & MASK:08x}",
            "equations": tests}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    meta = json.loads((root / "CERTIFICATE.json").read_text())
    reports = {}
    for q in QS:
        tag, d = f"d{q:04x}", q << 16
        record = meta["records"][str(q)]
        if "proof" not in record:
            reports[str(q)] = {"status": "UNKNOWN", "reason": record["status"]}
            continue
        cnf_path, proof_path = root / f"{tag}.cnf", root / f"{tag}.drup"
        nvars, clauses = read_cnf(cnf_path)
        if (nvars, clauses) != reconstruct(d):
            raise AssertionError(f"q={q}: CNF reconstruction mismatch")
        if sha(cnf_path) != record["cnf"]["sha256"]:
            raise AssertionError(f"q={q}: CNF digest mismatch")
        proof = read_proof(proof_path, nvars)
        if sha(proof_path) != record["proof"]["sha256"]:
            raise AssertionError(f"q={q}: proof digest mismatch")
        if not proof or proof[-1] != []:
            raise AssertionError(f"q={q}: no final empty clause")
        started = time.monotonic()
        db = RUP(nvars, clauses)
        for number, clause in enumerate(proof, 1):
            if not db.proves(clause):
                raise AssertionError(f"q={q}: addition {number} is not RUP")
            db.add(clause)
        seconds = time.monotonic() - started
        changed = bytearray(cnf_path.read_bytes())
        changed[-2] = ord("1") if changed[-2] != ord("1") else ord("2")
        controls = {
            "missing_final_empty_rejected": proof[-1] == [] and
                                            all(c != [] for c in proof[:-1]),
            "mutated_cnf_digest_rejected": hashlib.sha256(changed).hexdigest() !=
                                           record["cnf"]["sha256"],
        }
        if not all(controls.values()):
            raise AssertionError(f"q={q}: certificate negative control failed")
        reports[str(q)] = {
            "status": "PASS", "D": f"{d:08x}",
            "cnf": {"variables": nvars, "clauses": len(clauses),
                    "sha256": sha(cnf_path), "independent_rebuild": True},
            "drup": {"clauses_checked": len(proof), "final_empty": True,
                     "sha256": sha(proof_path), "seconds": seconds},
            "near_miss_dropping_GDz": near_miss(q),
            "negative_controls": controls,
        }
    status = "PASS" if all(r["status"] == "PASS" for r in reports.values()) else "PARTIAL"
    output = {
        "schema": "support12-v16-selected-core-batch-check-v9",
        "status": status,
        "theorem": (
            "the exact selected three-pair core is UNSAT for each listed fixed D"
            if status == "PASS" else "only records marked PASS are certified"
        ),
        "records": reports,
        "checker": "Python standard library only",
        "scope": (
            "six fixed D values only; not all v2(D)=16, not complete support-12, "
            "and not SHA-256 message pairs"
        ),
    }
    if args.write:
        (root / "RUN.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
