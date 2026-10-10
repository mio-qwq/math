#!/usr/bin/env python3
"""Independent, fixed-parameter exact audit of the original Pe(6,3) conjecture.

Source: https://arxiv.org/html/2604.15909v1#S3.SS3 (read 2026-10-10).
The whole OLD word, including its dropped first symbol, excludes the new symbol.
No external certificate, solver, network access, third-party module, floating
point operation, optimization search, or variable-parameter scan is used here.
Run this file with Python 3; its only output file is the sibling .json report.
"""

from collections import Counter, deque
from datetime import datetime, timezone
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import platform
import sys
from time import perf_counter_ns


D = 6
K = 3
ALPHABET = tuple(range(D + K))
LOW = frozenset((0, 1, 2))
HIGH = frozenset(range(3, 9))
SOURCE_URL = "https://arxiv.org/html/2604.15909v1#S3.SS3"


class VerificationError(Exception):
    def __init__(self, code, **details):
        super().__init__(code)
        self.details = {"code": code, **details}


def require(condition, code, **details):
    if not condition:
        raise VerificationError(code, **details)


def digest(value):
    """SHA256 of deterministic compact JSON; all mathematical values are ints."""
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"))
                  .encode("ascii")).hexdigest()


def original_arc(source, target):
    # Deliberately test the full source, not merely its surviving suffix.
    return source[1:] == target[:-1] and target[-1] not in source


def build_graph():
    vertices = tuple(permutations(ALPHABET, K))
    # Inspect all 504^2 ordered pairs against the literal original definition.
    adjacency = tuple(tuple(j for j, target in enumerate(vertices)
                            if original_arc(source, target))
                      for source in vertices)
    return vertices, adjacency


def audit_graph(vertices, adjacency):
    require(len(vertices) == 504 and len(set(vertices)) == 504,
            "wrong_vertex_count")
    vertex_set = set(vertices)
    # Independently regenerate words with explicit Cartesian loops.
    expected = {(a, b, c) for a in ALPHABET for b in ALPHABET
                for c in ALPHABET if a != b and a != c and b != c}
    require(vertex_set == expected, "wrong_vertex_universe")
    require(len(adjacency) == len(vertices), "wrong_adjacency_length")
    index = {word: i for i, word in enumerate(vertices)}
    indegrees = [0] * len(vertices)
    for i, word in enumerate(vertices):
        require(len(adjacency[i]) == len(set(adjacency[i])),
                "duplicate_arc", source=word)
        require(all(type(j) is int and 0 <= j < len(vertices)
                    for j in adjacency[i]), "invalid_arc_index", source=word)
        actual_targets = {vertices[j] for j in adjacency[i]}
        # Independent append-based generation, as opposed to pair matching.
        expected_targets = {(word[1], word[2], letter) for letter in ALPHABET
                            if all(letter != old for old in word)}
        require(actual_targets == expected_targets, "arc_relation_mismatch",
                source=word,
                unexpected=sorted(actual_targets - expected_targets),
                missing=sorted(expected_targets - actual_targets))
        require(len(adjacency[i]) == D, "wrong_outdegree", source=word)
        for j in adjacency[i]:
            require(i != j, "loop", source=word)
            indegrees[j] += 1
    require(set(indegrees) == {D}, "wrong_indegrees")
    return index


def all_pairs_bfs(adjacency):
    distances = []
    for source in range(len(adjacency)):
        row = [-1] * len(adjacency)
        row[source] = 0
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for target in adjacency[current]:
                if row[target] == -1:
                    row[target] = row[current] + 1
                    queue.append(target)
        require(all(type(d) is int and d >= 0 for d in row),
                "unreachable_vertex", source_index=source)
        require(row[source] == 0 and row.count(0) == 1,
                "bad_bfs_zero", source_index=source)
        # Independently certify each BFS row: edge triangle inequalities and
        # a predecessor with distance one less for every non-source vertex.
        has_predecessor = [False] * len(adjacency)
        has_predecessor[source] = True
        for u, targets in enumerate(adjacency):
            for v in targets:
                require(row[v] <= row[u] + 1, "bad_bfs_edge_inequality",
                        source_index=source, u=u, v=v)
                if row[v] == row[u] + 1:
                    has_predecessor[v] = True
        require(all(has_predecessor), "bad_bfs_predecessor",
                source_index=source)
        distances.append(tuple(row))
    return tuple(distances)


