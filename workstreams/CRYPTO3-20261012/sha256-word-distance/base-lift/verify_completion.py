#!/usr/bin/env python3
"""Definition-based replay of the base-completion parametrization.

This is separate implementation checking by the same researcher, not a
claim that the parametrization has received independent-agent review.
"""
import hashlib
import json
from pathlib import Path

import base_completion as candidate


def sigma_bits(word, a, b, shift):
    bits = [(word >> j) & 1 for j in range(32)]
    return sum((bits[(j + a) % 32] ^ bits[(j + b) % 32]
                ^ (bits[j + shift] if j + shift < 32 else 0)) << j for j in range(32))


def raw_residuals(words):
    if len(words) != 64 or any(type(x) is not int or not 0 <= x < 2 ** 32 for x in words):
        raise ValueError("word shape")
    return {t: (words[t] - sigma_bits(words[t - 2], 17, 19, 10) - words[t - 7]
                - sigma_bits(words[t - 15], 7, 18, 3) - words[t - 16]) % (2 ** 32)
            for t in range(16, 64)}


def expand(message):
    words = list(message)
    assert len(words) == 16
    for t in range(16, 64):
        words.append((sigma_bits(words[t - 2], 17, 19, 10) + words[t - 7]
                      + sigma_bits(words[t - 15], 7, 18, 3) + words[t - 16]) % (2 ** 32))
    return words


def digest_words(words):
    return hashlib.sha256(b"".join(w.to_bytes(4, "big") for w in words)).hexdigest()


def structural_check():
    support = {2, 9, 10, 16, 23, 24, 30, 37, 38, 44, 51, 52, 58}
    params = {0, 1, 3, 4, 5, 7, 8, 11, 12, 15, 29, 43, 57}
    assert set(candidate.SUPPORT) == support
    assert set(candidate.PARAMETERS) == params
    assert len(params) == len(support) == 13 and not params & support
    known = params | support
    used = set()
    for t, target in candidate.ORDER:
        assert 16 <= t < 64 and t not in used
        variables = {t, t - 2, t - 7, t - 15, t - 16}
        assert variables - known == {target}
        assert target not in known
        known.add(target)
        used.add(t)
    assert known == set(range(64))
    assert len(used) == 38
    assert set(range(16, 64)) - used == set(candidate.RESIDUAL_INDICES)
    return used


def main():
    used = structural_check()
    # These fixtures exercise nonzero words, high bits, signed wraparound,
    # and varying carries.  They are single-base round trips, not sparse pairs.
    fixtures = [
        [j + 1 for j in range(16)],
        [(2 ** 32 - 1) - j for j in range(16)],
        [(1 << 31) ^ (1 << j) for j in range(16)],
        [((0x9E3779B9 * (j + 1)) ^ 0xA5A55A5A) % (2 ** 32) for j in range(16)],
    ]
    rows = []
    for message in fixtures:
        expected = expand(message)
        active = {i: expected[i] for i in candidate.SUPPORT}
        parameters = {i: expected[i] for i in candidate.PARAMETERS}
        actual, residuals = candidate.complete(active, parameters)
        assert actual == expected
        check = raw_residuals(actual)
        assert not any(check.values()) and not any(residuals.values())
        assert residuals == {t: check[t] for t in candidate.RESIDUAL_INDICES}
        rows.append({"message": message, "all_64_words_equal": True,
                     "all_48_standard_recurrences_hold": True,
                     "expanded_words_big_endian_sha256": digest_words(actual)})
    # A damaged active anchor still gets interpolated exactly; only the
    # remaining original base equations determine whether it is a schedule.
    original = expand(fixtures[0])
    active = {i: original[i] for i in candidate.SUPPORT}
    parameters = {i: original[i] for i in candidate.PARAMETERS}
    active[16] ^= 1
    damaged, residuals = candidate.complete(active, parameters)
    direct = raw_residuals(damaged)
    assert not any(direct[t] for t in used)
    assert any(direct.values())
    assert all(damaged[i] == active[i] for i in active)
    assert all(damaged[i] == parameters[i] for i in parameters)
    assert residuals == {t: direct[t] for t in candidate.RESIDUAL_INDICES}
    tampered_word = list(original)
    tampered_word[13] ^= 1
    assert any(raw_residuals(tampered_word).values())
    print(json.dumps({
        "schema": "sha256-support0-base-completion-check-v1",
        "passed": True,
        "candidate_sha256": hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_definition": "FIPS 180-4 equations 4.6, 4.7 and Section 6.2.2",
        "structural_order_equations": len(used),
        "residual_indices": candidate.RESIDUAL_INDICES,
        "nonzero_single_base_roundtrips": rows,
        "negative_controls": {
            "damaged_active_anchor": {"all_38_used_equations_hold": True,
                                      "nonzero_residual_indices": [t for t, r in direct.items() if r]},
            "tampered_completed_word": "rejected by direct standard recurrence",
        },
        "scope": "Exact decomposition/evaluator checking; no support-0 pair found or sought; no surjectivity claim",
    }, indent=2))


if __name__ == "__main__":
    main()
