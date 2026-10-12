#!/usr/bin/env python3
"""Exact fixed-mask affine carry compilation for the coupled equations."""

import hashlib
import json
import time
from pathlib import Path

from mask_probe import K, MASK, f, g

HERE = Path(__file__).resolve().parent


def verify_local_tables():
    cases = []
    for active in (0, 1, 2):
        for t in ((0, 1) if active == 1 else (0,)):
            for u in ((0, 1) if active else (0,)):
                for v in ((0, 1) if active == 2 else (0,)):
                    incoming = 1-2*t if active == 1 else 0
                    total = incoming + ((1-2*u) if active else 0) + ((1-2*v) if active == 2 else 0)
                    assert total % 2 == 0
                    outgoing = total // 2
                    assert outgoing in (-1, 0, 1)
                    for next_parity in (0, 1):
                        arithmetic = outgoing % 2 == next_parity
                        linear = (next_parity == 0) if active == 0 else (
                            (t ^ u) == (1 ^ next_parity) if active == 1 else
                            (u ^ v) == (1 ^ next_parity))
                        assert arithmetic == linear
                        if arithmetic and next_parity:
                            assert outgoing == 1-2*u
                        cases.append({"active": active, "incoming_sign": t,
                                      "u": u, "v": v, "next_parity": next_parity,
                                      "outgoing": outgoing, "accepted": arithmetic})
    assert len(cases) == 18
    return cases


def bits(offset=0, complement=0):
    return [(1 << (offset+i), complement) for i in range(32)]


def sigma_forms(function, offset=0):
    return [(sum(((function(1 << j) >> i) & 1) << (offset+j) for j in range(32)), 0)
            for i in range(32)]


def carry_equations(a, b, left, right, stage):
    rows = []
    if (a ^ b) & 1:
        return [{"coefficient": 0, "rhs": 1, "stage": stage, "bit": 0, "kind": "initial_parity"}]
    sign = None

    def emit(forms, target, bit, kind):
        coefficient, rhs = 0, target
        for row, constant in forms:
            coefficient ^= row
            rhs ^= constant
        if coefficient or rhs:
            rows.append({"coefficient": coefficient, "rhs": rhs,
                         "stage": stage, "bit": bit, "kind": kind})

    for i in range(31):
        ai, bi = (a >> i) & 1, (b >> i) & 1
        next_parity = ((a ^ b) >> (i+1)) & 1
        if ai + bi == 0:
            assert sign is None
            if next_parity:
                emit([], 1, i, "inactive_gap")
                return rows
            sign = None
        elif ai + bi == 2:
            assert sign is None
            emit([left[i], right[i]], 1 ^ next_parity, i, "both_active")
            sign = left[i] if next_parity else None
        else:
            assert sign is not None
            current = left[i] if ai else right[i]
            emit([sign, current], 1 ^ next_parity, i, "single_active")
            sign = current if next_parity else None
    # The parity at bit31 already makes the final signed sum even.
    # Its carry out is arbitrary, since equality is modulo 2^32.
    return rows


def all_rows(a):
    return (carry_equations(K, g(K), bits(32), sigma_forms(g, 32), "h_q")
            + carry_equations(a, K, bits(0), bits(32, 1), "equal_input_derivatives")
            + carry_equations(f(a), f(K), sigma_forms(f, 0), sigma_forms(f, 32), "opposite_sigma0_derivatives"))


def eliminate(rows):
    pivots = {}
    for i, row in enumerate(rows):
        coefficient, rhs, proof = row["coefficient"], row["rhs"], 1 << i
        while coefficient:
            leading = coefficient.bit_length()-1
            if leading not in pivots:
                pivots[leading] = (coefficient, rhs, proof)
                break
            older, value, older_proof = pivots[leading]
            coefficient ^= older
            rhs ^= value
            proof ^= older_proof
        if not coefficient and rhs:
            selected = [j for j in range(len(rows)) if proof >> j & 1]
            coefficient_check = rhs_check = 0
            for j in selected:
                coefficient_check ^= rows[j]["coefficient"]
                rhs_check ^= rows[j]["rhs"]
            assert coefficient_check == 0 and rhs_check == 1
            return {"status": "inconsistent", "selected_rows": selected}
    assignment = 0
    for leading, (coefficient, rhs, _) in sorted(pivots.items()):
        value = rhs ^ ((coefficient & assignment).bit_count() & 1)
        assignment |= value << leading
    assert all(((r["coefficient"] & assignment).bit_count() & 1) == r["rhs"] for r in rows)
    return {"status": "consistent", "rank": len(pivots), "assignment": assignment}


def main():
    start = time.monotonic()
    tables = verify_local_tables()
    mask_file = HERE / "MASK_PROBE.json"
    masks = [int(v, 16) for v in json.loads(mask_file.read_text())["survivors_if_at_most_256"]]
    assert len(masks) == 132
    cases = []
    real_pairs = []
    for a in masks:
        rows = all_rows(a)
        outcome = eliminate(rows)
        if outcome["status"] == "consistent":
            assignment = outcome["assignment"]
            p, q = assignment & MASK, assignment >> 32
            pp, qp = p ^ a, q ^ K
            checks = [(q+g(q)-qp-g(qp)) & MASK,
                      (pp+q-p-qp) & MASK,
                      (f(pp)+f(qp)-f(p)-f(q)) & MASK]
            real_pairs.append({"A": f"{a:08x}", "p": p, "p_prime": pp,
                               "q": q, "q_prime": qp, "original_residuals": checks})
            assert checks == [0, 0, 0]
        cases.append({"A": f"{a:08x}", "row_count": len(rows),
                      "rows": [{**row, "coefficient": f"{row['coefficient']:016x}"} for row in rows],
                      **outcome})
    h_rows = carry_equations(K, g(K), bits(), sigma_forms(g), "h_q")
    h_outcome = eliminate(h_rows)
    result = {"schema": "CRYPTO3-coupled-affine-carry-probe-v1", "word_bits": 32,
              "K": f"{K:08x}", "mask_source_sha256": hashlib.sha256(mask_file.read_bytes()).hexdigest(),
              "carry_truth_tables": tables, "masks_checked": len(masks),
              "inconsistent_masks": sum(c["status"] == "inconsistent" for c in cases),
              "real_pairs_if_any": real_pairs,
              "h_affine_system_diagnostic": {"rows": len(h_rows), **h_outcome},
              "cases": cases, "seconds": time.monotonic()-start,
              "scope": "Exact fixed-mask coupled equations; no full schedule claim, no CNF/RUP imported."}
    (HERE / "AFFINE_PROBE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key not in ("cases", "carry_truth_tables")}, indent=2))


if __name__ == "__main__":
    main()
