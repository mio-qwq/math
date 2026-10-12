#!/usr/bin/env python3
"""One fixed Z3 discovery query for the support-12 low-26 factor relaxation.

This is discovery code, not the trusted checker.  check.py verifies the emitted
certificate using only the Python standard library.
"""

import json
import platform
import z3

W = 32
M = 26
MOD32 = 1 << 32
LOW = (1 << M) - 1


def sigma0(x):
    return z3.RotateRight(x, 7) ^ z3.RotateRight(x, 18) ^ z3.LShR(x, 3)


def sigma1(x):
    return z3.RotateRight(x, 17) ^ z3.RotateRight(x, 19) ^ z3.LShR(x, 10)


def factors(v):
    return [
        (10, "PF", v["a"], -v["b"], None),
        (11, "PF", v["b"], v["p"], None),
        (13, "PF", v["c"], v["q"], None),
        (15, "J", v["k"], v["l"], -v["a"]),
        (18, "J", v["b"], -v["p"] - v["a"], -v["b"] - v["c"]),
        (20, "J", -v["b"], -v["q"] - v["s"], -v["k"]),
        (26, "J", v["p"] + v["a"], -v["b"], v["s"]),
        (28, "J", v["q"] + v["s"], -v["b"], -v["l"]),
        (29, "J", v["c"], v["w"], -v["k"]),
        (34, "J", v["b"], -v["p"] - v["a"], v["b"] - v["c"]),
        (42, "J", v["p"] + v["a"], v["z"], -v["w"] - v["q"] - v["s"]),
        (43, "J", -v["b"], -v["p"] - v["a"], -v["c"]),
        (57, "PG", v["z"], None, v["b"]),
    ]


def main():
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=180_000, random_seed=777)
    names = "a b c k p q l s w z".split()
    values = {name: z3.BitVec(f"{name}_{M}", M) for name in names}
    solver.add(values["b"] == z3.BitVecVal(1 << 16, M))
    pairs = {}
    facs = factors(values)
    for index, kind, d, f_value, g_value in facs:
        # Nonzero low residues are an optional strengthening of the relaxation.
        solver.add(d != 0)
        if f_value is not None:
            solver.add(f_value != 0)
        if g_value is not None:
            solver.add(g_value != 0)
        x = z3.BitVec(f"x{index}_{M}", W)
        y = z3.BitVec(f"y{index}_{M}", W)
        pairs[index] = (x, y)
        solver.add(z3.Extract(M - 1, 0, y - x) == d)
        if f_value is not None:
            solver.add(z3.Extract(M - 1, 0, sigma0(y) - sigma0(x)) == f_value)
        if g_value is not None:
            solver.add(z3.Extract(M - 1, 0, sigma1(y) - sigma1(x)) == g_value)
    result = solver.check()
    if result != z3.sat:
        raise SystemExit(f"expected sat, got {result}: {solver.reason_unknown()}")
    model = solver.model()
    out = {
        "schema": "support12-factor-low26-witness-v1",
        "python": platform.python_version(),
        "z3": z3.get_version_string(),
        "width": M,
        "fixed_b": "00010000",
        "scalars": {name: f"{model.eval(values[name]).as_long():08x}" for name in names},
        "pairs": {
            str(index): {
                "kind": kind,
                "x": f"{model.eval(pairs[index][0]).as_long():08x}",
                "y": f"{model.eval(pairs[index][1]).as_long():08x}",
            }
            for index, kind, _, _, _ in facs
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
