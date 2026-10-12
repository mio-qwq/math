#!/usr/bin/env python3
"""Independent selected-core CNF builder and deletion-free DRUP checker.

This file was started before inspecting support12-v16-core-batch-v9.  It uses
only the standard SHA-256 small-sigma definitions and the frozen equations in
PRE_AUTHOR_FREEZE.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from collections import defaultdict, deque
from pathlib import Path

MASK = (1 << 32) - 1
HERE = Path(__file__).resolve().parent


def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def sigma(x: int, which: int) -> int:
    if which == 0:
        return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
    if which == 1:
        return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)
    raise ValueError(which)


def derivative(x: int, d: int, which: int) -> int:
    return (sigma((x + d) & MASK, which) - sigma(x, which)) & MASK


class CNF:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[tuple[int, ...]] = []

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def word(self) -> list[int]:
        return [self.var() for _ in range(32)]

    def add(self, *lits: int) -> None:
        clause = tuple(dict.fromkeys(lits))
        if any(-lit in clause for lit in clause):
            return
        self.clauses.append(clause)

    def fix_word(self, word: list[int], value: int) -> None:
        for bit, var in enumerate(word):
            self.add(var if ((value >> bit) & 1) else -var)

    def parity(self, inputs: list[int], output: int) -> None:
        """Truth-table CNF for output = xor(inputs); inputs are literals."""
        variables = inputs + [output]
        for assignment in range(1 << len(variables)):
            values = [(assignment >> i) & 1 for i in range(len(variables))]
            if values[-1] == (sum(values[:-1]) & 1):
                continue
            # Block precisely this assignment.  Literal inputs may be negated;
            # values refer to their literal truth values.
            clause: list[int] = []
            for lit, value in zip(variables, values):
                clause.append(-lit if value else lit)
            self.add(*clause)

    def sigma_word(self, src: list[int], which: int) -> list[int]:
        rotations, shift = ((7, 18), 3) if which == 0 else ((17, 19), 10)
        out = self.word()
        for bit in range(32):
            ins = [src[(bit + rotations[0]) & 31],
                   src[(bit + rotations[1]) & 31]]
            if bit + shift < 32:
                ins.append(src[bit + shift])
            self.parity(ins, out[bit])
        return out

    def add_constant(self, left: list[int], constant: int,
                     result: list[int]) -> None:
        """Encode result = left + constant mod 2^32 by truth tables."""
        carry: int | None = None  # known zero into bit 0
        for bit in range(32):
            cbit = (constant >> bit) & 1
            next_carry = self.var() if bit < 31 else None
            vars_here = [left[bit], result[bit]]
            if carry is not None:
                vars_here.append(carry)
            if next_carry is not None:
                vars_here.append(next_carry)
            for assignment in range(1 << len(vars_here)):
                val = {v: (assignment >> i) & 1
                       for i, v in enumerate(vars_here)}
                a = val[left[bit]]
                cin = 0 if carry is None else val[carry]
                total = a + cbit + cin
                valid = val[result[bit]] == (total & 1)
                if next_carry is not None:
                    valid = valid and val[next_carry] == (total >> 1)
                if valid:
                    continue
                self.add(*[(-v if val[v] else v) for v in vars_here])
            carry = next_carry

    def build_derivative_query(self, d: int, target_f: int,
                               target_g: int) -> None:
        z, zp = self.word(), self.word()
        self.add_constant(z, d, zp)
        fz = self.sigma_word(z, 0)
        fzp = self.sigma_word(zp, 0)
        gz = self.sigma_word(z, 1)
        gzp = self.sigma_word(zp, 1)
        self.add_constant(fz, target_f, fzp)
        self.add_constant(gz, target_g, gzp)

    def dimacs(self) -> bytes:
        rows = [f"p cnf {self.nvars} {len(self.clauses)}\n"]
        rows += [" ".join(map(str, clause)) + " 0\n" for clause in self.clauses]
        return "".join(rows).encode()


def parse_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    """Separate strict DIMACS parser; deliberately shares no CNF methods."""
    nvars = nclauses = None
    clauses: list[tuple[int, ...]] = []
    pending: list[int] = []
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        text = raw.strip()
        if not text or text.startswith("c"):
            continue
        if text.startswith("p"):
            if nvars is not None or pending:
                raise ValueError(f"bad header at {lineno}")
            fields = text.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise ValueError(f"bad header at {lineno}")
            nvars, nclauses = map(int, fields[2:])
            continue
        if nvars is None:
            raise ValueError(f"clause before header at {lineno}")
        for token in text.split():
            lit = int(token)
            if lit == 0:
                clause = tuple(dict.fromkeys(pending))
                if any(-x in clause for x in clause):
                    raise ValueError(f"tautological clause at {lineno}")
                clauses.append(clause)
                pending = []
            else:
                if abs(lit) > nvars:
                    raise ValueError(f"literal out of range at {lineno}")
                pending.append(lit)
    if nvars is None or nclauses is None or pending:
        raise ValueError("missing header or unterminated clause")
    if len(clauses) != nclauses:
        raise ValueError(f"header says {nclauses}, parsed {len(clauses)}")
    return nvars, clauses


def parse_drup(path: Path, nvars: int) -> list[tuple[int, ...]]:
    proof: list[tuple[int, ...]] = []
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        text = raw.strip()
        if not text or text.startswith("c"):
            continue
        if text.startswith("d ") or text == "d":
            raise ValueError(f"deletion at proof line {lineno}")
        ints = [int(token) for token in text.split()]
        if not ints or ints[-1] != 0 or 0 in ints[:-1]:
            raise ValueError(f"bad proof line {lineno}")
        clause = tuple(dict.fromkeys(ints[:-1]))
        if any(abs(lit) > nvars for lit in clause):
            raise ValueError(f"proof literal out of range at {lineno}")
        proof.append(clause)
    return proof


class RUPDatabase:
    """Deletion-free RUP database using occurrence-driven propagation."""
    def __init__(self, nvars: int, clauses: list[tuple[int, ...]]) -> None:
        self.nvars = nvars
        self.clauses: list[tuple[int, ...]] = []
        self.occ: dict[int, list[int]] = defaultdict(list)
        self.units: list[int] = []
        for clause in clauses:
            self.append(clause)

    def append(self, clause: tuple[int, ...]) -> None:
        cid = len(self.clauses)
        self.clauses.append(clause)
        for lit in clause:
            self.occ[lit].append(cid)
        if len(clause) == 1:
            self.units.append(clause[0])

    def rup(self, clause: tuple[int, ...]) -> bool:
        # Negating a tautological clause is immediately inconsistent.
        if any(-lit in clause for lit in clause):
            return True
        value = [0] * (self.nvars + 1)
        queue: deque[int] = deque()
        remaining: dict[int, int] = {}
        satisfied: set[int] = set()

        def assign(lit: int) -> bool:
            old = value[abs(lit)]
            new = 1 if lit > 0 else -1
            if old == -new:
                return False
            if old == 0:
                value[abs(lit)] = new
                queue.append(lit)
            return True

        for lit in clause:
            if not assign(-lit):
                return True
        for lit in self.units:
            if not assign(lit):
                return True

        while queue:
            lit = queue.popleft()
            for cid in self.occ.get(lit, ()):
                satisfied.add(cid)
            for cid in self.occ.get(-lit, ()):
                if cid in satisfied:
                    continue
                row = self.clauses[cid]
                rem = remaining.get(cid, len(row)) - 1
                remaining[cid] = rem
                if rem == 0:
                    return True
                if rem == 1:
                    unit = 0
                    row_satisfied = False
                    for candidate in row:
                        state = value[abs(candidate)]
                        if state == (1 if candidate > 0 else -1):
                            row_satisfied = True
                            satisfied.add(cid)
                            break
                        if state == 0:
                            unit = candidate
                    if not row_satisfied:
                        if unit == 0 or not assign(unit):
                            return True
        return False

    def check(self, proof: list[tuple[int, ...]]) -> None:
        if not proof or proof[-1] != ():
            raise ValueError("proof must end in the empty clause")
        for index, clause in enumerate(proof, 1):
            if not self.rup(clause):
                raise ValueError(f"non-RUP addition {index}: {clause}")
            self.append(clause)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class UniversalCNF:
    """Second, full-system builder used to audit the author DIMACS.

    This follows the frozen mathematical equations, but is structurally
    separate from the fixture-only CNF class above.  Fresh outputs are
    allocated by each operation, including an explicit 33-bit carry path;
    this makes a literal-for-literal comparison with the frozen formulas
    possible without importing either author program.
    """

    def __init__(self, d: int) -> None:
        self.d = d
        self.high = 0
        self.rows: list[tuple[int, ...]] = []

    def alloc(self, width: int = 32) -> list[int]:
        ans = list(range(self.high + 1, self.high + width + 1))
        self.high += width
        return ans

    def forbid(self, variables: list[int], bits: tuple[int, ...]) -> None:
        self.rows.append(tuple(-v if b else v for v, b in zip(variables, bits)))

    def functional_relation(self, variables: list[int], predicate) -> None:
        for packed in range(1 << len(variables)):
            bits = tuple((packed >> j) & 1 for j in range(len(variables)))
            if not predicate(bits):
                self.forbid(variables, bits)

    def modular_sum(self, a: list[int], b: int | list[int]) -> list[int]:
        out, carries = self.alloc(), self.alloc(33)
        self.rows.append((-carries[0],))
        for bit in range(32):
            variables = [a[bit], carries[bit], out[bit], carries[bit + 1]]
            if isinstance(b, list):
                variables.insert(1, b[bit])

                def legal(v: tuple[int, ...]) -> bool:
                    total = v[0] + v[1] + v[2]
                    return (v[3], v[4]) == (total & 1, total >> 1)
            else:
                k = (b >> bit) & 1

                def legal(v: tuple[int, ...], k: int = k) -> bool:
                    total = v[0] + v[1] + k
                    return (v[2], v[3]) == (total & 1, total >> 1)
            self.functional_relation(variables, legal)
        return out

    def equal_words(self, a: list[int], b: list[int]) -> None:
        for u, v in zip(a, b):
            self.rows.append((-u, v))
            self.rows.append((u, -v))

    def linear_word(self, word: list[int], which: int) -> list[int]:
        rotations, shift = ((7, 18), 3) if which == 0 else ((17, 19), 10)
        out = self.alloc()
        for bit in range(32):
            inputs = [word[(bit + r) & 31] for r in rotations]
            if bit + shift < 32:
                inputs.append(word[bit + shift])
            variables = inputs + [out[bit]]
            self.functional_relation(
                variables,
                lambda v: v[-1] == (sum(v[:-1]) & 1))
        return out

    def images(self, word: list[int]) -> tuple[list[int], ...]:
        shifted = self.modular_sum(word, self.d)
        return (self.linear_word(word, 0), self.linear_word(shifted, 0),
                self.linear_word(word, 1), self.linear_word(shifted, 1))

    def build(self) -> None:
        x, y, z, a = self.alloc(), self.alloc(), self.alloc(), self.alloc()
        fx, fxd, gx, gxd = self.images(x)
        self.equal_words(self.modular_sum(fx, a), fxd)
        raw_gx = self.alloc()
        self.equal_words(self.modular_sum(gx, raw_gx), gxd)
        t = self.modular_sum(raw_gx, self.d)

        fy, fyd, gy, gyd = self.images(y)
        self.equal_words(self.modular_sum(fy, a), fyd)
        t_plus_d = self.modular_sum(t, self.d)
        self.equal_words(self.modular_sum(gy, t_plus_d), gyd)

        fz, fzd, gz, gzd = self.images(z)
        self.equal_words(self.modular_sum(fzd, a), fz)
        self.equal_words(self.modular_sum(gzd, t), gz)

    def dimacs(self) -> bytes:
        body = "".join(" ".join(map(str, row)) + " 0\n" for row in self.rows)
        return (f"p cnf {self.high} {len(self.rows)}\n" + body).encode()


AUTHOR_NEAR = {
    5:  (0xBFFF89AB, 0xBFFF89A3, 0x3FFFE0C9),
    13: (0xBFFB96FD, 0xBFFB96E5, 0x3FF3FF87),
    21: (0x7FFD484D, 0x7FFD595F, 0xFFEDFCFC),
    23: (0xFFEC5B45, 0xFFEC4A57, 0x7FEC102B),
    25: (0xFFFBB4BD, 0xFFFBA5AF, 0xFFFBAA81),
    27: (0xFFF2336B, 0xFFF22279, 0x7FF25A01),
}


def equation_values(q: int, xyz: tuple[int, int, int], d: int | None = None) -> dict[str, bool]:
    d = (q << 16) if d is None else d & MASK
    x, y, z = xyz
    a = derivative(x, d, 0)
    t = (derivative(x, d, 1) + d) & MASK
    return {
        "F_y=A": derivative(y, d, 0) == a,
        "G_y=T+D": derivative(y, d, 1) == ((t + d) & MASK),
        "F_z=-A": derivative(z, d, 0) == ((-a) & MASK),
        "G_z=-T": derivative(z, d, 1) == ((-t) & MASK),
    }


def reversal_values(q: int, xyz: tuple[int, int, int]) -> dict[str, object]:
    d = q << 16
    shifted = tuple((w + d) & MASK for w in xyz)
    reverse_d = (-d) & MASK
    original = equation_values(q, xyz, d)
    reversed_eq = equation_values(q, shifted, reverse_d)
    pointwise = []
    for w in xyz:
        pointwise.append(all(
            derivative((w + d) & MASK, reverse_d, which) ==
            ((-derivative(w, d, which)) & MASK)
            for which in (0, 1)))
    return {"shifted_words": [f"{w:08x}" for w in shifted],
            "reverse_D": f"{reverse_d:08x}",
            "pointwise_derivative_negation": all(pointwise),
            "equation_vector_preserved": original == reversed_eq,
            "original_equations": original,
            "reversed_equations": reversed_eq}


def audit_author(author: Path, output: Path) -> dict[str, object]:
    requested = (5, 13, 21, 23, 25, 27)
    certificate = json.loads((author / "CERTIFICATE.json").read_text())
    manifest = json.loads((author / "SHA256.json").read_text())
    if tuple(certificate["q_values"]) != requested:
        raise AssertionError("author certificate q domain mismatch")
    manifest_results = {}
    for name, expected in manifest["files"].items():
        actual = sha256_bytes((author / name).read_bytes())
        manifest_results[name] = actual == expected
    if not all(manifest_results.values()):
        raise AssertionError("author SHA256 manifest mismatch")
    records: list[dict[str, object]] = []
    for q in requested:
        d = q << 16
        tag = f"d{q:04x}"
        cnf_path, proof_path = author / f"{tag}.cnf", author / f"{tag}.drup"
        frozen_bytes = cnf_path.read_bytes()
        frozen_n, frozen_rows = parse_dimacs(cnf_path)

        rebuilt = UniversalCNF(d)
        rebuilt.build()
        rebuilt_bytes = rebuilt.dimacs()
        exact_bytes = rebuilt_bytes == frozen_bytes
        exact_multiset = Counter(rebuilt.rows) == Counter(frozen_rows)
        if not exact_bytes or not exact_multiset or rebuilt.high != frozen_n:
            raise AssertionError(f"q={q}: independent CNF reconstruction mismatch")

        proof = parse_drup(proof_path, frozen_n)
        claimed = certificate["records"][str(q)]
        if (claimed["cnf"]["variables"] != frozen_n or
                claimed["cnf"]["clauses"] != len(frozen_rows) or
                claimed["cnf"]["sha256"] != sha256_bytes(frozen_bytes) or
                claimed["proof"]["added_clauses"] != len(proof) or
                claimed["proof"]["sha256"] != sha256_bytes(proof_path.read_bytes())):
            raise AssertionError(f"q={q}: author metadata disagrees with bytes")
        started = time.monotonic()
        database = RUPDatabase(frozen_n, frozen_rows)
        database.check(proof)
        elapsed = time.monotonic() - started

        # Negative proof controls.  These are checked with fresh databases so
        # the successful run above cannot contaminate the outcome.
        truncated_rejected = False
        try:
            RUPDatabase(frozen_n, frozen_rows).check(proof[:-1])
        except ValueError:
            truncated_rejected = True

        mutated = list(proof)
        mutate_at = next(i for i, clause in enumerate(mutated) if i > 0 and clause)
        original_lit = mutated[mutate_at][0]
        mutated[mutate_at] = (-original_lit,) + mutated[mutate_at][1:]
        mutation_description = (f"proof addition {mutate_at + 1} first literal "
                                f"flipped from {original_lit} to {-original_lit}")
        mutated[-1] = (1,)
        proof_mutation_rejected = False
        try:
            RUPDatabase(frozen_n, frozen_rows).check(mutated)
        except ValueError:
            proof_mutation_rejected = True

        # Dropping all clauses asserting the final G equation is a known SAT
        # relaxation; a valid proof of the original claim must not replay.
        weakened_rows = frozen_rows[:-64]
        weakened_rejected = False
        weakened_failure = None
        try:
            RUPDatabase(frozen_n, weakened_rows).check(proof)
        except ValueError as exc:
            weakened_rejected = True
            weakened_failure = str(exc)

        # Stronger locality control: find an individual final-G equality
        # clause whose deletion invalidates this exact trace.
        single_clause_rejected = False
        single_clause_number = None
        single_clause_failure = None
        for row_index in range(len(frozen_rows) - 1, len(frozen_rows) - 65, -1):
            one_missing = frozen_rows[:row_index] + frozen_rows[row_index + 1:]
            try:
                RUPDatabase(frozen_n, one_missing).check(proof)
            except ValueError as exc:
                single_clause_rejected = True
                single_clause_number = row_index + 1
                single_clause_failure = str(exc)
                break

        near = equation_values(q, AUTHOR_NEAR[q])
        if list(near.values()) != [True, True, True, False]:
            raise AssertionError(f"q={q}: direct near-miss evaluation failed")
        reverse = reversal_values(q, AUTHOR_NEAR[q])
        if not reverse["pointwise_derivative_negation"] or not reverse["equation_vector_preserved"]:
            raise AssertionError(f"q={q}: +/-D reversal identity failed")
        if not all((truncated_rejected, proof_mutation_rejected, weakened_rejected,
                    single_clause_rejected)):
            raise AssertionError(f"q={q}: a negative control was not rejected")

        records.append({
            "q": q, "D": f"{d:08x}", "status": "ACCEPT",
            "cnf": {"variables": frozen_n, "clauses": len(frozen_rows),
                    "sha256": sha256_bytes(frozen_bytes),
                    "independent_exact_bytes": exact_bytes,
                    "independent_clause_multiset": exact_multiset},
            "drup": {"additions": len(proof), "sha256": sha256_bytes(proof_path.read_bytes()),
                     "deletion_free": True, "final_empty": proof[-1] == (),
                     "independent_rup_seconds": elapsed},
            "near_miss_dropping_final_G": {
                "words": [f"{w:08x}" for w in AUTHOR_NEAR[q]],
                "equations": near},
            "reversal_control": reverse,
            "negative_controls": {
                "truncated_proof_rejected": truncated_rejected,
                "proof_mutation_rejected": proof_mutation_rejected,
                "proof_mutation": mutation_description,
                "drop_final_G_64_clauses_rejected": weakened_rejected,
                "weakened_proof_failure": weakened_failure,
                "single_final_G_clause_removed_rejected": single_clause_rejected,
                "removed_base_clause_number": single_clause_number,
                "single_clause_failure": single_clause_failure,
            },
        })

    report = {
        "schema": "CRYPTO3-v16-core-batch-independent-review-v1",
        "status": "ACCEPT",
        "per_q": records,
        "accepted_q": list(requested),
        "author_manifest": {"entries": len(manifest_results),
                            "all_match": all(manifest_results.values()),
                            "sha256": sha256_bytes((author / "SHA256.json").read_bytes())},
        "author_certificate_sha256": sha256_bytes((author / "CERTIFICATE.json").read_bytes()),
        "scope": ("exact selected three-pair UNSAT only for q in "
                  "{5,13,21,23,25,27}; combines with separately reviewed twin "
                  "exclusions only for the finite q<=31 window; no all-v2=16, "
                  "full-support, message, or distance-14 claim"),
    }
    output.write_text(json.dumps(report, indent=2) + "\n")
    return report


def build_from_fixture(q: int, x: int, y: int) -> tuple[CNF, dict[str, object]]:
    d = q << 16
    a = derivative(x, d, 0)
    gx = derivative(x, d, 1)
    fy = derivative(y, d, 0)
    gy = derivative(y, d, 1)
    if fy != a or gy != ((gx + 2 * d) & MASK):
        raise ValueError(f"q={q}: supplied x,y are not an exact twin")
    t = (gx + d) & MASK
    target_f, target_g = (-a) & MASK, (-t) & MASK
    cnf = CNF()
    cnf.build_derivative_query(d, target_f, target_g)
    record = {
        "q": q, "D": f"{d:08x}", "x": f"{x:08x}", "y": f"{y:08x}",
        "A": f"{a:08x}", "Gx": f"{gx:08x}", "T": f"{t:08x}",
        "target_Fz": f"{target_f:08x}", "target_Gz": f"{target_g:08x}",
        "variables": cnf.nvars, "clauses": len(cnf.clauses),
        "cnf_sha256": sha256_bytes(cnf.dimacs()),
        "reversal_control": {
            "delta": f"{((-d) & MASK):08x}",
            "base": f"{((x + d) & MASK):08x}",
            "F": f"{derivative((x+d)&MASK, (-d)&MASK, 0):08x}",
            "G": f"{derivative((x+d)&MASK, (-d)&MASK, 1):08x}",
            "expected_F": f"{((-a)&MASK):08x}",
            "expected_G": f"{((-gx)&MASK):08x}",
        },
    }
    return cnf, record


# First independently accepted exact twin fixture for each requested residue,
# copied from the prior general-v16 review object, not from the batch under audit.
FIXTURES = {
    5: (0x0ffb000a, 0x0ffb0002),
    13: (0x1ff30016, 0x1ff3000e),
    21: (0x7fec1112, 0x7fec0000),
    23: (0x7fec1110, 0x7fec0002),
    25: (0x7feb1116, 0x7feb0004),
    27: (0x7fe91114, 0x7fe90006),
}


def build_all(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    records = []
    for q, (x, y) in FIXTURES.items():
        cnf, record = build_from_fixture(q, x, y)
        path = output / f"q{q:02d}.cnf"
        path.write_bytes(cnf.dimacs())
        parsed_nvars, parsed_clauses = parse_dimacs(path)
        if parsed_nvars != cnf.nvars or parsed_clauses != cnf.clauses:
            raise AssertionError("independent DIMACS round trip failed")
        records.append(record)
    result = {
        "schema": "CRYPTO3-v16-selected-core-independent-precomparison-v1",
        "records": records,
        "scope": "six selected first twin fixtures only; not all v2=16",
    }
    (output / "PRECOMPARISON.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--output", type=Path, default=HERE / "independent-cnf")
    check = sub.add_parser("check-drup")
    check.add_argument("cnf", type=Path)
    check.add_argument("proof", type=Path)
    audit = sub.add_parser("audit-author")
    audit.add_argument("author", type=Path)
    audit.add_argument("--output", type=Path, default=HERE / "AUDIT.json")
    args = parser.parse_args()
    if args.command == "build":
        print(json.dumps(build_all(args.output), indent=2))
    elif args.command == "check-drup":
        nvars, clauses = parse_dimacs(args.cnf)
        proof = parse_drup(args.proof, nvars)
        db = RUPDatabase(nvars, clauses)
        db.check(proof)
        print(json.dumps({"status": "PASS", "variables": nvars,
                          "base_clauses": len(clauses),
                          "proof_additions": len(proof)}, indent=2))
    else:
        print(json.dumps(audit_author(args.author, args.output), indent=2))


if __name__ == "__main__":
    main()
