#!/usr/bin/env python3
"""Exact support interfaces and XOR-translation fibre diagnostics.

No SAT solver or external dependency is used. This script is a discovery
calculation; a separate direct-bit checker will bind any claimed result.
"""
from __future__ import annotations

import json
from pathlib import Path

MASK = (1 << 32) - 1
LOW = (1 << 31) - 1
S = (2, 9, 10, 16, 23, 24, 30, 37, 38, 44, 51, 52, 58)


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def f(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def g(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def interface(x, y):
    return ((y - x) & MASK, (f(y) - f(x)) & MASK, (g(y) - g(x)) & MASK)


def row(function, bit):
    return sum(((function(1 << j) >> bit) & 1) << j for j in range(32))


def kernel(rows):
    pivots = {}
    for value in rows:
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    basis = []
    for free in range(32):
        if free in pivots:
            continue
        value = 1 << free
        for pivot in sorted(pivots):
            if (pivots[pivot] & value).bit_count() & 1:
                value |= 1 << pivot
        basis.append(value)
    assert all(not (r & v).bit_count() % 2 for r in rows for v in basis)
    return basis


def span(basis):
    values = [0]
    for word in basis:
        values.extend(v ^ word for v in values[:])
    return values


def fibre(x, y, preserve):
    alpha = x ^ y
    functions = {"d": lambda a: a, "F": f, "G": g}
    rows = []
    for name in preserve:
        fun = functions[name]
        beta = fun(alpha) & LOW
        rows.extend(row(fun, i) for i in range(31) if (beta >> i) & 1)
    basis = kernel(rows)
    assert len(basis) <= 20, "bounded fibre limit"
    values = [(x ^ z, y ^ z) for z in span(basis)]
    data = {
        "seed": [x, y],
        "seed_interface": list(interface(x, y)),
        "xor_mask": alpha,
        "preserve": list(preserve),
        "dimension": len(basis),
        "basis": basis,
        "pair_count": len(values),
        "distinct_interfaces": sorted({interface(a, b) for a, b in values}),
    }
    return data


def equations():
    eqs = []
    for t in range(16, 64):
        terms = [(1, "d", t), (-1, "G", t - 2),
                 (-1, "d", t - 7), (-1, "F", t - 15),
                 (-1, "d", t - 16)]
        active = [term for term in terms if term[2] in S]
        eqs.append({"t": t, "terms": active})
    return eqs


def main():
    # Root supplied the first seed; this program recomputes its interface.
    p = (0x96e4e732, 0x1f60538d)
    q = (0x00305680, 0x88abc2db)
    assert interface(*p)[0] == interface(*q)[0] != 0
    assert (interface(*p)[1] + interface(*q)[1]) & MASK == 0
    assert (interface(*q)[0] + interface(*q)[2]) & MASK == 0
    report = {
        "schema": "crypto3-support0-active-interface-analysis-v1",
        "support": list(S),
        "equations": equations(),
        "nontrivial_equations": sum(bool(e["terms"]) for e in equations()),
        "seed_origin": "Root supplied the four words; interfaces recomputed here.",
        "fibres": {
            "q_dG": fibre(*q, "dG"),
            "q_dFG": fibre(*q, "dFG"),
            "p_dF": fibre(*p, "dF"),
            "p_dFG": fibre(*p, "dFG"),
        },
        "scope": "Local actual pairs only; no complete difference or base lift claimed.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
