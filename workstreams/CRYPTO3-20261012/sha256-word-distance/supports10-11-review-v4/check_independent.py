#!/usr/bin/env python3
"""Definition-based independent local review, without author-code imports.

This checks a necessary two-actual-pair core, not full SHA schedules.
Read-only by default; --save writes only into this review directory.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SUPPORTS = BASE / "shift-reduction-v3" / "supports-v2.json"
PINNED = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"
WORD = (1 << 32) - 1


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & WORD


def f(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def g(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def row(t, support):
    terms = [("d", t, 1), ("G", t - 2, -1), ("d", t - 7, -1),
             ("F", t - 15, -1), ("d", t - 16, -1)]
    return {q + str(i): c for q, i, c in terms if i in support}


def combine(rows, coefficients):
    result = {}
    for t, coefficient in coefficients.items():
        for symbol, value in rows[t].items():
            result[symbol] = result.get(symbol, 0) + coefficient * value
    return {symbol: value for symbol, value in result.items() if value}


def derive(supports):
    bridges = []
    for sid, m in ((10, 1), (11, 2)):
        assert 18 in supports[sid]
        rows = {t: row(t, set(supports[sid])) for t in range(16, 64)}
        coefficients = {34: 1, 27: 1, 20: 1}
        if sid == 11:
            coefficients[18] = -1
        assert combine(rows, {33: -1}) == {"d26": 1, "F18": 1}
        assert combine(rows, {41: -1}) == {"d34": 1, "F26": 1}
        assert combine(rows, coefficients) == {"d34": 1, "d18": -m, "G18": -1}
        bridges.append({"support": sid, "m": m, "rows": rows,
                        "B_minus_mA_minus_C": coefficients,
                        "nonzero_requirement": "d18 != 0, since 18 belongs to the support"})
    return bridges


def nullspace(rows):
    """Row RREF, independent of a column-image elimination procedure."""
    rows = list(rows)
    pivots = []
    active = 0
    for bit in range(32):
        found = next((j for j in range(active, len(rows)) if rows[j] >> bit & 1), None)
        if found is None:
            continue
        rows[active], rows[found] = rows[found], rows[active]
        for j in range(len(rows)):
            if j != active and rows[j] >> bit & 1:
                rows[j] ^= rows[active]
        pivots.append(bit)
        active += 1
    reduced = rows[:active]
    basis = []
    for free in range(32):
        if free in pivots:
            continue
        vector = 1 << free
        for pivot, equation in zip(pivots, reduced):
            if equation >> free & 1:
                vector |= 1 << pivot
        assert all((equation & vector).bit_count() % 2 == 0 for equation in rows)
        basis.append(vector)
    return basis, pivots, reduced


def map_rows(transform, width):
    return [sum(((transform(1 << j) >> bit) & 1) << j for j in range(32))
            for bit in range(width)]


def full_span(basis):
    result = [0]
    for vector in basis:
        result += [x ^ vector for x in result]
    assert len(set(result)) == len(result) == 1 << len(basis)
    return sorted(result)


def signed_carry(mask_terms, width=32):
    """Relax all source/output signs independently; retain every modular carry.

    A mask bit contributes either -1 or +1 times its positional weight.
    At one position n active mask terms give {-n,-n+2,...,n}.
    End carry is unrestricted: congruence is modulo 2**width.
    """
    carries = {0}
    trace = []
    for bit in range(width):
        count = sum(mask >> bit & 1 for mask in mask_terms)
        digits = range(-count, count + 1, 2)
        carries = {(carry + digit) // 2 for carry in carries for digit in digits
                   if (carry + digit) % 2 == 0}
        trace.append(sorted(carries))
        if not carries:
            return False, bit, trace
    return True, None, trace


def delta_values(mask, width):
    modulus = (1 << width) - 1
    submask = mask
    values = set()
    while True:
        values.add((mask - 2 * submask) & modulus)
        if submask == 0:
            break
        submask = (submask - 1) & mask
    return values


def signed_carry_controls():
    # All pairs and triples of 3-bit masks checked against full sign enumeration.
    checks = 0
    for a in range(8):
        for b in range(8):
            for c in range(8):
                brute = any((x + y + z) % 8 == 0 for x in delta_values(a, 3)
                            for y in delta_values(b, 3) for z in delta_values(c, 3))
                assert signed_carry([a, b, c], 3)[0] == brute
                checks += 1
    # Top-bit signs coincide modulo 2**32: a nonzero final carry must be allowed.
    assert signed_carry([1 << 31, 1 << 31])[0]
    assert not signed_carry([1, 2])[0]
    return checks


def check_kernel_packet(masks):
    assert len(masks) == 65536
    assert len(set(masks)) == 65536
    assert all(0 <= mask <= WORD and f(mask) & 65535 == 0 for mask in masks)


def rejection_control(packet):
    """A read-only tamper test: missing, duplicate, and nonkernel masks must fail."""
    outcomes = {}
    variants = {"missing": packet[:-1], "duplicate": packet[:-1] + [packet[0]],
                "nonkernel": packet[:-1] + [1]}
    for name, damaged in variants.items():
        try:
            check_kernel_packet(damaged)
        except AssertionError:
            outcomes[name] = "rejected"
        else:
            raise AssertionError("damaged packet accepted: " + name)
    # Corrupt a needed raw recurrence by changing support membership.
    data = json.loads(SUPPORTS.read_text())["supports"]
    data[11] = [i for i in data[11] if i != 18]
    try:
        derive(data)
    except AssertionError:
        outcomes["removed_support11_word18"] = "rejected"
    else:
        raise AssertionError("damaged support bridge accepted")
    return outcomes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    source = SUPPORTS.read_bytes()
    assert hashlib.sha256(source).hexdigest() == PINNED
    supports = json.loads(source)["supports"]
    bridges = derive(supports)
    k_rows = [1 << bit for bit in range(16)] + map_rows(g, 16)
    k_basis, k_pivots, k_reduced = nullspace(k_rows)
    l_basis, l_pivots, l_reduced = nullspace(map_rows(f, 16))
    assert len(k_pivots) == 31 and k_basis == [0x44AB0000]
    assert len(l_pivots) == 16 and len(l_basis) == 16
    K = k_basis[0]
    assert K & 65535 == g(K) & 65535 == 0
    packet = full_span(l_basis)
    check_kernel_packet(packet)
    first_survivors = []
    failure_histogram = {}
    for L in packet:
        feasible, failed_bit, _ = signed_carry([L, f(K)])
        if feasible:
            first_survivors.append(L)
        else:
            failure_histogram[failed_bit] = failure_histogram.get(failed_bit, 0) + 1
    expected = [0x4804DDD6, 0x5804FFF6, 0xC814DDF6, 0xD805EEE6, 0xD814FFD6]
    assert first_survivors == expected
    second = {}
    for m in (1, 2):
        exclusions = []
        for L in first_survivors:
            feasible, failed_bit, trace = signed_carry([f(L), (m * K) & WORD, g(K)])
            assert not feasible
            exclusions.append({"L": L, "fL": f(L), "first_impossible_bit": failed_bit,
                               "carry_trace": trace})
        second[m] = exclusions
    controls = rejection_control(packet)
    controls["signed_carry_exhaustive_3bit_triples"] = signed_carry_controls()
    packet_text = "".join(f"{L:08x}\n" for L in packet)
    output = {
        "schema": "independent-two-actual-pair-valuation-review-v4",
        "supports_source_sha256": PINNED,
        "scope": "For all ordered unequal actual X, all actual Y, and m in {1,2}, the two core equations imply NOT(2^16 divides dX and 2^16 divides m*dX+GX).",
        "global_sha256_distance14": False,
        "bridges": bridges,
        "K_basis": k_basis, "K_rank": len(k_pivots), "K_rref": k_reduced,
        "L_basis": l_basis, "L_rank": len(l_pivots), "L_rref": l_reduced,
        "L_masks": len(packet), "kernel_text_sha256": hashlib.sha256(packet_text.encode()).hexdigest(),
        "fK": f(K), "gK": g(K), "first_survivors": first_survivors,
        "first_failure_histogram": failure_histogram,
        "second_exclusions": second, "negative_controls": controls,
    }
    if args.save:
        (HERE / "RESULTS.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
        (HERE / "kernel-masks.txt").write_text(packet_text)
    print(json.dumps({key: output[key] for key in ("schema", "L_masks", "first_survivors", "kernel_text_sha256", "negative_controls")}, sort_keys=True))


if __name__ == "__main__":
    main()
