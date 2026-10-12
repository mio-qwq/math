#!/usr/bin/env python3
"""Pre-author exact audit of the selected twin condition for odd q=33..63.

No author-v10 file is imported.  The finite model is rebuilt from the SHA-256
small-sigma definitions and the frozen v9 theorem statement.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASK32 = (1 << 32) - 1
NVARS = 64
VARMASK = (1 << NVARS) - 1
QS = tuple(range(33, 64, 2))


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK32


def sigma(x, which):
    if which == 0:
        return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def make_rows(which):
    cols = tuple(sigma(1 << j, which) for j in range(32))
    return tuple(sum(((cols[j] >> i) & 1) << j for j in range(32))
                 for i in range(32))


ROWS = (make_rows(0), make_rows(1))


def sigma_linear(x, which):
    return sum(((row & x).bit_count() & 1) << i
               for i, row in enumerate(ROWS[which]))


for _which in (0, 1):
    for _x in (0, 1, 2, 3, 0x12345678, 0x80000000, MASK32):
        need(sigma(_x, _which) == sigma_linear(_x, _which),
             "small-sigma row reconstruction failed")


def input_classes(q):
    """Exact upper-word partition for x -> x+q*2^16."""
    need(q in QS, "q outside frozen interval")
    groups = {}
    for u in range(1 << 16):
        alpha = u ^ ((u + q) & 0xffff)
        groups.setdefault(alpha, []).append(u)
    result = []
    seen = set()
    for alpha, members in sorted(groups.items()):
        equations = []
        for j in range(16):
            values = {(u >> j) & 1 for u in members}
            if len(values) == 1:
                equations.append((1 << (j + 16), next(iter(values))))
        regenerated = [u for u in range(1 << 16)
                       if all(((u >> (c.bit_length() - 17)) & 1) == b
                              for c, b in equations)]
        need(regenerated == members, f"q={q}: non-cube mask class {alpha:04x}")
        need(not seen.intersection(members), f"q={q}: overlapping mask classes")
        seen.update(members)
        result.append((alpha << 16, tuple(equations), len(members)))
    need(seen == set(range(1 << 16)), f"q={q}: mask classes do not partition")
    return tuple(result)


def affine_equations(allowed, arity):
    equations = []
    for form in range(1, 1 << arity):
        values = {(form & x).bit_count() & 1 for x in allowed}
        if len(values) == 1:
            equations.append((form, next(iter(values))))
    rebuilt = tuple(x for x in range(1 << arity)
                    if all(((form & x).bit_count() & 1) == rhs
                           for form, rhs in equations))
    need(rebuilt == tuple(allowed), "carry table is not recovered exactly")
    return tuple(equations)


def insert(basis, equations, stats):
    """Highest-pivot GF(2) elimination; receipt is original packed rows."""
    out = dict(basis)
    for coeff, rhs in equations:
        word = coeff | (rhs << NVARS)
        receipt = frozenset((word,))
        while word & VARMASK:
            pivot = (word & VARMASK).bit_length() - 1
            if pivot not in out:
                out[pivot] = (word, receipt)
                break
            old, old_receipt = out[pivot]
            word ^= old
            receipt = receipt.symmetric_difference(old_receipt)
        if word == 1 << NVARS:
            total = 0
            for row in receipt:
                total ^= row
            need(total == 1 << NVARS, "invalid contradiction receipt")
            stats["checked_contradictions"] += 1
            return None
        need(word == 0 or (word & VARMASK), "malformed reduced equation")
    return out


def transitions(which, ax, ay, target, bit, carry):
    tx = (sigma_linear(ax, which) >> bit) & 1
    ty = (sigma_linear(ay, which) >> bit) & 1
    forms = []
    if tx:
        forms.append(ROWS[which][bit])
    if ty:
        forms.append(ROWS[which][bit] << 32)
    groups = {}
    for assignment in range(1 << len(forms)):
        cursor = 0
        bx = 0
        by = 0
        if tx:
            bx = (assignment >> cursor) & 1
            cursor += 1
        if ty:
            by = (assignment >> cursor) & 1
        digit = carry + ((by ^ ty) - by) - ((bx ^ tx) - bx)
        digit -= (target >> bit) & 1
        if digit % 2 == 0:
            groups.setdefault(digit // 2, []).append(assignment)
    result = []
    for nxt, allowed in sorted(groups.items()):
        expanded = []
        for small, rhs in affine_equations(tuple(allowed), len(forms)):
            coeff = 0
            for j, form in enumerate(forms):
                if (small >> j) & 1:
                    coeff ^= form
            expanded.append((coeff, rhs))
        result.append((nxt, tuple(expanded)))
    return tuple(result)


def impose(states, which, ax, ay, target, stats):
    active = [(0, basis) for basis in states]
    for bit in range(32):
        following = []
        for carry, basis in active:
            for nxt, equations in transitions(which, ax, ay, target, bit, carry):
                stats["carry_edges"] += 1
                new_basis = insert(basis, equations, stats)
                if new_basis is not None:
                    following.append((nxt, new_basis))
        active = following
    return tuple(basis for _, basis in active)


def solve_free_zero(basis):
    word = 0
    for pivot in sorted(basis):
        equation, _ = basis[pivot]
        coeff = equation & VARMASK
        rhs = equation >> NVARS
        if ((coeff & word).bit_count() & 1) != rhs:
            word |= 1 << pivot
        need(((coeff & word).bit_count() & 1) == rhs,
             "recovered assignment violates basis")
    return word


def record(q, packed, ax, ay):
    d = q << 16
    x = packed & MASK32
    y = (packed >> 32) & MASK32
    xp = (x + d) & MASK32
    yp = (y + d) & MASK32
    fx = (sigma(xp, 0) - sigma(x, 0)) & MASK32
    fy = (sigma(yp, 0) - sigma(y, 0)) & MASK32
    gx = (sigma(xp, 1) - sigma(x, 1)) & MASK32
    gy = (sigma(yp, 1) - sigma(y, 1)) & MASK32
    need(fx == fy, "fixture fails sigma0 equality")
    need((gy - gx) & MASK32 == (2 * d) & MASK32,
         "fixture fails full sigma1 gap")
    need(x ^ xp == ax and y ^ yp == ay, "fixture mask mismatch")
    return {"x": x, "x_plus_D": xp, "y": y, "y_plus_D": yp,
            "xor_x": ax, "xor_y": ay, "common_F": fx,
            "G_x": gx, "G_y": gy, "G_gap": (gy - gx) & MASK32}


def validate(q, item):
    d = q << 16
    x, xp, y, yp = (item[k] for k in ("x", "x_plus_D", "y", "y_plus_D"))
    need((xp - x) & MASK32 == d and (yp - y) & MASK32 == d,
         "fixture has wrong D")
    need(x ^ xp == item["xor_x"] and y ^ yp == item["xor_y"],
         "fixture has wrong xor mask")
    fx = (sigma(xp, 0) - sigma(x, 0)) & MASK32
    fy = (sigma(yp, 0) - sigma(y, 0)) & MASK32
    gx = (sigma(xp, 1) - sigma(x, 1)) & MASK32
    gy = (sigma(yp, 1) - sigma(y, 1)) & MASK32
    need(fx == fy == item["common_F"], "fixture F mismatch")
    need(gx == item["G_x"] and gy == item["G_y"], "fixture G mismatch")
    need((gy - gx) & MASK32 == item["G_gap"] == (2 * d) & MASK32,
         "fixture gap mismatch")


def reverse_check(q, item):
    d = (-(q << 16)) & MASK32
    x, xp = item["x_plus_D"], item["x"]
    y, yp = item["y_plus_D"], item["y"]
    need((xp - x) & MASK32 == d and (yp - y) & MASK32 == d,
         "reversal has wrong negative D")
    fx = (sigma(xp, 0) - sigma(x, 0)) & MASK32
    fy = (sigma(yp, 0) - sigma(y, 0)) & MASK32
    gx = (sigma(xp, 1) - sigma(x, 1)) & MASK32
    gy = (sigma(yp, 1) - sigma(y, 1)) & MASK32
    need(fx == fy == (-item["common_F"]) & MASK32,
         "reversal does not negate common F")
    need((gy - gx) & MASK32 == (2 * d) & MASK32,
         "reversal has wrong negative gap")


def classify(q):
    classes = input_classes(q)
    stats = Counter()
    f_leaves = 0
    twin_leaves = 0
    fixtures = []
    for ax, ex, _ in classes:
        for ay, ey, _ in classes:
            shifted = tuple((coeff << 32, rhs) for coeff, rhs in ey)
            initial = insert({}, ex + shifted, stats)
            need(initial is not None, "disjoint input cubes conflict")
            after_f = impose((initial,), 0, ax, ay, 0, stats)
            f_leaves += len(after_f)
            after_g = impose(after_f, 1, ax, ay, 2 * (q << 16), stats)
            twin_leaves += len(after_g)
            for basis in after_g:
                fixtures.append(record(q, solve_free_zero(basis), ax, ay))
    need(len(fixtures) == twin_leaves, "fixture/leaf count mismatch")
    histogram = Counter(size for _, _, size in classes)
    return {"q": q, "D": q << 16, "input_classes": len(classes),
            "class_size_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "sigma0_leaves": f_leaves, "full32_twin_leaves": twin_leaves,
            "fixtures": fixtures, "stats": dict(stats)}


def controls(results):
    attempted = rejected = reversed_count = 0
    for result in results:
        q = result["q"]
        for item in result["fixtures"]:
            validate(q, item)
            reverse_check(q, item)
            reversed_count += 1
            for field in ("x_plus_D", "y_plus_D", "xor_x", "xor_y",
                          "common_F", "G_x", "G_y", "G_gap"):
                attempted += 1
                damaged = dict(item)
                damaged[field] ^= 1
                try:
                    validate(q, damaged)
                except RuntimeError:
                    rejected += 1
    need(attempted == rejected, "damaged fixture accepted")
    return {"actual_fixtures_checked": reversed_count,
            "negative_reversals_checked": reversed_count,
            "damaged_fixtures_attempted": attempted,
            "damaged_fixtures_rejected": rejected}


def main():
    started = time.monotonic()
    need(QS == (33, 35, 37, 39, 41, 43, 45, 47,
                49, 51, 53, 55, 57, 59, 61, 63),
         "range sentinel failed")
    results = [classify(q) for q in QS]
    audit_controls = controls(results)
    payload = {
        "schema": "CRYPTO3-support12-v16-q33-63-independent-pre-author-v10",
        "status": "PASS",
        "question": "selected twin core for D=q*2^16, every odd q in [33,63]",
        "range": {"q_min": 33, "q_max": 63, "odd_only": True,
                  "q_values": list(QS), "count": len(QS)},
        "results": results,
        "controls": audit_controls,
        "negative_orientation": "bijection checked by reversing every actual surviving fixture",
        "scope": "exact bounded selected twin condition only; no third pair, support assignment, message pair, distance-14 proof, or Lean formalization",
        "python": sys.version,
        "platform": platform.platform(),
        "elapsed_seconds": time.monotonic() - started,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    out = HERE / "PRE_AUTHOR_RUN.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS", "elapsed_seconds": payload["elapsed_seconds"],
        "classification": [[r["q"], r["input_classes"],
                            r["sigma0_leaves"], r["full32_twin_leaves"]]
                           for r in results],
        "controls": audit_controls,
        "output": str(out),
    }, indent=2))


if __name__ == "__main__":
    main()
