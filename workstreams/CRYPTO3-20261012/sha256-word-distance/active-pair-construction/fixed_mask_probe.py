#!/usr/bin/env python3
"""One complete fixed-mask construction-family probe; no SMT.

The mask family is stated in MECHANISM.md before this calculation.
Every word pair at every active coordinate is an independent variable.
An early empty mandatory interface proves failure of this restricted
family, and deliberately stops the probe without searching other masks.
"""
from __future__ import annotations

import json

from analyze import LOW, MASK, f, g, interface, row, span, fibre

FUN = {"d": lambda x: x, "F": f, "G": g}


def affine(rows):
    pivots = {}
    for number, item in enumerate(rows):
        coefficient, rhs = item["row"], item["rhs"]
        used = 1 << number
        while coefficient:
            pivot = coefficient.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (coefficient, rhs, used)
                break
            other, bit, provenance = pivots[pivot]
            coefficient ^= other
            rhs ^= bit
            used ^= provenance
        else:
            if rhs:
                return {"status": "empty", "reason": "linear_conflict",
                        "combination": [j for j in range(len(rows)) if used >> j & 1]}
    particular = 0
    for pivot in sorted(pivots):
        coefficient, rhs, _ = pivots[pivot]
        if ((coefficient & particular).bit_count() & 1) != rhs:
            particular |= 1 << pivot
    basis = []
    for free in range(32):
        if free in pivots:
            continue
        value = 1 << free
        for pivot in sorted(pivots):
            if (pivots[pivot][0] & value).bit_count() & 1:
                value |= 1 << pivot
        basis.append(value)
    assert all(((r["row"] & particular).bit_count() & 1) == r["rhs"] for r in rows)
    assert all(not (r["row"] & v).bit_count() % 2 for r in rows for v in basis)
    return {"status": "nonempty", "particular": particular,
            "dimension": len(basis), "basis": basis, "rank": len(pivots)}


def solve_mask(alpha, requirements):
    rows = []
    result = {"input_xor_mask": alpha, "requirements": requirements}
    for kind, target in requirements.items():
        function = FUN[kind]
        beta = function(alpha)
        delta = (beta - target) & MASK
        if delta & 1:
            result.update(status="empty", reason="parity", kind=kind,
                          output_mask=beta, target=target)
            return result
        signs = delta >> 1
        bad = signs & (~beta & LOW)
        if bad:
            result.update(status="empty", reason="unavailable_sign_bit", kind=kind,
                          output_mask=beta, target=target,
                          required_sign_word=signs,
                          impossible_bit=(bad & -bad).bit_length() - 1)
            return result
        for bit in range(31):
            if beta >> bit & 1:
                rows.append({"kind": kind, "bit": bit,
                             "row": row(function, bit), "rhs": (signs >> bit) & 1})
    result["rows"] = rows
    result.update(affine(rows))
    return result


def all_pairs(solution):
    assert solution["status"] == "nonempty"
    assert solution["dimension"] <= 20, "bounded exact enumeration cap"
    for z in span(solution["basis"]):
        a = solution["particular"] ^ z
        yield a, a ^ solution["input_xor_mask"]


def main():
    q = (0x00305680, 0x88abc2db)
    p = (0x96e4e732, 0x1f60538d)
    D = (q[1] - q[0]) & MASK
    alpha_q, alpha_p = q[0] ^ q[1], p[0] ^ p[1]
    alpha_r = f(alpha_q)

    q_solution = solve_mask(alpha_q, {"d": D, "G": (-D) & MASK})
    assert q_solution["status"] == "nonempty"
    q_pairs = list(all_pairs(q_solution))
    q_by_a = {}
    for a, b in q_pairs:
        A = (-interface(a, b)[1]) & MASK
        q_by_a.setdefault(A, []).append([a, b])

    p_solutions = []
    viable_p = {}
    for A in sorted(q_by_a):
        solution = solve_mask(alpha_p, {"d": D, "F": A})
        p_solutions.append(solution)
        if solution["status"] == "nonempty":
            entries = []
            for a, b in all_pairs(solution):
                assert interface(a, b)[:2] == (D, A)
                entries.append({"pair": [a, b], "G": interface(a, b)[2]})
            viable_p[A] = entries

    # Every complete family assignment needs R_3 at index 52 with
    # d(R_3)=F(P_2)=A_2 and G(R_3)=-d(R_2)=-F(P_1)=-A_1.
    terminal = []
    for A1 in sorted(viable_p):
        for A2 in sorted(viable_p):
            solution = solve_mask(alpha_r, {"d": A2, "G": (-A1) & MASK})
            solution.update(A1=A1, A2=A2)
            terminal.append(solution)
    survivors = [x for x in terminal if x["status"] == "nonempty"]

    report = {
        "schema": "crypto3-support0-fixed-mask-construction-v1",
        "D": D,
        "masks": {"Q": alpha_q, "P": alpha_p, "R": alpha_r},
        "q_fibre": q_solution,
        "q_pairs": q_pairs,
        "q_A_values": sorted(q_by_a),
        "p_opposite_F_fibres": p_solutions,
        "p_viable_interfaces": {str(a): v for a, v in sorted(viable_p.items())},
        "terminal_R3_fibres": terminal,
        "terminal_surviving_interfaces": len(survivors),
        "result": ("restricted_family_excluded_at_terminal_R3" if not survivors
                   else "terminal_not_excluded_no_full_family_claim"),
        "scope": "One D and three fixed XOR masks only; not an exclusion of support 0.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
