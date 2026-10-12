#!/usr/bin/env python3
"""Independent semantic checks for the fourteen triple-state representation.

Uses only the Python standard library. It does not import discovery checkers.
The full shift graph is reconstructed from literal words and append adjacency.
This validates an elementary proof and finite fixtures, not a finite optimizer.
"""

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


SOURCE_SHA256 = "3cdcefd81b32054db42c9efb1c663d17e30e65d022cf95cf157a190958db6898"
SOURCE = Path(__file__).resolve().parent.parent / "construction" / "FOURTEEN_STATE_REDUCTION.md"


class Rejected(ValueError):
    pass


def need(condition, reason):
    if not condition:
        raise Rejected(reason)


def words(r, n):
    return list(itertools.product(range(r), repeat=n))


def validate_input(r, code):
    need(type(r) is int and r >= 1, "alphabet must be a positive integer")
    need(all(len(w) == 4 for w in code), "incorrect word length")
    need(all(type(x) is int and 0 <= x < r for w in code for x in w), "letter outside bound alphabet")
    need(len(set(code)) == len(code), "duplicate code listing")


def literal_strictness(r, code):
    """Count occurrences directly; equal selected windows count separately."""
    validate_input(r, code)
    selected = set(code)
    maximum, witness = -1, None
    for u in itertools.product(range(r), repeat=8):
        hits = [i for i in range(5) if u[i:i + 4] in selected]
        if len(hits) > maximum:
            maximum, witness = len(hits), [list(u), hits]
    return maximum, witness


def local_signature(code):
    result = []
    for v in sorted(code):
        left = next((d for d in range(1, 4) if any(w[d:] == v[:4 - d] for w in code)), 4)
        right = next((d for d in range(1, 4) if any(w[:4 - d] == v[d:] for w in code)), 4)
        result.append([list(v), left, right])
    return result


def literal_graph(r):
    vertices = words(r, 3)
    index = {v: i for i, v in enumerate(vertices)}
    arcs = [(index[w[:3]], index[w[1:]], w) for w in words(r, 4)]
    return vertices, arcs


def maximum_counts(r, code):
    """F_t from raw append arcs, with every start state allowed."""
    validate_input(r, code)
    vertices, arcs = literal_graph(r)
    selected = set(code)
    table = [[0] * len(vertices)]
    for _ in range(5):
        row = [-1] * len(vertices)
        for source, target, w in arcs:
            row[target] = max(row[target], table[-1][source] + int(w in selected))
        need(min(row) >= 0, "missing incoming arc")
        table.append(row)
    return vertices, arcs, table


def derive_target():
    """Generate all permitted hit sequences before computing hit-time labels."""
    sequences = []
    for increments in itertools.product((0, 1), repeat=5):
        values = [0]
        for bit in increments:
            values.append(values[-1] + bit)
        if values[4] >= 1 and values[5] <= 2:
            first = values.index(1)
            second = values.index(2) if 2 in values else 6
            sequences.append(((first, second), values))
    sequences.sort()
    profiles = [p for p, _ in sequences]
    heights = [h for _, h in sequences]
    need(len(profiles) == 14 and len(set(profiles)) == 14, "incorrect profile classification")
    allowed, marked = [], []
    for i, (a, b) in enumerate(profiles):
        for j, (c, d) in enumerate(profiles):
            semantic_allowed = all(heights[j][t] >= heights[i][t - 1] for t in range(1, 6))
            semantic_marked = all(heights[j][t] >= heights[i][t - 1] + 1 for t in range(1, 6))
            need(semantic_allowed == (c <= a + 1 and (b >= 5 or d <= b + 1)), "allowed formula disagrees")
            need(semantic_marked == (c == 1 and b >= 5 and d <= a + 1), "marked formula disagrees")
            if semantic_allowed:
                allowed.append((i, j))
            if semantic_marked:
                need(semantic_allowed, "marked edge is not allowed")
                marked.append((i, j))
    need(len(allowed) == 138 and len(marked) == 20, "incorrect target counts")
    return profiles, heights, allowed, marked


