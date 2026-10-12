"""Exact integer evaluation of the proved Ka(m,4) finite upper bound.

The radical in the theorem is evaluated through its integer quadratic,
so this command does not trust floating-point rounding.
"""

import argparse
import json


def falling(m, k):
    out = 1
    for j in range(k):
        out *= m - j
    return out


def correction_polynomial(m):
    return (8 * falling(m, 2) + 12 * falling(m, 3)
            + 15 * falling(m, 4) + 3 * falling(m, 5))


def bound(m):
    if type(m) is not int or m < 2:
        raise ValueError("m must be an integer alphabet size at least two")
    fourth = m ** 4
    poly = correction_polynomial(m)

    def residual(size):
        return 6 * size ** 2 - 9 * size * fourth + 2 * fourth ** 2 + 3 * m * poly

    lo, hi = 0, fourth
    assert residual(lo) > 0 and residual(hi) < 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if residual(mid) >= 0:
            lo = mid
        else:
            hi = mid
    return dict(alphabet_size=m, polynomial_P=poly, upper_bound=lo,
                residual_at_bound=residual(lo),
                residual_at_next_integer=residual(lo+1),
                original_vertex_count=m*(m-1)**3,
                status="proved upper bound; not an exact GP number")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("m", nargs="+", type=int)
    args = parser.parse_args()
    print(json.dumps([bound(m) for m in args.m], indent=2))


if __name__ == "__main__":
    main()
