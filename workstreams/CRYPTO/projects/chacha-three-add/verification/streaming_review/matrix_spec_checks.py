#!/usr/bin/env python3
"""Independent mathematical-specification checks, not a third production implementation.

This deliberately small harness may store all prefixes for n<=4. The proposed
streaming algorithm's space bound is reviewed mathematically in a separate note.
Discovery streaming code has not been read when this harness is first executed.
The preceding 22 verification artifacts and their manifest are read-only inputs.
"""

from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
from itertools import permutations
import json
from pathlib import Path
import platform
import sys


HERE = Path(__file__).resolve().parent
OLD = HERE.parent


def identity():
    return [[Q(int(i == j)) for j in range(4)] for i in range(4)]


def multiply(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def inverse(a):
    aug = [row[:] + unit for row, unit in zip(a, identity())]
    for col in range(4):
        pivot = next(row for row in range(col, 4) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        divisor = aug[col][col]
        aug[col] = [x / divisor for x in aug[col]]
        for row in range(4):
            if row != col:
                factor = aug[row][col]
                aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [row[4:] for row in aug]


def determinant(a):
    # Independent Leibniz determinant: only 24 products for a 4-by-4 matrix.
    answer = Q(0)
    for p in permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))
        term = Q(-1 if inversions % 2 else 1)
        for i in range(4):
            term *= a[i][p[i]]
        answer += term
    return answer


def kernel(fixed_bit=None, mask="none"):
    out = [[Q(0) for _ in range(4)] for _ in range(4)]
    denominator = 8 if fixed_bit is None else 4
    for old_state in range(4):
        borrow, carry = divmod(old_state, 2)
        for s_bit in (0, 1):
            if fixed_bit is None:
                b_choices = (0, 1)
            else:
                delta = s_bit - fixed_bit - borrow
                b_choices = (delta % 2,)
            for b_bit in b_choices:
                next_borrow = int(s_bit - b_bit - borrow < 0) if fixed_bit is None else int(delta < 0)
                for y_bit in (0, 1):
                    next_carry = int(s_bit + y_bit + carry >= 2)
                    sign = (b_bit if "B" in mask else 0) ^ (y_bit if "Y" in mask else 0)
                    out[2 * next_borrow + next_carry][old_state] += Q(-1 if sign else 1, denominator)
    return out


KERNELS = {fixed: {mask: kernel(fixed, mask) for mask in ("none", "B", "Y", "BY")}
           for fixed in (None, 0, 1)}


def phase(position, i, k):
    out = identity()
    for state in range(4):
        borrow, carry = divmod(state, 2)
        exponent = (borrow if position == i else 0) ^ (borrow if position == k else 0)
        exponent ^= carry if position == i else 0
        out[state][state] = Q(-1 if exponent else 1)
    return out


def row_value(terminal_row, operator):
    return multiply(terminal_row, operator)[0][0]


def evaluate_spec(n, r, q, i, fixed_a=None, wrong_phase_order=False):
    r, q = r % n, q % n
    j, k = (i - q) % n, (i - r - q) % n
    t_matrices, signed_kernels = [], []
    prefixes = [identity()]
    for pos in range(n):
        fixed_bit = None if fixed_a is None else (fixed_a >> pos) & 1
        d = phase(pos, i, k)
        matrices = {}
        for mask, p in KERNELS[fixed_bit].items():
            matrices[mask] = multiply(d, p) if wrong_phase_order else multiply(p, d)
        t_matrices.append(matrices["none"])
        signed_kernels.append(matrices)
        prefixes.append(multiply(matrices["none"], prefixes[-1]))
    terminal = multiply([[Q(1)] * 4], prefixes[n])

    def insert(pos, mask):
        # Literal proposed interaction-picture formula, with column vectors.
        return multiply(multiply(multiply(inverse(prefixes[pos]), inverse(t_matrices[pos])),
                                 signed_kernels[pos][mask]), prefixes[pos])

    pairs = ([(t, q + t) for t in range(i - q)] if i >= q
             else [(n - q + t, t) for t in range(i)])
    defining_pairs = [((l - q) % n, l) for l in range(i) if (l - q) % n < j]
    assert pairs == defining_pairs
    numerator = terminal[0][0]
    moment_checks = []
    for h, l in pairs:
        if h == l:
            operator = insert(h, "BY")
        elif h < l:
            operator = multiply(insert(l, "Y"), insert(h, "B"))
        else:
            operator = multiply(insert(h, "B"), insert(l, "Y"))
        inserted_moment = row_value(terminal, operator)
        # Separate literal matrix chain with the relevant input masks at bits.
        direct_chain = identity()
        for pos in range(n):
            mask = ("B" if pos == h else "") + ("Y" if pos == l else "")
            direct_chain = multiply(signed_kernels[pos][mask or "none"], direct_chain)
        direct_moment = multiply([[Q(1)] * 4], direct_chain)[0][0]
        assert inserted_moment == direct_moment
        numerator -= 2**h * inserted_moment
        moment_checks.append({"h": h, "l": l, "moment": str(inserted_moment),
                              "same_position": h == l, "pass": True})
    return numerator / 2**j, moment_checks


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_strings(a):
    return [[str(x) for x in row] for row in a]


