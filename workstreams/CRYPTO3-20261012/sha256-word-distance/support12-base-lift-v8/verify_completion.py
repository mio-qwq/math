#!/usr/bin/env python3
"""Definition-based validation of the support-12 base chart."""
import hashlib
import json
from pathlib import Path
import platform
import random
import sys

import base_completion as candidate

MASK = (1 << 32) - 1


def sigma_bits(word, a, b, shift):
    bits = [(word >> j) & 1 for j in range(32)]
    return sum((bits[(j + a) % 32] ^ bits[(j + b) % 32]
                ^ (bits[j + shift] if j + shift < 32 else 0)) << j
               for j in range(32))


def raw_residuals(words):
    if len(words) != 64 or any(type(x) is not int or not 0 <= x <= MASK for x in words):
        raise ValueError("word shape")
    return {
        t: (words[t] - sigma_bits(words[t - 2], 17, 19, 10) - words[t - 7]
            - sigma_bits(words[t - 15], 7, 18, 3) - words[t - 16]) & MASK
        for t in range(16, 64)
    }


def expand(message):
    words = list(message)
    if len(words) != 16:
        raise ValueError("message length")
    for t in range(16, 64):
        words.append((sigma_bits(words[t - 2], 17, 19, 10) + words[t - 7]
                      + sigma_bits(words[t - 15], 7, 18, 3)
                      + words[t - 16]) & MASK)
    return words


def digest_words(words):
    return hashlib.sha256(b"".join(w.to_bytes(4, "big") for w in words)).hexdigest()


def structural_check():
    support = {10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57}
    parameters = {9, 12, 14, 19, 22}
    assert set(candidate.SUPPORT) == support
    assert set(candidate.PARAMETERS) == parameters
    assert len(support) == 13 and len(parameters) == 5 and not support & parameters
    known = support | parameters
    used = set()
    for t, target in candidate.ORDER:
        assert 16 <= t < 64 and t not in used
        positions = {t, t - 2, t - 7, t - 15, t - 16}
        assert positions - known == {target}
        assert target not in known
        known.add(target)
        used.add(t)
    assert known == set(range(64))
    assert len(used) == 46
    assert set(range(16, 64)) - used == set(candidate.RESIDUAL_INDICES)
    # Direct definition checks for both computed inverses.
    for j in range(32):
        bit = 1 << j
        assert candidate.sigma0(candidate.INV0(bit)) == bit
        assert candidate.sigma1(candidate.INV1(bit)) == bit
    return used


def main():
    used = structural_check()
    rng = random.Random(0x12BA5E08)
    fixtures = [
        [j + 1 for j in range(16)],
        [MASK - j for j in range(16)],
        [(1 << 31) ^ (1 << j) for j in range(16)],
        [((0x9E3779B9 * (j + 1)) ^ 0xA5A55A5A) & MASK for j in range(16)],
    ]
    fixtures.extend([[rng.getrandbits(32) for _ in range(16)] for _ in range(12)])
    rows = []
    for message in fixtures:
        expected = expand(message)
        active = {i: expected[i] for i in candidate.SUPPORT}
        parameters = {i: expected[i] for i in candidate.PARAMETERS}
        actual, residuals = candidate.complete(active, parameters)
        direct = raw_residuals(actual)
        assert actual == expected
        assert not any(direct.values()) and not any(residuals.values())
        assert residuals == {t: direct[t] for t in candidate.RESIDUAL_INDICES}
        rows.append({"all_64_words_equal": True,
                     "all_48_rows_zero": True,
                     "schedule_sha256": digest_words(actual)})

    # Mutating one prescribed active word keeps all 46 constructed rows but
    # is rejected by at least one of the two untouched original rows.
    original = expand(fixtures[0])
    active = {i: original[i] for i in candidate.SUPPORT}
    parameters = {i: original[i] for i in candidate.PARAMETERS}
    active[10] ^= 1
    damaged, residuals = candidate.complete(active, parameters)
    direct = raw_residuals(damaged)
    assert not any(direct[t] for t in used)
    assert any(residuals.values())
    assert residuals == {t: direct[t] for t in candidate.RESIDUAL_INDICES}
    assert all(damaged[i] == active[i] for i in active)
    assert all(damaged[i] == parameters[i] for i in parameters)

    # Corrupting a constructed coordinate destroys a used original row.
    corrupted = list(original)
    corrupted[31] ^= 1
    corrupted_rows = raw_residuals(corrupted)
    assert any(corrupted_rows[t] for t in used)

    report = {
        "schema": "sha256-support12-base-lift-verification-v8",
        "status": "PASS",
        "source_definition": "FIPS 180-4 equations 4.6, 4.7 and Section 6.2.2",
        "candidate_sha256": hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version,
        "platform": platform.platform(),
        "used_original_rows": len(used),
        "residual_indices": candidate.RESIDUAL_INDICES,
        "roundtrips": rows,
        "negative_controls": {
            "damaged_active_10": {
                "all_46_constructed_rows_zero": True,
                "nonzero_residuals": [t for t, value in residuals.items() if value],
            },
            "corrupted_constructed_31": {
                "rejected_used_rows": [t for t in sorted(used) if corrupted_rows[t]],
            },
        },
        "scope": ("exact base-chart implementation checks; no active-pair "
                  "witness, no automatic residual solvability, no distance bound"),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

