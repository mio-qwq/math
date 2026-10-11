#!/usr/bin/env python3
"""Known reversible-prefix method applied to an exact local correlation.

The core evaluator uses O(n) rational arithmetic operations and a constant
number of O(n)-bit rational matrices.  It never stores all n prefixes.
No root/verifier implementation is imported; frozen JSON/JSONL counts are
read only by the test harness.  No third-party dependencies or randomness.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import permutations
import json
from pathlib import Path
import platform
import resource
import shlex
import sys
import time
import traceback


F = Fraction
ZERO, ONE = F(0), F(1)
IDENTITY = tuple(tuple(F(a == b) for b in range(4)) for a in range(4))


@dataclass
class ArithmeticStats:
    matrix_products: int = 0
    row_products: int = 0
    scalar_products: int = 0
    max_numerator_bits: int = 0
    max_denominator_bits: int = 0

    def observe_values(self, values) -> None:
        for value in values:
            self.max_numerator_bits = max(self.max_numerator_bits, abs(value.numerator).bit_length())
            self.max_denominator_bits = max(self.max_denominator_bits, value.denominator.bit_length())

    def observe_matrix(self, matrix) -> None:
        self.observe_values(value for row in matrix for value in row)


def matmul(left, right, stats=None):
    out = [[ZERO for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for k in range(4):
            if left[a][k]:
                for b in range(4):
                    if right[k][b]:
                        out[a][b] += left[a][k] * right[k][b]
                        if stats is not None:
                            stats.scalar_products += 1
    out = tuple(tuple(row) for row in out)
    if stats is not None:
        stats.matrix_products += 1
        stats.observe_matrix(out)
    return out


def rowmul(row, matrix, stats=None):
    out = [ZERO] * 4
    for a in range(4):
        if row[a]:
            for b in range(4):
                if matrix[a][b]:
                    out[b] += row[a] * matrix[a][b]
                    if stats is not None:
                        stats.scalar_products += 1
    out = tuple(out)
    if stats is not None:
        stats.row_products += 1
        stats.observe_values(out)
    return out


def invert4(matrix):
    """Exact Gauss-Jordan inversion; called only for three constant matrices."""
    aug = [list(matrix[a]) + list(IDENTITY[a]) for a in range(4)]
    determinant = ONE
    for col in range(4):
        pivot = next((row for row in range(col, 4) if aug[row][col]), None)
        if pivot is None:
            raise ValueError("singular transition matrix")
        if pivot != col:
            aug[pivot], aug[col] = aug[col], aug[pivot]
            determinant = -determinant
        value = aug[col][col]
        determinant *= value
        aug[col] = [entry / value for entry in aug[col]]
        for row in range(4):
            if row != col and aug[row][col]:
                multiplier = aug[row][col]
                aug[row] = [x - multiplier * y for x, y in zip(aug[row], aug[col])]
    return tuple(tuple(row[4:]) for row in aug), determinant


def determinant_leibniz(matrix):
    """A second exact determinant calculation, using 24 permutation terms."""
    total = ZERO
    for perm in permutations(range(4)):
        inversions = sum(perm[a] > perm[b] for a in range(4) for b in range(a + 1, 4))
        term = F(-1 if inversions % 2 else 1)
        for row, col in enumerate(perm):
            term *= matrix[row][col]
        total += term
    return total


def build_transition(mode, mask):
    """Rows are destination states; columns are source states (2*beta+gamma)."""
    counts = [[0] * 4 for _ in range(4)]
    choices = 8 if mode == "uniform" else 4
    for beta in range(2):
        for gamma in range(2):
            source = 2 * beta + gamma
            for s in range(2):
                for y in range(2):
                    bs = range(2) if mode == "uniform" else ((s - int(mode) - beta) & 1,)
                    for b in bs:
                        subtrahend = b if mode == "uniform" else int(mode)
                        beta_next = int(subtrahend + beta > s)
                        gamma_next = (s + y + gamma) // 2
                        destination = 2 * beta_next + gamma_next
                        phase = (b if "B" in mask else 0) ^ (y if "Y" in mask else 0)
                        counts[destination][source] += 1 - 2 * phase
    return tuple(tuple(F(value, choices) for value in row) for row in counts)


def scale_columns(matrix, diagonal):
    return tuple(tuple(value * diagonal[col] for col, value in enumerate(row)) for row in matrix)


def scale_rows(matrix, diagonal):
    return tuple(tuple(value * diagonal[row] for value in entries)
                 for row, entries in enumerate(matrix))


def constant_tables():
    """Only 3 modes x 4 boundary phases, independent of n."""
    bases = {}
    tables = {}
    for mode in ("uniform", "0", "1"):
        base = build_transition(mode, "")
        inverse, determinant = invert4(base)
        assert determinant == determinant_leibniz(base) == F(1, 16)
        assert matmul(base, inverse) == matmul(inverse, base) == IDENTITY
        marked = {mask: build_transition(mode, mask) for mask in ("B", "Y", "BY")}
        insertion = {mask: matmul(inverse, marked[mask]) for mask in marked}
        bases[mode] = {"matrix": base, "inverse": inverse, "determinant": determinant}
        tables[mode] = {}
        for code in range(4):
            beta_phase, gamma_phase = code >> 1, code & 1
            diagonal = tuple(F(1 - 2 * (((state >> 1) * beta_phase)
                                      ^ ((state & 1) * gamma_phase))) for state in range(4))
            # T=P D, T^-1=D P^-1, E^X=T^-1 K^X=D P^-1 P^X D.
            transition = scale_columns(base, diagonal)
            transition_inverse = scale_rows(inverse, diagonal)
            phase_insertion = {mask: scale_rows(scale_columns(insertion[mask], diagonal), diagonal)
                               for mask in insertion}
            assert matmul(transition, transition_inverse) == IDENTITY
            tables[mode][code] = (transition, transition_inverse, phase_insertion)
    return bases, tables


BASES, TABLES = constant_tables()


def step_table(p, i, k, fixed_a):
    mode = "uniform" if fixed_a is None else str((fixed_a >> p) & 1)
    beta_phase = int(p == i) ^ int(p == k)
    gamma_phase = int(p == i)
    return TABLES[mode][2 * beta_phase + gamma_phase]


def advance(prefix, inverse, p, i, k, fixed_a, stats):
    transition, transition_inverse, _ = step_table(p, i, k, fixed_a)
    return (matmul(transition, prefix, stats),
            matmul(inverse, transition_inverse, stats))


def conjugated_insertion(prefix, inverse, p, mask, i, k, fixed_a, stats):
    _, _, insertion = step_table(p, i, k, fixed_a)
    return matmul(matmul(inverse, insertion[mask], stats), prefix, stats)


def streaming_correlation(n, r, q, i, fixed_a=None, stats=None):
    """Exact local correlation with no list/cache of n prefixes.

    A constant number of matrices/rows is live.  The caller may collect test
    outputs; that reporting storage is not part of this evaluator.
    """
    if not (n >= 1 and 0 <= r < n and 0 <= q < n and 0 <= i < n):
        raise ValueError("invalid width, rotation, or bit index")
    if fixed_a is not None and not 0 <= fixed_a < (1 << n):
        raise ValueError("fixed first word is outside the n-bit domain")
    if stats is None:
        stats = ArithmeticStats()
    j, k = (i - q) % n, (i - r - q) % n
    # f G_n = f T_(n-1) ... T_0, evaluated as one descending row scan.
    final_row = (ONE,) * 4
    for p in range(n - 1, -1, -1):
        transition, _, _ = step_table(p, i, k, fixed_a)
        final_row = rowmul(final_row, transition, stats)
    baseline = final_row[0]
    if i >= q:
        length, distance = i - q, q
        low_mask, high_mask = "B", "Y"
        coefficient_exponent_offset = 0
    else:
        length, distance = i, n - q
        low_mask, high_mask = "Y", "B"
        coefficient_exponent_offset = distance
    if length == 0:
        answer = baseline / (1 << j)
        stats.observe_values((answer,))
        return answer
    low_prefix, low_inverse = IDENTITY, IDENTITY
    high_prefix, high_inverse = IDENTITY, IDENTITY
    if distance:
        for p in range(distance):
            high_prefix, high_inverse = advance(high_prefix, high_inverse, p, i, k, fixed_a, stats)
    weighted_sum = ZERO
    for t in range(length):
        if distance == 0:
            same = conjugated_insertion(low_prefix, low_inverse, t, "BY", i, k, fixed_a, stats)
            moment = sum((final_row[state] * same[state][0] for state in range(4)), ZERO)
        else:
            low = conjugated_insertion(low_prefix, low_inverse, t, low_mask, i, k, fixed_a, stats)
            high = conjugated_insertion(high_prefix, high_inverse, t + distance,
                                       high_mask, i, k, fixed_a, stats)
            left = rowmul(final_row, high, stats)
            moment = sum((left[state] * low[state][0] for state in range(4)), ZERO)
        weighted_sum += (1 << (coefficient_exponent_offset + t)) * moment
        stats.observe_values((moment, weighted_sum))
        low_prefix, low_inverse = advance(low_prefix, low_inverse, t, i, k, fixed_a, stats)
        if distance:
            high_prefix, high_inverse = advance(high_prefix, high_inverse,
                                               t + distance, i, k, fixed_a, stats)
    answer = (baseline - weighted_sum) / (1 << j)
    stats.observe_values((answer,))
    return answer


def matrix_record(matrix):
    return [[str(value) for value in row] for row in matrix]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = Path(__file__).resolve().parent.parent
    paths = {
        "uniform_word_counts": project / "verification/independent_word_counts.jsonl",
        "fixed_word_counts": project / "verification/general_fixed_word_counts.jsonl",
        "standard32": project / "verification/general_standard32_exact.json",
    }
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    records = []
    timings = {}
    aggregate = ArithmeticStats()
    failures = []

    def check(n, r, q, i, a, expected, source):
        per_call = ArithmeticStats()
        actual = streaming_correlation(n, r, q, i, a, per_call)
        assert actual == expected, (source, n, r, q, i, a, str(actual), str(expected))
        # The exact implementation has at most 8n dynamic 4x4 products.
        assert per_call.matrix_products <= 8 * n
        aggregate.matrix_products += per_call.matrix_products
        aggregate.row_products += per_call.row_products
        aggregate.scalar_products += per_call.scalar_products
        aggregate.max_numerator_bits = max(aggregate.max_numerator_bits, per_call.max_numerator_bits)
        aggregate.max_denominator_bits = max(aggregate.max_denominator_bits, per_call.max_denominator_bits)
        records.append({"source": source, "n": n, "r": r, "q": q, "i": i,
                        "fixed_a": a, "correlation": str(actual),
                        "dynamic_matrix_products": per_call.matrix_products,
                        "max_numerator_bits": per_call.max_numerator_bits,
                        "max_denominator_bits": per_call.max_denominator_bits})

    try:
        print("PASS independent transition enumeration, both determinant methods: all three det(P)=1/16.", flush=True)
        print("Planned comparisons: 216 uniform original-word, 1274 fixed-word, 160 standard32 values; no new brute force.", flush=True)
        stage = time.monotonic()
        before = len(records)
        for line in paths["uniform_word_counts"].read_text().splitlines():
            row = json.loads(line)
            if row.get("kind") != "exhaustive":
                continue
            for i, value in enumerate(row["signed_sums"]):
                check(row["n"], row["r"], row["q"], i, None,
                      F(value, row["samples"]), "uniform_original_words")
        timings["uniform_original_words"] = {"cases": len(records) - before,
                                               "seconds": time.monotonic() - stage}
        assert timings["uniform_original_words"]["cases"] == 216
        print("PASS all 216 uniform original-word values.", flush=True)
        stage = time.monotonic()
        before = len(records)
        for line in paths["fixed_word_counts"].read_text().splitlines():
            row = json.loads(line)
            if row.get("kind") != "fixed_a_exhaustive":
                continue
            for i, value in enumerate(row["signed_sums"]):
                check(row["n"], row["r"], row["q"], i, row["a"],
                      F(value, row["samples"]), "fixed_original_words")
        timings["fixed_original_words"] = {"cases": len(records) - before,
                                             "seconds": time.monotonic() - stage}
        assert timings["fixed_original_words"]["cases"] == 1274
        print("PASS all 1274 fixed-word original-word values.", flush=True)
        stage = time.monotonic()
        before = len(records)
        standard = json.loads(paths["standard32"].read_text())
        for i, value in enumerate(standard["uniform_a"]):
            check(standard["n"], standard["r"], standard["q"], i, None,
                  F(value["numerator"], value["denominator"]), "standard32_uniform")
        for key, values in standard["fixed_a"].items():
            a = int(key, 16)
            for i, value in enumerate(values):
                check(standard["n"], standard["r"], standard["q"], i, a,
                      F(value["numerator"], value["denominator"]), "standard32_fixed")
        timings["standard32"] = {"cases": len(records) - before,
                                   "seconds": time.monotonic() - stage}
        assert timings["standard32"]["cases"] == 160
        print("PASS all 160 independent standard32 values.", flush=True)
    except Exception:
        failures.append(traceback.format_exc())
    success = not failures
    report = {
        "status": "passed_research_self_check" if success else "failed",
        "novelty": "Known reversible-prefix matrix method instantiated for this local function; no originality claim.",
        "independent_verification": False,
        "data_review_boundary": "Only frozen data files were read; no root/verifier implementation was imported or inspected.",
        "randomness": "none",
        "started_at_utc": started,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - start,
        "command": shlex.join([sys.executable] + sys.argv),
        "exit_code_on_completion": 0 if success else 1,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_sha256": {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()},
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "machine": platform.machine(),
                        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        "constant_matrices": {mode: {"P": matrix_record(item["matrix"]),
                                     "P_inverse": matrix_record(item["inverse"]),
                                     "determinant": str(item["determinant"])}
                              for mode, item in BASES.items()},
        "timings": timings,
        "arithmetic_statistics": vars(aggregate),
        "space_note": "Core keeps a constant number of matrices and rows, not n prefixes. Test result records and input JSON parsing are separate harness storage.",
        "records": records,
        "failures": failures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"timings": timings, "arithmetic_statistics": vars(aggregate),
                      "failures": failures}, indent=2), flush=True)
    print(f"Saved {args.output}; exit code {0 if success else 1}.", flush=True)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
