#!/usr/bin/env python3
"""Bounded mask discovery; no actual-schedule conclusion follows."""
import hashlib
import json
import platform
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 1 << 32
MASK = N - 1


def rot(x, k):
    return ((x >> k) | (x << (32-k))) & MASK


def f(x):
    return rot(x, 7) ^ rot(x, 18) ^ (x >> 3)


def g(x):
    return rot(x, 17) ^ rot(x, 19) ^ (x >> 10)


def output_row(L, j):
    return sum(((L(1 << i) >> j) & 1) << i for i in range(32))


def kernel(rows):
    pivots = {}
    for row in rows:
        while row:
            i = row.bit_length()-1
            if i not in pivots:
                pivots[i] = row
                break
            row ^= pivots[i]
    basis = []
    for i in range(32):
        if i in pivots:
            continue
        x = 1 << i
        for j in sorted(pivots):
            if (x & pivots[j]).bit_count() & 1:
                x ^= 1 << j
        assert all((x & row).bit_count() % 2 == 0 for row in rows)
        basis.append(x)
    return basis, len(pivots)


def span(basis):
    vals = [0]
    for x in basis:
        vals += [v ^ x for v in vals]
    return vals


def zero_sum(a, b):
    """Exact independent signed-bit feasibility, signs need not be actual."""
    carry = {0}
    for i in range(32):
        count = ((a >> i) & 1)+((b >> i) & 1)
        terms = [0] if count == 0 else [-1, 1] if count == 1 else [-2, 0, 2]
        carry = {(c+t)//2 for c in carry for t in terms if (c+t) % 2 == 0}
        if not carry:
            return False, i
    return True, None


def main():
    started = time.monotonic()
    low16 = [1 << i for i in range(16)] + [output_row(g, i) for i in range(16)]
    bx, rx = kernel(low16)
    by, ry = kernel([output_row(f, i) for i in range(16)])
    assert bx == [0x44ab0000]
    gamma = f(bx[0])
    hits = []
    hist = {}
    for alpha in span(by):
        ok, bit = zero_sum(alpha, gamma)
        if ok:
            hits.append(alpha)
        else:
            hist[str(bit)] = hist.get(str(bit), 0)+1
    result = {
        "scope": "necessary two-pair core; k=16 simultaneous valuations only",
        "equations": ["dY=-FX", "FY=-m*dX-GX", "m in {1,2}",
                      "2^16 divides dX and m*dX+GX"],
        "python": platform.python_version(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "support_sha256": hashlib.sha256((HERE.parent/'supports-v2.json').read_bytes()).hexdigest(),
        "kernel_X_rank": rx, "kernel_X_basis": bx,
        "FX_xor_mask": gamma,
        "kernel_Y_rank": ry, "kernel_Y_basis": by,
        "examined_masks": 1 << len(by),
        "survivor_count": len(hits),
        "survivors": hits,
        "first_empty_carry_histogram": hist,
        "elapsed_s": time.monotonic()-started,
        "interpretation": "nonempty necessary cover is not actual-pair feasibility"
    }
    (HERE/'MASK_PROBE.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'survivors'}, indent=2))


if __name__ == '__main__':
    main()