def main():
    old_manifest = OLD / "INDEPENDENT_VERIFICATION_MANIFEST.json"
    frozen = json.loads(old_manifest.read_text())
    frozen_hash = sha(old_manifest)
    for item in frozen["files"]:
        assert sha(OLD / item["file"]) == item["sha256"], ("frozen artifact changed", item["file"])
    report = {"started_utc": datetime.now(timezone.utc).isoformat(),
              "command": [sys.executable, str(Path(__file__).resolve())],
              "environment": {"python": sys.version, "platform": platform.platform()},
              "source_sha256": sha(Path(__file__).resolve()),
              "frozen_manifest_sha256": frozen_hash,
              "frozen_old_files_checked": len(frozen["files"]),
              "independence": "Supplied mathematical specification only; no new discovery implementation read before this run.",
              "scope": "Kernel determinants and a small prefix-storage test harness, not a third streaming production implementation.",
              "random_seed": None, "new_original_word_enumerations": 0}
    try:
        kernel_results = {}
        same_position_controls = []
        for fixed_bit in (None, 0, 1):
            name = "uniform" if fixed_bit is None else f"fixed_{fixed_bit}"
            p = KERNELS[fixed_bit]["none"]
            inv = inverse(p)
            det = determinant(p)
            assert det == Q(1, 16)
            assert multiply(p, inv) == multiply(inv, p) == identity()
            assert all(sum(p[row][col] for row in range(4)) == 1 for col in range(4))
            kernel_results[name] = {"P": matrix_strings(p), "inverse": matrix_strings(inv),
                                    "determinant": str(det), "both_inverse_products_identity": True,
                                    "inverse_column_norm": str(max(sum(abs(inv[row][col]) for row in range(4))
                                                                   for col in range(4)))}
            by = KERNELS[fixed_bit]["BY"]
            sequential = multiply(multiply(KERNELS[fixed_bit]["B"], inv), KERNELS[fixed_bit]["Y"])
            difference = next(((row, col) for row in range(4) for col in range(4)
                               if by[row][col] != sequential[row][col]), None)
            same_position_controls.append({"kernel": name, "joint_equals_sequential": difference is None,
                                           "first_difference": None if difference is None else {
                                               "row": difference[0], "column": difference[1],
                                               "P_BY": str(by[difference[0]][difference[1]]),
                                               "P_B_inverse_P_P_Y": str(sequential[difference[0]][difference[1]])}})

        uniform_rows = [json.loads(line) for line in (OLD / "independent_word_counts.jsonl").read_text().splitlines()]
        uniform_rows = {(row["n"], row["r"], row["q"]): row for row in uniform_rows if row["kind"] == "exhaustive"}
        fixed_rows = [json.loads(line) for line in (OLD / "general_fixed_word_counts.jsonl").read_text().splitlines()]
        fixed_rows = {(row["n"], row["r"], row["q"], row["a"]): row for row in fixed_rows}
        cases = [(3, 0, 0, 0, None), (3, 0, 0, 1, None), (3, 1, 0, 2, None),
                 (3, 1, 1, 2, None), (3, 1, 2, 0, None), (3, 1, 2, 1, None),
                 (4, 3, 2, 1, None), (4, 2, 1, 3, None), (4, 0, 2, 3, None), (4, 3, 3, 2, None),
                 (2, 0, 0, 1, 0), (2, 0, 0, 1, 1), (3, 1, 1, 2, 5), (3, 1, 1, 2, 4),
                 (4, 3, 2, 1, 15), (4, 2, 1, 3, 10), (4, 0, 2, 3, 11), (4, 3, 3, 2, 6)]
        comparison_rows = []
        for n, r, q, i, fixed_a in cases:
            row = uniform_rows[n, r, q] if fixed_a is None else fixed_rows[n, r, q, fixed_a]
            observed = Q(row["signed_sums"][i], row["samples"])
            calculated, checks = evaluate_spec(n, r, q, i, fixed_a)
            assert observed == calculated, (n, r, q, i, fixed_a, observed, calculated)
            comparison_rows.append({"n": n, "r": r, "q": q, "i": i, "fixed_a": fixed_a,
                                    "correlation": str(calculated), "inserted_moments": checks, "pass": True})
        wrong_phase, _ = evaluate_spec(3, 0, 0, 0, wrong_phase_order=True)
        assert wrong_phase == Q(1, 2)
        assert wrong_phase != Q(1)

        for item in frozen["files"]:
            assert sha(OLD / item["file"]) == item["sha256"]
        assert sha(old_manifest) == frozen_hash
        report.update({"status": "pass", "exit_code": 0,
                       "kernel_results": kernel_results,
                       "same_position_kernel_controls": same_position_controls,
                       "original_word_comparisons": len(comparison_rows),
                       "uniform_cases": sum(c[-1] is None for c in cases),
                       "fixed_a_cases": sum(c[-1] is not None for c in cases),
                       "inserted_moment_comparisons": sum(len(row["inserted_moments"]) for row in comparison_rows),
                       "comparisons": comparison_rows,
                       "phase_order_negative_control": {"n": 3, "r": 0, "q": 0, "i": 0,
                                                         "correct": "1", "incorrect_D_P": str(wrong_phase)},
                       "frozen_old_files_and_manifest_unchanged": True})
    except Exception as exc:
        report.update({"status": "failed", "exit_code": 1, "error": repr(exc)})
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (HERE / "matrix_spec_run.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in
                      ("status", "kernel_results", "same_position_kernel_controls", "original_word_comparisons",
                       "uniform_cases", "fixed_a_cases", "inserted_moment_comparisons", "phase_order_negative_control",
                       "frozen_old_files_and_manifest_unchanged")}, indent=2))


if __name__ == "__main__":
    main()
