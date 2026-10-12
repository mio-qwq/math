#!/usr/bin/env python3
"""Independent fixed-D circuit reconstruction and MILP SAT check.

This file deliberately does not import or execute the author's generator.
Bits are little endian.  Every non-input circuit wire gets a Tseitin
variable, and every claimed word equality is imposed by unit/equivalence
clauses.  The DIMACS instance can also be checked by any ordinary SAT solver.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

MASK = (1 << 32) - 1
D = 0x000F0000
HERE = Path(__file__).resolve().parent


def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def sigma0(x: int) -> int:
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x: int) -> int:
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def derivative(fn, x: int) -> int:
    return (fn((x + D) & MASK) - fn(x)) & MASK


class CNF:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[tuple[int, ...]] = []
        self.names: dict[str, list[int]] = {}
        self.false = self.var("false")
        self.add(-self.false)

    def var(self, _name: str = "") -> int:
        self.nvars += 1
        return self.nvars

    def word(self, name: str) -> list[int]:
        out = [self.var(f"{name}[{i}]") for i in range(32)]
        self.names[name] = out
        return out

    def add(self, *lits: int) -> None:
        assert lits and all(x != 0 and abs(x) <= self.nvars for x in lits)
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
        # m iff at least two of a,b,c are true.
        self.add(-a, -b, m)
        self.add(-a, -c, m)
        self.add(-b, -c, m)
        self.add(a, b, -m)
        self.add(a, c, -m)
        self.add(b, c, -m)
        return m

    def add_words(self, a: list[int], b: list[int], carry: int | None = None) -> list[int]:
        assert len(a) == len(b) == 32
        c = self.false if carry is None else carry
        out = []
        for ai, bi in zip(a, b):
            out.append(self.xor3(ai, bi, c))
            c = self.majority(ai, bi, c)
        return out

    def constant(self, x: int) -> list[int]:
        return [-self.false if ((x >> i) & 1) else self.false for i in range(32)]

    def equal(self, a: list[int], b: list[int]) -> None:
        assert len(a) == len(b)
        for ai, bi in zip(a, b):
            self.add(-ai, bi)
            self.add(ai, -bi)

    def zero(self, a: list[int]) -> None:
        for ai in a:
            self.add(-ai)

    def sigma(self, w: list[int], which: int) -> list[int]:
        if which == 0:
            r1, r2, shift = 7, 18, 3
        else:
            r1, r2, shift = 17, 19, 10
        out = []
        for i in range(32):
            sh = w[i + shift] if i + shift < 32 else self.false
            out.append(self.xor3(w[(i + r1) % 32], w[(i + r2) % 32], sh))
        return out

    def derivative(self, w: list[int], which: int) -> list[int]:
        wd = self.add_words(w, self.constant(D))
        after = self.sigma(wd, which)
        before = self.sigma(w, which)
        # after - before = after + bitwise-not(before) + 1 mod 2^32.
        before_inv = [self.inv(v) for v in before]
        return self.add_words(after, before_inv, -self.false)

    def dimacs(self) -> bytes:
        lines = [f"p cnf {self.nvars} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, c)) + " 0" for c in self.clauses)
        return ("\n".join(lines) + "\n").encode()


def build(drop_last_gz_equation: bool = False) -> CNF:
    cnf = CNF()
    x, y, z = cnf.word("x"), cnf.word("y"), cnf.word("z")
    fx, gx = cnf.derivative(x, 0), cnf.derivative(x, 1)
    fy, gy = cnf.derivative(y, 0), cnf.derivative(y, 1)
    fz, gz = cnf.derivative(z, 0), cnf.derivative(z, 1)

    # A=F_D(x), T=G_D(x)+D has been substituted out:
    # F_D(y)=F_D(x); G_D(y)=G_D(x)+2D;
    # F_D(z)=-F_D(x); G_D(z)=-G_D(x)-D.
    cnf.equal(fy, fx)
    cnf.equal(gy, cnf.add_words(gx, cnf.constant((2 * D) & MASK)))
    cnf.zero(cnf.add_words(fz, fx))
    last = cnf.add_words(cnf.add_words(gz, gx), cnf.constant(D))
    for bit, wire in enumerate(last):
        if not drop_last_gz_equation:
            cnf.add(-wire)
    return cnf


def solve_milp(cnf: CNF, time_limit: float) -> dict:
    import numpy as np
    from scipy import __version__ as scipy_version
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_array

    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    lower = np.empty(len(cnf.clauses), dtype=float)
    for row, clause in enumerate(cnf.clauses):
        negatives = 0
        for lit in clause:
            rows.append(row)
            cols.append(abs(lit) - 1)
            data.append(1.0 if lit > 0 else -1.0)
            negatives += lit < 0
        lower[row] = 1 - negatives
    matrix = coo_array((np.array(data), (np.array(rows), np.array(cols))),
                       shape=(len(cnf.clauses), cnf.nvars)).tocsr()
    constraint = LinearConstraint(matrix, lower, np.full(len(lower), np.inf))
    started = time.monotonic()
    result = milp(
        c=np.zeros(cnf.nvars),
        integrality=np.ones(cnf.nvars),
        bounds=Bounds(np.zeros(cnf.nvars), np.ones(cnf.nvars)),
        constraints=constraint,
        options={"time_limit": time_limit, "presolve": True},
    )
    elapsed = time.monotonic() - started
    answer = {
        "backend": "scipy.optimize.milp/HiGHS",
        "scipy": scipy_version,
        "status_code": int(result.status),
        "message": result.message,
        "seconds": elapsed,
        "sat": None if result.status not in (0, 2) else result.status == 0,
    }
    if result.status == 0:
        vals = np.rint(result.x).astype(int)
        witness = {}
        for name in ("x", "y", "z"):
            word = sum(int(vals[v - 1]) << i for i, v in enumerate(cnf.names[name]))
            witness[name] = f"{word:08x}"
        answer["witness"] = witness
        answer["direct_check"] = direct_check(*(int(witness[n], 16) for n in ("x", "y", "z")))
    return answer


def direct_check(x: int, y: int, z: int, drop_last_gz_equation: bool = False) -> bool:
    fx, gx = derivative(sigma0, x), derivative(sigma1, x)
    fy, gy = derivative(sigma0, y), derivative(sigma1, y)
    fz, gz = derivative(sigma0, z), derivative(sigma1, z)
    last = (gz + gx + D) & MASK
    return (fy == fx and gy == ((gx + 2 * D) & MASK)
            and ((fz + fx) & MASK) == 0
            and (drop_last_gz_equation or last == 0))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true", help="drop G_D(z)=-T")
    parser.add_argument("--emit-only", action="store_true", help="write DIMACS without solving")
    parser.add_argument("--time-limit", type=float, default=300.0)
    args = parser.parse_args()
    cnf = build(args.negative)
    dimacs = cnf.dimacs()
    path = HERE / ("near_miss.cnf" if args.negative else "independent.cnf")
    path.write_bytes(dimacs)
    if args.emit_only:
        print(json.dumps({"mode": "drop_G_D(z)=-T" if args.negative else "exact",
                          "variables": cnf.nvars, "clauses": len(cnf.clauses),
                          "cnf_sha256": hashlib.sha256(dimacs).hexdigest()},
                         sort_keys=True, indent=2))
        return
    result = solve_milp(cnf, args.time_limit)
    result.update({
        "python": platform.python_version(),
        "mode": "drop_G_D(z)=-T" if args.negative else "exact",
        "variables": cnf.nvars,
        "clauses": len(cnf.clauses),
        "cnf_sha256": hashlib.sha256(dimacs).hexdigest(),
    })
    print(json.dumps(result, sort_keys=True, indent=2))
    if result["sat"] is None:
        raise SystemExit(2)
    if args.negative and not result["sat"]:
        raise SystemExit("negative control unexpectedly UNSAT")
    if not args.negative and result["sat"]:
        raise SystemExit("exact instance unexpectedly SAT")


if __name__ == "__main__":
    main()