def gp_statistics(words, index, distances):
    require(len(words) == len(set(words)), "duplicate_candidate_vertex")
    require(all(word in index for word in words), "invalid_candidate_vertex")
    ids = [index[word] for word in words]
    checked = 0
    violations = 0
    first_violation = None
    slack_counts = Counter()
    # Ordered (source, intermediate, target); all three vertices distinct.
    # Finite integer equality is exactly membership of a directed geodesic.
    for u in ids:
        for w in ids:
            if w == u:
                continue
            for v in ids:
                if v == u or v == w:
                    continue
                checked += 1
                duv = distances[u][v]
                duw = distances[u][w]
                dwv = distances[w][v]
                slack = duw + dwv - duv
                require(slack >= 0, "distance_triangle_failure")
                slack_counts[slack] += 1
                if slack == 0:
                    violations += 1
                    if first_violation is None:
                        first_violation = {
                            "source": words[ids.index(u)],
                            "intermediate": words[ids.index(w)],
                            "target": words[ids.index(v)],
                            "source_target_distance": duv,
                            "source_intermediate_distance": duw,
                            "intermediate_target_distance": dwv,
                        }
    require(checked == len(words) * (len(words) - 1) * (len(words) - 2),
            "incomplete_triple_enumeration")
    return {"ordered_distinct_triples_checked": checked,
            "geodesic_violations": violations,
            "first_violation": first_violation,
            "slack_histogram": dict(sorted(slack_counts.items()))}


def audit_gp(words, index, distances):
    result = gp_statistics(words, index, distances)
    require(result["geodesic_violations"] == 0,
            "not_in_general_position", **result)
    return result


def reject_control(name, callback):
    try:
        callback()
    except VerificationError as error:
        return {"name": name, "actually_rejected": True, **error.details}
    raise VerificationError("negative_control_was_accepted", name=name)


def audit_five_step_paths(words, index, adjacency):
    checked = 0
    for u in words:
        for v in words:
            if u == v:
                continue
            a, b, t = u
            c, e, s = v
            spare = sorted(HIGH - {a, b, c, e})
            require(len(spare) >= 2, "insufficient_spare_symbols")
            x, y = spare[:2]
            path = [u, (b, t, x), (t, x, y), (x, y, c), (y, c, e), v]
            require(len(set(path)) == 6, "five_step_witness_repeats_vertex",
                    source=u, target=v)
            for left, right in zip(path, path[1:]):
                require(index[right] in adjacency[index[left]],
                        "five_step_witness_has_nonarc", left=left, right=right)
            checked += 1
    return checked


