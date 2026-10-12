#!/usr/bin/env python3
"""Independent exact replay of the fixed-D support-12 twin obstruction.

This checker deliberately does not import the author's check.py.  It derives
the SHA-256 small-sigma output rows by evaluating basis vectors and explores
the bit carries by assigning the at-most-two toggled output bits directly.
Only Python's standard library is required.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

WORD_BITS = 32
VARIABLES = 64
MOD32 = 1 << WORD_BITS
MASK32 = MOD32 - 1
D = 1 << 16
HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-image-v8"
EXPECTED_AUTHOR = {
    "CERTIFICATE.json": "4901cd8605e7f81b601d3229e0441a32a4ad41cc2ee316fbf452e405efec77e6",
    "CHECK-RUN.json": "369009f4baae28eb6d46f00314594f54ec15d08c18035819b0241929ff88bfba",
    "MECHANISM.md": "dce231c92568685cbdfb48ce9283747f457b22d309b91c10b4bd5d0914a43a90",
    "PROOF.md": "c41efebfae7c29286c7c1907f4021b51e86069be3d0f6af29c206c7829f09417",
    "README.md": "7693a93994308547e56b9eec282cc718c94d36079dbf64557edd870ccded28ee",
    "STATUS.md": "244f11ab2869e6f513a52fc6c84aec6737d7d3b56fd08c65d5f4cbf9c752d057",
    "check.py": "7b47fa737b0beffd098fdc5c332c5cb9caa54bd5611c86b275f07a2d229d9724",
    "explore.py": "2d0be20f754a20010759fecdca2ff347ec6df419a3d5f37ffe615e3f47ffff17",
}
EXPECTED_MANIFEST = "f8166c958baead817204a262dbe0487ca5b856f05b5baa94433f5d69b0ef7c90"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rotr(x, amount):
    return ((x >> amount) | (x << (32 - amount))) & MASK32


def small_sigma(x, kind):
    if kind == 0:
        return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
    if kind == 1:
        return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)
    raise ValueError("sigma kind")


def output_rows(kind):
    """Derive Boolean rows from the definition, not the author's row code."""
    rows = [0] * 32
    for input_bit in range(32):
        image = small_sigma(1 << input_bit, kind)
        for output_bit in range(32):
            if (image >> output_bit) & 1:
                rows[output_bit] |= 1 << input_bit
    return tuple(rows)


ROWS = (output_rows(0), output_rows(1))


def canonical_input_classes():
    """Analytic carry classes for x -> x+2^16, including wraparound."""
    result = []
    for length in range(1, 17):
        alpha = ((1 << length) - 1) << 16
        equations = []
        if length < 16:
            for j in range(length - 1):
                equations.append((1 << (16 + j), 1))
            equations.append((1 << (16 + length - 1), 0))
        else:
            # q=0x7fff and q=0xffff share the all-one XOR mask.
            for j in range(15):
                equations.append((1 << (16 + j), 1))
        result.append((alpha, tuple(equations)))
    return tuple(result)


CLASSES = canonical_input_classes()


def equation_holds(equation, assignment):
    coeff, rhs = equation
    return ((coeff & assignment).bit_count() & 1) == rhs


def check_class_partition():
    counts = Counter()
    for q in range(1 << 16):
        alpha = (q ^ ((q + 1) & 0xFFFF)) << 16
        matches = []
        assignment = q << 16
        for index, (candidate, equations) in enumerate(CLASSES):
            if candidate == alpha and all(equation_holds(eq, assignment) for eq in equations):
                matches.append(index)
        require(len(matches) == 1, f"upper-word class multiplicity at {q:#x}")
        counts[matches[0]] += 1
    expected = [1 << (15 - i) for i in range(15)] + [2]
    require([counts[i] for i in range(16)] == expected, "analytic class counts")
    require(sum(counts.values()) == 1 << 16, "class coverage")
    # Low input bits are deliberately absent from every class equation.
    require(all(coeff & 0xFFFF == 0 for _, eqs in CLASSES for coeff, _ in eqs),
            "a class incorrectly restricts the free low half")
    return expected


