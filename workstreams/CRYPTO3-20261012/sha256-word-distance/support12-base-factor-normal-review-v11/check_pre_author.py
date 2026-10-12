#!/usr/bin/env python3
"""Independent pre-author checker for the support-12 18-word normal form."""

from __future__ import annotations

import json
import random

M = (1 << 32) - 1
T = (10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43)
P = (9, 12, 14, 19, 22)
S = T + (57,)
ORDER0 = (
    (26, 24), (28, 21), (29, 27), (34, 32), (36, 36), (43, 41),
    (27, 25), (41, 39), (25, 23), (30, 30), (39, 37), (44, 44),
    (37, 35), (42, 40), (35, 33), (40, 38), (45, 45), (38, 31),
    (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51),
    (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (58, 58),
    (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (31, 16),
    (32, 17), (24, 8), (23, 7), (22, 6), (21, 5), (20, 4),
    (19, 3), (18, 2), (17, 1), (16, 0),
)
ORDER = ORDER0[:29] + ((57, 57),) + ORDER0[29:]


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def f(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def g(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def invmap(fn):
    basis = {}
    for j in range(32):
        y, x = fn(1 << j), 1 << j
        while y:
            p = (y & -y).bit_length() - 1
            if p not in basis:
                basis[p] = (y, x)
                break
            y ^= basis[p][0]
            x ^= basis[p][1]
        else:
            raise AssertionError("singular sigma")

    def inv(y):
        x = 0
        while y:
            p = (y & -y).bit_length() - 1
            y ^= basis[p][0]
            x ^= basis[p][1]
        return x

    return inv


IF, IG = invmap(f), invmap(g)


def pos(t):
    return (t, t - 2, t - 7, t - 15, t - 16)


def residual(w, t):
    return (w[t] - g(w[t - 2]) - w[t - 7] - f(w[t - 15]) - w[t - 16]) & M


def chart(inputs):
    w = [None] * 64
    for i, x in inputs.items():
        assert i in T + P and w[i] is None and 0 <= x <= M
        w[i] = x
    for t, target in ORDER:
        unknown = [i for i in pos(t) if w[i] is None]
        assert unknown == [target], (t, target, unknown)
        terms = ((t - 2, g, IG), (t - 7, int, int),
                 (t - 15, f, IF), (t - 16, int, int))
        if target == t:
            w[target] = sum(fn(w[i]) for i, fn, _ in terms) & M
        else:
            rhs = sum(fn(w[i]) for i, fn, _ in terms if i != target)
            inv = next(iv for i, _, iv in terms if i == target)
            w[target] = inv((w[t] - rhs) & M)
    assert all(x is not None for x in w)
    return w


def dependency():
    d = [None] * 64
    for i in T + P:
        d[i] = {f"x{i}"}
    for t, target in ORDER:
        assert [i for i in pos(t) if d[i] is None] == [target]
        d[target] = set().union(*(d[i] for i in pos(t) if i != target))
    return d


def d0(x, d):
    return (f((x + d) & M) - f(x)) & M


def d1(x, d):
    return (g((x + d) & M) - g(x)) & M


def defs(w, z):
    H = w[57]
    b = d1(H, z)
    k = (-d1(w[20], -b & M)) & M
    a = (-d1(w[15], k)) & M
    c = (-d1(w[43], -b & M)) & M
    p = d0(w[11], b)
    q = d0(w[13], c)
    l = d0(w[15], k)
    s = d1(w[26], (p + a) & M)
    ww = d0(w[29], c)
    return {"a": a, "b": b, "c": c, "k": k, "p": p,
            "q": q, "l": l, "s": s, "w": ww, "z": z}


def local22(w, v):
    a, b, c, k = (v[x] for x in "abck")
    p, q, l, s, ww, z = (v[x] for x in ("p", "q", "l", "s", "w", "z"))
    return {
        "10F": (d0(w[10], a) + b) & M,
        "11F": (d0(w[11], b) - p) & M,
        "13F": (d0(w[13], c) - q) & M,
        "15F": (d0(w[15], k) - l) & M,
        "15G": (d1(w[15], k) + a) & M,
        "18F": (d0(w[18], b) + p + a) & M,
        "18G": (d1(w[18], b) + b + c) & M,
        "20F": (d0(w[20], -b & M) + q + s) & M,
        "20G": (d1(w[20], -b & M) + k) & M,
        "26F": (d0(w[26], (p + a) & M) + b) & M,
        "26G": (d1(w[26], (p + a) & M) - s) & M,
        "28F": (d0(w[28], (q + s) & M) + b) & M,
        "28G": (d1(w[28], (q + s) & M) + l) & M,
        "29F": (d0(w[29], c) - ww) & M,
        "29G": (d1(w[29], c) + k) & M,
        "34F": (d0(w[34], b) + p + a) & M,
        "34G": (d1(w[34], b) - b + c) & M,
        "42F": (d0(w[42], (p + a) & M) - z) & M,
        "42G": (d1(w[42], (p + a) & M) + ww + q + s) & M,
        "43F": (d0(w[43], -b & M) + p + a) & M,
        "43G": (d1(w[43], -b & M) + c) & M,
        "57G": (d1(w[57], z) - b) & M,
    }


ELIMINATED = {"11F", "13F", "15F", "15G", "20G", "26G", "29F", "43G", "57G"}
REMAINING = ("10F", "18F", "18G", "20F", "26F", "28F", "28G",
             "29G", "34F", "34G", "42F", "42G", "43F")


def difference_table(v):
    a, b, c, k = (v[x] for x in "abck")
    p, q, l, s, ww, z = (v[x] for x in ("p", "q", "l", "s", "w", "z"))
    return {
        10: (a, -b & M, None), 11: (b, p, None), 13: (c, q, None),
        15: (k, l, -a & M), 18: (b, -p-a & M, -b-c & M),
        20: (-b & M, -q-s & M, -k & M),
        26: ((p+a) & M, -b & M, s),
        28: ((q+s) & M, -b & M, -l & M),
        29: (c, ww, -k & M), 34: (b, -p-a & M, (b-c) & M),
        42: ((p+a) & M, z, -ww-q-s & M),
        43: (-b & M, -p-a & M, -c & M), 57: (z, None, b),
    }


def diff_rows(table):
    out = []
    for t in range(16, 64):
        dt = table.get(t, (0, 0, 0))[0]
        G2 = table.get(t - 2, (0, 0, 0))[2] or 0
        d7 = table.get(t - 7, (0, 0, 0))[0]
        F15 = table.get(t - 15, (0, 0, 0))[1] or 0
        d16 = table.get(t - 16, (0, 0, 0))[0]
        out.append((dt - G2 - d7 - F15 - d16) & M)
    return out


def main():
    deps = dependency()
    assert len(ORDER) == len({t for t, _ in ORDER}) == len({x for _, x in ORDER}) == 47
    assert set(range(16, 64)) - {t for t, _ in ORDER} == {33}
    assert "x57" not in set().union(*deps)
    # z is not a chart input, hence H and R33 are structurally z-independent.

    rng = random.Random(0x12BA5EFAC)
    trials = 10000
    for _ in range(trials):
        inp = {i: rng.getrandbits(32) for i in T + P}
        w = chart(inp)
        assert all(residual(w, t) == 0 for t, _ in ORDER)
        z = rng.getrandbits(32)
        v = defs(w, z)
        eq = local22(w, v)
        assert len(eq) == 22 and all(eq[x] == 0 for x in ELIMINATED)
        assert tuple(x for x in eq if x not in ELIMINATED) == REMAINING
        assert len(REMAINING) == 13
        table = difference_table(v)
        assert all(x == 0 for x in diff_rows(table))
        classes = [v["a"], v["b"], v["c"], v["k"],
                   (v["p"] + v["a"]) & M, (v["q"] + v["s"]) & M, z]
        ds = [table[i][0] for i in S]
        assert all(ds) == all(classes)

    # Damage controls cover an easy sign error, a wrong q+s incidence, a
    # projected/wrong-base position-57 derivative, and omission of R33.
    inp = {i: rng.getrandbits(32) for i in T + P}
    w = chart(inp)
    v = defs(w, 1)
    good = local22(w, v)
    bad_sign = dict(v); bad_sign["c"] = (-v["c"]) & M
    assert local22(w, bad_sign) != good
    bad_incidence = dict(v); bad_incidence["s"] = (v["s"] + 1) & M
    assert local22(w, bad_incidence)["28F"] != good["28F"]
    projected_b = d1(0, 1)
    forced_b = d1(4, 1)
    assert projected_b == 0xA000 and forced_b == 0xFFFFA000 and projected_b != forced_b
    damaged = list(w); damaged[33] = (damaged[33] + 1) & M
    assert residual(damaged, 33) != residual(w, 33)

    result = {
        "schema": "CRYPTO3-support12-base-factor-normal-review-v11-pre-author",
        "status": "PASS",
        "free_words": 18,
        "base_inputs": 17,
        "extra_factor_words": ["z"],
        "local_factor_equalities_before": 22,
        "triangular_definitions": 9,
        "local_factor_equalities_after": 13,
        "total_equations_with_R33": 14,
        "nonzero_classes": ["a", "b", "c", "k", "p+a", "q+s", "z"],
        "active_positions": list(S),
        "random_identity_trials": trials,
        "rewritten_chart_rows": 47,
        "only_residual_row": 33,
        "H_and_R33_independent_of_z": True,
        "position57_condition": "D1(H,z)=b",
        "negative_controls": 4,
        "scope": "algebraic equivalence only; no satisfiability, message witness, distance-14 bound, Lean, or human review",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
