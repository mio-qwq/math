#!/usr/bin/env python3
"""Independent definition-based gate for the inherited CRYPTO2 finite evidence.

Only the Python standard library is used. No source checker, optimizer,
solver, or discovery module is imported or executed. Main execution checks
every supplied potential inequality exactly once; controls exercise separate
validation layers instead of rerunning the large certificate.

The universal implication is a written proof in REVIEW.md, not Lean.
"""
import argparse
import base64
from collections import Counter
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
import zlib

HERE = Path(__file__).resolve().parent
WIDTH = 32
MOD = 1 << WIDTH
MASK = MOD - 1
HALF = MOD >> 1
STATES = 1 << 16
ROWS = 49
BOUND = 13
PINNED_COMMIT = "80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51"
RAW_HASH = "1f04aa2b5ac13c5144e677cf75eb6d6af323d518abf96ec65a44a96fa07df23c"
SOURCE_HASHES = {
    "PROOF.md": "2a215fb80a452a2f0223a8458f241799003bdd3beb8e47b61afd58524e52a424",
    "certificate.json": "9ddf8469a51f24c97ecb57f32686af404a2ba7d36b1c98abec6a4405eb219b1b",
    "check.py": "3afa75cb04996c6babc7944de946fecf9d432fd580ba3cbaeff14e800ad20e35",
    "v2/PROOF.md": "6e905e1c973703cd5896b54fdeb11430b7e4a5658264561ee304712388a043e1",
    "v2/supports.json": "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf",
    "v2/exclusions.json": "8611e9bbae742c6b74f2a361640135937b9c24bed24cf9801b8a9d4868e3eaca",
    "v2/check.py": "5536a3b4aefae109aed679e51649c3d2cf622f7fb074a40bf52d0cd9bdbbd721",
    "v2/TAIL.json": "601f0457629a04526be53119dd78bdcef0c47f4d5718b372ab96311abb15e804",
}


class GateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def exact_integer(value, low, high, label):
    require(type(value) is int and low <= value < high, label)


def no_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, "duplicate JSON key")
        obj[key] = value
    return obj


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=no_duplicate_keys)


def rotate_right(word, amount):
    return ((word >> amount) | (word << (WIDTH - amount))) & MASK


def small_sigma(word, which):
    exact_integer(word, 0, MOD, "sigma word range")
    if which == 0:
        return rotate_right(word, 7) ^ rotate_right(word, 18) ^ (word >> 3)
    require(which == 1, "sigma number")
    return rotate_right(word, 17) ^ rotate_right(word, 19) ^ (word >> 10)


def image_by_columns(word, columns):
    result = 0
    for bit, column in enumerate(columns):
        if word & (1 << bit):
            result ^= column
    return result


def inverse_columns(which):
    """Build [A | I] by independent basis images, then eliminate rows over F2."""
    columns = [small_sigma(1 << bit, which) for bit in range(WIDTH)]
    rows = [sum(((columns[col] >> row) & 1) << col for col in range(WIDTH))
            | (1 << (WIDTH + row)) for row in range(WIDTH)]
    pivots = 0
    for col in range(WIDTH):
        pivot = next((row for row in range(pivots, WIDTH)
                      if rows[row] & (1 << col)), None)
        require(pivot is not None, "sigma matrix rank")
        rows[pivots], rows[pivot] = rows[pivot], rows[pivots]
        for row in range(WIDTH):
            if row != pivots and rows[row] & (1 << col):
                rows[row] ^= rows[pivots]
        pivots += 1
    require([row & MASK for row in rows] == [1 << j for j in range(WIDTH)],
            "matrix reduced identity")
    inverse = [sum(((rows[row] >> (WIDTH + col)) & 1) << row
                   for row in range(WIDTH)) for col in range(WIDTH)]
    return columns, inverse


