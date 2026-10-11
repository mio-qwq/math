#!/usr/bin/env python3
"""Independent arbitrary-bit/fixed-a correlation checker, exact integer DP.

Only the mathematical specification was supplied by the discovery agent. Its
experiments/ and tooling/ implementation have not been read. Direct word counts
are computed by separate C++ code; existing blind uniform counts are reused.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent


def integer_moment(n: int, i: int, k: int, *, h: int | None = None,
                   l: int | None = None, fixed_a: int | None = None) -> int:
    """Signed count for borrow_i xor borrow_k xor carry_i xor B_h xor Y_l.

    Four states are (borrow, carry) into the current bit, encoded as 2*b+c.
    For uniform a the input letters are independent (S_p,B_p,Y_p), 8 choices.
    For fixed a they are (S_p,Y_p), 4 choices, with B=S-a derived by subtraction.
    Boundary signs are inserted BEFORE the bit at that position is consumed.
    All n positions are processed, including positions whose signs are trivial.
    """
    if n < 1 or not (0 <= i < n and 0 <= k < n):
        raise ValueError("word width and boundaries out of range")
    if (h is None) != (l is None):
        raise ValueError("both Walsh positions must be specified together")
    if h is not None and not (0 <= h < n and 0 <= l < n):
        raise ValueError("Walsh positions out of range")
    if fixed_a is not None and not (0 <= fixed_a < (1 << n)):
        raise ValueError("fixed word out of range")
    counts = [1, 0, 0, 0]
    for pos in range(n):
        following = [0, 0, 0, 0]
        for state, count in enumerate(counts):
            if count == 0:
                continue
            borrow, carry = divmod(state, 2)
            boundary = (borrow if pos == i else 0) ^ (borrow if pos == k else 0)
            boundary ^= carry if pos == i else 0
            for s_bit in (0, 1):
                if fixed_a is None:
                    b_options = (0, 1)
                else:
                    delta = s_bit - ((fixed_a >> pos) & 1) - borrow
                    b_options = (delta & 1,)
                for b_bit in b_options:
                    if fixed_a is None:
                        next_borrow = int(s_bit - b_bit - borrow < 0)
                    else:
                        next_borrow = int(delta < 0)
                    for y_bit in (0, 1):
                        phase = boundary
                        if pos == h:
                            phase ^= b_bit
                        if pos == l:
                            phase ^= y_bit
                        next_carry = int(s_bit + y_bit + carry >= 2)
                        next_state = 2 * next_borrow + next_carry
                        following[next_state] += -count if phase else count
        counts = following
    return sum(counts)


def correlation(n: int, r: int, q: int, i: int,
                fixed_a: int | None = None) -> Fraction:
    if n < 1 or not (0 <= i < n):
        raise ValueError("word width or output bit out of range")
    r %= n
    q %= n
    j = (i - q) % n
    k = (i - r - q) % n
    signed_count = integer_moment(n, i, k, fixed_a=fixed_a)
    for l in range(i):
        h = (l - q) % n
        if h < j:
            signed_count -= (1 << h) * integer_moment(n, i, k, h=h, l=l,
                                                      fixed_a=fixed_a)
    alphabet = 8 if fixed_a is None else 4
    return Fraction(signed_count, (alphabet ** n) * (1 << j))


def exact(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator,
            "fraction": str(value), "decimal_approximation": float(value)}


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(command: list[str], records: list[dict]) -> subprocess.CompletedProcess:
    start = time.perf_counter()
    result = subprocess.run(command, cwd=HERE, text=True, capture_output=True)
    records.append({"argv": command, "cwd": str(HERE), "exit_code": result.returncode,
                    "elapsed_seconds": time.perf_counter() - start,
                    "stdout": result.stdout, "stderr": result.stderr})
    if result.returncode:
        raise RuntimeError(f"Command failed: {command!r}: {result.stderr}")
    return result


def main() -> int:
    records: list[dict] = []
    compiler = os.environ.get("CRYPTO_VERIFY_CXX", "g++")
    source = HERE / "general_fixed_word_enumerator.cpp"
    executable = HERE / "general_fixed_word_enumerator"
    report = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "role": "independent verification agent; no discovery implementation read",
        "model": "n-bit three additions, XOR replacement of all three additions; left rotation",
        "correlation_convention": "E[(-1)^bit_i(w XOR L)]; signed; bias is Cor/2",
        "random_seed": None,
        "randomness_note": "All finite tests exhaust the declared domain; all DP arithmetic is exact.",
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "machine": platform.machine()},
        "source_sha256": {}, "commands": records,
    }
    provenance_paths = [Path(__file__).resolve(), source,
                        HERE / "independent_word_counts.jsonl",
                        HERE.parent / "proofs" / "special_bit_signed_correlation.md"]
    report["source_sha256"] = {str(p): file_hash(p) for p in provenance_paths}
    try:
        version = run_command([compiler, "--version"], records)
        report["environment"]["compiler"] = version.stdout.splitlines()[0]
        run_command([compiler, "-O3", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                     str(source), "-o", str(executable)], records)
        raw = run_command([str(executable)], records)
        fixed_path = HERE / "general_fixed_word_counts.jsonl"
        fixed_path.write_text(raw.stdout)
        # The raw full enumeration is stored in its own file instead of twice.
        records[-1]["stdout"] = f"stored in {fixed_path.name}"
        records[-1]["stdout_sha256"] = file_hash(fixed_path)
        fixed_rows = [json.loads(line) for line in raw.stdout.splitlines()]
        uniform_rows = [json.loads(line) for line in (HERE / "independent_word_counts.jsonl")
                        .read_text().splitlines()]
        uniform_rows = [row for row in uniform_rows if row["kind"] == "exhaustive"]

        comparisons = []
        for row in uniform_rows:
            n, r, q = row["n"], row["r"], row["q"]
            for i, observed in enumerate(row["signed_sums"]):
                expected = Fraction(observed, row["samples"])
                actual = correlation(n, r, q, i)
                comparisons.append({"model": "uniform", "n": n, "r": r, "q": q,
                                    "i": i, "correlation": str(actual), "pass": actual == expected})
                if actual != expected:
                    raise AssertionError(("uniform counterexample", row, i, expected, actual))

        aggregate = defaultdict(lambda: None)
        fixed_by_n = defaultdict(int)
        for row in fixed_rows:
            n, r, q, a = row["n"], row["r"], row["q"], row["a"]
            key = (n, r, q)
            if aggregate[key] is None:
                aggregate[key] = [0] * n
            for i, observed in enumerate(row["signed_sums"]):
                aggregate[key][i] += observed
                expected = Fraction(observed, row["samples"])
                actual = correlation(n, r, q, i, fixed_a=a)
                comparisons.append({"model": "fixed_a", "n": n, "r": r, "q": q,
                                    "a": a, "i": i, "correlation": str(actual),
                                    "pass": actual == expected})
                fixed_by_n[n] += 1
                if actual != expected:
                    raise AssertionError(("fixed-a counterexample", row, i, expected, actual))

        # Averaging the independently enumerated conditional distributions
        # gives another direct uniform count, and covers n=1,2 boundary widths.
        aggregate_comparisons = []
        for (n, r, q), signed_sums in sorted(aggregate.items()):
            for i, signed_sum in enumerate(signed_sums):
                expected = Fraction(signed_sum, 1 << (4 * n))
                actual = correlation(n, r, q, i)
                aggregate_comparisons.append({"n": n, "r": r, "q": q, "i": i,
                                              "pass": actual == expected})
                if actual != expected:
                    raise AssertionError(("conditional-average counterexample", n, r, q, i))

        known = Fraction(-47180567524833621, 1180591620717411303424)
        standard = {"n": 32, "r": 16, "q": 12,
                    "note": "Uniform b,c,d; a either uniform or the stated fixed word. No full-cipher claim.",
                    "uniform_a": [exact(correlation(32, 16, 12, i)) for i in range(32)],
                    "fixed_a": {}}
        for a in (0x61707865, 0x3320646e, 0x79622D32, 0x6B206574):
            standard["fixed_a"][f"0x{a:08x}"] = [exact(correlation(32, 16, 12, i, a))
                                                 for i in range(32)]
        if correlation(32, 16, 12, 28) != known:
            raise AssertionError("standard endpoint disagrees with previously verified fraction")
        standard_path = HERE / "general_standard32_exact.json"
        standard_path.write_text(json.dumps(standard, indent=2) + "\n")

        negative_controls = []
        negative = correlation(3, 1, 1, 2)
        assert negative == Fraction(-3, 16)
        negative_controls.append({"type": "absolute correlation is not signed correlation",
                                  "n": 3, "r": 1, "q": 1, "i": 2,
                                  "correct": str(negative), "incorrect": str(abs(negative)),
                                  "separated": negative != abs(negative)})
        negative_controls.append({"type": "signed bias is half the correlation",
                                  "correct_correlation": str(negative),
                                  "signed_bias": str(negative / 2),
                                  "separated": negative != negative / 2})
        for row in uniform_rows:
            n, r, q = row["n"], row["r"], row["q"]
            found = False
            for i, observed in enumerate(row["signed_sums"]):
                j, k = (i-q) % n, (i-r-q) % n
                incomplete = Fraction(integer_moment(n, i, k), 8**n * 2**j)
                correct = Fraction(observed, row["samples"])
                if correct != incomplete:
                    negative_controls.append({"type": "omitting Walsh correction terms fails",
                                              "n": n, "r": r, "q": q, "i": i,
                                              "correct": str(correct), "incorrect": str(incomplete),
                                              "separated": True})
                    found = True
                    break
            if found:
                break
        assert found
        for row in fixed_rows:
            n, r, q, a = row["n"], row["r"], row["q"], row["a"]
            found = False
            for i, observed in enumerate(row["signed_sums"]):
                correct = Fraction(observed, row["samples"])
                incorrect = correlation(n, r, q, i)
                if correct != incorrect:
                    negative_controls.append({"type": "fixed a cannot be replaced by uniform a",
                                              "n": n, "r": r, "q": q, "i": i, "a": a,
                                              "correct": str(correct), "incorrect": str(incorrect),
                                              "separated": True})
                    found = True
                    break
            if found:
                break
        assert found
        negative_controls.append({"type": "non-wrapping endpoint formula cannot be used at wrapped endpoint",
                                  "n": 3, "r": 1, "q": 2, "i": 0,
                                  "correct_general_formula": str(correlation(3, 1, 2, 0)),
                                  "incorrect_endpoint_formula": "-3/16",
                                  "separated": correlation(3, 1, 2, 0) != Fraction(-3, 16)})

        report.update({"status": "pass", "uniform_parameter_groups": len(uniform_rows),
                       "uniform_bit_comparisons": sum(row["n"] for row in uniform_rows),
                       "fixed_a_parameter_groups": len(fixed_rows),
                       "fixed_a_bit_comparisons": sum(fixed_by_n.values()),
                       "fixed_a_bit_comparisons_by_width": dict(fixed_by_n),
                       "conditional_average_uniform_bit_comparisons": len(aggregate_comparisons),
                       "standard_endpoint": exact(known),
                       "standard_values_file": standard_path.name,
                       "standard_values_sha256": file_hash(standard_path),
                       "negative_controls": negative_controls,
                       "comparisons": comparisons,
                       "conditional_average_comparisons": aggregate_comparisons})
    except Exception as exc:
        report["status"] = "failed"
        report["error"] = repr(exc)
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (HERE / "general_independent_run.json").write_text(json.dumps(report, indent=2) + "\n")
        if executable.exists():
            executable.unlink()
    print(json.dumps({key: report[key] for key in
                      ("status", "uniform_parameter_groups", "uniform_bit_comparisons",
                       "fixed_a_parameter_groups", "fixed_a_bit_comparisons",
                       "fixed_a_bit_comparisons_by_width", "conditional_average_uniform_bit_comparisons",
                       "standard_endpoint", "negative_controls")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
