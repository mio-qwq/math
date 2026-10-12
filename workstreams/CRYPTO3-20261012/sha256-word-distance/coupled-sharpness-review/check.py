#!/usr/bin/env python3
"""Independent, read-only FIPS bit-source verification of four local words."""

import argparse
import hashlib
import json
from pathlib import Path
import platform


MOD = 1 << 32
MASK = MOD - 1
WORDS = (0x0019F0ED, 0x973448ED, 0xDFF7F75F, 0x77124F5F)
CLAIMED_D = 0x971A5800


def sigma_bits(word, rotate_a, rotate_b, shift):
    """Directly construct each output bit; do not implement word rotations."""
    answer = 0
    for output_bit in range(32):
        a = (word >> ((output_bit + rotate_a) % 32)) & 1
        b = (word >> ((output_bit + rotate_b) % 32)) & 1
        c = ((word >> (output_bit + shift)) & 1) if output_bit + shift < 32 else 0
        answer |= (a ^ b ^ c) << output_bit
    return answer


def valuation(nonzero_residue):
    if not 0 < nonzero_residue < MOD:
        raise ValueError("valuation requires a nonzero canonical residue")
    return (nonzero_residue & -nonzero_residue).bit_length() - 1


def evaluate(words, f_parameters=(7, 18, 3), g_parameters=(17, 19, 10)):
    if len(words) != 4 or any(type(w) is not int or not 0 <= w < MOD for w in words):
        raise ValueError("expected four canonical 32-bit words")
    p, pp, q, qp = words
    fp, fpp, fq, fqp = [sigma_bits(w, *f_parameters) for w in words]
    gp, gpp, gq, gqp = [sigma_bits(w, *g_parameters) for w in words]
    d_p, d_q = (pp - p) % MOD, (qp - q) % MOD
    f_p, f_q, g_q = (fpp - fp) % MOD, (fqp - fq) % MOD, (gqp - gq) % MOD
    return {
        "words": dict(zip(("p", "p_prime", "q", "q_prime"), words)),
        "f_words": dict(zip(("p", "p_prime", "q", "q_prime"), (fp, fpp, fq, fqp))),
        "g_words": dict(zip(("p", "p_prime", "q", "q_prime"), (gp, gpp, gq, gqp))),
        "residues": {
            "d_p": d_p, "d_q": d_q, "minus_D": (-d_p) % MOD,
            "F_p": f_p, "F_q": f_q, "G_q": g_q,
            "h_q": (q + gq) % MOD, "h_q_prime": (qp + gqp) % MOD,
            "p_prime_plus_q": (pp + q) % MOD, "p_plus_q_prime": (p + qp) % MOD,
            "f_prime_sum": (fpp + fqp) % MOD, "f_sum": (fp + fq) % MOD,
            "q_xor_q_prime": q ^ qp,
        },
        "valuation_D": valuation(d_p) if d_p else None,
        "odd_quotient_D": d_p >> valuation(d_p) if d_p else None,
        "f_parameters": list(f_parameters),
        "g_parameters": list(g_parameters),
    }


def validate(words=WORDS, claimed_d=CLAIMED_D, claimed_valuation=11,
             f_parameters=(7, 18, 3), g_parameters=(17, 19, 10)):
    value = evaluate(words, f_parameters, g_parameters)
    r = value["residues"]
    checks = {
        "same_nonzero_difference": r["d_p"] == r["d_q"] != 0,
        "claimed_difference": r["d_p"] == claimed_d,
        "g_difference_cancels_D": (r["G_q"] + r["d_p"]) % MOD == 0,
        "f_differences_cancel": (r["F_p"] + r["F_q"]) % MOD == 0,
        "claimed_valuation": value["valuation_D"] == claimed_valuation,
    }
    failed = [key for key, passed in checks.items() if not passed]
    if failed:
        raise ValueError("failed: " + ", ".join(failed))
    value["checks"] = checks
    return value


def negative_controls():
    controls = []
    for index, name in enumerate(("p", "p_prime", "q", "q_prime")):
        damaged = list(WORDS)
        damaged[index] ^= 1
        controls.append(("flip_bit_0_of_" + name, {"words": tuple(damaged)}))
    controls.extend([
        ("wrong_f_rotation_7_to_6", {"f_parameters": (6, 18, 3)}),
        ("wrong_g_rotation_19_to_18", {"g_parameters": (17, 18, 10)}),
        ("damaged_claimed_D", {"claimed_d": CLAIMED_D ^ 1}),
        ("damaged_claimed_valuation", {"claimed_valuation": 10}),
    ])
    reports = []
    for name, arguments in controls:
        try:
            validate(**arguments)
        except ValueError as error:
            reports.append({"name": name, "rejected": True, "reason": str(error)})
        else:
            raise AssertionError("negative control was accepted: " + name)
    return reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, help="explicitly save the result; default is read-only")
    args = parser.parse_args()
    value = validate()
    for group in ("words", "f_words", "g_words", "residues"):
        value[group] = {key: f"0x{number:08x}" for key, number in value[group].items()}
    report = {
        "status": "PASS",
        "scope": "four local words only; no SHA-256 schedule witness",
        "implementation": "per-output-bit reconstruction from the FIPS 180-4 sigma source indices",
        "python": platform.python_version(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "evaluation": value,
        "negative_controls": negative_controls(),
    }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.record is not None:
        args.record.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
