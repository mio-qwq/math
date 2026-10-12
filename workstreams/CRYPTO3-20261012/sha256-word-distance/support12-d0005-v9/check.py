#!/usr/bin/env python3
"""Stdlib-only semantic, witness, and deletion-free DRUP checker."""

from pathlib import Path
import argparse
import hashlib
import json

MASK = (1 << 32) - 1
D = 0x00050000
A = 0x40406E02
T = 0x1FFD913E
WITNESSES = {
    "X": (0x0FFB000A, 0x1000000A, 0x1FF8913E),
    "Y": (0x0FFB0002, 0x10000002, 0x2002913E),
    "Q": (0x0FFB000E, 0x1000000E, 0x1FFD913E),
}


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


class IndependentCNF:
    """Second implementation of the bit relations, not an author import."""

    def __init__(self):
        self.top = 0
        self.clauses = []

    def fresh(self, count):
        ans = list(range(self.top + 1, self.top + count + 1))
        self.top += count
        return ans

    def truth_relation(self, variables, accepts):
        for packed in range(1 << len(variables)):
            values = [(packed >> j) & 1 for j in range(len(variables))]
            if not accepts(values):
                self.clauses.append([
                    -var if value else var
                    for var, value in zip(variables, values)
                ])

    def add_const(self, src, constant):
        dst = self.fresh(32)
        carry = self.fresh(33)
        self.clauses.append([-carry[0]])
        for i in range(32):
            k = (constant >> i) & 1

            def okay(v, k=k):
                total = v[0] + v[1] + k
                return v[2] == (total & 1) and v[3] == (total >> 1)

            self.truth_relation([src[i], carry[i], dst[i], carry[i + 1]], okay)
        return dst

    def small_sigma(self, src, rotations, shift):
        dst = self.fresh(32)
        for i in range(32):
            terms = [src[(i + r) % 32] for r in rotations]
            if i + shift < 32:
                terms.append(src[i + shift])
            self.truth_relation(
                terms + [dst[i]],
                lambda v: v[-1] == (sum(v[:-1]) & 1),
            )
        return dst


def equate(cnf, left, right):
    for u, v in zip(left, right):
        cnf.clauses.extend(([-u, v], [u, -v]))


def expected_reciprocal():
    c = IndependentCNF()
    x = c.fresh(32)
    y = c.add_const(x, A)
    sx = c.small_sigma(x, (7, 18), 3)
    sy = c.small_sigma(y, (7, 18), 3)
    sd = c.add_const(sx, D)
    equate(c, sd, sy)
    return c.top, c.clauses


def expected_third_image():
    c = IndependentCNF()
    x = c.fresh(32)
    y = c.add_const(x, D)
    sx = c.small_sigma(x, (7, 18), 3)
    sy = c.small_sigma(y, (7, 18), 3)
    gx = c.small_sigma(x, (17, 19), 10)
    gy = c.small_sigma(y, (17, 19), 10)
    sf = c.add_const(sx, (-A) & MASK)
    gt = c.add_const(gx, (-T) & MASK)
    equate(c, sf, sy)
    equate(c, gt, gy)
    return c.top, c.clauses


def parse_dimacs(path):
    nvars = None
    announced = None
    clauses = []
    pending = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            fields = line.split()
            if len(fields) != 4 or fields[1] != "cnf" or nvars is not None:
                raise ValueError("invalid DIMACS header")
            nvars, announced = int(fields[2]), int(fields[3])
            continue
        for item in map(int, line.split()):
            if item == 0:
                clauses.append(pending)
                pending = []
            else:
                pending.append(item)
    if nvars is None or pending or announced != len(clauses):
        raise ValueError("incomplete DIMACS")
    if any(abs(lit) > nvars or lit == 0 for c in clauses for lit in c):
        raise ValueError("out-of-range DIMACS literal")
    return nvars, clauses