def target_walks(size, allowed, marked):
    marked = set(marked)
    table = [[0] * size]
    for _ in range(5):
        row = [-1] * size
        for u, v in allowed:
            row[v] = max(row[v], table[-1][u] + int((u, v) in marked))
        table.append(row)
    return table


def completion(r, code, target):
    profiles, heights, allowed, marked = target
    vertices, arcs, counts = maximum_counts(r, code)
    need(max(counts[5]) <= 2, "non-strict input to completion")
    if not code:
        assignment = [profiles.index((4, 6))] * len(vertices)
    else:
        assignment = []
        for s in range(len(vertices)):
            values = [counts[t][s] for t in range(6)]
            need(values in heights, "path-count sequence outside target profiles")
            assignment.append(heights.index(values))
    allowed, marked = set(allowed), set(marked)
    need(all((assignment[u], assignment[v]) in allowed for u, v, _ in arcs), "assignment has forbidden transition")
    completed = [w for u, v, w in arcs if (assignment[u], assignment[v]) in marked]
    need(set(code).issubset(completed), "completion lost original code word")
    _, _, new_counts = maximum_counts(r, completed)
    need(new_counts == counts, "completion changed count functions")
    return vertices, counts, assignment, completed, new_counts


def fixture(name, r, code, target):
    code = sorted(tuple(w) for w in code)
    maximum, witness = literal_strictness(r, code)
    signature = local_signature(code)
    need((maximum <= 2) == all(a + b >= 5 for _, a, b in signature), "local criterion disagrees with literal windows")
    need(maximum <= 2, "fixture is not strict")
    vertices, counts, assignment, completed, new_counts = completion(r, code, target)
    new_maximum, new_witness = literal_strictness(r, completed)
    need(new_maximum <= 2 and new_maximum == max(new_counts[5]), "completed code is not literally strict")
    need(maximum == max(counts[5]), "literal windows disagree with raw path counts")
    _, _, _, second, _ = completion(r, completed, target)
    need(second == completed, "completion is not idempotent")
    return {
        "name": name,
        "alphabet": r,
        "word_length": 4,
        "window_word_length": 8,
        "code": [list(w) for w in code],
        "strict_maximum": maximum,
        "strict_witness": witness,
        "local_signature": signature,
        "triple_states": [list(v) for v in vertices],
        "path_counts_before": counts,
        "assignment": assignment,
        "completed_code": [list(w) for w in completed],
        "completed_strict_maximum": new_maximum,
        "completed_strict_witness": new_witness,
        "path_counts_after": new_counts,
    }


def fresh_certificate():
    need(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256, "review source hash mismatch")
    target = derive_target()
    profiles, heights, allowed, marked = target
    dp = target_walks(len(profiles), allowed, marked)
    need(max(dp[5]) <= 2, "target walk has three marked edges")
    need(all(dp[t][v] <= heights[v][t] for t in range(6) for v in range(len(profiles))), "target DP exceeds profile heights")
    ternary = [w for w in words(3, 4) if w[0] <= w[2] and w[1] > w[3]]
    fixtures = [
        fixture("one-letter empty", 1, [], target),
        fixture("binary empty", 2, [], target),
        fixture("binary singleton", 2, [(0, 0, 0, 1)], target),
        fixture("binary three-word strict template", 2, [(0, 1, 0, 0), (0, 1, 1, 0), (1, 1, 1, 0)], target),
        fixture("ternary seven-word subcode", 3, ternary[:7], target),
        fixture("ternary eighteen-word strict template", 3, ternary, target),
    ]
    return {
        "schema": "independent-fourteen-state-v1",
        "source_sha256": SOURCE_SHA256,
        "definitions": {"word_length": 4, "state_length": 3, "walk_length": 5, "occurrences_count_with_multiplicity": True},
        "profiles": [list(p) for p in profiles],
        "height_sequences": heights,
        "allowed": [list(e) for e in allowed],
        "marked": [list(e) for e in marked],
        "target_path_counts": dp,
        "fixtures": fixtures,
    }


