#!/usr/bin/env python3
"""Read-only independent row and actual-pair checks; standard library only."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 1 << 32
H = 1 << 31
K = 1 << 18
L = 1 << 22
MASK = N - 1


def need(ok, why):
    if not ok:
        raise ValueError(why)


def g(word):
    need(type(word) is int and 0 <= word < N, "unsigned actual word")
    def ror(amount):
        return ((word >> amount) | (word << (32-amount))) & MASK
    return ror(17) ^ ror(19) ^ (word >> 10)


def rows_from_basis():
    columns = [g(1 << bit) for bit in range(32)]
    return [sorted(bit for bit in range(32) if (columns[bit] >> row) & 1)
            for row in range(32)]


def validate_rows(claim):
    rows = rows_from_basis()
    for j in range(32):
        expected = [(j+17) % 32, (j+19) % 32]
        if j+10 < 32:
            expected.append(j+10)
        need(rows[j] == sorted(expected), "full FIPS output row")
    for j in range(claim["stable_begin"], claim["stable_end"] + 1):
        need(all(i < 18 for i in rows[j]), "stable output depends on high input")
        need(rows[j] == [j-15, j-13], "stable two-index identity")
    need(rows[31] == claim["top_indices"], "top row input indices")
    need(claim["top_indices"] == [16, 18], "top row parity dependency")
    return rows


def decompose(pair, expected_difference):
    before, after = pair
    need((after-before) % N == expected_difference % N, "actual pair difference")
    need(expected_difference % K == 0, "18-bit divisibility")
    e = (expected_difference // K) & 1
    left, right = g(before), g(after)
    need(((left ^ right) >> 22) & 0x1ff == 0, "bits 22 through 30 fixed")
    need(((left ^ right) >> 31) == e, "top-bit common parity")
    q = (right & (L-1)) - (left & (L-1))
    need(abs(q) < L, "low22 ordinary difference range")
    derivative = (right-left) % N
    need(derivative == (e*H+q) % N, "common halfword decomposition")
    return e, q, derivative


def check_three_pairs(pairs, difference):
    x, y, r = pairs
    data = [decompose(x, difference), decompose(y, difference),
            decompose(r, -difference)]
    need(len({item[0] for item in data}) == 1, "three pair parities agree")
    _, qx, gx = data[0]
    _, qy, gy = data[1]
    _, qr, gr = data[2]
    a, b = qy-qr, qy-qx
    need((gy-gr) % N == a % N and (gy-gx) % N == b % N,
         "common H cancels in actual gaps")
    need(abs(a) < 2*L and abs(b) < 2*L, "gap representative range")
    return a, b, data


def validate_integer_bound(claim):
    need(claim["low_width"] == 22, "low-output width")
    need(claim["multiple_bound"] == 3*(1 << 23), "B-minus-2A bound")
    need(claim["multiple_bound"] < N, "unique multiple of N in bound")
    actual_q = [q for q in range(1, 17) if q*K < L]
    need(claim["positive_quotients"] == actual_q == list(range(1, 16)),
         "strict final integer range")


def actual_pair_checks():
    # These triples retain real word values and modular wrap. They test
    # decompositions and reversal; no triple is asserted to satisfy the
    # lemma's two extra gap hypotheses or an actual schedule.
    quotients = list(range(1, 18)) + [31, 32, 127, 128, 8191, 8192]
    bases = [0, 0xffffffff, 0x01234567, 0x7ffc0000, 0x8003ffff, 0xdeadbeef]
    triples = 0
    reversed_triples = 0
    full_gap_hits = 0
    for quotient in quotients:
        for orientation in (-1, 1):
            difference = (orientation*quotient*K) % N
            for j in range(len(bases)):
                a, b, c = bases[j], bases[(j+1) % len(bases)], bases[(j+3) % len(bases)]
                pairs = ((a, (a+difference) % N), (b, (b+difference) % N),
                         (c, (c-difference) % N))
                aa, bb, data = check_three_pairs(pairs, difference)
                reverse = tuple((after, before) for before, after in pairs)
                ar, br, reverse_data = check_three_pairs(reverse, (-difference) % N)
                need(ar == -aa and br == -bb, "integer gap reversal")
                for original, reversed_pair in zip(data, reverse_data):
                    e, q, derivative = original
                    er, qr, derivative_r = reversed_pair
                    need(er == e and qr == -q and derivative_r == (-derivative) % N,
                         "actual derivative reversal")
                if bb % N == 2*difference % N and aa % N == difference:
                    need(bb == 2*aa and abs(aa) < L and aa % K == 0 and aa != 0,
                         "conditional lemma in actual triple")
                    full_gap_hits += 1
                triples += 1
                reversed_triples += 1
    return {"actual_three_pair_triples": triples,
            "their_reversed_triples": reversed_triples,
            "ordered_pair_decompositions": 3*(triples+reversed_triples),
            "matched_full_gap_hypotheses": full_gap_hits,
            "scope": "Tests of actual-pair identities and reversal, not a feasibility or quantified proof by samples."}


def main():
    claim = {"stable_begin": 22, "stable_end": 30, "top_indices": [16, 18],
             "low_width": 22, "multiple_bound": 3*(1 << 23),
             "positive_quotients": list(range(1, 16))}
    rows = validate_rows(claim)
    validate_integer_bound(claim)
    pairs = actual_pair_checks()
    controls = []
    def reject(name, modified, checker):
        try:
            checker(modified)
        except ValueError as error:
            controls.append({"control": name, "rejected_by": str(error)})
        else:
            raise ValueError("negative control accepted")
    bad = copy.deepcopy(claim)
    bad["stable_begin"] = 21
    reject("include output bit 21 in fixed range", bad, validate_rows)
    bad = copy.deepcopy(claim)
    bad["stable_end"] = 31
    reject("declare top output bit fixed", bad, validate_rows)
    bad = copy.deepcopy(claim)
    bad["top_indices"] = [16, 17]
    reject("move top parity input from bit18 to bit17", bad, validate_rows)
    bad = copy.deepcopy(claim)
    bad["positive_quotients"].append(16)
    reject("replace strict q ceiling15 by16", bad, validate_integer_bound)
    result = {"schema": "CRYPTO3-independent-width18-review-v5",
              "accepted_finite_dependencies": True,
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "all_output_rows": rows,
              "high_fixed_rows": list(range(22, 31)),
              "top_row": rows[31], "claim": claim,
              "actual_pair_checks": pairs, "rejected_controls": controls,
              "proof_scope": "Independent written modular/integer proof in REVIEW.md plus direct row and actual-pair implementation checks; not Lean."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