def verify_inverses(certificate):
    supplied = certificate["sigma_inverse_columns"]
    require(type(supplied) is list and len(supplied) == 2,
            "inverse outer shape")
    reconstructed = []
    compositions = 0
    for which, given in enumerate(supplied):
        require(type(given) is list and len(given) == WIDTH,
                "inverse column count")
        for word in given:
            exact_integer(word, 0, MOD, "inverse unsigned word")
        forward, inverse = inverse_columns(which)
        require(given == inverse, "inverse reconstruction mismatch")
        for col in range(WIDTH):
            require(small_sigma(given[col], which) == 1 << col,
                    "right inverse composition")
            require(image_by_columns(forward[col], given) == 1 << col,
                    "left inverse composition")
            compositions += 2
        reconstructed.append(inverse)
    return reconstructed, {"ranks": [32, 32], "reconstructed_columns": 64,
                           "right_inverse_columns_checked": 64,
                           "basis_composition_checks": compositions,
                           "sigma0_half": small_sigma(HALF, 0),
                           "sigma1_inverse_half": reconstructed[1][31]}


def verify_source_identity():
    provenance = load_json(HERE / "PROVENANCE.json")
    require(provenance["source_commit"] == PINNED_COMMIT, "source commit")
    expected = {"sources/" + name for name in SOURCE_HASHES}
    records = provenance["files"]
    require(len(records) == 8 and {r["local_path"] for r in records} == expected,
            "provenance file coverage")
    observed = []
    for record in records:
        local = record["local_path"]
        data = (HERE / local).read_bytes()
        require(hashlib.sha256(data).hexdigest()
                == record["sha256"] == SOURCE_HASHES[local.removeprefix("sources/")],
                "pinned source SHA256")
        require(len(data) == record["bytes"], "source byte length")
        blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii")
                            + b"\0" + data).hexdigest()
        require(blob == record["git_blob"], "source Git blob object")
        require(record["source_path"]
                == "workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/"
                + local.removeprefix("sources/"), "source path")
        observed.append({"local_path": local, "git_blob": blob,
                         "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    return observed


def unpack_potential(certificate):
    require(certificate["schema"] == "sha256-word-support-relaxation-v1",
            "v1 schema")
    require(certificate["shape"] == [ROWS, STATES], "potential dimensions")
    require(certificate["state_encoding"] == "bit j is W[t-16+j] active",
            "activity state encoding")
    exact_integer(certificate["bound"], BOUND, BOUND + 1, "fixed bound 13")
    packed = base64.b64decode(certificate["potentials_zlib_base64"], validate=True)
    decompressor = zlib.decompressobj()
    raw = decompressor.decompress(packed)
    raw += decompressor.flush()
    require(decompressor.eof and not decompressor.unused_data
            and not decompressor.unconsumed_tail, "single complete zlib stream")
    require(len(raw) == ROWS * STATES, "raw potential length")
    require(hashlib.sha256(raw).hexdigest() == certificate["potential_sha256"]
            == RAW_HASH, "pinned raw potential SHA256")
    return raw


def verify_end_row(raw):
    require(len(raw) == ROWS * STATES, "terminal validator shape")
    require(all(value == 0 for value in raw[48 * STATES:]), "terminal zeros")
    return STATES


def verify_initial_bounds(raw):
    require(len(raw) == ROWS * STATES, "initial validator shape")
    minimum_slack = 64
    equal = []
    for state in range(1, STATES):
        slack = state.bit_count() + raw[state] - BOUND
        require(slack >= 0, "initial weight lower bound")
        minimum_slack = min(minimum_slack, slack)
        if slack == 0:
            equal.append(state)
    return equal, {"checked_states": STATES - 1, "minimum_slack": minimum_slack,
                   "equality_states": equal}


def permitted_edges():
    """Fixed relation from the four exact lag positions, with no minimization."""
    source_positions = tuple(16 - lag for lag in (16, 15, 7, 2))
    relation = []
    for state in range(STATES):
        total = sum((state >> position) & 1 for position in source_positions)
        for bit in range(2):
            if total + bit != 1:
                successor = (state >> 1) | (bit << 15)
                relation.append((state, bit, successor))
    require(len(relation) == 27 * 4096, "per-row edge count")
    return relation


def verify_transition_bounds(raw, edges):
    require(len(raw) == ROWS * STATES, "transition validator shape")
    checked = 0
    slack_histogram = Counter()
    data = memoryview(raw)
    for t in range(16, 64):
        now = data[(t - 16) * STATES:(t - 15) * STATES]
        following = data[(t - 15) * STATES:(t - 14) * STATES]
        for state, bit, successor in edges:
            slack = bit + following[successor] - now[state]
            require(slack >= 0, "permitted transition inequality")
            slack_histogram[slack] += 1
            checked += 1
    require(checked == 5308416, "complete transition count")
    return {"checked_inequalities": checked, "rows": 48,
            "per_row_edges": len(edges),
            "slack_histogram": dict(sorted(slack_histogram.items()))}


def support_tuple(items):
    require(type(items) is list and all(type(i) is int and 0 <= i < 64 for i in items),
            "support coordinate type/range")
    require(items == sorted(set(items)) and len(items) == BOUND
            and any(i < 16 for i in items), "13-word nonzero support format")
    return tuple(items)


def verify_witness(certificate):
    support = support_tuple(certificate["support_witness"])
    active = set(support)
    for t in range(16, 64):
        require(sum(i in active for i in (t, t-2, t-7, t-15, t-16)) != 1,
                "relaxation witness recurrence")
    return {"support": list(support), "weight": len(support), "rows_checked": 48}


def encode_activity(bits):
    return sum(bit << position for position, bit in enumerate(bits))


def enumerate_equal_paths(raw, starts):
    # A path is a tuple of activity bits. Both states are reconstructed from
    # its last sixteen coordinates, independently of the v1 state update.
    frontier = {tuple((mask >> i) & 1 for i in range(16)) for mask in starts}
    layer_sizes = [len(frontier)]
    visited = len(frontier)
    tested_choices = 0
    equality_choices = 0
    for t in range(16, 64):
        following = set()
        for prefix in frontier:
            require(len(prefix) == t, "equality path length")
            current_state = encode_activity(prefix[-16:])
            require(sum(prefix) + raw[(t - 16) * STATES + current_state] == BOUND,
                    "equality path cost invariant")
            for bit in range(2):
                tested_choices += 1
                candidate = prefix + (bit,)
                incidence = sum(candidate[i] for i in (t, t-2, t-7, t-15, t-16))
                if incidence == 1:
                    continue
                next_state = encode_activity(candidate[-16:])
                if raw[(t - 16) * STATES + current_state] != (
                        bit + raw[(t - 15) * STATES + next_state]):
                    continue
                following.add(candidate)
                equality_choices += 1
        frontier = following
        layer_sizes.append(len(frontier))
        visited += len(frontier)
    actual = {tuple(i for i, bit in enumerate(prefix) if bit) for prefix in frontier}
    require(all(sum(prefix) == BOUND for prefix in frontier), "terminal equality weight")
    return actual, {"initial_states": len(starts), "nodes_including_terminal": visited,
                    "layer_sizes": layer_sizes, "both_bit_choices_tested": tested_choices,
                    "equality_choices": equality_choices, "terminal_supports": len(actual)}


def compare_support_certificate(supplied, starts, actual, stats):
    require(supplied["schema"] == "sha256-minimum-supports-v2", "v2 support schema")
    exact_integer(supplied["bound"], BOUND, BOUND + 1, "v2 bound")
    require(supplied["start_states"] == starts, "complete equality starts")
    supports = [support_tuple(s) for s in supplied["supports"]]
    require(len(supports) == len(set(supports)) == 15
            and set(supports) == actual, "complete equality terminal set")
    require(supplied["visited_nodes"] == stats["nodes_including_terminal"] == 735,
            "complete equality node count")
    return supports


def verify_halfword_dependencies(inverses, exclusion):
    require(exclusion["schema"] == "sha256-impossible-chain-v2", "exclusion schema")
    require(type(exclusion["word_bits"]) is int and exclusion["word_bits"] == WIDTH,
            "exclusion word width")
    beta = small_sigma(HALF, 0)
    preimage = inverses[1][31]
    require(exclusion["sigma0_half"] == beta == 0x11002000, "halfword sigma0 image")
    require(exclusion["sigma1_inverse_half"] == preimage == 0xc6eeaad6,
            "halfword sigma1 preimage")
    require(small_sigma(preimage, 1) == HALF and preimage % 4 == 2,
            "halfword inverse low bits")
    positions = [i for i in range(WIDTH) if beta & (1 << i)]
    require(positions == [13, 24, 28], "halfword image support")
    residues = set()
    for choices in range(8):
        base = sum(((choices >> j) & 1) << position
                   for j, position in enumerate(positions))
        difference = ((base ^ beta) - base) % MOD
        residues.add(difference % (1 << 24))
    require(residues == {1 << 13, (1 << 24) - (1 << 13)}, "signed-sum low24 residues")
    carry_count = 0
    low_sigma_values = set()
    for quotient in range(128):
        for direction in (-1, 1):
            other = (quotient + direction) & 127
            alpha = (quotient ^ other) << 13
            require(not (alpha & (1 << 19)) or bool(alpha & (1 << 18)),
                    "adjacent quotient carry implication")
            low = small_sigma(alpha, 0) & 3
            require(low == (((alpha >> 18) & 1) | (((alpha >> 19) & 1) << 1)),
                    "sigma0 low-two-bit dependency")
            require(low != 2, "forbidden low-two-bit image")
            low_sigma_values.add(low)
            carry_count += 1
    modulo_four_count = 0
    for first in range(4):
        for second in range(4):
            require(((second - first) % 4 == 2) == (first ^ second == 2),
                    "mod4 versus XOR equivalence")
            modulo_four_count += 1
    return {"halfword": HALF, "sigma0_half_hex": f"{beta:08x}",
            "sigma1_inverse_half_hex": f"{preimage:08x}",
            "signed_image_choices": 8, "low24_residues": sorted(residues),
            "adjacent_quotient_cases": carry_count,
            "sigma0_low_two_values": sorted(low_sigma_values),
            "modulo_four_cases": modulo_four_count}


def raw_difference_row(support, t):
    exact_integer(t, 16, 64, "difference recurrence index")
    variables = [("d", t, 1), ("g", t-2, -1), ("d", t-7, -1),
                 ("f", t-15, -1), ("d", t-16, -1)]
    return {(kind, index): coefficient for kind, index, coefficient in variables
            if index in support}


def verify_schedule_substitutions(exclusion, supports):
    expected_cases = [
        {"support_index": 3, "u": 27, "x": 34, "a": 42, "r": 43, "b": 57},
        {"support_index": 14, "u": 25, "x": 32, "a": 40, "r": 41, "b": 55},
    ]
    require(exclusion["cases"] == expected_cases, "exact excluded case parameters")
    checked = []
    for case in exclusion["cases"]:
        index = case["support_index"]
        support = set(supports[index])
        u, x, a, r, b = [case[name] for name in ("u", "x", "a", "r", "b")]
        require({u, x, a, r, b} <= support, "forced nonzero coordinates")
        needed = [
            (x, {("d", x): 1, ("d", u): -1}),
            (r, {("d", r): 1, ("d", u): -1}),
            (r+7, {("d", r): -1, ("d", x): -1}),
            (x+15, {("d", a): -1, ("f", x): -1}),
            (b, {("d", b): 1, ("f", a): -1}),
            (b+2, {("g", b): -1, ("d", r): -1}),
        ]
        for t, identity in needed:
            actual = raw_difference_row(support, t)
            require(actual == identity, "original difference recurrence substitution")
            checked.append({"support_index": index, "t": t,
                            "terms": [[kind, i, coefficient]
                                      for (kind, i), coefficient in sorted(actual.items())]})
    remaining = [i for i in range(15) if i not in (3, 14)]
    require(exclusion["remaining_indices"] == remaining, "complete surviving indices")
    return {"excluded_indices": [3, 14], "remaining_indices": remaining,
            "original_recurrence_identities_checked": 12, "identities": checked}


def verify_zero_base_constants(inverses):
    word = inverses[0][31]
    require(word == 0x94857ee6, "zero-base inverse")
    first = small_sigma((-small_sigma(word, 1)) % MOD, 0)
    second = small_sigma(HALF, 1)
    require(first == 0xabacb99f and second == 0x00205000 and first != second,
            "restricted zero-base obstruction constants")
    return {"scope": "S0 with zero base only", "forced_word_hex": f"{word:08x}",
            "unequal_constant_hex": [f"{first:08x}", f"{second:08x}"]}


def verify_tail(tail):
    require(tail["status"] == "sat", "tail status")
    pairs = tail["pairs"]
    require(type(pairs) is dict and set(pairs) == {"x", "a", "r", "b"},
            "tail coordinate names")
    differences = {}
    for name in ("x", "a", "r", "b"):
        pair = pairs[name]
        require(type(pair) is list and len(pair) == 2, "tail pair shape")
        for word in pair:
            exact_integer(word, 0, MOD, "tail unsigned word")
        first, second = pair
        differences[name] = {"d": (second - first) % MOD,
                             "f": (small_sigma(second, 0) - small_sigma(first, 0)) % MOD,
                             "g": (small_sigma(second, 1) - small_sigma(first, 1)) % MOD}
        require(differences[name]["d"] != 0, "tail all pairs active")
    d = lambda name: differences[name]["d"]
    f = lambda name: differences[name]["f"]
    g = lambda name: differences[name]["g"]
    require((d("r") + d("x")) % MOD == 0, "tail opposite raw differences")
    require(f("r") == f("x"), "tail equal sigma0 derivatives")
    require((d("a") + f("x")) % MOD == 0, "tail first derivative link")
    require(d("b") == f("a"), "tail second derivative link")
    require(g("b") == d("x"), "tail final sigma1 link")
    require(d("x") != HALF, "tail does not satisfy forced-halfword premise")
    return {"verified_equations": 5, "active_pairs": 4, "delta_x": d("x"),
            "differences_hex": {name: {kind: f"{value:08x}" for kind, value in values.items()}
                                for name, values in differences.items()},
            "scope": "Unforced five-equation independent-pair tail only; not a schedule."}


def negative_controls(certificate, raw, inverses, starts, support_cert,
                      actual, stats, exclusion, supports, tail, edges):
    records = []

    def reject(name, function):
        try:
            function()
        except GateError as error:
            records.append({"control": name, "rejected_by": str(error)})
        else:
            raise GateError("negative control accepted: " + name)

    bad = copy.deepcopy(certificate)
    bad["sigma_inverse_columns"][0][0] ^= 1
    reject("alter one sigma inverse column", lambda: verify_inverses(bad))
    bad_bound = copy.deepcopy(certificate)
    bad_bound["bound"] = 14
    reject("claim fixed bound 14", lambda: unpack_potential(bad_bound))
    bad_hash = copy.deepcopy(certificate)
    bad_hash["potential_sha256"] = "0" * 64
    reject("alter compressed-certificate raw digest", lambda: unpack_potential(bad_hash))
    bad_terminal = bytearray(raw)
    bad_terminal[-1] = 1
    reject("alter terminal value (numeric validator)", lambda: verify_end_row(bad_terminal))
    bad_initial = bytearray(raw)
    bad_initial[1] = 0
    reject("lower a nonzero initial potential (numeric validator)",
           lambda: verify_initial_bounds(bad_initial))
    bad_transition = bytearray(raw)
    bad_transition[0] = 255
    reject("raise initial zero-state potential (numeric validator)",
           lambda: verify_transition_bounds(bad_transition, edges))
    bad_starts = copy.deepcopy(support_cert)
    bad_starts["start_states"].pop()
    reject("omit one equality starting state", lambda: compare_support_certificate(
        bad_starts, starts, actual, stats))
    bad_supports = copy.deepcopy(support_cert)
    bad_supports["supports"].pop()
    reject("omit one terminal support", lambda: compare_support_certificate(
        bad_supports, starts, actual, stats))
    duplicated = copy.deepcopy(support_cert)
    duplicated["supports"][1] = duplicated["supports"][0]
    reject("duplicate one terminal support", lambda: compare_support_certificate(
        duplicated, starts, actual, stats))
    bad_exclusion = copy.deepcopy(exclusion)
    bad_exclusion["sigma1_inverse_half"] ^= 1
    reject("alter asserted halfword preimage", lambda: verify_halfword_dependencies(
        inverses, bad_exclusion))
    bad_case = copy.deepcopy(exclusion)
    bad_case["cases"][0]["a"] = 43
    reject("alter an exclusion coordinate", lambda: verify_schedule_substitutions(
        bad_case, supports))
    bad_remaining = copy.deepcopy(exclusion)
    bad_remaining["remaining_indices"].pop()
    reject("omit one surviving index", lambda: verify_schedule_substitutions(
        bad_remaining, supports))
    bad_tail = copy.deepcopy(tail)
    bad_tail["pairs"]["x"][0] ^= 1
    reject("tamper an unforced-tail word", lambda: verify_tail(bad_tail))
    malformed_tail = copy.deepcopy(tail)
    malformed_tail["pairs"]["x"][0] = True
    reject("Boolean in unsigned tail word", lambda: verify_tail(malformed_tail))
    reject("duplicate JSON object key", lambda: json.loads('{"x":1,"x":2}',
           object_pairs_hook=no_duplicate_keys))
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    began = datetime.now(timezone.utc).isoformat()
    clock = time.perf_counter()
    sources = verify_source_identity()
    certificate = load_json(HERE / "sources/certificate.json")
    support_cert = load_json(HERE / "sources/v2/supports.json")
    exclusion = load_json(HERE / "sources/v2/exclusions.json")
    tail = load_json(HERE / "sources/v2/TAIL.json")
    inverses, inverse_stats = verify_inverses(certificate)
    raw = unpack_potential(certificate)
    terminal_count = verify_end_row(raw)
    starts, initial_stats = verify_initial_bounds(raw)
    edges = permitted_edges()
    transitions = verify_transition_bounds(raw, edges)
    witness = verify_witness(certificate)
    actual, path_stats = enumerate_equal_paths(raw, starts)
    supports = compare_support_certificate(support_cert, starts, actual, path_stats)
    halfword_stats = verify_halfword_dependencies(inverses, exclusion)
    substitutions = verify_schedule_substitutions(exclusion, supports)
    zero_base = verify_zero_base_constants(inverses)
    tail_stats = verify_tail(tail)
    result = {
        "schema": "CRYPTO3-inherited-full-finite-gate-v4",
        "accepted": True,
        "source_commit": PINNED_COMMIT,
        "source_files": sources,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "actual_schedule_distance_lower_bound": BOUND,
        "support_relaxation_exact_minimum": BOUND,
        "sigma_invertibility": inverse_stats,
        "potential": {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                      "terminal_zeros_checked": terminal_count,
                      "initial_bounds": initial_stats,
                      "transitions": transitions},
        "relaxation_witness": witness,
        "complete_equality_paths": path_stats,
        "complete_supports_indexed": [list(s) for s in supports],
        "halfword_chain_dependencies": halfword_stats,
        "universal_exclusion_substitutions": substitutions,
        "zero_base_obstruction_constants": zero_base,
        "unforced_tail_boundary": tail_stats,
        "proof_scope": "Written universal mathematics plus independent full finite-certificate replay; not Lean or human peer review.",
        "no_claims": ["distance 13 attainable", "distance at least 14", "cryptanalytic attack", "historical originality"],
    }
    if args.negative:
        result["rejected_controls"] = negative_controls(
            certificate, raw, inverses, starts, support_cert, actual, path_stats,
            exclusion, supports, tail, edges)
    result["runtime"] = {"began_utc": began,
                         "ended_utc": datetime.now(timezone.utc).isoformat(),
                         "elapsed_seconds": time.perf_counter() - clock,
                         "python": platform.python_version(),
                         "implementation": platform.python_implementation(),
                         "argv": sys.argv}
    output = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