def add_equations(basis, equations):
    """Incremental GF(2) elimination with highest-variable pivots."""
    rows = list(basis)
    for coeff, rhs in equations:
        word = coeff | (rhs << VARIABLES)
        while word & ((1 << VARIABLES) - 1):
            pivot = (word & ((1 << VARIABLES) - 1)).bit_length() - 1
            if rows[pivot]:
                word ^= rows[pivot]
            else:
                rows[pivot] = word
                break
        if word == 1 << VARIABLES:
            return None
    return tuple(rows)


EMPTY_BASIS = (0,) * VARIABLES


def instantiate_class(equations, offset):
    return tuple((coeff << offset, rhs) for coeff, rhs in equations)


def advance(states, kind, alpha_x, alpha_y, constant, bits, stats):
    """Exact digit DP with an exhaustively derived local truth relation."""
    next_states = list(states)
    for bit in range(bits):
        produced = []
        toggle_x = (small_sigma(alpha_x, kind) >> bit) & 1
        toggle_y = (small_sigma(alpha_y, kind) >> bit) & 1
        forms = []
        if toggle_x:
            forms.append(("x", ROWS[kind][bit]))
        if toggle_y:
            forms.append(("y", ROWS[kind][bit] << 32))
        target_bit = (constant >> bit) & 1
        for carry_in, basis in next_states:
            allowed_by_carry = {}
            for values in range(1 << len(forms)):
                stats["assignments_tried"] += 1
                vx = vy = 0
                for j, (side, _) in enumerate(forms):
                    value = (values >> j) & 1
                    if side == "x":
                        vx = value
                    else:
                        vy = value
                dx = (1 - 2 * vx) if toggle_x else 0
                dy = (1 - 2 * vy) if toggle_y else 0
                numerator = carry_in + dy - dx - target_bit
                if numerator & 1:
                    continue
                stats["parity_edges"] += 1
                allowed_by_carry.setdefault(numerator // 2, []).append(values)
            for carry_out, allowed in sorted(allowed_by_carry.items()):
                # Enumerate every local truth-table value first, then derive
                # all constant linear relations.  Verify the compression by
                # reconstructing the truth set before using it.
                little_equations = []
                for mask in range(1, 1 << len(forms)):
                    rhs_values = {(mask & value).bit_count() & 1 for value in allowed}
                    if len(rhs_values) == 1:
                        little_equations.append((mask, next(iter(rhs_values))))
                reconstructed = [
                    value for value in range(1 << len(forms))
                    if all(((mask & value).bit_count() & 1) == rhs
                           for mask, rhs in little_equations)
                ]
                require(reconstructed == allowed, "non-affine local truth set")
                equations = []
                for little_mask, rhs in little_equations:
                    coeff = 0
                    for j, (_, form) in enumerate(forms):
                        if (little_mask >> j) & 1:
                            coeff ^= form
                    equations.append((coeff, rhs))
                new_basis = add_equations(basis, equations)
                if new_basis is None:
                    stats["linear_conflicts"] += 1
                    continue
                produced.append((carry_out, new_basis))
        next_states = produced
    return next_states


def recover(basis):
    assignment = 0
    # A row pivoted on p only has coefficients below p, so solve upward.
    for pivot, row in enumerate(basis):
        if not row:
            continue
        coeff = row & ((1 << VARIABLES) - 1)
        rhs = row >> VARIABLES
        value = rhs ^ ((coeff & assignment).bit_count() & 1)
        if value:
            assignment |= 1 << pivot
    for row in basis:
        if row:
            coeff = row & ((1 << VARIABLES) - 1)
            rhs = row >> VARIABLES
            require(((coeff & assignment).bit_count() & 1) == rhs, "recovery")
    return assignment


def enumerate_twins(f_bits, g_bits, gap, preserve_leaves=False):
    stats = Counter()
    f_count = g_count = 0
    leaves = []
    for alpha_x, equations_x in CLASSES:
        for alpha_y, equations_y in CLASSES:
            basis = add_equations(
                EMPTY_BASIS,
                instantiate_class(equations_x, 0) + instantiate_class(equations_y, 32),
            )
            require(basis is not None, "disjoint class variables conflict")
            after_f = advance([(0, basis)], 0, alpha_x, alpha_y, 0, f_bits, stats)
            f_count += len(after_f)
            # Each modular equation starts at its own least-significant bit;
            # the discarded final carry of the f congruence is not an input
            # carry to the unrelated g congruence.
            after_g = advance([(0, b) for _, b in after_f],
                              1, alpha_x, alpha_y, gap, g_bits, stats)
            g_count += len(after_g)
            if preserve_leaves:
                leaves.extend((alpha_x, alpha_y, carry, b) for carry, b in after_g)
    return {
        "f_leaves": f_count,
        "g_leaves": g_count,
        "stats": dict(stats),
    }, leaves


def classify_frontier(leaves):
    groups = Counter()
    for alpha_x, alpha_y, carry, _ in leaves:
        groups[(alpha_x, alpha_y,
                (small_sigma(alpha_x, 1) >> 30) & 1,
                (small_sigma(alpha_y, 1) >> 30) & 1,
                carry)] += 1
    return [
        {"xor_x": ax, "xor_y": ay, "gx30": gx, "gy30": gy,
         "incoming_carry": carry, "leaves": count}
        for (ax, ay, gx, gy, carry), count in sorted(groups.items())
    ]


def direct_word_check(leaf):
    alpha_x, alpha_y, _, basis = leaf
    packed = recover(basis)
    x = packed & MASK32
    y = (packed >> 32) & MASK32
    xp = (x + D) & MASK32
    yp = (y + D) & MASK32
    require((x ^ xp) == alpha_x and (y ^ yp) == alpha_y, "input XOR recovery")
    f_x = (small_sigma(xp, 0) - small_sigma(x, 0)) & MASK32
    f_y = (small_sigma(yp, 0) - small_sigma(y, 0)) & MASK32
    g_x = (small_sigma(xp, 1) - small_sigma(x, 1)) & MASK32
    g_y = (small_sigma(yp, 1) - small_sigma(y, 1)) & MASK32
    gap = (g_y - g_x) & MASK32
    require(f_x == f_y, "recovered sigma0 mismatch")
    require(gap % (1 << 30) == 2 * D, "recovered low-30 gap")
    require(gap % (1 << 31) != 2 * D, "boundary witness unexpectedly extends")
    return {
        "x": x, "xp": xp, "y": y, "yp": yp,
        "xor_x": alpha_x, "xor_y": alpha_y,
        "F": f_x, "G_gap": gap,
    }


def check_negative_symmetry(witness):
    x, xp = witness["x"], witness["xp"]
    y, yp = witness["y"], witness["yp"]
    require((x - xp) & MASK32 == (-D) & MASK32, "reverse x difference")
    require((y - yp) & MASK32 == (-D) & MASK32, "reverse y difference")
    reverse_fx = (small_sigma(x, 0) - small_sigma(xp, 0)) & MASK32
    reverse_fy = (small_sigma(y, 0) - small_sigma(yp, 0)) & MASK32
    reverse_gx = (small_sigma(x, 1) - small_sigma(xp, 1)) & MASK32
    reverse_gy = (small_sigma(y, 1) - small_sigma(yp, 1)) & MASK32
    require(reverse_fx == reverse_fy == (-witness["F"]) & MASK32,
            "reverse sigma0 derivative")
    require((reverse_gy - reverse_gx) & MASK32 == (-witness["G_gap"]) & MASK32,
            "reverse sigma1 gap")
    require((-(2 * D)) % (1 << 31) == (2 * ((-D) & MASK32)) % (1 << 31),
            "negative-D target symmetry")
    return {
        "map": "(x,x+D) -> (x+D,x)",
        "negative_delta": (-D) & MASK32,
        "status": "bijection_checked",
    }


def validate_frontier(frontier):
    masks = [((1 << length) - 1) << 16 for length in range(11, 16)]
    expected = [
        {"xor_x": mask, "xor_y": mask, "gx30": 1, "gy30": 1,
         "incoming_carry": carry, "leaves": 2}
        for mask in masks for carry in (-1, 1)
    ]
    require(frontier == expected, "bit-30 frontier classification")


def run(negative=False):
    source_hashes = {
        name: hashlib.sha256((AUTHOR / name).read_bytes()).hexdigest()
        for name in EXPECTED_AUTHOR
    }
    require(source_hashes == EXPECTED_AUTHOR, "author source changed")
    manifest_bytes = (AUTHOR / "manifest.json").read_bytes()
    require(hashlib.sha256(manifest_bytes).hexdigest() == EXPECTED_MANIFEST,
            "author manifest changed")
    manifest = json.loads(manifest_bytes)
    require(manifest["files"] == EXPECTED_AUTHOR, "author manifest file map")
    class_counts = check_class_partition()
    theorem, _ = enumerate_twins(32, 31, 2 * D)
    require((theorem["f_leaves"], theorem["g_leaves"]) == (414, 0),
            "fixed-D theorem counts")
    low30, leaves = enumerate_twins(32, 30, 2 * D, True)
    f31, _ = enumerate_twins(31, 31, 2 * D)
    gap0, _ = enumerate_twins(32, 31, 0)
    require((low30["f_leaves"], low30["g_leaves"]) == (414, 20), "low30 control")
    require((f31["f_leaves"], f31["g_leaves"]) == (408, 20), "F31 control")
    require((gap0["f_leaves"], gap0["g_leaves"]) == (414, 58), "zero-gap control")
    frontier = classify_frontier(leaves)
    validate_frontier(frontier)
    # At bit 30 both derivatives are toggled, so dy-dx is even.  The
    # incoming carry is odd and the target bit is zero: no parity edge exists.
    require(all(row["gx30"] == row["gy30"] == 1 for row in frontier), "frontier toggles")
    require(all(abs(row["incoming_carry"]) == 1 for row in frontier), "frontier carries")
    require(((2 * D) >> 30) & 1 == 0, "target bit 30")
    witness = direct_word_check(leaves[0])
    symmetry = check_negative_symmetry(witness)
    controls = {
        "truncate_G_mod_2^30": low30,
        "truncate_F_mod_2^31": f31,
        "replace_gap_by_zero": gap0,
        "direct_boundary_witness": witness,
    }
    if negative:
        rejected = 0
        for mutation in range(4):
            bad = [dict(item) for item in frontier]
            if mutation == 0:
                bad[0]["incoming_carry"] = 0
            elif mutation == 1:
                bad[0]["gx30"] = 0
            elif mutation == 2:
                bad[0]["leaves"] += 1
            else:
                bad.pop()
            try:
                validate_frontier(bad)
            except AssertionError:
                rejected += 1
        require(rejected == 4, "frontier negative controls")
        controls["damaged_frontiers_rejected"] = rejected
    return {
        "status": "PASS",
        "acceptance": "fixed D=+/-0x00010000 selected twin core only",
        "claim": "no two +D pairs have equal sigma0 derivative and sigma1 gap 2D modulo 2^31",
        "not_claimed": [
            "all exact-v2(D)=16 residues",
            "the complete support-12 system",
            "a 16-word or 64-word SHA-256 message pair",
            "distance 13 attainability or distance at least 14",
        ],
        "class_partition": {"upper_values": 1 << 16, "class_counts": class_counts,
                            "low_bits_free_per_class_member": 1 << 16},
        "theorem": theorem,
        "bit30_frontier": frontier,
        "controls": controls,
        "negative_D_symmetry": symmetry,
        "author_source_sha256": source_hashes,
        "author_manifest_sha256": EXPECTED_MANIFEST,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "method": "independent direct toggled-bit digit DP with highest-pivot GF(2) elimination",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.negative), sort_keys=True))