def main():
    start = perf_counter_ns()
    vertices, adjacency = build_graph()
    index = audit_graph(vertices, adjacency)
    distances = all_pairs_bfs(adjacency)
    candidate = tuple((a, b, t) for a in sorted(HIGH) for b in sorted(HIGH)
                      if a != b for t in sorted(LOW))
    require(len(candidate) == 90, "wrong_candidate_cardinality")
    gp = audit_gp(candidate, index, distances)
    pair_histogram = Counter(distances[index[u]][index[v]]
                             for u in candidate for v in candidate if u != v)
    require(sum(pair_histogram.values()) == 8010, "incomplete_pair_enumeration")
    require(min(pair_histogram) == 3 and max(pair_histogram) == 5,
            "claimed_pair_distance_range_is_false")
    witness_count = audit_five_step_paths(candidate, index, adjacency)
    require(witness_count == 8010, "incomplete_five_step_witness_check")

    # Wrong control 1: dropping x1 does NOT license immediate reuse of x1.
    wrong_adjacency = list(adjacency)
    wrong_source = index[(0, 1, 2)]
    wrong_target = index[(1, 2, 0)]
    require(wrong_target not in wrong_adjacency[wrong_source],
            "control_edge_already_present")
    wrong_adjacency[wrong_source] = adjacency[wrong_source] + (wrong_target,)
    control_graph = reject_control(
        "illegally_allow_the_dropped_first_letter",
        lambda: audit_graph(vertices, tuple(wrong_adjacency)))

    # Wrong control 2: keep 90 valid graph vertices but insert a true geodesic
    # midpoint. The callback uses the SAME exhaustive general-position check.
    # Known obstruction: (3,4,0) -> (4,0,5) -> (0,5,6) -> (5,6,1).
    midpoint = (4, 0, 5)
    wrong_candidate = tuple(sorted(set(candidate) - {(8, 7, 2)} | {midpoint}))
    require(len(wrong_candidate) == 90 and midpoint not in candidate,
            "malformed_wrong_candidate_control")
    control_set = reject_control(
        "replace_one_candidate_vertex_by_a_geodesic_midpoint",
        lambda: audit_gp(wrong_candidate, index, distances))
    control_set["known_obstruction"] = {
        "source": [3, 4, 0], "intermediate": list(midpoint),
        "target": [5, 6, 1],
        "distance_equation": [distances[index[(3, 4, 0)]][index[(5, 6, 1)]],
                              distances[index[(3, 4, 0)]][index[midpoint]],
                              distances[index[midpoint]][index[(5, 6, 1)]]],
    }
    require(control_set["known_obstruction"]["distance_equation"] == [3, 1, 2],
            "wrong_control_obstruction")

    conjectured_value = 2
    for i in range(K - 1):
        conjectured_value *= D + K - 2 - i
    require(K >= 3 and D >= 2 * K and conjectured_value == 84,
            "outside_original_conjecture_domain")
    require(len(candidate) > conjectured_value, "not_a_counterexample")
    edges = [(i, j) for i, targets in enumerate(adjacency) for j in targets]
    pair_witnesses = {}
    for u in candidate:
        for v in candidate:
            if u != v:
                length = distances[index[u]][index[v]]
                if length not in pair_witnesses:
                    pair_witnesses[length] = {"source": u, "target": v}
    script = Path(__file__).resolve()
    report = {
        "status": "PASS",
        "audit_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "script_sha256": sha256(script.read_bytes()).hexdigest(),
        "source": {"original_version": "arXiv:2604.15909v1",
                   "original_definition_url": SOURCE_URL,
                   "target": "unnumbered exactness conjecture after Theorem 3.6",
                   "original_gp_definition": "Definition 2.1",
                   "source_checked_on": "2026-10-10",
                   "latest_abs_history_observed": "v1 only; 2026-04-17 10:10:49 UTC",
                   "historical_priority_gate": "not established by this audit"},
        "parameters": {"d": D, "k": K, "alphabet": ALPHABET},
        "graph": {"vertex_count": len(vertices), "arc_count": len(edges),
                  "all_ordered_vertex_pairs_tested": len(vertices) ** 2,
                  "indegree": D, "outdegree": D,
                  "all_pairs_integer_bfs_rows": len(distances),
                  "strongly_connected": True,
                  "computed_directed_diameter": max(map(max, distances)),
                  "vertex_order_sha256": digest(vertices),
                  "indexed_arc_list_sha256": digest(edges),
                  "all_pairs_distance_matrix_sha256": digest(distances)},
        "candidate": {"definition": "(a,b,t): 3<=a,b<=8, a!=b, 0<=t<=2",
                      "cardinality": len(candidate), "vertices": candidate,
                      "candidate_sha256": digest(candidate),
                      "ordered_distinct_pair_count": 8010,
                      "pair_distance_histogram": dict(sorted(pair_histogram.items())),
                      "distance_witness_pairs": pair_witnesses,
                      "verified_five_step_paths": witness_count,
                      "distance_matrix_in_listed_order":
                          [[distances[index[u]][index[v]] for v in candidate]
                           for u in candidate]},
        "general_position": gp,
        "negative_controls": [control_graph, control_set],
        "mathematical_conclusion": {
            "proved_by_this_exact_audit": "gp(Pe(6,3)) >= 90 > 84",
            "conjectured_value": conjectured_value,
            "original_exactness_conjecture_violated": True,
            "Theorem_3_6_lower_bound_contradicted": False,
            "maximum_general_position_number_determined": False,
            "smallest_counterexample_determined": False,
            "novelty_or_priority_claimed": False,
            "Lean_checked": False},
        "elapsed_nanoseconds": perf_counter_ns() - start,
    }
    output = script.with_suffix(".json")
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    print(json.dumps({"status": report["status"],
                      "vertex_count": len(vertices), "arc_count": len(edges),
                      "candidate_count": len(candidate),
                      "ordered_triples_checked": gp["ordered_distinct_triples_checked"],
                      "geodesic_violations": gp["geodesic_violations"],
                      "pair_distance_histogram": dict(sorted(pair_histogram.items())),
                      "controls_rejected": len(report["negative_controls"]),
                      "conclusion": report["mathematical_conclusion"]["proved_by_this_exact_audit"],
                      "output": str(output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except VerificationError as error:
        print(json.dumps({"status": "FAIL", **error.details}, sort_keys=True),
              file=sys.stderr)
        sys.exit(1)