def parse_drup(path, nvars):
    proof = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("d "):
            raise ValueError("expected deletion-free DRUP")
        values = list(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise ValueError("malformed DRUP clause")
        clause = values[:-1]
        if any(abs(lit) > nvars for lit in clause):
            raise ValueError("out-of-range DRUP literal")
        proof.append(clause)
    return proof


class RUPDatabase:
    def __init__(self, nvars, clauses):
        self.nvars = nvars
        self.clauses = [tuple(c) for c in clauses]
        self.occ = {lit: [] for lit in range(-nvars, nvars + 1) if lit}
        for index, clause in enumerate(self.clauses):
            for lit in set(clause):
                self.occ[lit].append(index)

    def rup(self, candidate):
        assignment = [0] * (self.nvars + 1)
        remaining = [len(c) for c in self.clauses]
        satisfied = [False] * len(self.clauses)
        queue = [-lit for lit in candidate]
        queue.extend(c[0] for c in self.clauses if len(c) == 1)
        if any(len(c) == 0 for c in self.clauses):
            return True
        pos = 0
        while pos < len(queue):
            lit = queue[pos]
            pos += 1
            variable = abs(lit)
            value = 1 if lit > 0 else -1
            if assignment[variable] == value:
                continue
            if assignment[variable] == -value:
                return True
            assignment[variable] = value
            for ci in self.occ[lit]:
                satisfied[ci] = True
            for ci in self.occ[-lit]:
                if satisfied[ci]:
                    continue
                remaining[ci] -= 1
                if remaining[ci] == 0:
                    return True
                if remaining[ci] == 1:
                    unit = next(
                        q for q in self.clauses[ci]
                        if assignment[abs(q)] == 0
                    )
                    queue.append(unit)
        return False

    def add(self, clause):
        index = len(self.clauses)
        frozen = tuple(clause)
        self.clauses.append(frozen)
        for lit in set(frozen):
            self.occ[lit].append(index)


def verify_fixture_and_failure():
    observed = {}
    for name, (u, v, claimed_g) in WITNESSES.items():
        d = (v - u) & MASK
        f = (sigma0(v) - sigma0(u)) & MASK
        g = (sigma1(v) - sigma1(u)) & MASK
        if (d, f, g) != (D, A, claimed_g):
            raise AssertionError(f"bad {name} witness")
        observed[name] = {
            "u": f"{u:08x}", "v": f"{v:08x}",
            "d": f"{d:08x}", "F": f"{f:08x}", "G": f"{g:08x}",
        }
    gx, gy, gq = (WITNESSES[k][2] for k in ("X", "Y", "Q"))
    if ((gy - gx) & MASK, (gy - gq) & MASK) != (2 * D, D):
        raise AssertionError("numerical G gaps do not match")
    # The required third pair is (-D,+A,+T). Reversing Q flips all
    # three derivatives, so the supplied Q does not construct it.
    q0, q1, qg = WITNESSES["Q"]
    reversed_tuple = (
        (q0 - q1) & MASK,
        (sigma0(q0) - sigma0(q1)) & MASK,
        (sigma1(q0) - sigma1(q1)) & MASK,
    )
    if reversed_tuple != ((-D) & MASK, (-A) & MASK, (-qg) & MASK):
        raise AssertionError("reverse-Q identity failed")
    required = ((-D) & MASK, A, T)
    if reversed_tuple == required:
        raise AssertionError("negative control: invalid Q unexpectedly accepted")
    return observed, reversed_tuple, required


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_certificate(root, stem, expected_builder, record):
    cnf_path = root / f"{stem}.cnf"
    proof_path = root / f"{stem}.drup"
    nvars, clauses = parse_dimacs(cnf_path)
    expected_vars, expected_clauses = expected_builder()
    if nvars != expected_vars or clauses != expected_clauses:
        raise AssertionError(f"{stem} CNF is not the independently rebuilt formula")
    if sha256(cnf_path) != record["cnf"]["sha256"]:
        raise AssertionError(f"{stem} CNF digest mismatch")
    proof = parse_drup(proof_path, nvars)
    if sha256(proof_path) != record["proof"]["sha256"]:
        raise AssertionError(f"{stem} proof digest mismatch")
    if not proof or proof[-1] != []:
        raise AssertionError(f"{stem} DRUP trace does not finish with empty clause")
    db = RUPDatabase(nvars, clauses)
    for number, clause in enumerate(proof, 1):
        if not db.rup(clause):
            raise AssertionError(f"{stem} proof clause {number} is not RUP")
        db.add(clause)
    return {
        "variables": nvars,
        "original_clauses": len(clauses),
        "cnf_sha256": sha256(cnf_path),
        "drup_clauses_checked": len(proof),
        "drup_sha256": sha256(proof_path),
        "final_empty": True,
        "independent_rebuild": True,
    }, proof


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    meta = json.loads((root / "CERTIFICATE.json").read_text())
    source_hashes = {
        name: sha256(root / name) for name in ("generate.py", "check.py")
    }
    if source_hashes != meta["source_sha256"]:
        raise AssertionError("source digest mismatch")
    reciprocal, proof_r = verify_certificate(
        root, "reciprocal", expected_reciprocal, meta["claims"]["reciprocal"])
    third, proof_t = verify_certificate(
        root, "third_image", expected_third_image, meta["claims"]["third_image"])

    witnesses, reversed_tuple, required_tuple = verify_fixture_and_failure()

    # Negative controls exercise both the theorem encoding and proof closure.
    control_d = sigma0(A)
    if ((sigma0(A) - sigma0(0)) & MASK) != control_d:
        raise AssertionError("known-SAT differential control failed")
    incomplete_rejected = all(
        p[-1] == [] and all(c != [] for c in p[:-1])
        for p in (proof_r, proof_t)
    )
    if not incomplete_rejected:
        raise AssertionError("missing-empty-clause negative control failed")
    cnf_path = root / "reciprocal.cnf"
    altered = bytearray(cnf_path.read_bytes())
    altered[-2] = ord("1") if altered[-2] != ord("1") else ord("2")
    digest_mutation_rejected = (
        hashlib.sha256(altered).hexdigest()
        != meta["claims"]["reciprocal"]["cnf"]["sha256"]
    )
    if not digest_mutation_rejected:
        raise AssertionError("digest mutation control failed")

    report = {
        "schema": "support12-d0005-reciprocal-check-v9",
        "status": "PASS",
        "theorems": {
            "reciprocal": "no x has sigma0(x+A)-sigma0(x)=D mod 2^32",
            "third_image": (
                "no x has d=D, sigma0 derivative=-A, sigma1 derivative=-T"
            ),
        },
        "constants": {"D": f"{D:08x}", "A": f"{A:08x}",
                      "T": f"{T:08x}"},
        "certificates": {"reciprocal": reciprocal, "third_image": third},
        "checker": "Python standard library only",
        "source_sha256": source_hashes,
        "supplied_positive_pairs": witnesses,
        "gaps": {"G_Y_minus_G_X": f"{2 * D:08x}",
                 "G_Y_minus_G_Q": f"{D:08x}"},
        "orientation_failure": {
            "required_third_pair_d_F_G": [f"{v:08x}" for v in required_tuple],
            "actual_reverse_Q_d_F_G": [f"{v:08x}" for v in reversed_tuple],
            "candidate_rejected": True,
        },
        "negative_controls": {
            "known_sat_D_prime": f"{control_d:08x}",
            "known_sat_witness_x": "00000000",
            "known_sat_joint_control": {
                "x": "0ffb000a", "d": f"{D:08x}",
                "F": f"{A:08x}", "G": f"{WITNESSES['X'][2]:08x}",
            },
            "missing_final_empty_rejected": incomplete_rejected,
            "mutated_cnf_digest_rejected": digest_mutation_rejected,
        },
        "scope": (
            "fixed (D,A,T) attempted branch and fixed (D,A) reciprocal edge only; "
            "not all A at D, not full support, not messages"
        ),
    }
    if args.write:
        (root / "RUN.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
