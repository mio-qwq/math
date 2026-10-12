#!/usr/bin/env python3
"""Independent exact boundary review; never imports candidate checker code.

This checker proves finite support substitutions, not existence of any
distance-13 pair. The universal window theorem is written separately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MASK = (1 << 32) - 1
SUPPORT_HASH = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"

# Offset r means V_i = W_(i+r). Negative r is a right shift.
CLAIMS = [(0, 1, 9), (1, 2, 9), (2, 3, 9), (4, 4, 9),
          (6, 1, 12), (7, 3, 12), (13, 2, 12),
          (0, -1, 1), (0, -2, 2), (0, -3, 4), (3, 2, 14)]
REPRESENTATIVES = [5, 8, 9, 10, 11, 12]


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sigma(word: int, which: int) -> int:
    """Original per-output-bit definition, independent of rotate code."""
    first, second, shift = (7, 18, 3) if which == 0 else (17, 19, 10)
    value = 0
    for bit in range(32):
        a = (word >> ((bit + first) % 32)) & 1
        b = (word >> ((bit + second) % 32)) & 1
        c = (word >> (bit + shift)) & 1 if bit + shift < 32 else 0
        value |= (a ^ b ^ c) << bit
    return value


def rotate_sigma(word: int, which: int) -> int:
    first, second, shift = (7, 18, 3) if which == 0 else (17, 19, 10)
    def rot(n: int) -> int:
        return ((word >> n) | (word << (32 - n))) & MASK
    return rot(first) ^ rot(second) ^ (word >> shift)


def rank_columns(columns: list[int]) -> tuple[int, list[int]]:
    pivots: dict[int, int] = {}
    for column in columns:
        residual = column
        while residual:
            leading = residual.bit_length() - 1
            if leading not in pivots:
                pivots[leading] = residual
                break
            residual ^= pivots[leading]
    return len(pivots), [pivots[p] for p in sorted(pivots)]


def recurrence_extension(inputs: list[int], lowest: int, highest: int) -> dict[int, int]:
    require(len(inputs) == 16, "exactly sixteen words required")
    values = {i: word & MASK for i, word in enumerate(inputs)}
    for t in range(16, highest + 1):
        values[t] = (sigma(values[t - 2], 1) + values[t - 7]
                     + sigma(values[t - 15], 0) + values[t - 16]) & MASK
    for j in range(-1, lowest - 1, -1):
        values[j] = (values[j + 16] - sigma(values[j + 14], 1)
                     - values[j + 9] - sigma(values[j + 1], 0)) & MASK
    return values


def predecessors(index: int, backwards: bool) -> list[tuple[str, int, int]]:
    if backwards:
        return [("d", index + 16, 1), ("G", index + 14, -1),
                ("d", index + 9, -1), ("F", index + 1, -1)]
    return [("G", index - 2, 1), ("d", index - 7, 1),
            ("F", index - 15, 1), ("d", index - 16, 1)]


def support_extension(support: set[int], offset: int) -> tuple[dict[int, str], list[dict]]:
    """Conservative exact oracle: zero/one active predecessor only.

    A sigma derivative is nonzero exactly when its actual input differs,
    since both original sigmas have binary rank 32. Two or more active
    terms cannot be asserted to vanish or survive without extra proof.
    """
    states = {i: "nonzero" if i in support else "zero" for i in range(64)}
    rows = []
    indices = range(64, 64 + offset) if offset > 0 else range(-1, offset - 1, -1)
    for index in indices:
        terms = predecessors(index, offset < 0)
        payload = [{"symbol": name, "index": source, "coefficient": sign,
                    "input_status": states[source]}
                   for name, source, sign in terms]
        nonzero = [x for x in payload if x["input_status"] == "nonzero"]
        unknown = [x for x in payload if x["input_status"] == "unknown"]
        if unknown or len(nonzero) > 1:
            status = "unknown"
        elif nonzero:
            status = "nonzero"
        else:
            status = "zero"
        states[index] = status
        rows.append({"new_old_index": index,
                     "original_recurrence_index": index + 16 if offset < 0 else index,
                     "terms": payload, "conclusion": status})
    return states, rows


def certify_map(supports: list[set[int]], source: int, offset: int, target: int) -> dict:
    states, rows = support_extension(supports[source], offset)
    require(all(states[i + offset] != "unknown" for i in range(64)),
            "unknown boundary activity")
    translated = {i for i in range(64) if states[i + offset] == "nonzero"}
    require(translated == supports[target], "target exact support is incorrect")
    require(any(i < 16 for i in translated), "initial blocks not certified distinct")
    original_preserved = sorted(j for j in supports[source] if offset <= j < offset + 64)
    return {"source": source, "offset": offset, "target": target,
            "shift_direction": "left" if offset > 0 else "right",
            "shift_size": abs(offset), "boundary_rows": rows,
            "deleted_active_original_indices": sorted(supports[source] - set(original_preserved)),
            "added_active_old_indices": sorted(j for j in states if not 0 <= j < 64
                                               and offset <= j < offset + 64
                                               and states[j] == "nonzero"),
            "new_exact_support": sorted(translated),
            "distinct_initial_indices": sorted(i for i in translated if i < 16)}


def exhaustive_safe_maps(supports: list[set[int]]) -> list[dict]:
    maps = []
    for source in range(15):
        for offset in range(-63, 64):
            if offset == 0:
                continue
            states, _ = support_extension(supports[source], offset)
            if any(states[i + offset] == "unknown" for i in range(64)):
                continue
            exact = {i for i in range(64) if states[i + offset] == "nonzero"}
            for target, candidate in enumerate(supports):
                if exact == candidate:
                    maps.append({"source": source, "offset": offset, "target": target})
    return maps


def negative_controls(supports: list[set[int]]) -> list[dict]:
    tests = []
    attempts = [("tail64_in_support3_cannot_be_zero", 3, 2, 3),
                ("blind_reverse_9_to_0_has_unknown_prefix", 9, -1, 0),
                ("shift0_right4_cannot_equal_support4", 0, -4, 4),
                ("wrong_shift_magnitude_for_2_to_9", 2, 2, 9),
                ("right14_to3_does_not_have_zero_prefix", 14, -2, 3),
                ("discard_added_tail_in_3_to14", 3, 2, 12)]
    for label, source, offset, target in attempts:
        try:
            certify_map(supports, source, offset, target)
        except ValueError as error:
            tests.append({"name": label, "rejected": True, "reason": str(error)})
        else:
            raise ValueError("negative map accepted: " + label)
    # A concrete right shift of inputs that differ at W15 creates W[-1].
    a = [0] * 16
    b = a.copy()
    b[15] = 1
    x = recurrence_extension(a, -1, 64)
    y = recurrence_extension(b, -1, 64)
    require(x[-1] != y[-1], "arbitrary-input prefix counterexample lost")
    tests.append({"name": "unconditional_equal_right_prefix_is_false",
                  "rejected": True, "inputs_a": a, "inputs_b": b,
                  "new_prefix_a": x[-1], "new_prefix_b": y[-1]})
    # A concrete tail requires all its dependencies, not just the last two words.
    a = [0] * 16
    b = a.copy()
    b[0] = 1
    x = recurrence_extension(a, 0, 64)
    y = recurrence_extension(b, 0, 64)
    require(x[64] != y[64], "arbitrary-input tail counterexample lost")
    tests.append({"name": "unconditional_equal_left_tail_is_false",
                  "rejected": True, "inputs_a": a, "inputs_b": b,
                  "word64_a": x[64], "word64_b": y[64]})
    return tests


def implementation_crosschecks() -> dict:
    words = [0, MASK] + [1 << i for i in range(32)]
    words += [int.from_bytes(hashlib.sha256(("shift-review-v4-word:" + str(i)).encode())
                             .digest()[:4], "little") for i in range(64)]
    for word in words:
        for which in (0, 1):
            require(sigma(word, which) == rotate_sigma(word, which), "sigma definitions differ")
    pair_count = 16
    offset_count = 127
    comparisons = 0
    for counter in range(pair_count):
        a = [int.from_bytes(hashlib.sha256(("shift-review-v4-A:" + str(counter) + ":" + str(i))
                                          .encode()).digest()[:4], "little") for i in range(16)]
        b = a.copy()
        b[counter] ^= 1 << (counter % 32)
        x = recurrence_extension(a, -63, 126)
        y = recurrence_extension(b, -63, 126)
        for offset in range(-63, 64):
            shifted_a = [x[offset + i] for i in range(16)]
            shifted_b = [y[offset + i] for i in range(16)]
            require(shifted_a != shifted_b, "translated inputs lost distinctness")
            vx = recurrence_extension(shifted_a, 0, 63)
            vy = recurrence_extension(shifted_b, 0, 63)
            for i in range(64):
                require(vx[i] == x[offset + i], "A window is not a valid expansion")
                require(vy[i] == y[offset + i], "B window is not a valid expansion")
                comparisons += 2
    return {"scope": "deterministic implementation crosschecks; not a universal proof",
            "sigma_words": len(words), "sigma_checks": 2 * len(words),
            "distinct_pairs": pair_count, "offsets_per_pair": offset_count,
            "word_equalities_checked": comparisons}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    support_path = ROOT / "supports-v2.json"
    require(digest(support_path) == SUPPORT_HASH, "support source hash changed")
    package = json.loads(support_path.read_text())
    raw = package["supports"]
    require(len(raw) == 15 and len({tuple(s) for s in raw}) == 15, "support count")
    require(all(len(s) == 13 and s == sorted(set(s)) and min(s) >= 0 and max(s) < 64
                for s in raw), "support format")
    supports = list(map(set, raw))
    sigma_ranks = []
    for which in (0, 1):
        columns = [sigma(1 << bit, which) for bit in range(32)]
        rank, pivots = rank_columns(columns)
        require(rank == 32, "sigma is not injective")
        sigma_ranks.append({"sigma": which, "rank": rank, "columns": columns,
                            "eliminated_pivots": pivots})
    certified = [certify_map(supports, *claim) for claim in CLAIMS]
    exhaustive = exhaustive_safe_maps(supports)
    omitted = [m for m in exhaustive if (m["source"], m["offset"], m["target"]) not in CLAIMS]
    route = {source: target for source, offset, target in CLAIMS if offset > 0}
    coverage = []
    for source in range(15):
        path = [source]
        while path[-1] not in REPRESENTATIVES and path[-1] != 14:
            require(path[-1] in route, "uncovered support")
            path.append(route[path[-1]])
            require(len(path) < 16, "reduction loop")
        coverage.append({"source": source, "route": path,
                         "endpoint": "inherited-excluded-support14" if path[-1] == 14
                         else "remaining-representative"})
    data = {
        "schema": "crypto3-independent-shift-review-v4",
        "claim_status": "independently checked conditional boundary theorem",
        "support_source": {"path": str(support_path.relative_to(ROOT.parent)),
                           "sha256": digest(support_path), "bytes": support_path.stat().st_size},
        "checker_source_sha256": digest(Path(__file__).resolve()),
        "recurrence": {"modulus": 1 << 32,
                       "forward_lags": [["G", 2], ["d", 7], ["F", 15], ["d", 16]],
                       "inverse_offsets": [["d", 16, 1], ["G", 14, -1],
                                           ["d", 9, -1], ["F", 1, -1]]},
        "sigma_ranks": sigma_ranks,
        "certified_maps": certified,
        "exhaustive_safe_mapping_domain": {"source_supports": 15, "nonzero_offsets": 126,
                                           "oracle": "zero/one active term; >=2 or unknown remain unknown"},
        "exhaustive_safe_maps": exhaustive,
        "extra_maps_beyond_eleven_claims": omitted,
        "coverage": coverage,
        "representatives": REPRESENTATIVES,
        "classification_dependency": "all distance-13 supports are in frozen fifteen; not re-proved here",
        "inherited_exclusion_dependency": "support14 is impossible; not re-proved by this checker",
        "negative_controls": negative_controls(supports),
        "implementation_crosschecks": implementation_crosschecks(),
        "no_candidate_checker_import_or_execution": True,
        "no_distance13_witness_or_distance14_bound": True,
    }
    rendered = json.dumps(data, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
