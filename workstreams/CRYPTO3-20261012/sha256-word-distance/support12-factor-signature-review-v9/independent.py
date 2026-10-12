#!/usr/bin/env python3
"""Blind low-26 reconstruction of the corrected support-12 factor graph.

This checker was written from the accepted support12-full-factor-v9 normal
form.  It imports no author factor-signature code or data.  The SAT encoding
uses 32-bit words for every local pair, evaluates the FIPS small sigmas on all
32 bits, and couples only bits 0..25 of d/F/G to the projected graph.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

MASK32 = (1 << 32) - 1
MASK26 = (1 << 26) - 1
B_FIXED = 1 << 16
HERE = Path(__file__).resolve().parent
SCALARS = ("a", "b", "c", "k", "p", "q", "l", "s", "w", "z")


def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK32


def sigma0(x: int) -> int:
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x: int) -> int:
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


# Each expression is a tuple of (sign, scalar-name) terms over Z/(2^26).
FACTORS = (
    (10, "PF", ((1, "a"),), ((-1, "b"),), None),
    (11, "PF", ((1, "b"),), ((1, "p"),), None),
    (13, "PF", ((1, "c"),), ((1, "q"),), None),
    (15, "J", ((1, "k"),), ((1, "l"),), ((-1, "a"),)),
    (18, "J", ((1, "b"),), ((-1, "p"), (-1, "a")),
     ((-1, "b"), (-1, "c"))),
    (20, "J", ((-1, "b"),), ((-1, "q"), (-1, "s")),
     ((-1, "k"),)),
    (26, "J", ((1, "p"), (1, "a")), ((-1, "b"),),
     ((1, "s"),)),
    (28, "J", ((1, "q"), (1, "s")), ((-1, "b"),),
     ((-1, "l"),)),
    (29, "J", ((1, "c"),), ((1, "w"),), ((-1, "k"),)),
    (34, "J", ((1, "b"),), ((-1, "p"), (-1, "a")),
     ((1, "b"), (-1, "c"))),
    (42, "J", ((1, "p"), (1, "a")), ((1, "z"),),
     ((-1, "w"), (-1, "q"), (-1, "s"))),
    (43, "J", ((-1, "b"),), ((-1, "p"), (-1, "a")),
     ((-1, "c"),)),
    (57, "PG", ((1, "z"),), None, ((1, "b"),)),
)


class CNF:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[tuple[int, ...]] = []
        self.names: dict[str, list[int]] = {}
        self.false = self.var()
        self.add(-self.false)

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def word(self, name: str, width: int) -> list[int]:
        answer = [self.var() for _ in range(width)]
        self.names[name] = answer
        return answer

    def add(self, *lits: int) -> None:
        assert lits and all(lit and abs(lit) <= self.nvars for lit in lits)
        self.clauses.append(tuple(lits))

    def inv(self, a: int) -> int:
        c = self.var()
        self.add(a, c)
        self.add(-a, -c)
        return c

    def xor2(self, a: int, b: int) -> int:
        c = self.var()
        self.add(a, b, -c)
        self.add(a, -b, c)
        self.add(-a, b, c)
        self.add(-a, -b, -c)
        return c

    def xor3(self, a: int, b: int, c: int) -> int:
        return self.xor2(self.xor2(a, b), c)

    def majority(self, a: int, b: int, c: int) -> int:
        m = self.var()
        self.add(-a, -b, m)
        self.add(-a, -c, m)
        self.add(-b, -c, m)
        self.add(a, b, -m)
        self.add(a, c, -m)
        self.add(b, c, -m)
        return m

    def add_words(self, a: list[int], b: list[int], carry: int | None = None) -> list[int]:
        assert len(a) == len(b)
        c = self.false if carry is None else carry
        answer = []
        for ai, bi in zip(a, b):
            answer.append(self.xor3(ai, bi, c))
            c = self.majority(ai, bi, c)
        return answer

    def neg_word(self, a: list[int]) -> list[int]:
        return self.add_words([self.inv(x) for x in a], self.constant(1, len(a)))

    def constant(self, value: int, width: int) -> list[int]:
        return [-self.false if (value >> i) & 1 else self.false for i in range(width)]

    def equal(self, a: list[int], b: list[int]) -> None:
        assert len(a) == len(b)
        for ai, bi in zip(a, b):
            self.add(-ai, bi)
            self.add(ai, -bi)

    def sigma(self, word: list[int], which: int) -> list[int]:
        assert len(word) == 32
        r1, r2, shift = (7, 18, 3) if which == 0 else (17, 19, 10)
        answer = []
        for bit in range(32):
            shifted = word[bit + shift] if bit + shift < 32 else self.false
            answer.append(self.xor3(word[(bit + r1) % 32],
                                   word[(bit + r2) % 32], shifted))
        return answer

    def difference_low26(self, after: list[int], before: list[int]) -> list[int]:
        # Low 26 bits of 32-bit modular subtraction depend only on low 26 bits.
        inv = [self.inv(x) for x in before[:26]]
        return self.add_words(after[:26], inv, -self.false)

    def dimacs(self) -> bytes:
        lines = [f"p cnf {self.nvars} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return ("\n".join(lines) + "\n").encode()


def expression(cnf: CNF, scalar: dict[str, list[int]], terms) -> list[int]:
    value = cnf.constant(0, 26)
    for sign, name in terms:
        term = scalar[name] if sign == 1 else cnf.neg_word(scalar[name])
        value = cnf.add_words(value, term)
    return value


def build() -> CNF:
    cnf = CNF()
    scalar = {name: cnf.word(name, 26) for name in SCALARS}
    cnf.equal(scalar["b"], cnf.constant(B_FIXED, 26))

    # Exact-support conditions inherited from the corrected factor theorem.
    for number, terms in enumerate((
        ((1, "a"),), ((1, "b"),), ((1, "c"),), ((1, "k"),),
        ((1, "p"), (1, "a")), ((1, "q"), (1, "s")), ((1, "z"),),
    )):
        value = expression(cnf, scalar, terms)
        cnf.add(*value)  # nonzero modulo 2^26

    for index, kind, d_terms, f_terms, g_terms in FACTORS:
        x = cnf.word(f"x{index}", 32)
        y = cnf.word(f"y{index}", 32)

        # y-x=d modulo 2^26.  Bits 26..31 are deliberately not coupled.
        d = expression(cnf, scalar, d_terms)
        cnf.equal(cnf.add_words(x[:26], d), y[:26])

        if f_terms is not None:
            sx = cnf.sigma(x, 0)
            sy = cnf.sigma(y, 0)
            f = cnf.difference_low26(sy, sx)
            cnf.equal(f, expression(cnf, scalar, f_terms))
        if g_terms is not None:
            sx = cnf.sigma(x, 1)
            sy = cnf.sigma(y, 1)
            g = cnf.difference_low26(sy, sx)
            cnf.equal(g, expression(cnf, scalar, g_terms))
    return cnf


def eval_terms(values: dict[str, int], terms) -> int:
    return sum(sign * values[name] for sign, name in terms) & MASK26


def direct_check(values: dict[str, int], pairs: dict[str, dict[str, str]]) -> dict:
    assert values["b"] == B_FIXED
    assert all(0 <= values[name] <= MASK26 for name in SCALARS)
    nonzero_terms = (
        ((1, "a"),), ((1, "b"),), ((1, "c"),), ((1, "k"),),
        ((1, "p"), (1, "a")), ((1, "q"), (1, "s")), ((1, "z"),),
    )
    assert all(eval_terms(values, terms) != 0 for terms in nonzero_terms)
    checked = []
    high_bits = []
    for index, kind, d_terms, f_terms, g_terms in FACTORS:
        x = int(pairs[str(index)]["x"], 16)
        y = int(pairs[str(index)]["y"], 16)
        d32 = (y - x) & MASK32
        f32 = (sigma0(y) - sigma0(x)) & MASK32
        g32 = (sigma1(y) - sigma1(x)) & MASK32
        assert (d32 & MASK26) == eval_terms(values, d_terms)
        if f_terms is not None:
            assert (f32 & MASK26) == eval_terms(values, f_terms)
        if g_terms is not None:
            assert (g32 & MASK26) == eval_terms(values, g_terms)
        checked.append({
            "index": index, "kind": kind,
            "x": f"{x:08x}", "y": f"{y:08x}",
            "d32": f"{d32:08x}", "F32": f"{f32:08x}", "G32": f"{g32:08x}",
            "d26": f"{d32 & MASK26:07x}",
            "F26": f"{f32 & MASK26:07x}",
            "G26": f"{g32 & MASK26:07x}",
        })
        high_bits.append({
            "index": index,
            "d_high6": d32 >> 26,
            "F_high6": f32 >> 26,
            "G_high6": g32 >> 26,
        })
    return {
        "status": "PASS",
        "direct_sigma_checks": len(checked),
        "factors": checked,
        "observed_uncoupled_high6": high_bits,
        "scope": "low26 factor feasibility only; no full32 factor or common-base/message claim",
    }


def solve_milp(cnf: CNF, time_limit: float) -> dict:
    import numpy as np
    import scipy
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_array

    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    lower = np.empty(len(cnf.clauses), dtype=float)
    for row, clause in enumerate(cnf.clauses):
        negatives = 0
        for literal in clause:
            rows.append(row)
            cols.append(abs(literal) - 1)
            data.append(1.0 if literal > 0 else -1.0)
            negatives += literal < 0
        lower[row] = 1 - negatives
    matrix = coo_array((np.array(data), (np.array(rows), np.array(cols))),
                       shape=(len(cnf.clauses), cnf.nvars)).tocsr()
    started = time.monotonic()
    result = milp(
        c=np.zeros(cnf.nvars), integrality=np.ones(cnf.nvars),
        bounds=Bounds(np.zeros(cnf.nvars), np.ones(cnf.nvars)),
        constraints=LinearConstraint(matrix, lower, np.full(len(lower), np.inf)),
        options={"time_limit": time_limit, "presolve": True},
    )
    elapsed = time.monotonic() - started
    answer = {
        "backend": "scipy.optimize.milp/HiGHS",
        "scipy": scipy.__version__,
        "seconds": elapsed,
        "status_code": int(result.status),
        "message": result.message,
        "sat": result.status == 0,
    }
    if result.status != 0:
        return answer
    model = np.rint(result.x).astype(int)
    decode = lambda name: sum(int(model[var - 1]) << bit
                              for bit, var in enumerate(cnf.names[name]))
    values = {name: decode(name) for name in SCALARS}
    pairs = {str(index): {"x": f"{decode(f'x{index}'):08x}",
                          "y": f"{decode(f'y{index}'):08x}"}
             for index, *_ in FACTORS}
    answer["scalars"] = {name: f"{value:07x}" for name, value in values.items()}
    answer["pairs"] = pairs
    answer["direct_check"] = direct_check(values, pairs)
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--time-limit", type=float, default=900.0)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--write-cnf", action="store_true")
    parser.add_argument("--emit-only", action="store_true")
    parser.add_argument("--decode-model", type=Path)
    args = parser.parse_args()
    if args.check:
        data = json.loads(args.check.read_text())
        values = {name: int(data["scalars"][name], 16) for name in SCALARS}
        print(json.dumps(direct_check(values, data["pairs"]), indent=2, sort_keys=True))
        return

    cnf = build()
    dimacs = cnf.dimacs()
    if args.write_cnf:
        (HERE / "independent.cnf").write_bytes(dimacs)
    if args.emit_only:
        print(json.dumps({"variables": cnf.nvars, "clauses": len(cnf.clauses),
                          "cnf_sha256": hashlib.sha256(dimacs).hexdigest()},
                         sort_keys=True))
        return
    if args.decode_model:
        bits = [int(x) for x in args.decode_model.read_text().split()]
        assert len(bits) == cnf.nvars and set(bits) <= {0, 1}
        decode = lambda name: sum(bits[var - 1] << bit
                                  for bit, var in enumerate(cnf.names[name]))
        values = {name: decode(name) for name in SCALARS}
        pairs = {str(index): {"x": f"{decode(f'x{index}'):08x}",
                              "y": f"{decode(f'y{index}'):08x}"}
                 for index, *_ in FACTORS}
        print(json.dumps({
            "scalars": {name: f"{value:07x}" for name, value in values.items()},
            "pairs": pairs, "direct_check": direct_check(values, pairs),
        }, indent=2, sort_keys=True))
        return
    result = solve_milp(cnf, args.time_limit)
    result.update({
        "schema": "CRYPTO3-support12-factor-signature-review-v9-blind-low26",
        "python": platform.python_version(),
        "fixed_b": f"{B_FIXED:07x}",
        "modulus": 1 << 26,
        "variables": cnf.nvars,
        "clauses": len(cnf.clauses),
        "cnf_sha256": hashlib.sha256(dimacs).hexdigest(),
        "high_bits_coupled": 0,
        "high_bits_per_projected_coordinate": 6,
    })
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["sat"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
