#!/usr/bin/env python3
"""Independent CNF reconstruction and deletion-free RUP audit, q=33..63.

This script imports no author code and uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from collections import Counter, defaultdict, deque
from pathlib import Path

MASK = (1 << 32) - 1
QS = tuple(range(33, 64, 2))
HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-v16-core-q33-63-v10"

# Concrete prefix witnesses.  Each satisfies the first three derived
# equations and fails only the final G_D(z)=-T equation.
NEAR = {
    37: (0xffe59b73, 0xffe58a61, 0xffe5a74b),
    39: (0x7fe46a5b, 0x7fe47b49, 0x7ff4b8ae),
    41: (0x7feb02d7, 0x7feb13c5, 0xffeba774),
    43: (0x7feb3f21, 0x7feb2e33, 0xffeb8b90),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rotr(x: int, amount: int) -> int:
    return ((x >> amount) | (x << (32 - amount))) & MASK


def small_sigma(x: int, index: int) -> int:
    if index == 0:
        return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
    if index == 1:
        return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)
    raise ValueError(index)


def derivative(x: int, d: int, index: int) -> int:
    return (small_sigma((x + d) & MASK, index) - small_sigma(x, index)) & MASK


class Formula:
    """Independent, deterministic Boolean encoding of the frozen equations."""

    def __init__(self, difference: int) -> None:
        self.difference = difference
        self.high = 0
        self.rows: list[tuple[int, ...]] = []

    def allocate(self, width: int = 32) -> list[int]:
        result = list(range(self.high + 1, self.high + width + 1))
        self.high += width
        return result

    def relation(self, variables: list[int], predicate) -> None:
        for packed in range(1 << len(variables)):
            bits = tuple((packed >> bit) & 1 for bit in range(len(variables)))
            if not predicate(bits):
                self.rows.append(tuple(-var if val else var
                                       for var, val in zip(variables, bits)))

    def sum_constant(self, source: list[int], constant: int) -> list[int]:
        output, carries = self.allocate(), self.allocate(33)
        self.rows.append((-carries[0],))
        for bit in range(32):
            k = (constant >> bit) & 1
            variables = [source[bit], carries[bit], output[bit], carries[bit + 1]]

            def legal(v: tuple[int, ...], k: int = k) -> bool:
                total = v[0] + v[1] + k
                return (v[2], v[3]) == (total & 1, total >> 1)

            self.relation(variables, legal)
        return output

    def sum_words(self, left: list[int], right: list[int]) -> list[int]:
        output, carries = self.allocate(), self.allocate(33)
        self.rows.append((-carries[0],))
        for bit in range(32):
            variables = [left[bit], right[bit], carries[bit],
                         output[bit], carries[bit + 1]]

            def legal(v: tuple[int, ...]) -> bool:
                total = v[0] + v[1] + v[2]
                return (v[3], v[4]) == (total & 1, total >> 1)

            self.relation(variables, legal)
        return output

    def equal(self, left: list[int], right: list[int]) -> None:
        for a, b in zip(left, right):
            self.rows.extend(((-a, b), (a, -b)))

    def sigma_word(self, source: list[int], index: int) -> list[int]:
        rotations, shift = ((7, 18), 3) if index == 0 else ((17, 19), 10)
        output = self.allocate()
        for bit in range(32):
            inputs = [source[(bit + r) & 31] for r in rotations]
            if bit + shift < 32:
                inputs.append(source[bit + shift])
            variables = inputs + [output[bit]]
            self.relation(variables,
                          lambda v: v[-1] == (sum(v[:-1]) & 1))
        return output

    def images(self, word: list[int]) -> tuple[list[int], ...]:
        shifted = self.sum_constant(word, self.difference)
        return (self.sigma_word(word, 0), self.sigma_word(shifted, 0),
                self.sigma_word(word, 1), self.sigma_word(shifted, 1))

    def build(self) -> None:
        x, y, z, a = (self.allocate() for _ in range(4))

        sx0, sdx0, sx1, sdx1 = self.images(x)
        self.equal(self.sum_words(sx0, a), sdx0)
        gx = self.allocate()
        self.equal(self.sum_words(sx1, gx), sdx1)
        t = self.sum_constant(gx, self.difference)

        sy0, sdy0, sy1, sdy1 = self.images(y)
        self.equal(self.sum_words(sy0, a), sdy0)
        t_plus_d = self.sum_constant(t, self.difference)
        self.equal(self.sum_words(sy1, t_plus_d), sdy1)

        sz0, sdz0, sz1, sdz1 = self.images(z)
        self.equal(self.sum_words(sdz0, a), sz0)
        self.equal(self.sum_words(sdz1, t), sz1)

    def dimacs(self) -> bytes:
        body = "".join(" ".join(map(str, row)) + " 0\n" for row in self.rows)
        return (f"p cnf {self.high} {len(self.rows)}\n" + body).encode()


def read_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    nvars = announced = None
    clauses: list[tuple[int, ...]] = []
    pending: list[int] = []
    for line_number, raw in enumerate(path.read_text().splitlines(), 1):
        text = raw.strip()
        if not text or text.startswith("c"):
            continue
        if text.startswith("p "):
            fields = text.split()
            if nvars is not None or fields[:2] != ["p", "cnf"] or len(fields) != 4:
                raise ValueError(f"bad DIMACS header at line {line_number}")
            nvars, announced = int(fields[2]), int(fields[3])
            continue
        if nvars is None:
            raise ValueError("clause before header")
        for token in text.split():
            literal = int(token)
            if literal == 0:
                clauses.append(tuple(pending))
                pending = []
            else:
                if not 1 <= abs(literal) <= nvars:
                    raise ValueError(f"literal out of range at line {line_number}")
                pending.append(literal)
    if nvars is None or pending or announced != len(clauses):
        raise ValueError("incomplete or count-mismatched DIMACS")
    return nvars, clauses


def read_proof(path: Path, nvars: int) -> list[tuple[int, ...]]:
    proof: list[tuple[int, ...]] = []
    for line_number, raw in enumerate(path.read_text().splitlines(), 1):
        text = raw.strip()
        if not text or text.startswith("c"):
            continue
        if text == "d" or text.startswith("d "):
            raise ValueError(f"deletion found at line {line_number}")
        values = [int(x) for x in text.split()]
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise ValueError(f"bad proof line {line_number}")
        clause = tuple(values[:-1])
        if any(not 1 <= abs(lit) <= nvars for lit in clause):
            raise ValueError(f"proof literal out of range at line {line_number}")
        proof.append(clause)
    return proof


class RUP:
    """Occurrence-driven unit propagation over an append-only database."""

    def __init__(self, nvars: int, clauses: list[tuple[int, ...]]) -> None:
        self.nvars = nvars
        self.clauses: list[tuple[int, ...]] = []
        self.occ: dict[int, list[int]] = defaultdict(list)
        self.units: list[int] = []
        for clause in clauses:
            self.add(clause)

    def add(self, clause: tuple[int, ...]) -> None:
        index = len(self.clauses)
        self.clauses.append(clause)
        for literal in set(clause):
            self.occ[literal].append(index)
        if len(clause) == 1:
            self.units.append(clause[0])

    def proves(self, candidate: tuple[int, ...]) -> bool:
        assignment = [0] * (self.nvars + 1)
        queue: deque[int] = deque()
        remaining: dict[int, int] = {}
        satisfied: set[int] = set()

        def assign(literal: int) -> bool:
            variable = abs(literal)
            sign = 1 if literal > 0 else -1
            if assignment[variable] == -sign:
                return False
            if assignment[variable] == 0:
                assignment[variable] = sign
                queue.append(literal)
            return True

        for literal in candidate:
            if not assign(-literal):
                return True
        for literal in self.units:
            if not assign(literal):
                return True
        if any(not clause for clause in self.clauses):
            return True

        while queue:
            literal = queue.popleft()
            satisfied.update(self.occ.get(literal, ()))
            for clause_index in self.occ.get(-literal, ()):
                if clause_index in satisfied:
                    continue
                clause = self.clauses[clause_index]
                rem = remaining.get(clause_index, len(clause)) - 1
                remaining[clause_index] = rem
                if rem == 0:
                    return True
                if rem == 1:
                    unit = 0
                    row_satisfied = False
                    for item in clause:
                        state = assignment[abs(item)]
                        if state == (1 if item > 0 else -1):
                            row_satisfied = True
                            satisfied.add(clause_index)
                            break
                        if state == 0:
                            unit = item
                    if not row_satisfied and (unit == 0 or not assign(unit)):
                        return True
        return False

    def check(self, proof: list[tuple[int, ...]], require_empty: bool = True) -> None:
        if require_empty and (not proof or proof[-1] != ()):
            raise ValueError("proof does not end in the empty clause")
        for number, clause in enumerate(proof, 1):
            if not self.proves(clause):
                raise ValueError(f"non-RUP addition {number}")
            self.add(clause)


def equation_vector(d: int, xyz: tuple[int, int, int]) -> dict[str, bool]:
    x, y, z = xyz
    a = derivative(x, d, 0)
    t = (derivative(x, d, 1) + d) & MASK
    return {
        "F_D(y)=A": derivative(y, d, 0) == a,
        "G_D(y)=T+D": derivative(y, d, 1) == ((t + d) & MASK),
        "F_D(z)=-A": derivative(z, d, 0) == ((-a) & MASK),
        "G_D(z)=-T": derivative(z, d, 1) == ((-t) & MASK),
    }


def reversal_control(d: int, words: tuple[int, int, int]) -> dict[str, object]:
    reverse_d = (-d) & MASK
    shifted = tuple((word + d) & MASK for word in words)
    pointwise = all(
        derivative((word + d) & MASK, reverse_d, index) ==
        ((-derivative(word, d, index)) & MASK)
        for word in words for index in (0, 1))
    original = equation_vector(d, words)
    reversed_vector = equation_vector(reverse_d, shifted)
    return {
        "negative_D": f"{reverse_d:08x}",
        "shifted_words": [f"{word:08x}" for word in shifted],
        "pointwise_derivatives_negate": pointwise,
        "equation_vector_preserved": original == reversed_vector,
    }


def rejected(action) -> tuple[bool, str | None]:
    try:
        action()
    except ValueError as error:
        return True, str(error)
    return False, None


def audit() -> dict[str, object]:
    certificate_path = AUTHOR / "CERTIFICATE.json"
    certificate = json.loads(certificate_path.read_text())
    if tuple(certificate["q_values"]) != QS:
        raise AssertionError("author q domain is not exactly odd 33..63")

    entries: list[dict[str, object]] = []
    for q in QS:
        d = q << 16
        tag = f"d{q:04x}"
        cnf_path = AUTHOR / f"{tag}.cnf"
        proof_path = AUTHOR / f"{tag}.drup"
        author_bytes = cnf_path.read_bytes()
        nvars, clauses = read_dimacs(cnf_path)

        independent = Formula(d)
        independent.build()
        rebuilt = independent.dimacs()
        exact_bytes = rebuilt == author_bytes
        exact_multiset = Counter(independent.rows) == Counter(clauses)
        if not exact_bytes or not exact_multiset or independent.high != nvars:
            raise AssertionError(f"q={q}: independent CNF mismatch")

        proof = read_proof(proof_path, nvars)
        author_record = certificate["records"][str(q)]
        if (author_record["cnf"]["variables"] != nvars or
                author_record["cnf"]["clauses"] != len(clauses) or
                author_record["cnf"]["sha256"] != sha256(author_bytes) or
                author_record["proof"]["added_clauses"] != len(proof) or
                author_record["proof"]["sha256"] != sha256(proof_path.read_bytes())):
            raise AssertionError(f"q={q}: author metadata mismatch")

        started = time.monotonic()
        RUP(nvars, clauses).check(proof)
        elapsed = time.monotonic() - started

        truncated_ok, truncated_error = rejected(
            lambda: RUP(nvars, clauses).check(proof[:-1]))

        # Search the 64 clauses encoding the last equality for one definition
        # clause on which the concrete trace depends.
        removed_clause = None
        removed_error = None
        for row_index in range(len(clauses) - 1, len(clauses) - 65, -1):
            damaged = clauses[:row_index] + clauses[row_index + 1:]
            is_rejected, error = rejected(lambda damaged=damaged:
                                          RUP(nvars, damaged).check(proof))
            if is_rejected:
                removed_clause = row_index + 1
                removed_error = error
                break

        mutated = list(proof)
        # The first learned clause happens to remain RUP after this literal
        # flip.  Use the first nonempty addition after it; this is a genuine
        # local proof corruption and is rejected at that exact addition.
        mutation_index = next(i for i, clause in enumerate(mutated[:-1])
                              if i > 0 and clause)
        changed_clause = list(mutated[mutation_index])
        changed_clause[0] = -changed_clause[0]
        mutated[mutation_index] = tuple(changed_clause)
        mutation_ok, mutation_error = rejected(
            lambda: RUP(nvars, clauses).check(mutated))

        sample = NEAR.get(q, (0x01234567 ^ q, 0x89abcdef ^ q, 0xfedcba98 ^ q))
        reverse = reversal_control(d, sample)
        if not reverse["pointwise_derivatives_negate"] or not reverse["equation_vector_preserved"]:
            raise AssertionError(f"q={q}: reversal control failed")

        near: dict[str, object]
        if q in NEAR:
            vector = equation_vector(d, NEAR[q])
            if list(vector.values()) != [True, True, True, False]:
                raise AssertionError(f"q={q}: near-miss arithmetic failed")
            near = {"status": "PASS", "words": [f"{w:08x}" for w in NEAR[q]],
                    "equations": vector}
        else:
            near = {"status": "NOT_APPLICABLE",
                    "reason": "no prefix fixture used; the independent control set uses q=37,39,41,43"}

        if not truncated_ok or removed_clause is None or not mutation_ok:
            raise AssertionError(f"q={q}: negative control did not reject")

        entries.append({
            "q": q, "D": f"{d:08x}", "status": "ACCEPT",
            "cnf": {"variables": nvars, "clauses": len(clauses),
                    "sha256": sha256(author_bytes),
                    "independent_exact_bytes": exact_bytes,
                    "independent_clause_multiset": exact_multiset},
            "drup": {"additions_checked": len(proof),
                     "sha256": sha256(proof_path.read_bytes()),
                     "deletion_free": True, "final_empty": proof[-1] == (),
                     "independent_rup_seconds": elapsed},
            "near_miss": near,
            "negative_symmetry": reverse,
            "negative_controls": {
                "truncated_proof_rejected": truncated_ok,
                "truncated_failure": truncated_error,
                "single_definition_clause_removed_rejected": True,
                "removed_base_clause_number": removed_clause,
                "definition_damage_failure": removed_error,
                "proof_literal_mutation_rejected": mutation_ok,
                "proof_mutation_addition": mutation_index + 1,
                "proof_mutation_failure": mutation_error,
            },
        })

    result = {
        "schema": "CRYPTO3-v16-selected-core-q33-63-independent-review-v10",
        "status": "ACCEPT",
        "accepted_q": list(QS),
        "author_certificate_sha256": sha256(certificate_path.read_bytes()),
        "author_run_sha256": sha256((AUTHOR / "RUN.json").read_bytes()),
        "checker": {"python": platform.python_version(),
                    "source_sha256": sha256(Path(__file__).read_bytes()),
                    "command": ("python -B workstreams/CRYPTO3-20261012/sha256-word-distance/"
                                "support12-v16-core-q33-63-review-v10/independent_review.py --write")},
        "per_q": entries,
        "scope": ("selected three-pair core only for D=+/-q*2^16, odd q=33..63; "
                  "not all exact-v2=16 differences, not a support-12 solution, not "
                  "a SHA-256 message pair, not distance 13 attainability, not a "
                  "distance-at-least-14 theorem, and not Lean"),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    result = audit()
    if arguments.write:
        (HERE / "AUDIT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "accepted_q": result["accepted_q"],
                      "rup_additions": sum(row["drup"]["additions_checked"]
                                           for row in result["per_q"])}, sort_keys=True))


if __name__ == "__main__":
    main()
