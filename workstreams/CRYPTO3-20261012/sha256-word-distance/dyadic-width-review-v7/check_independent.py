#!/usr/bin/env python3
"""Read-only independent dyadic row/range/lift checks; no solver or author code."""
import hashlib
import json
from pathlib import Path

N = 1 << 32
L = 1 << 22
MASK = N-1


def need(condition, why):
    if not condition:
        raise ValueError(why)


def g(word):
    def rotate(amount):
        return ((word >> amount) | (word << (32-amount))) & MASK
    return rotate(17) ^ rotate(19) ^ (word >> 10)


def v2(word):
    need(0 < word < N, "nonzero residue for valuation")
    return (word & -word).bit_length()-1


def rows():
    basis = [g(1 << j) for j in range(32)]
    return [sorted(i for i in range(32) if (basis[i] >> j) & 1) for j in range(32)]


def verify_rows(matrix, k, stable_begin=22, top_indices=None):
    for j in range(stable_begin, k+13):
        need(matrix[j] == [j-15, j-13] and all(i < k for i in matrix[j]),
             "fixed-row exact dependency")
    need(matrix[k+13] == ([k-2, k] if top_indices is None else top_indices),
         "common parity row")


def check_pair(before, difference, k):
    modulus = 1 << (k+14)
    half = modulus >> 1
    after = (before+difference) % N
    low_difference = (g(after) & (L-1)) - (g(before) & (L-1))
    derivative = (g(after)-g(before)) % N
    need(abs(low_difference) < L, "ordinary low22 range")
    need(derivative % modulus == (half+low_difference) % modulus,
         "actual common-half decomposition")
    reversed_difference = (g(before)-g(after)) % N
    need(reversed_difference % modulus == (half-low_difference) % modulus,
         "actual reversal common-half decomposition")


def require_zero_multiple_bound(k, bound):
    need(bound < (1 << (k+14)), "bound cannot exclude nonzero modulus multiple")


def main():
    matrix = rows()
    for j in range(32):
        original = [(j+17) % 32, (j+19) % 32]
        if j < 22:
            original.append(j+10)
        need(matrix[j] == sorted(original), "all FIPS rows")
    budgets = []
    pair_checks = 0
    lift_checks = 0
    for k in range(9, 19):
        verify_rows(matrix, k)
        modulus = 1 << (k+14)
        lifts = N // modulus
        qmax = (1 << (22-k))-1
        candidates = {1, 3, qmax}
        hs = {0, min(1, lifts-1), lifts-1}
        for q in candidates:
            for h in hs:
                for sign in (-1, 1):
                    difference = (sign*q*(1 << k)+h*modulus) % N
                    need(v2(difference) == k, "exact-valuation lift")
                    reverse = (-difference) % N
                    need(reverse == (-sign*q*(1 << k)+((-h) % lifts)*modulus) % N,
                         "full residue lift reversal")
                    lift_checks += 1
                    for base in (0, 0xffffffff, 0xdeadbeef):
                        check_pair(base, difference, k)
                        pair_checks += 1
        # A=qY-qR, B=qY-qX. The exact coefficient vector, in X,Y,R order,
        # is (-1,-1,+2), not a sum of independent A/B interval bounds.
        a = [0, 1, -1]
        b = [-1, 1, 0]
        combination = [b[j]-2*a[j] for j in range(3)]
        need(combination == [-1, -1, 2], "shared-output coefficient identity")
        maximum = sum(abs(c) for c in combination)*(L-1)
        need(maximum == 4*(L-1), "sharp joint representative norm")
        if k >= 10:
            require_zero_multiple_bound(k, maximum)
        signed_count = 2*(1 << (21-k))*lifts
        original_stratum = 1 << (31-k)
        need(signed_count*(1 << (k-9)) == original_stratum,
             "lift-budget reduction fraction")
        budgets.append({"k": k, "modulus": modulus, "top_row": matrix[k+13],
                        "positive_odd_q_count": 1 << (21-k), "q_max": qmax,
                        "h_count": lifts, "signed_lift_count": signed_count,
                        "original_valuation_stratum_count": original_stratum,
                        "B_minus_2A_forced_zero_by_joint_bound": k >= 10})
    # k9 permits a nonzero multiple. This tuple is representative integers
    # only, not a six-word core witness.
    qx, qy, qr = 0, -1024, L-512
    a, b, modulus = qy-qr, qy-qx, 1 << 23
    d = a % modulus
    need(all(abs(q) < L for q in (qx, qy, qr)), "k9 integer representative range")
    need(b-2*a == modulus and b % modulus == 2*d % modulus and v2(d) == 9,
         "k9 nonzero multiple example")
    need(abs(a) > L, "k9 integer width inference fails")
    # k8's proposed top output row is not forced by its input difference.
    top_changes = [((g(before) ^ g((before+256) % N)) >> 21) & 1
                   for before in (0, N-256)]
    need(matrix[21] == [6, 8, 31] and top_changes == [1, 0],
         "k8 common-parity boundary")
    rejected = []
    def reject(label, function):
        try:
            function()
        except ValueError as error:
            rejected.append({"control": label, "rejected_by": str(error)})
        else:
            raise ValueError("malformed control accepted")
    reject("include SHR-bearing row21 as fixed at k10", lambda: verify_rows(matrix, 10, 21))
    reject("move k18 parity input18 to17", lambda: verify_rows(matrix, 18, top_indices=[16, 17]))
    reject("use 3*2^23 coarse bound at k10", lambda: require_zero_multiple_bound(10, 3*(1 << 23)))
    reject("force zero multiple with same bound at k9", lambda: require_zero_multiple_bound(9, 4*(L-1)))
    print(json.dumps({"schema": "CRYPTO3-independent-dyadic-width-check-v7",
                      "accepted_finite_dependencies": True,
                      "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "all_g_output_rows": matrix,
                      "nontrivial_joint_width_k_range": list(range(10, 19)),
                      "common_half_decomposition_k_range": list(range(9, 19)),
                      "case_budgets": budgets,
                      "lift_boundary_fixtures_checked": lift_checks,
                      "actual_pair_decompositions_and_reversals_checked": pair_checks,
                      "sample_scope": "Implementation checks only; none is asserted to satisfy the full three-pair core.",
                      "k9_counterexample_scope": "Representative integer obstruction to B=2A inference only.",
                      "k9_counterexample": {"qx": qx, "qy": qy, "qr": qr, "A": a, "B": b,
                                            "B_minus_2A": modulus, "D_mod_M": d},
                      "k9_final_formula": "Vacuous: covers its complete exact-valuation stratum.",
                      "k8_top_row": matrix[21], "k8_actual_top_changes": top_changes,
                      "rejected_controls": rejected}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
