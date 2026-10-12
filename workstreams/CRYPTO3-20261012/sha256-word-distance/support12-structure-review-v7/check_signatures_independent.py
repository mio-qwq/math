#!/usr/bin/env python3
"""Blind independent construction: all sigma0 valuation signatures.

No author-v7 files are opened. No solver or word/message enumeration is used.
--save writes only the independent table and receipt in this directory.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUPPORTS = HERE.parent / "shift-reduction-v3" / "supports-v2.json"
PINNED_SUPPORTS = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"
MASK = (1 << 32) - 1


def sigma_rows():
    result = []
    for output_bit in range(32):
        row = (1 << ((output_bit + 7) % 32)) ^ (1 << ((output_bit + 18) % 32))
        if output_bit + 3 < 32:
            row ^= 1 << (output_bit + 3)
        result.append(row)
    return result


def direct_f(x):
    r7 = ((x >> 7) | (x << 25)) & MASK
    r18 = ((x >> 18) | (x << 14)) & MASK
    return r7 ^ r18 ^ (x >> 3)


def evaluate_rows(rows, x):
    return sum(((row & x).bit_count() % 2) << bit for bit, row in enumerate(rows))


def constraints(k, l, rows):
    return ([(1 << i, 0) for i in range(k)] + [(1 << k, 1)] +
            [(rows[i], 0) for i in range(l)] + [(rows[l], 1)])


def solve_binary(equations):
    basis = {}
    for i, (source_row, source_rhs) in enumerate(equations):
        row, rhs, provenance = source_row, source_rhs, 1 << i
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (row, rhs, provenance)
                break
            b, value, origin = basis[pivot]
            row ^= b
            rhs ^= value
            provenance ^= origin
        if row == 0 and rhs == 1:
            return {"feasible": False, "contradicting_row_combination": provenance}
    witness = 0
    for pivot in sorted(basis):
        row, rhs, _ = basis[pivot]
        if (row & witness).bit_count() % 2 != rhs:
            witness |= 1 << pivot
    return {"feasible": True, "xor_mask_witness": witness}


def rank(rows):
    basis = {}
    for row in rows:
        while row:
            pivot = row.bit_length()-1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return len(basis)


def homogeneous_form_check(k, l, rows):
    # On the kernel of H, two nonzero binary forms can simultaneously be 1:
    # their joint image is either <(1,1)> or the full two-dimensional space.
    H = [1 << i for i in range(k)] + rows[:l]
    r = rank(H)
    return rank(H + [1 << k]) > r and rank(H + [rows[l]]) > r


def original_rows(support):
    result = {}
    for t in range(16, 64):
        row = {}
        for kind, i, coefficient in (("d", t, 1), ("G", t-2, -1), ("d", t-7, -1),
                                      ("F", t-15, -1), ("d", t-16, -1)):
            if i in support:
                key = kind + str(i)
                row[key] = row.get(key, 0) + coefficient
        result[t] = {key: value for key, value in row.items() if value}
    return result


def combo(rows, coefficients):
    result = {}
    for t, coefficient in coefficients.items():
        for key, value in rows[int(t)].items():
            result[key] = result.get(key, 0) + coefficient*value
    return {key: value for key, value in result.items() if value}


def independent_bridges(support):
    rows = original_rows(support)
    assert all(i in support for i in (13, 18, 26, 34, 43))
    identities = [
        ({33: -1}, {"d26": 1, "F18": 1}),
        ({41: -1, 34: -1}, {"F26": 1, "d18": 1}),
        ({34: 1}, {"d34": 1, "d18": -1}),
        ({49: -1, 42: -1, 33: 1}, {"F34": 1, "F18": -1}),
        ({20: -1, 27: -1, 18: 1}, {"G18": 1, "d13": 1, "d18": 1}),
        ({36: -1, 29: -1, 27: 1, 18: -1}, {"G34": 1, "d13": 1, "d18": -1}),
        ({50: -1, 34: -1}, {"d43": 1, "d18": 1}),
        ({58: -1, 42: -1, 33: 1}, {"F43": 1, "F18": -1}),
        ({45: -1, 29: -1}, {"G43": 1, "d13": 1}),
    ]
    for coefficients, target in identities:
        assert combo(rows, coefficients) == target
    return [{"original_rows": coefficients, "target": target} for coefficients, target in identities]


def build_packet():
    source = SUPPORTS.read_bytes()
    assert hashlib.sha256(source).hexdigest() == PINNED_SUPPORTS
    support = json.loads(source)["supports"][12]
    f_rows = sigma_rows()
    assert all(evaluate_rows(f_rows, 1 << i) == direct_f(1 << i) for i in range(32))
    certificates = [[solve_binary(constraints(k, l, f_rows)) for l in range(32)]
                    for k in range(32)]
    forward = [[certificates[k][l]["feasible"] for l in range(32)] for k in range(32)]
    anti = [[forward[k][l] and forward[l][k] for l in range(32)] for k in range(32)]
    return {"schema": "independent-support12-sigma0-signatures-v7",
            "source_support_sha256": PINNED_SUPPORTS, "support_index": 12,
            "original_f_binary_rows": f_rows, "recurrence_bridges": independent_bridges(support),
            "signature_certificates": certificates, "forward_signature_table": forward,
            "anti_cycle_necessary_table": anti,
            "scope": "All sigma0 XOR-mask signatures exactly; anti-cycle signature compatibility is only necessary for actual coupled pair equations."}


def verify_packet(packet):
    assert packet["schema"] == "independent-support12-sigma0-signatures-v7"
    assert packet["source_support_sha256"] == PINNED_SUPPORTS
    assert packet["support_index"] == 12
    support = json.loads(SUPPORTS.read_text())["supports"][12]
    assert packet["recurrence_bridges"] == json.loads(json.dumps(independent_bridges(support)))
    rows = sigma_rows()
    assert packet["original_f_binary_rows"] == rows
    certificates = packet["signature_certificates"]
    assert len(certificates) == 32 and all(len(row) == 32 for row in certificates)
    table = [[False]*32 for _ in range(32)]
    for k in range(32):
        for l in range(32):
            equations = constraints(k, l, rows)
            cert = certificates[k][l]
            assert type(cert["feasible"]) is bool
            if cert["feasible"]:
                word = cert["xor_mask_witness"]
                assert type(word) is int and 0 < word <= MASK
                assert all((row & word).bit_count() % 2 == rhs for row, rhs in equations)
                image = direct_f(word)
                assert image != 0
                assert (word & -word).bit_length()-1 == k
                assert (image & -image).bit_length()-1 == l
                table[k][l] = True
            else:
                combination = cert["contradicting_row_combination"]
                assert type(combination) is int and 0 < combination < 1 << len(equations)
                left = right = 0
                for i, (row, rhs) in enumerate(equations):
                    if combination >> i & 1:
                        left ^= row
                        right ^= rhs
                assert left == 0 and right == 1  # Exact original-row proof of 0=1.
            assert homogeneous_form_check(k, l, rows) == table[k][l]
    assert packet["forward_signature_table"] == table
    anti = [[table[k][l] and table[l][k] for l in range(32)] for k in range(32)]
    assert packet["anti_cycle_necessary_table"] == anti
    allowed = [(k, l) for k in range(32) for l in range(32) if anti[k][l]]
    assert sum(map(sum, table)) == 417 and len(allowed) == 309
    assert all(k+l <= 30 and k <= 23 and l <= 23 for k, l in allowed)
    assert [(k, l) for k, l in allowed if l >= 18] == [(i, i+18) for i in range(6)]
    return {"forward_signatures": 417, "verified_original_row_infeasibility_proofs": 607,
            "anti_cycle_necessary_signatures": 309, "systems_checked": 1024,
            "homogeneous_form_method_agreements": 1024,
            "max_k_plus_l": max(k+l for k, l in allowed),
            "max_k": max(k for k, l in allowed), "max_l": max(l for k, l in allowed),
            "l_at_least_18_cases": [[k, l] for k, l in allowed if l >= 18],
            "original_48_row_bridge_identities": 9}


def negative_controls(packet):
    bad_cell = next((k, l) for k in range(32) for l in range(32)
                    if not packet["signature_certificates"][k][l]["feasible"])
    controls = [
        ("wrong_sigma_row", lambda p: p["original_f_binary_rows"].__setitem__(0, 1)),
        ("zero_feasible_witness", lambda p: p["signature_certificates"][0][0].update(xor_mask_witness=0)),
        ("zero_infeasible_row_combination", lambda p: p["signature_certificates"][bad_cell[0]][bad_cell[1]].update(contradicting_row_combination=0)),
        ("false_anti_cycle_cell", lambda p: p["anti_cycle_necessary_table"][24].__setitem__(6, True)),
        ("false_forward_cell", lambda p: p["forward_signature_table"][0].__setitem__(0, False)),
        ("wrong_anti_cycle_bridge_sign", lambda p: p["recurrence_bridges"][0]["target"].update(F18=-1)),
    ]
    rejected = []
    for name, mutation in controls:
        damaged = copy.deepcopy(packet)
        mutation(damaged)
        try:
            verify_packet(damaged)
        except (AssertionError, KeyError):
            rejected.append(name)
        else:
            raise AssertionError("damaged signature evidence accepted: " + name)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    packet = json.loads(json.dumps(build_packet()))
    if not args.save and (HERE / "SIGNATURES.json").exists():
        frozen = json.loads((HERE / "SIGNATURES.json").read_text())
        assert frozen == packet
    run = {"status": "PASS", "stage": "blind independent construction before author-v7 read",
           "results": verify_packet(packet), "negative_controls_rejected": negative_controls(packet),
           "reviewer_checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "source_support_sha256": PINNED_SUPPORTS,
           "scope": "Necessary anti-cycle valuation constraints only; not actual-pair sufficiency, complete message realizability, or support exclusion."}
    if args.save:
        (HERE / "SIGNATURES.json").write_text(json.dumps(packet, indent=2, sort_keys=True)+"\n")
        (HERE / "INDEPENDENT_RUN.json").write_text(json.dumps(run, indent=2, sort_keys=True)+"\n")
    print(json.dumps(run, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
