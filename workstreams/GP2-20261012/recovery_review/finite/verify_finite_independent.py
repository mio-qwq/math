#!/usr/bin/env python3
"""Independent, exact review of the fixed GP2 six-letter certificate.

Uses no GP2 Python imports or optimization packages. Hyperedges are rebuilt by
gap-compatible joins of forced four-letter words rather than enumerating all
eight-letter words. Strictness is cross-checked by literal eight-letter windows.
All acceptance conditions use explicit exceptions, including under python -O.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT = HERE.parents[1] / "stage2" / "forced_cover_certificate.json"
LEVELS = (
    (1, 2, 0, 1, 2, 0),
    (0, 1, 2, 1, 1, 0),
    (2, 0, 1, 2, 2, 1),
    (1, 2, 1, 1, 0, 0),
    (1, 0, 2, 1, 0, 0),
    (1, 0, 2, 2, 2, 2),
)


class InvalidCertificate(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def word(raw, length, n):
    need(isinstance(raw, (list, tuple)) and len(raw) == length,
         "wrong word length")
    need(all(type(a) is int and 0 <= a < n for a in raw),
         "word letter outside the integer alphabet")
    return tuple(raw)


def unrank(k, n, length):
    values = []
    for _ in range(length):
        k, a = divmod(k, n)
        values.append(a)
    return tuple(reversed(values))


def rank(w, n):
    k = 0
    for a in w:
        k = n * k + a
    return k


def reconstruct_orbits(n, levels):
    """Integer cyclic rotations, with every word represented once."""
    seen = set()
    all_orbits, viable, forced = [], [], set()
    power = n ** 3
    for k in range(n ** 4):
        if k in seen:
            continue
        rotations, j = set(), k
        for _ in range(4):
            rotations.add(j)
            leading, tail = divmod(j, power)
            j = n * tail + leading
        seen.update(rotations)
        orbit = tuple(unrank(j, n, 4) for j in sorted(rotations))
        all_orbits.append(orbit)
        candidates = tuple(w for w in orbit
                           if levels[n * w[0] + w[1]] < levels[n * w[2] + w[3]])
        if candidates:
            need(len(orbit) == 4 and len(candidates) <= 2,
                 "nonprimitive or more than two candidates")
            viable.append(candidates)
            if len(candidates) == 1:
                forced.add(candidates[0])
    need(len(seen) == n ** 4, "rotation partition is incomplete")
    return all_orbits, viable, forced


def reconstruct_edges(forced):
    """Three selected occurrences: positive gaps a,b with a+b<=4.

    u[a:]==v[:4-a] and v[b:]==w[:4-b] suffice, because every
    intersection of the outer windows is contained in the middle window.
    The shifted start positions can be padded to an eight-letter word.
    Edge values are sets, so repeated word occurrences count correctly.
    """
    prefixes = {d: defaultdict(list) for d in (1, 2, 3)}
    suffixes = {d: defaultdict(list) for d in (1, 2, 3)}
    for w in sorted(forced):
        for d in (1, 2, 3):
            prefixes[d][w[:4-d]].append(w)
            suffixes[d][w[d:]].append(w)
    edges, witnesses, gap_counts = set(), {}, {}
    for a in (1, 2, 3):
        for b in range(1, 5-a):
            count = 0
            for v in sorted(forced):
                for u in suffixes[a][v[:4-a]]:
                    for w in prefixes[b][v[b:]]:
                        seq = u + v[4-a:] + w[4-b:]
                        need(seq[:4] == u and seq[a:a+4] == v
                             and seq[a+b:a+b+4] == w,
                             "joined windows failed literal reconstruction")
                        edge = frozenset((u, v, w))
                        edges.add(edge)
                        witnesses.setdefault(edge, (seq, (0, a, a+b)))
                        count += 1
            gap_counts[f"{a},{b}"] = count
    return edges, witnesses, gap_counts


def first_literal_violation(n, code):
    """Exhaust all original eight-letter words; no DP or solver."""
    for x in itertools.product(range(n), repeat=8):
        selected_starts = [i for i in range(5) if x[i:i+4] in code]
        if len(selected_starts) >= 3:
            return x, selected_starts
    return None


def digest_edges(n, edges):
    encoded = sorted(tuple(sorted(rank(w, n) for w in e)) for e in edges)
    payload = json.dumps(encoded, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def verify(document, literal=True):
    need(isinstance(document, dict), "top-level JSON is not an object")
    need(document.get("schema") == "GP2-forced-cover-v1", "unknown schema")
    n = document.get("n")
    need(type(n) is int and n == 6, "this certificate is for six letters")
    levels = document.get("levels")
    need(isinstance(levels, list) and len(levels) == n*n,
         "level array has incorrect dimensions")
    need(all(type(v) is int and v in (0, 1, 2) for v in levels),
         "levels are not integers in {0,1,2}")
    need(levels == [v for row in LEVELS for v in row],
         "certificate is not bound to the published fixed level array")
    all_orbits, viable, forced = reconstruct_orbits(n, levels)
    need(len(viable) == document.get("viable_orbits") == 310,
         "viable rotation count mismatch")
    need(len(forced) == document.get("forced_words") == 189,
         "unique-candidate word count mismatch")
    edges, witnesses, gap_counts = reconstruct_edges(forced)
    need(len(edges) == document.get("hyperedge_count") == 7919,
         "hyperedge count mismatch")
    histogram = dict(sorted(Counter(map(len, edges)).items()))
    need(histogram == {2: 41, 3: 7878}, "unexpected edge rank histogram")
    need(document.get("rank_histogram") == {str(k): v for k, v in histogram.items()},
         "saved edge rank histogram mismatch")

    raw_cover = document.get("cover")
    need(isinstance(raw_cover, list), "cover is not a list")
    cover_list = [word(w, 4, n) for w in raw_cover]
    cover = set(cover_list)
    need(len(cover_list) == len(cover) == 64, "cover is not 64 distinct words")
    need(cover <= forced, "cover contains a non-forced word")
    need(all(e & cover for e in edges), "cover misses a forbidden configuration")
    if literal:
        need(first_literal_violation(n, forced-cover) is None,
             "remaining forced set fails literal five-window strictness")

    matching = document.get("disjoint_matching")
    need(isinstance(matching, list) and len(matching) == 64,
         "matching does not have 64 records")
    used, matching_ranks = set(), Counter()
    for rec in matching:
        need(isinstance(rec, dict), "matching record is not an object")
        seq = word(rec.get("word8"), 8, n)
        starts = rec.get("starts")
        need(isinstance(starts, list) and len(starts) == 3
             and len(set(starts)) == 3
             and all(type(i) is int and 0 <= i <= 4 for i in starts),
             "matching must have three distinct valid occurrences")
        declared = rec.get("forbidden_words")
        need(isinstance(declared, list), "forbidden word support is not a list")
        support = frozenset(word(w, 4, n) for w in declared)
        need(support == frozenset(seq[i:i+4] for i in starts),
             "matching support differs from actual window occurrences")
        need(support in edges and support <= forced,
             "matching record is not a true forced-word hyperedge")
        need(not support & used, "matching hyperedges share a vertex")
        used.update(support)
        matching_ranks[len(support)] += 1
    need(len(used) == 187 and dict(matching_ranks) == {2: 5, 3: 59},
         "matching rank or vertex count mismatch")

    # A size-64 disjoint matching and size-64 cover squeeze the optimum;
    # no floating-point arithmetic or optimizer is used.
    need(len(matching) == len(cover), "primal and dual integer witnesses differ")
    rotation_bound = Fraction(len(viable), n**4)
    loss = Fraction(len(cover), n**4)
    upper = rotation_bound-loss
    need(upper == Fraction(41, 216), "exact fixed-array upper fraction mismatch")
    return {
        "scope": "all strict C contained in V_ell for the published fixed array",
        "alphabet_size": n,
        "all_rotation_orbits": len(all_orbits),
        "viable_primitive_orbits": len(viable),
        "one_candidate_orbits": len(forced),
        "two_candidate_orbits": sum(len(o) == 2 for o in viable),
        "hyperedges": len(edges),
        "edge_rank_histogram": histogram,
        "gap_occurrence_counts": gap_counts,
        "cover_size": len(cover),
        "matching_size": len(matching),
        "matching_rank_histogram": dict(sorted(matching_ranks.items())),
        "matching_used_vertices": len(used),
        "minimum_vertex_cover": len(cover),
        "rotation_bound": str(rotation_bound),
        "forced_loss": str(loss),
        "fixed_array_upper": str(upper),
        "hypergraph_sha256": digest_edges(n, edges),
        "literal_eight_letter_strictness_checked": literal,
    }


def self_test(document):
    """Actually call the acceptance function on independently damaged data."""
    def change_level_out(d): d["levels"][0] = 3
    def change_level_in(d): d["levels"][0] = 0
    def remove_cover(d): d["cover"].pop()
    def duplicate_cover(d): d["cover"][0] = d["cover"][1]
    def invalid_letter(d): d["disjoint_matching"][0]["word8"][0] = 6
    def invalid_parameter(d): d["n"] = 5
    def repeated_starts(d): d["disjoint_matching"][0]["starts"][0] = d["disjoint_matching"][0]["starts"][1]
    def mismatched_support(d): d["disjoint_matching"][0]["forbidden_words"].pop()
    def overlapping_matching(d): d["disjoint_matching"][1] = d["disjoint_matching"][0]
    def wrong_edge_count(d): d["hyperedge_count"] -= 1
    def wrong_histogram(d): d["rank_histogram"]["2"] -= 1
    def boolean_letter(d): d["cover"][0][0] = bool(d["cover"][0][0])
    damage = (change_level_out, change_level_in, remove_cover, duplicate_cover,
              invalid_letter, invalid_parameter, repeated_starts, mismatched_support,
              overlapping_matching, wrong_edge_count, wrong_histogram, boolean_letter)
    results = []
    for mutation in damage:
        bad = copy.deepcopy(document)
        mutation(bad)
        try:
            verify(bad, literal=False)
        except InvalidCertificate as exc:
            results.append({"mutation": mutation.__name__, "rejected": str(exc)})
        else:
            raise InvalidCertificate("negative control was accepted: " + mutation.__name__)
    # Reintroduce every individual cover word: minimality must create an
    # explicit forbidden witness, even if cardinality guards were removed.
    n, levels = document["n"], document["levels"]
    _, _, forced = reconstruct_orbits(n, levels)
    edges, witnesses, _ = reconstruct_edges(forced)
    cover = {tuple(w) for w in document["cover"]}
    all_essential = []
    for removed in sorted(cover):
        smaller = cover-{removed}
        uncovered = next((e for e in edges if not e & smaller), None)
        need(uncovered is not None, "a cover member was not essential")
        seq, starts = witnesses[uncovered]
        seq = seq + (0,)*(8-len(seq))
        need(sum(seq[i:i+4] in forced-smaller for i in range(5)) >= 3,
             "essential-cover witness did not produce three selected occurrences")
        all_essential.append({"restored_word": list(removed), "word8": list(seq),
                              "starts": list(starts)})
    return {"acceptance_function_negative_controls": results,
            "all_64_cover_members_individually_essential": all_essential}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path, default=DEFAULT)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = args.certificate.read_bytes()
    document = json.loads(source)
    report = verify(document)
    report["certificate_sha256"] = hashlib.sha256(source).hexdigest()
    if args.self_test:
        report["negative_controls"] = self_test(document)
    output = json.dumps(report, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output)
    print("PASS: independent fixed six-letter certificate review")
    print(json.dumps({k: v for k, v in report.items() if k != "negative_controls"},
                     sort_keys=True))
    if args.self_test:
        print("PASS: 12 damaged certificates rejected through acceptance function")
        print("PASS: 64 individually restored cover words have literal violation witnesses")


if __name__ == "__main__":
    main()
