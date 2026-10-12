#!/usr/bin/env python3
"""Compress discovered XOR row selections into ten small proof families."""

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    source = HERE / "AFFINE_PROBE.json"
    data = json.loads(source.read_text())
    mask_source = HERE / "MASK_PROBE.json"
    mask_data = json.loads(mask_source.read_text())
    groups = defaultdict(list)
    for case in data["cases"]:
        assert case["status"] == "inconsistent"
        counts = Counter((case["rows"][i]["coefficient"], case["rows"][i]["rhs"])
                         for i in case["selected_rows"])
        signature = tuple(sorted(key for key, count in counts.items() if count % 2))
        coefficient = rhs = 0
        for row, value in signature:
            coefficient ^= int(row, 16)
            rhs ^= value
        assert coefficient == 0 and rhs == 1
        groups[signature].append(case["A"])
    ordered = sorted(groups.items(), key=lambda item: (len(item[0]), item[1]))
    row_bank = sorted({row for signature in groups for row in signature})
    index = {row: i for i, row in enumerate(row_bank)}
    families = [{"id": i, "mask_count": len(masks), "masks": masks,
                 "row_ids": [index[row] for row in signature]}
                for i, (signature, masks) in enumerate(ordered)]
    assert len(row_bank) == 26 and len(families) == 10
    assert sum(family["mask_count"] for family in families) == 132
    certificate = {
        "schema": "CRYPTO3-fixed-K-coupled-affine-certificate-v1",
        "status": "candidate second proof; independent-agent review recorded separately",
        "definition": {"word_bits": 32, "f_rotations": [7, 18], "f_shift": 3,
                       "g_rotations": [17, 19], "g_shift": 10,
                       "K": "fbca7000", "f_K": "828ee412", "g_K": "763e9000"},
        "equations": ["q+g(q)=q_prime+g(q_prime)",
                      "p_prime+q=p+q_prime", "f(p_prime)+f(q_prime)=f(p)+f(q)"],
        "mask_reconstruction": {"q_prime": "q xor K", "p_prime": "p xor A"},
        "signed_derivative_coefficients": {"h_q": [1, 1], "equal_input_derivatives": [1, -1],
                                           "opposite_sigma0_derivatives": [1, 1]},
        "final_carry": "unrestricted modulo 2^32",
        "necessary_mask_exhaustivity": {
            "fixed_one_bits": [12, 19], "fixed_zero_bits": list(range(12)) + [18],
            "free_bits": list(range(13, 18)) + list(range(20, 32)),
            "assignments": 131072, "after_input_obstruction": 24576,
            "after_both_obstructions": 132,
            "survivor_mask_sha256": mask_data["survivor_mask_sha256"]},
        "carry_table_cases": data["carry_truth_tables"],
        "row_encoding": "64 variables: p bit i at coefficient bit i; q bit i at coefficient bit 32+i; rhs in F2",
        "row_bank": [{"id": i, "coefficient": coefficient, "rhs": rhs,
                      "p_bits": [j for j in range(32) if int(coefficient, 16) >> j & 1],
                      "q_bits": [j for j in range(32) if int(coefficient, 16) >> (32+j) & 1]}
                     for i, (coefficient, rhs) in enumerate(row_bank)],
        "families": families,
        "scope": "No solution of the stated three local equations for fixed K; not a complete message-schedule exclusion by itself.",
        "discovery_provenance_not_premises": {
            "AFFINE_PROBE.json": hashlib.sha256(source.read_bytes()).hexdigest(),
            "MASK_PROBE.json": hashlib.sha256(mask_source.read_bytes()).hexdigest()},
    }
    path = HERE / "CERTIFICATE.json"
    path.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({"certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "bytes": path.stat().st_size, "families": 10, "row_bank": 26,
                      "masks": 132, "template_row_occurrences": sum(len(f["row_ids"]) for f in families)}, indent=2))


if __name__ == "__main__":
    main()
