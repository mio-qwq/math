#!/usr/bin/env python3
"""Small, solver-free independent certificate for h(x)=x+sigma1(x).

The sigma implementation uses per-output-bit indexing. Kernel reconstruction
uses columns of the full low-input/low-output map, not the discovery code.
No code or data is imported from the discoverer's implementation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
from pathlib import Path

BITS = 32
MASK = (1 << BITS) - 1
HERE = Path(__file__).resolve().parent


def sigma1(value: int) -> int:
    if not isinstance(value, int) or not 0 <= value <= MASK:
        raise ValueError("not an unsigned 32-bit word")
    out = 0
    for j in range(BITS):
        b = ((value >> ((j + 17) % BITS)) & 1)
        b ^= ((value >> ((j + 19) % BITS)) & 1)
        if j + 10 < BITS:
            b ^= ((value >> (j + 10)) & 1)
        out |= b << j
    return out


def h(value: int) -> int:
    return (value + sigma1(value)) & MASK


def hx(value: int) -> str:
    return f"{value:08x}"


def rank(vectors: list[int]) -> int:
    remaining = list(vectors)
    result = 0
    for j in range(BITS):
        chosen = next((i for i in range(result, len(remaining))
                       if (remaining[i] >> j) & 1), None)
        if chosen is None:
            continue
        remaining[result], remaining[chosen] = remaining[chosen], remaining[result]
        for i in range(result + 1, len(remaining)):
            if (remaining[i] >> j) & 1:
                remaining[i] ^= remaining[result]
        result += 1
    return result


def kernel(low_bits: int) -> tuple[int, list[int], list[int]]:
    low_mask = (1 << low_bits) - 1

    def image(value: int) -> int:
        return (value & low_mask) | ((sigma1(value) & low_mask) << low_bits)

    columns = [image(1 << i) for i in range(BITS)]
    pivots: dict[int, tuple[int, int]] = {}
    basis = []
    for i, column in enumerate(columns):
        residual = column
        combination = 1 << i
        while residual:
            lead = residual.bit_length() - 1
            if lead not in pivots:
                pivots[lead] = (residual, combination)
                break
            other, other_combination = pivots[lead]
            residual ^= other
            combination ^= other_combination
        if not residual:
            basis.append(combination)
    assert len(pivots) + len(basis) == BITS
    assert rank(basis) == len(basis)
    assert all(image(vector) == 0 for vector in basis)
    return len(pivots), basis, columns


def obstruction(d: int, e: int) -> int | None:
    """First single active summand bit with no preceding mask activity."""
    for i in range(BITS):
        single = ((d >> i) & 1) != ((e >> i) & 1)
        previous_inactive = i == 0 or not (((d | e) >> (i - 1)) & 1)
        if single and previous_inactive:
            return i
    return None


def signed_carry_test(d: int, e: int) -> tuple[bool, int | None]:
    """Independent summand-sign relaxation, for checking the mask criterion."""
    carry = {0}
    for i in range(BITS):
        da = (-1, 1) if (d >> i) & 1 else (0,)
        db = (-1, 1) if (e >> i) & 1 else (0,)
        following = set()
        for old in carry:
            for a in da:
                for b in db:
                    total = old + a + b
                    if total % 2 == 0:
                        following.add(total // 2)
        carry = following
        assert carry <= {-1, 0, 1}
        if not carry:
            return False, i
    return True, None


def mask_classification(low_bits: int) -> dict:
    r, basis, columns = kernel(low_bits)
    cases = []
    seen = set()
    surviving = []
    for selector in range(1, 1 << len(basis)):
        d = 0
        for i, value in enumerate(basis):
            if (selector >> i) & 1:
                d ^= value
        assert d and d not in seen
        seen.add(d)
        e = sigma1(d)
        assert (d | e) & ((1 << low_bits) - 1) == 0
        first = obstruction(d, e)
        carry_ok, carry_first = signed_carry_test(d, e)
        assert carry_ok == (first is None)
        assert first == carry_first
        if first is None:
            surviving.append(hx(d))
        cases.append({"selector": selector, "xor_mask": hx(d),
                      "sigma1_mask": hx(e), "first_obstruction_bit": first})
    return {"low_bits": low_bits, "map_rank": r,
            "map_columns": [hx(v) for v in columns],
            "kernel_dimension": len(basis), "kernel_basis": [hx(v) for v in basis],
            "nonzero_masks_checked": len(cases),
            "surviving_masks": sorted(surviving), "cases": cases}


def witness_record(x: int, y: int) -> dict:
    assert 0 <= x <= MASK and 0 <= y <= MASK
    assert x != y and (x & 4095) == (y & 4095)
    assert h(x) == h(y)
    assert (x & 8191) != (y & 8191)
    return {"x": hx(x), "y": hx(y), "sigma1_x": hx(sigma1(x)),
            "sigma1_y": hx(sigma1(y)), "h_x": hx(h(x)), "h_y": hx(h(y)),
            "xor_mask": hx(x ^ y), "additive_delta_y_minus_x": hx((y - x) & MASK),
            "common_low_12": f"{x & 4095:03x}"}


def power_of_two_record() -> dict:
    checked = 0
    equal_valuation = []
    interval_images = []
    for k in range(BITS):
        for last in range(k, BITS):
            checked += 1
            d = (1 << (last + 1)) - (1 << k)
            e = sigma1(d)
            if e and (e & -e) == (1 << k):
                equal_valuation.append({"k": k, "last": last,
                                        "xor_mask": hx(d), "sigma1_mask": hx(e)})
                shifted = e >> k
                if (shifted & (shifted + 1)) == 0:
                    interval_images.append({"k": k, "last": last,
                                            "image_last": k + shifted.bit_length() - 1,
                                            "xor_mask": hx(d), "sigma1_mask": hx(e)})
    assert checked == 528
    assert interval_images == [{"k": 0, "last": 31, "image_last": 21,
                                "xor_mask": "ffffffff", "sigma1_mask": "003fffff"}]
    final_pairs = []
    for x, y in ((0x7FFFFFFF, 0x80000000), (0xFFFFFFFF, 0)):
        assert (y - x) & MASK == 1
        assert (x ^ y) == MASK
        assert h(x) != h(y)
        final_pairs.append({"x": hx(x), "y": hx(y), "h_x": hx(h(x)), "h_y": hx(h(y)),
                            "h_difference": hx((h(y) - h(x)) & MASK)})
    return {"input_intervals_checked": checked,
            "equal_valuation_cases": equal_valuation,
            "same_start_interval_images": interval_images,
            "remaining_actual_pairs": final_pairs}


def rebuild() -> dict:
    assert sigma1(1) == 0xA000
    assert sigma1(0x80000000) == 0x205000
    assert sigma1(MASK) == 0x3FFFFF
    low13 = mask_classification(13)
    assert low13["map_rank"] == 26 and low13["kernel_dimension"] == 6
    assert low13["nonzero_masks_checked"] == 63 and not low13["surviving_masks"]
    low12 = mask_classification(12)
    assert low12["map_rank"] == 24 and low12["kernel_dimension"] == 8
    assert low12["nonzero_masks_checked"] == 255
    assert low12["surviving_masks"] == ["fbca7000"]
    return {"schema": "CRYPTO3-independent-local-h-v1",
            "definition": {"bits": 32, "rotr": [17, 19], "shr": 10,
                           "outer_operation": "addition modulo 2^32"},
            "low13": low13, "low12": low12,
            "boundary_witness": witness_record(0xCD027F2A, 0x36C80F2A),
            "power_of_two": power_of_two_record()}


def verify(data: dict) -> None:
    if data != rebuild():
        raise ValueError("certificate differs from independent exact reconstruction")


def negative_controls(data: dict) -> list[dict]:
    variants = []
    changed = copy.deepcopy(data)
    changed["definition"]["rotr"][0] = 18
    variants.append(("wrong_sigma_rotation", changed))
    changed = copy.deepcopy(data)
    changed["low13"]["kernel_basis"][0] = "00000001"
    variants.append(("damaged_kernel_basis", changed))
    changed = copy.deepcopy(data)
    changed["low13"]["cases"].pop()
    variants.append(("missing_low13_case", changed))
    changed = copy.deepcopy(data)
    changed["low13"]["cases"][0]["first_obstruction_bit"] = 31
    variants.append(("false_obstruction_bit", changed))
    changed = copy.deepcopy(data)
    changed["low12"]["surviving_masks"] = []
    variants.append(("falsely_injective_mod_4096", changed))
    changed = copy.deepcopy(data)
    changed["boundary_witness"]["y"] = hx(int(changed["boundary_witness"]["y"], 16) ^ 1)
    variants.append(("damaged_input_word", changed))
    changed = copy.deepcopy(data)
    changed["boundary_witness"]["sigma1_y"] = "00000000"
    variants.append(("tampered_sigma_word", changed))
    changed = copy.deepcopy(data)
    changed["power_of_two"]["same_start_interval_images"] = []
    variants.append(("missing_exceptional_interval", changed))
    result = []
    for name, changed in variants:
        try:
            verify(changed)
        except ValueError:
            result.append({"case": name, "rejected": True})
        else:
            raise AssertionError(f"negative control accepted: {name}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "independent_certificate.json")
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    if args.emit:
        args.certificate.write_text(json.dumps(rebuild(), indent=2) + "\n")
    data = json.loads(args.certificate.read_text())
    verify(data)
    controls = negative_controls(data) if args.selftest else []
    record = {"status": "PASS", "python": platform.python_version(),
              "low13_nonzero_masks": len(data["low13"]["cases"]),
              "low12_nonzero_masks": len(data["low12"]["cases"]),
              "low12_only_surviving_mask": data["low12"]["surviving_masks"],
              "power_of_two_intervals": data["power_of_two"]["input_intervals_checked"],
              "boundary_witness": data["boundary_witness"],
              "negative_controls": controls,
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "certificate_sha256": hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
              "proof_scope": "local h map only; no new full-schedule distance bound",
              "formalization": "not Lean-formalized"}
    if args.record:
        args.record.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