def validate_certificate(cert, expected):
    need(cert == expected, "certificate disagrees with independent reconstruction")


def negative_checks(expected):
    passed = []

    def rejects(name, action):
        try:
            action()
        except Rejected:
            passed.append(name)
        else:
            raise Rejected("negative control accepted: " + name)

    target = derive_target()
    for code, label in [([(0, 0, 0, 0)], "constant selected word"), ([(0, 1, 0, 1)], "period-two selected word"),
                        ([(0, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 1)], "three overlapping distinct words")]:
        maximum, _ = literal_strictness(2, code)
        need(maximum >= 3, "intended non-strict negative lacks witness")
        need(any(a + b <= 4 for _, a, b in local_signature(code)), "local criterion missed non-strict negative")
        rejects(label, lambda code=code: completion(2, code, target))
    rejects("word length mismatch", lambda: maximum_counts(2, [(0, 0, 1)]))
    rejects("alphabet binding mismatch", lambda: maximum_counts(2, [(0, 1, 2, 0)]))
    rejects("duplicate input listing", lambda: maximum_counts(2, [(0, 0, 0, 1), (0, 0, 0, 1)]))
    mutations = [
        ("profile time corruption", lambda c: c["height_sequences"][0].__setitem__(1, 0)),
        ("parameter field corruption", lambda c: c["definitions"].__setitem__("walk_length", 4)),
        ("source binding corruption", lambda c: c.__setitem__("source_sha256", "0" * 64)),
        ("literal-object corruption", lambda c: c["fixtures"][2]["code"].append([0, 0, 0, 0])),
        ("path-count corruption", lambda c: c["fixtures"][2]["path_counts_before"][1].__setitem__(0, 4)),
        ("assignment corruption", lambda c: c["fixtures"][2]["assignment"].__setitem__(0, 99)),
        ("completion corruption", lambda c: c["fixtures"][2]["completed_code"].append([0, 0, 0, 0])),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(expected)
        mutate(changed)
        rejects(name, lambda changed=changed: validate_certificate(changed, expected))
    profiles, _, allowed, marked = target
    loop = profiles.index((4, 6))
    need((loop, loop) in allowed and (loop, loop) not in marked, "negative loop choice invalid")
    corrupt_dp = target_walks(len(profiles), allowed, marked + [(loop, loop)])
    need(max(corrupt_dp[5]) >= 5, "spurious marked loop not exposed")
    rejects("spurious marked loop", lambda: need(max(corrupt_dp[5]) <= 2, "five marked repetitions"))
    return passed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write a new certificate; refuses to replace an existing file")
    parser.add_argument("--verify", type=Path, help="reconstruct and compare an existing certificate")
    args = parser.parse_args()
    need(not (args.write and args.verify), "choose either write or verify")
    cert = fresh_certificate()
    if args.verify:
        validate_certificate(json.loads(args.verify.read_text()), cert)
    negatives = negative_checks(cert)
    if args.write:
        with args.write.open("x") as stream:
            json.dump(cert, stream, indent=2, sort_keys=True)
            stream.write("\n")
    print("PASS: source SHA256 " + SOURCE_SHA256)
    print("PASS: independent hit-sequence classification: 14 profiles")
    print("PASS: all 196 ordered profile pairs: 138 allowed, 20 marked")
    print("PASS: five-step target walk maximum = 2; every shorter profile bound holds")
    for f in cert["fixtures"]:
        print("PASS: {name}; alphabet={alphabet}; |C|={old}; |completion|={new}; literal maximum={mx}".format(
            **f, old=len(f["code"]), new=len(f["completed_code"]), mx=f["completed_strict_maximum"]))
    print("PASS: containment, every F_0..F_5, and idempotence in every fixture")
    print("PASS: " + str(len(negatives)) + " negative controls: " + "; ".join(negatives))
    if args.verify:
        print("PASS: certificate exactly replays from literal inputs")
    if args.write:
        print("WROTE: " + args.write.name)
    print("SCOPE: proof/semantic checks, no claim to compute an optimum or to compile Lean")


if __name__ == "__main__":
    main()
