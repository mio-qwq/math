#!/usr/bin/env python3
"""Finite exact regression from Braun--Bruegge's original Corollary 25.

This program imports no project module or discovery data.  Its facet counts
use the original shortest-path j-sum and the separately stated boundary
clauses.  It is a finite regression, not a proof of any universal inequality.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import platform
import sys
from time import perf_counter


SOURCE_PDF_SHA256 = "52e4b28b4e4106af07768940e60bb06fdd76f638b288e0139ec7bc5c05dd397a"
SOURCE_URL = "https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def choose(m: int, j: int) -> int:
    return comb(m, j) if 0 <= j <= m else 0


def B(m: int, t: int) -> int:
    """Centered binomial row, used only in target short-path expressions."""
    if m < 0:
        raise ValueError("negative row")
    if abs(t) > m or (m + t) % 2:
        return 0
    return choose(m, (m + t) // 2)


@lru_cache(maxsize=None)
def F(a: int, b: int, c: int) -> int:
    """Proposition 22: sum indexed by negative steps on the shortest path."""
    a, b, c = sorted((a, b, c), reverse=True)
    if c < 1 or len({a % 2, b % 2, c % 2}) != 1:
        raise ValueError("F here has positive rows of common parity")
    return sum(
        choose(c, j)
        * choose(b, (b - c) // 2 + j)
        * choose(a, (a - c) // 2 + j)
        for j in range(c + 1)
    )


def cycle_count(length: int) -> int:
    """Source cycle formula; length 2 is only its single-edge auxiliary."""
    if length < 2:
        raise ValueError("C_1 is not assigned a graph meaning")
    if length % 2 == 0:
        return choose(length, length // 2)
    return length * choose(length - 1, (length - 1) // 2)


def raw_theta(paths: tuple[int, int, int]) -> tuple[int, set[tuple[int, int]], int]:
    """Construct the graph, exposing coincident length-one edges by deduplication."""
    next_vertex = 2
    edges: set[tuple[int, int]] = set()
    inserted = 0
    for length in paths:
        if type(length) is not int or length < 1:
            raise ValueError("path lengths must be positive integers")
        vertices = [0] + list(range(next_vertex, next_vertex + length - 1)) + [1]
        next_vertex += length - 1
        for u, v in zip(vertices, vertices[1:]):
            edges.add(tuple(sorted((u, v))))
            inserted += 1
    return next_vertex, edges, inserted


def validate(paths: tuple[int, int, int]) -> int:
    if len(paths) != 3 or any(type(x) is not int or x < 1 for x in paths):
        raise ValueError("three positive integer path lengths required")
    if paths.count(1) > 1:
        raise ValueError("repeated length-one paths violate the simple theta domain")
    n, edges, inserted = raw_theta(paths)
    require(n == sum(paths) - 1, "theta vertex count")
    require(len(edges) == inserted == n + 1, "theta distinct-edge count")
    return n


@lru_cache(maxsize=None)
def facets(paths: tuple[int, int, int]) -> tuple[int, str]:
    """Original Corollary 25, with no zero row and explicit boundary clauses."""
    validate(paths)
    odds = sorted(x for x in paths if x % 2)
    evens = sorted(x for x in paths if x % 2 == 0)
    if len(odds) in (0, 3):
        return F(*paths), "25(i)"
    if len(evens) == 2:
        a, b = evens
        z = odds[0]
        if z == 1:
            return a * b * F(a - 1, b - 1, 1) + cycle_count(a) * cycle_count(b), "25(iii)"
        return z * F(a, b, z - 1) + a * b * F(a - 1, b - 1, z), "25(ii), two even"
    a, b = odds
    z = evens[0]
    if a == 1:
        return z * F(z - 1, b, 1) + b * cycle_count(b - 1) * cycle_count(z), "25(iv)"
    return z * F(a, b, z - 1) + a * b * F(a - 1, b - 1, z), "25(ii), two odd"


def N(a: int, b: int, c: int) -> int:
    return facets(tuple(sorted((a, b, c))))[0]


def short_even(p: int, q: int, offset: int = 2) -> Fraction:
    require(p >= 2 and q >= 2 and p % 2 == q % 2 == 0, "even short-path domain")
    return Fraction(p * q + offset, 2) * B(p, 0) * B(q, 0)


def short_odd(x: int, y: int, offset: int = 5) -> Fraction:
    require(x >= 1 and y >= 1 and x % 2 == y % 2 == 1, "odd short-path domain")
    require(not (x == y == 1), "simple odd short-path domain")
    return Fraction(x * y + offset, 4) * B(x + 1, 0) * B(y + 1, 0)


def predicted_triple(n: int) -> tuple[int, int, int]:
    if n % 2:
        k = (n + 1) // 2
        paths = (k - 1, k - 1, 2) if k % 2 == 0 else (k, k - 2, 2)
    else:
        k = n // 2
        paths = (k, k, 1) if k % 2 == 0 else (k + 1, k - 1, 1)
    return tuple(sorted(paths))


def predicted_H(n: int) -> Fraction:
    if n % 2:
        k = (n + 1) // 2
        if k % 2 == 0:
            return Fraction(k * k - 2 * k + 6, 4) * choose(k, k // 2) ** 2
        return Fraction(k * (k * k - 2 * k + 5), k + 1) * choose(k - 1, (k - 1) // 2) ** 2
    k = n // 2
    if k % 2 == 0:
        return Fraction(k * k + 2, 2) * choose(k, k // 2) ** 2
    return Fraction(2 * k * (k * k + 1), k + 1) * choose(k - 1, (k - 1) // 2) ** 2


def original_M(n: int) -> int:
    if n < 5:
        raise ValueError("original Definition 12 is used only for n >= 5")
    k = (n + 1) // 2 if n % 2 else n // 2
    a, b = (k - 1, k + 1) if k % 2 == 0 else (k, k)
    return cycle_count(a) * cycle_count(b) * (1 if n % 2 else 2)


def predicted_ratio(n: int) -> Fraction:
    require(n >= 5, "ratio is restricted to original M domain")
    if n % 2:
        k = (n + 1) // 2
        return Fraction(k * k - 2 * k + (6 if k % 2 == 0 else 5), k * (k + 1))
    k = n // 2
    return Fraction(k * k + (2 if k % 2 == 0 else 1), k * (k + 1))


def fraction_json(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def damage_controls() -> list[dict]:
    control_paths = (2, 3, 3)
    truth = N(*control_paths)
    corrupted = short_odd(3, 3, offset=4)
    require(corrupted != truth, "coefficient 5 -> 4 damage was not detected")
    omitted_xy = 2 * F(3, 3, 1) + F(2, 2, 2)
    require(omitted_xy != truth, "omitted xy damage was not detected")
    invalid = (1, 1, 4)
    vertices, edges, attempted = raw_theta(invalid)
    rejected = False
    rejection = None
    try:
        facets(invalid)
    except ValueError as exc:
        rejected, rejection = True, str(exc)
    require(rejected and len(edges) != vertices + 1, "duplicate length-one damage was not detected")
    return [
        {"mutation": "short odd coefficient 5 -> 4", "paths": control_paths,
         "correct_N": truth, "mutated_value": fraction_json(corrupted), "detected": True},
        {"mutation": "omit xy in Corollary 25(ii)", "paths": control_paths,
         "correct_N": truth, "mutated_value": omitted_xy, "detected": True},
        {"mutation": "allow repeated length-one paths", "paths": invalid,
         "vertices": vertices, "attempted_path_edges": attempted, "distinct_edges": len(edges),
         "required_bicyclic_edges": vertices + 1, "rejection": rejection, "detected": True},
    ]


def run(min_n: int, max_n: int) -> tuple[list[dict], list[dict], Counter]:
    checks: Counter = Counter()
    rows, orders = [], []
    for n in range(min_n, max_n + 1):
        current = []
        for a in range(1, (n + 1) // 3 + 1):
            for b in range(a, (n + 1 - a) // 2 + 1):
                c = n + 1 - a - b
                paths = (a, b, c)
                if paths.count(1) > 1:
                    continue
                value, clause = facets(paths)
                same = len({x % 2 for x in paths}) == 1
                row = {"n": n, "paths": paths, "N": value, "same_parity": same, "source_clause": clause}
                rows.append(row)
                current.append(row)
                checks["legal_unordered_triples"] += 1
                checks["source_" + clause] += 1
                if same:
                    continue
                repeated_parity = 0 if sum(x % 2 == 0 for x in paths) == 2 else 1
                pair = sorted(x for x in paths if x % 2 == repeated_parity)
                z = next(x for x in paths if x % 2 != repeated_parity)
                for x, y in sorted({tuple(pair), tuple(reversed(pair))}):
                    if repeated_parity == 0:
                        target = (x, y + z - 1, 1)
                        threshold, kind = 1, "even_order"
                    else:
                        if x < 3:
                            continue
                        target = (x, y + z - 2, 2)
                        threshold, kind = 2, "odd_order"
                    require(sum(target) == n + 1, f"compression changes order: {paths}, {target}")
                    after = N(*target)
                    require(value <= after, f"compression failed: {paths}, {target}, {value}, {after}")
                    require((value < after) == (z > threshold), f"compression strictness failed: {paths}, {target}")
                    checks["compression_" + kind] += 1
                    checks["compression_" + kind + ("_strict" if z > threshold else "_identity")] += 1
                if z == (1 if repeated_parity == 0 else 2):
                    x, y = pair
                    short = short_even(x, y) if repeated_parity == 0 else short_odd(x, y)
                    require(short.denominator == 1 and short == value, f"short formula failed: {paths}")
                    kind = "even_order" if repeated_parity == 0 else "odd_order"
                    checks["short_formula_" + kind] += 1
                    if y >= x + 4:
                        balanced = N(x + 2, y - 2, z)
                        require(balanced > value, f"strict inward balancing failed: {paths}")
                        checks["balancing_" + kind] += 1
        require(bool(current), f"empty domain at n={n}")
        high = max(row["N"] for row in current)
        winners = [row["paths"] for row in current if row["N"] == high]
        target = predicted_triple(n)
        require(winners == [target], f"unique predicted maximizer failed at n={n}: {winners}")
        formula = predicted_H(n)
        require(formula.denominator == 1 and formula == high, f"maximum closed formula failed at n={n}")
        checks["unique_maximizer_orders"] += 1
        checks["maximum_closed_formulas"] += 1
        same_values = [row["N"] for row in current if row["same_parity"]]
        for value in same_values:
            require(value < high, f"same-parity exclusion failed at n={n}")
            checks["same_parity_strict_exclusion"] += 1
        order = {"n": n, "legal_unordered_triples": len(current), "maximizing_paths": target,
                 "max_N": high, "number_of_maximizers": len(winners),
                 "same_parity_triples": len(same_values), "same_parity_max_N": max(same_values, default=None),
                 "original_Conjecture_33_domain": n >= 10}
        if n >= 5:
            bound = original_M(n)
            ratio = Fraction(high, bound)
            require(ratio == predicted_ratio(n) and ratio < 1, f"M-ratio formula failed at n={n}")
            order.update({"M_original_Definition_12": bound, "H_over_M": fraction_json(ratio)})
            checks["maximum_to_M_ratios"] += 1
        else:
            order["M_original_Definition_12"] = None
            order["M_scope_note"] = "No graph value is assigned to C_1; the n=4 theta maximum is computed directly."
        orders.append(order)
    return rows, orders, checks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-n", type=int, default=4)
    parser.add_argument("--max-n", type=int, default=40)
    parser.add_argument("--source-pdf", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--target-sha256", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    require(4 <= args.min_n <= args.max_n, "finite window must start at a legal theta order")
    source_bytes = args.source_pdf.read_bytes()
    target_bytes = args.target.read_bytes()
    require(sha256(source_bytes).hexdigest() == SOURCE_PDF_SHA256, "source PDF hash mismatch")
    require(sha256(target_bytes).hexdigest() == args.target_sha256, "target manuscript hash mismatch")
    start = perf_counter()
    began = datetime.now(timezone.utc).isoformat()
    rows, orders, checks = run(args.min_n, args.max_n)
    controls = damage_controls()
    elapsed = perf_counter() - start
    require(args.target.read_bytes() == target_bytes, "target manuscript changed during this run")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    data = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)
    data_path = args.output_dir / "exact_counts.jsonl"
    data_path.write_text(data, encoding="utf-8")
    result = {
        "status": "PASS finite exact regression", "universal_proof": False,
        "method": "Original Proposition 22 shortest-path j-sum and Corollary 25(i)-(iv), with explicit boundary clauses",
        "independence": "Python standard library only; no imports of project code, root discovery data, or previous graph checker",
        "source": {"url": SOURCE_URL, "sha256": SOURCE_PDF_SHA256, "bytes": len(source_bytes),
                   "locations": ["Proposition 22", "Corollary 25, p. 15", "Definition 12, p. 7", "Conjecture 33, p. 24"]},
        "target": {"file": "theta/MAXIMIZERS.md", "sha256": args.target_sha256, "bytes": len(target_bytes),
                   "use": "Target mappings and closed expressions only; no proof acceptance is asserted by this computation"},
        "environment": {"python": sys.version, "implementation": platform.python_implementation(),
                        "platform": platform.platform(), "arithmetic": "Python arbitrary-precision integers and fractions.Fraction"},
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "run_started_utc": began, "elapsed_seconds": elapsed,
        "window": {"min_n": args.min_n, "max_n": args.max_n, "orders": len(orders)},
        "checks": dict(sorted(checks.items())), "damage_controls": controls,
        "data_file": {"file": data_path.name, "sha256": sha256(data.encode()).hexdigest(), "rows": len(rows)},
        "order_maxima": orders,
        "limitations": ["The tested finite window is not a proof for all path lengths.",
                        "This run does not enumerate graph facets or invoke a polytope package.",
                        "No Lean theorem or independent human peer review is claimed.",
                        "Original M(n) is evaluated only for n >= 5; Conjecture 33 originally asks n >= 10."]
    }
    (args.output_dir / "RESULTS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: finite exact scalar regression")
    print(f"UTC: {began}")
    print(f"Python: {platform.python_version()} ({platform.python_implementation()})")
    print(f"Window: {args.min_n} <= n <= {args.max_n}")
    print(f"Source SHA256: {SOURCE_PDF_SHA256}")
    print(f"Target SHA256: {args.target_sha256}")
    print(f"Script SHA256: {result['script_sha256']}")
    print(f"Exact counts SHA256: {result['data_file']['sha256']}")
    for label, count in sorted(checks.items()):
        print(f"{label}: {count}")
    print(f"Targeted damage controls detected: {len(controls)}/{len(controls)}")
    print(f"Elapsed seconds: {elapsed:.6f}")
    print("Finite regression only; universal theorem requires the separate mathematical proof.")


if __name__ == "__main__":
    main()
