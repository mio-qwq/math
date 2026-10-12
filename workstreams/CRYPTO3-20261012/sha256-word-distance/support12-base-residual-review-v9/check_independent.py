#!/usr/bin/env python3
"""Blind composition check for support-12 base row 57 and the PG factor."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

MASK = (1 << 32) - 1
SUPPORT = (10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57)
PARAMETERS = (9, 12, 14, 19, 22)
ORIGINAL_ORDER = (
    (26, 24), (28, 21), (29, 27), (34, 32), (36, 36), (43, 41),
    (27, 25), (41, 39), (25, 23), (30, 30), (39, 37), (44, 44),
    (37, 35), (42, 40), (35, 33), (40, 38), (45, 45), (38, 31),
    (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51),
    (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (58, 58),
    (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (31, 16),
    (32, 17), (24, 8), (23, 7), (22, 6), (21, 5), (20, 4),
    (19, 3), (18, 2), (17, 1), (16, 0),
)

# Row 57 is inserted as a solve immediately after row 56, before row 59 can
# consume coordinate 57.  Row 58 is independent of coordinate 57.
REWRITTEN_ORDER = ORIGINAL_ORDER[:29] + ((57, 57),) + ORIGINAL_ORDER[29:]


def rotr(word: int, count: int) -> int:
    return ((word >> count) | (word << (32 - count))) & MASK


def sigma0(word: int) -> int:
    return rotr(word, 7) ^ rotr(word, 18) ^ (word >> 3)


def sigma1(word: int) -> int:
    return rotr(word, 17) ^ rotr(word, 19) ^ (word >> 10)


def inverse_map(fn):
    basis = {}
    for j in range(32):
        value, preimage = fn(1 << j), 1 << j
        while value:
            pivot = (value & -value).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value, preimage
                break
            value ^= basis[pivot][0]
            preimage ^= basis[pivot][1]
        else:
            raise AssertionError("singular small sigma")

    def inverse(value: int) -> int:
        result = 0
        while value:
            pivot = (value & -value).bit_length() - 1
            value ^= basis[pivot][0]
            result ^= basis[pivot][1]
        return result

    return inverse


INV0 = inverse_map(sigma0)
INV1 = inverse_map(sigma1)


def row_positions(t: int):
    return (t, t - 2, t - 7, t - 15, t - 16)


def residual(words, t: int) -> int:
    return (
        words[t] - sigma1(words[t - 2]) - words[t - 7]
        - sigma0(words[t - 15]) - words[t - 16]
    ) & MASK


def run_order(initial: dict[int, int], order):
    words = [None] * 64
    for i, value in initial.items():
        assert words[i] is None and 0 <= value <= MASK
        words[i] = value
    used = []
    for t, target in order:
        unknown = [i for i in row_positions(t) if words[i] is None]
        assert unknown == [target], (t, target, unknown)
        terms = (
            (t - 2, sigma1, INV1),
            (t - 7, lambda x: x, lambda x: x),
            (t - 15, sigma0, INV0),
            (t - 16, lambda x: x, lambda x: x),
        )
        if target == t:
            words[target] = sum(fn(words[i]) for i, fn, _ in terms) & MASK
        else:
            other = sum(fn(words[i]) for i, fn, _ in terms if i != target)
            inv = next(inv for i, _, inv in terms if i == target)
            words[target] = inv((words[t] - other) & MASK)
        used.append(t)
    assert all(word is not None for word in words)
    assert len(used) == len(set(used))
    return words


def dependency_trace(initial_indices, order):
    deps = [None] * 64
    for i in initial_indices:
        deps[i] = {f"u{i}" if i in SUPPORT else f"p{i}"}
    for t, target in order:
        assert [i for i in row_positions(t) if deps[i] is None] == [target]
        deps[target] = set().union(*(deps[i] for i in row_positions(t) if i != target))
    assert all(dep is not None for dep in deps)
    return deps


def expand(message):
    words = list(message) + [0] * 48
    for t in range(16, 64):
        words[t] = (
            sigma1(words[t - 2]) + words[t - 7]
            + sigma0(words[t - 15]) + words[t - 16]
        ) & MASK
    return words


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    original_initial = SUPPORT + PARAMETERS
    rewritten_initial = tuple(i for i in SUPPORT if i != 57) + PARAMETERS

    old_deps = dependency_trace(original_initial, ORIGINAL_ORDER)
    u57_coordinates = [i for i, dep in enumerate(old_deps) if "u57" in dep]
    r33_deps = set().union(*(old_deps[i] for i in row_positions(33)))
    r57_deps = set().union(*(old_deps[i] for i in row_positions(57)))
    rhs57_deps = set().union(old_deps[55], old_deps[50], old_deps[42], old_deps[41])
    assert u57_coordinates == [57, 59, 61, 63]
    assert "u57" not in r33_deps and "u57" in r57_deps
    assert "u57" not in rhs57_deps

    # Structural exactness of the rewritten chart.
    new_deps = dependency_trace(rewritten_initial, REWRITTEN_ORDER)
    assert len(REWRITTEN_ORDER) == 47
    assert len({t for t, _ in REWRITTEN_ORDER}) == 47
    assert len({target for _, target in REWRITTEN_ORDER}) == 47
    assert set(range(16, 64)) - {t for t, _ in REWRITTEN_ORDER} == {33}
    assert set(rewritten_initial) | {target for _, target in REWRITTEN_ORDER} == set(range(64))
    assert "u57" not in set().union(*new_deps)

    rng = random.Random(0xBA5E57)
    roundtrips = 0
    identity_checks = 0
    for case in range(12):
        message = [rng.getrandbits(32) for _ in range(16)]
        actual = expand(message)
        old_initial = {i: actual[i] for i in original_initial}
        new_initial = {i: actual[i] for i in rewritten_initial}
        old = run_order(old_initial, ORIGINAL_ORDER)
        new = run_order(new_initial, REWRITTEN_ORDER)
        assert old == actual == new
        assert residual(old, 33) == residual(old, 57) == 0
        assert residual(new, 33) == 0
        roundtrips += 1

        # Vary only prescribed u57.  The old row-57 residual changes by the
        # same modular delta; exactly coordinates 57,59,61,63 may change.
        delta = (case + 1) * 0x1020305 & MASK
        damaged_initial = dict(old_initial)
        damaged_initial[57] = (damaged_initial[57] + delta) & MASK
        damaged = run_order(damaged_initial, ORIGINAL_ORDER)
        changed = [i for i in range(64) if damaged[i] != old[i]]
        assert changed == [57, 59, 61, 63]
        assert residual(damaged, 33) == residual(old, 33)
        assert residual(damaged, 57) == delta
        forced = (
            sigma1(damaged[55]) + damaged[50]
            + sigma0(damaged[42]) + damaged[41]
        ) & MASK
        assert forced == actual[57]
        assert residual(damaged, 57) == (damaged[57] - forced) & MASK
        identity_checks += 1

    # PG(z,b) can be true through a witness x different from the forced base
    # B, while the required derivative at B is false.  This definition-level
    # control prevents retaining existential PG in the exact composition.
    z, witness_x, forced_base = 1, 0, 4
    b = (sigma1((witness_x + z) & MASK) - sigma1(witness_x)) & MASK
    pointwise_at_forced = (
        sigma1((forced_base + z) & MASK) - sigma1(forced_base)
    ) & MASK
    assert b == 0x0000A000
    assert pointwise_at_forced == 0xFFFFA000 and pointwise_at_forced != b

    result = {
        "schema": "CRYPTO3-support12-base-residual-review-v9-pre-author",
        "status": "PASS",
        "old_chart": {
            "initial_count": len(original_initial),
            "used_rows": len(ORIGINAL_ORDER),
            "residual_rows": [33, 57],
            "coordinates_depending_on_u57": u57_coordinates,
            "R33_depends_on_u57": False,
            "R57_form": "u57 - (g(C55)+C50+f(C42)+C41)",
            "R57_rhs_depends_on_u57": False,
        },
        "rewritten_chart": {
            "initial_coordinates": list(rewritten_initial),
            "inserted_solve": [57, 57],
            "used_rows": len(REWRITTEN_ORDER),
            "residual_rows": [33],
            "forced_u57": "B=g(C55)+C50+f(C42)+C41",
        },
        "composition": {
            "factor_normal_form_position_57": "PG(z,b)",
            "exact_composed_condition": "g(B+z)-g(B)=b mod 2^32",
            "private_F57": "f(B+z)-f(B); unconstrained by rows 16..63",
            "pg_is_only_a_necessary_projection_after_base_composition": True,
        },
        "roundtrips": roundtrips,
        "u57_identity_checks": identity_checks,
        "pg_separation_control": {
            "z": z,
            "PG_witness_x": witness_x,
            "b": b,
            "forced_base_B": forced_base,
            "derivative_at_B": pointwise_at_forced,
        },
        "source_sha256": sha(Path(__file__)),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
