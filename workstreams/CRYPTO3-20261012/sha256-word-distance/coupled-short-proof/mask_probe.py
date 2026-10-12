#!/usr/bin/env python3
"""Bounded necessary-mask screen for one specified proof mechanism."""

import hashlib
import json
import time
from pathlib import Path

MASK = (1 << 32) - 1
K = 0xfbca7000
HERE = Path(__file__).resolve().parent


def rotr(x, n):
    return ((x >> n) | (x << (32-n))) & MASK


def f(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def g(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def bad(a, b):
    return ((a ^ b) & ~((a | b) << 1)) & MASK


def affine_rank(words):
    if not words:
        return None
    pivot = {}
    for word in words:
        v = word ^ words[0]
        while v:
            j = v.bit_length()-1
            if j not in pivot:
                pivot[j] = v
                break
            v ^= pivot[j]
    return len(pivot)


def same_mask_linear_check():
    fk = f(K)
    equations = []
    for i in range(31):
        if K >> i & 1:
            equations.append((1 << i, 0, {"kind": "z", "bit": i, "rhs": 0}))
        if fk >> i & 1:
            row = sum(((f(1 << j) >> i) & 1) << j for j in range(32))
            equations.append((row, 1, {"kind": "f(z)", "bit": i, "rhs": 1}))
    pivots = {}
    for i, (coefficient, rhs, _) in enumerate(equations):
        proof = 1 << i
        while coefficient:
            leading = coefficient.bit_length()-1
            if leading not in pivots:
                pivots[leading] = (coefficient, rhs, proof)
                break
            old, value, old_proof = pivots[leading]
            coefficient ^= old
            rhs ^= value
            proof ^= old_proof
        if not coefficient and rhs:
            indices = [i for i in range(len(equations)) if proof >> i & 1]
            total_row = total_rhs = 0
            for i in indices:
                total_row ^= equations[i][0]
                total_rhs ^= equations[i][1]
            assert total_row == 0 and total_rhs == 1
            return {"status": "inconsistent", "contradiction_rows": [equations[i][2] for i in indices]}
    return {"status": "consistent", "rank": len(pivots), "equations": len(equations)}


def main():
    start = time.monotonic()
    assert f(K) == 0x828ee412 and g(K) == 0x763e9000
    fixed = (1 << 12) | (1 << 19)
    free = [i for i in range(13, 32) if i not in (18, 19)]
    assert len(free) == 17
    columns = [f(1 << i) for i in free]
    a, fa, fk = fixed, f(fixed), f(K)
    first_pass = 0
    survivors = []
    for selection in range(1 << len(free)):
        if selection:
            changed = (selection & -selection).bit_length()-1
            a ^= 1 << free[changed]
            fa ^= columns[changed]
        if bad(a, K):
            continue
        first_pass += 1
        if bad(fa, fk):
            continue
        assert fa == f(a)
        survivors.append(a)
    survivors.sort()
    both_and, both_or = MASK, 0
    for a in survivors:
        both_and &= a
        both_or |= a
    raw = "".join(f"{a:08x}\n" for a in survivors).encode()
    result = {
        "schema": "CRYPTO3-coupled-short-mask-probe-v1",
        "mechanism": "shared additive input difference plus opposite sigma0 derivatives, necessary signed-mask obstructions only",
        "masks_screened": 1 << len(free), "after_input_obstruction": first_pass,
        "after_both_obstructions": len(survivors), "affine_hull_dimension": affine_rank(survivors),
        "common_one_bits_hex": f"{both_and:08x}", "common_zero_bits_hex": f"{MASK ^ both_or:08x}",
        "survivor_mask_sha256": hashlib.sha256(raw).hexdigest(),
        "survivors_if_at_most_256": [f"{a:08x}" for a in survivors] if len(survivors) <= 256 else None,
        "K_survives": K in survivors,
        "A_equals_K_linear_check": same_mask_linear_check(),
        "seconds": time.monotonic()-start,
        "limitations": "No actual p,q assignment searched or claimed; the fixed-mask h condition has not been imposed in this probe.",
    }
    (HERE / "MASK_PROBE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "survivors_if_at_most_256"}, indent=2))


if __name__ == "__main__":
    main()
