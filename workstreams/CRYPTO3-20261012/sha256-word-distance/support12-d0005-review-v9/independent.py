#!/usr/bin/env python3
"""Independent bit-blast, DRUP production, and DRUP checking for fixed q=5."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict, deque
from pathlib import Path

MASK = (1 << 32) - 1
D = 0x00050000
A = 0x40406E02
T = 0x1FFD913E
X = 0x0FFB000A
Y = 0x0FFB0002
HERE = Path(__file__).resolve().parent


def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def f(x: int) -> int:
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def g(x: int) -> int:
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def derivative(fun, x: int, step: int) -> int:
    return (fun((x + step) & MASK) - fun(x)) & MASK


class CNF:
    def __init__(self) -> None:
        self.nv = 0
        self.clauses: list[tuple[int, ...]] = []

    def new(self) -> int:
        self.nv += 1
        return self.nv

    def add(self, *lits: int) -> None:
        self.clauses.append(tuple(lits))

    def relation(self, variables: list[int], predicate) -> None:
        assert len(set(variables)) == len(variables)
        for values in itertools.product((False, True), repeat=len(variables)):
            if predicate(*values):
                continue
            self.add(*(v if not value else -v for v, value in zip(variables, values)))

    def parity(self, inputs: list[int], output: int) -> None:
        variables = inputs + [output]
        self.relation(variables, lambda *values: values[-1] == (sum(values[:-1]) & 1))

    def add_constant(self, bits: list[int], constant: int) -> list[int]:
        out: list[int] = []
        carry: int | None = None
        for i, bit in enumerate(bits):
            k = bool((constant >> i) & 1)
            y = self.new()
            out.append(y)
            last = i == 31
            cout = None if last else self.new()
            variables = [bit] + ([] if carry is None else [carry]) + [y] + ([] if cout is None else [cout])

            def valid(*values, k=k, has_carry=carry is not None, has_cout=cout is not None):
                j = 0
                a = values[j]
                j += 1
                cin = values[j] if has_carry else False
                j += int(has_carry)
                yy = values[j]
                j += 1
                total = int(a) + int(k) + int(cin)
                if yy != bool(total & 1):
                    return False
                return (not has_cout) or values[j] == bool(total >> 1)

            self.relation(variables, valid)
            carry = cout
        return out

    def linear_sigma(self, bits: list[int], which: str) -> list[int]:
        rotations, shift = ((7, 18), 3) if which == "f" else ((17, 19), 10)
        out = []
        for i in range(32):
            sources = [bits[(i + r) % 32] for r in rotations]
            if i + shift < 32:
                sources.append(bits[i + shift])
            y = self.new()
            self.parity(sources, y)
            out.append(y)
        return out

    def equal_words(self, left: list[int], right: list[int]) -> None:
        for a, b in zip(left, right):
            self.add(-a, b)
            self.add(a, -b)

    def write(self, path: Path) -> None:
        with path.open("w", encoding="ascii", newline="\n") as handle:
            handle.write(f"p cnf {self.nv} {len(self.clauses)}\n")
            for clause in self.clauses:
                handle.write(" ".join(map(str, clause)) + " 0\n")


def build_query(step: int, target_f: int, target_g: int | None) -> tuple[CNF, list[int]]:
    cnf = CNF()
    x = [cnf.new() for _ in range(32)]
    xp = cnf.add_constant(x, step)
    fx = cnf.linear_sigma(x, "f")
    fxp = cnf.linear_sigma(xp, "f")
    cnf.equal_words(cnf.add_constant(fx, target_f), fxp)
    if target_g is not None:
        gx = cnf.linear_sigma(x, "g")
        gxp = cnf.linear_sigma(xp, "g")
        cnf.equal_words(cnf.add_constant(gx, target_g), gxp)
    return cnf, x


def parse_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    nv = None
    clauses = []
    pending = []
    for line in path.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "p":
            assert fields[1] == "cnf" and nv is None
            nv = int(fields[2])
            expected = int(fields[3])
            continue
        for field in fields:
            lit = int(field)
            if lit:
                pending.append(lit)
            else:
                clauses.append(tuple(pending))
                pending = []
    assert nv is not None and not pending and len(clauses) == expected
    assert all(0 < abs(lit) <= nv for clause in clauses for lit in clause)
    return nv, clauses


class DRUPChecker:
    """Small independent forward RUP checker with DRUP deletion support."""

    def __init__(self, nv: int, clauses: list[tuple[int, ...]]) -> None:
        self.nv = nv
        self.clauses: list[tuple[int, ...]] = []
        self.active: list[bool] = []
        self.occ = defaultdict(list)
        self.by_clause = defaultdict(list)
        for clause in clauses:
            self._insert(clause)

    @staticmethod
    def canonical(clause: tuple[int, ...] | list[int]) -> tuple[int, ...]:
        return tuple(sorted(set(clause), key=lambda z: (abs(z), z < 0)))

    def _insert(self, clause: tuple[int, ...] | list[int]) -> int:
        clause = self.canonical(clause)
        cid = len(self.clauses)
        self.clauses.append(clause)
        self.active.append(True)
        self.by_clause[clause].append(cid)
        for lit in clause:
            self.occ[lit].append(cid)
        return cid

    def delete(self, clause: tuple[int, ...] | list[int]) -> bool:
        key = self.canonical(clause)
        for cid in reversed(self.by_clause.get(key, ())):
            if self.active[cid]:
                self.active[cid] = False
                return True
        return False

    def rup(self, clause: tuple[int, ...] | list[int]) -> bool:
        clause = self.canonical(clause)
        if any(-lit in clause for lit in clause):
            return True
        values: dict[int, bool] = {}
        queue: deque[int] = deque()

        def force(lit: int) -> bool:
            value = lit > 0
            old = values.get(abs(lit))
            if old is not None:
                return old != value
            values[abs(lit)] = value
            queue.append(lit)
            return False

        for lit in clause:
            if force(-lit):
                return True
        for cid, old_clause in enumerate(self.clauses):
            if self.active[cid] and len(old_clause) == 0:
                return True
            if self.active[cid] and len(old_clause) == 1 and force(old_clause[0]):
                return True
        while queue:
            true_lit = queue.popleft()
            for cid in self.occ[-true_lit]:
                if not self.active[cid]:
                    continue
                unresolved = []
                satisfied = False
                for lit in self.clauses[cid]:
                    value = values.get(abs(lit))
                    if value is None:
                        unresolved.append(lit)
                    elif value == (lit > 0):
                        satisfied = True
                        break
                if satisfied:
                    continue
                if not unresolved:
                    return True
                if len(unresolved) == 1 and force(unresolved[0]):
                    return True
        return False

    def run(self, proof_lines: list[str]) -> dict:
        additions = deletions = 0
        empty = False
        for line_no, line in enumerate(proof_lines, 1):
            fields = line.split()
            if not fields or fields[0] == "c":
                continue
            deletion = fields[0] == "d"
            nums = fields[1:] if deletion else fields
            assert nums and nums[-1] == "0", (line_no, line)
            clause = tuple(map(int, nums[:-1]))
            assert all(0 < abs(lit) <= self.nv for lit in clause), (line_no, clause)
            if deletion:
                assert self.delete(clause), (line_no, "missing deletion", clause)
                deletions += 1
            else:
                assert self.rup(clause), (line_no, "not RUP", clause)
                self._insert(clause)
                additions += 1
                empty |= not clause
        assert empty, "proof never derived the empty clause"
        return {"additions": additions, "deletions": deletions, "empty_clause": empty}


def solve_and_prove(cnf: CNF, cnf_path: Path, proof_path: Path) -> dict:
    from pysat.solvers import Solver

    cnf.write(cnf_path)
    with Solver(name="glucose3", bootstrap_with=cnf.clauses, with_proof=True) as solver:
        status = solver.solve()
        assert status is False
        proof = solver.get_proof()
    assert proof and proof[-1].strip() == "0"
    proof_path.write_text("\n".join(proof) + "\n", encoding="ascii", newline="\n")
    nv, parsed = parse_dimacs(cnf_path)
    checked = DRUPChecker(nv, parsed).run(proof)

    truncated_rejected = False
    try:
        DRUPChecker(nv, parsed).run(proof[:-1])
    except (AssertionError, ValueError):
        truncated_rejected = True
    assert truncated_rejected
    return {
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
        "status": "UNSAT",
        "proof_lines": len(proof),
        "drup_check": checked,
        "negative_control_truncated_proof_rejected": truncated_rejected,
    }


def solve_sat_control(step: int, target_f: int, target_g: int | None) -> dict:
    from pysat.solvers import Solver

    cnf, xvars = build_query(step, target_f, target_g)
    with Solver(name="glucose3", bootstrap_with=cnf.clauses) as solver:
        assert solver.solve()
        positives = set(lit for lit in solver.get_model() if lit > 0)
    word = sum((1 << i) for i, var in enumerate(xvars) if var in positives)
    assert derivative(f, word, step) == target_f
    if target_g is not None:
        assert derivative(g, word, step) == target_g
    return {"word": f"{word:08x}", "F": f"{target_f:08x}", "G": None if target_g is None else f"{target_g:08x}"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    gx = derivative(g, X, D)
    gy = derivative(g, Y, D)
    orientation = {
        "D": f"{D:08x}", "A": f"{A:08x}", "T": f"{T:08x}",
        "X": {"word": f"{X:08x}", "F_D": f"{derivative(f, X, D):08x}", "G_D": f"{gx:08x}"},
        "Y": {"word": f"{Y:08x}", "F_D": f"{derivative(f, Y, D):08x}", "G_D": f"{gy:08x}"},
        "third_forward": [f"{D:08x}", f"{(-A) & MASK:08x}", f"{(-T) & MASK:08x}"],
        "reciprocal_forward": [f"{A:08x}", f"{D:08x}"],
    }
    assert derivative(f, X, D) == derivative(f, Y, D) == A
    assert gx == (T - D) & MASK and gy == (T + D) & MASK

    third, _ = build_query(D, (-A) & MASK, (-T) & MASK)
    reciprocal, _ = build_query(A, D, None)
    third_result = solve_and_prove(third, HERE / "third-image.cnf", HERE / "third-image.drup")
    reciprocal_result = solve_and_prove(reciprocal, HERE / "reciprocal.cnf", HERE / "reciprocal.drup")

    controls = {
        "known_X_joint_query_is_sat": solve_sat_control(D, A, gx),
        "known_Y_joint_query_is_sat": solve_sat_control(D, A, gy),
        "known_X_sigma0_query_is_sat": solve_sat_control(D, A, None),
    }
    out = {
        "schema": "support12-d0005-independent-review-v9",
        "orientation": orientation,
        "queries": {"third_image": third_result, "reciprocal": reciprocal_result},
        "controls": controls,
        "scope_exclusions": ["other q=5 A", "full support", "message", "distance14"],
    }
    for name in ("third-image.cnf", "third-image.drup", "reciprocal.cnf", "reciprocal.drup"):
        out.setdefault("artifact_sha256", {})[name] = sha256(HERE / name)
    encoded = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.write:
        (HERE / "INDEPENDENT_RUN.json").write_text(encoded, encoding="utf-8", newline="\n")
    else:
        frozen = (HERE / "INDEPENDENT_RUN.json").read_text(encoding="utf-8")
        assert frozen == encoded
    print(encoded, end="")


if __name__ == "__main__":
    main()
