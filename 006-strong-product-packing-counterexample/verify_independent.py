"""Independent exact Q6 packing-complex replay.  No imported project checker.

The first phase builds and checks everything without reading ROOT artifacts.
The second phase compares independently saved data with ROOT artifacts only.
All arithmetic is exact integer/set arithmetic; no solver or Lean is invoked.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def save(path, obj):
    path = Path(path)
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")) + "\n", encoding="utf-8")
    return digest(path)


def rho(a, b):
    assert 0 <= a < 64 and 0 <= b < 64
    return (a ^ b).bit_count()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def label(kind, support):
    return kind + ":" + ",".join(map(str, support))


def independently_build_and_check(out):
    started = utc()
    source_hash = digest(__file__)
    # The directory is new.  No ROOT graph or certificate is opened here.
    out.mkdir(parents=False, exist_ok=False)
    save(out / "status.json", {"status": "IN_PROGRESS", "started_utc": started,
                              "source_sha256": source_hash})
    nodes = []
    for kind in ("A", "S"):
        for a in range(64):
            nodes.append({"id": len(nodes), "kind": kind, "support": [a],
                          "label": label(kind, [a])})
    for a, b in combinations(range(64), 2):
        if rho(a, b) == 4:
            nodes.append({"id": len(nodes), "kind": "E", "support": [a, b],
                          "label": label("E", [a, b])})
    size = len(nodes)
    require(size == 608, "expected exactly 608 nodes")
    require(Counter(n["kind"] for n in nodes) == {"A": 64, "S": 64, "E": 480},
            "wrong node types or distance-four unordered pairs")
    require(len({n["label"] for n in nodes}) == size, "duplicate node")

    # First construction: incidence edges, then compatibility of supports.
    edges = set()
    for n in nodes[64:]:
        for a in n["support"]:
            edges.add((a, n["id"]))
    for left, right in combinations(nodes[64:], 2):
        words = sorted(set(left["support"]) | set(right["support"]))
        if all(rho(a, b) >= 4 for a, b in combinations(words, 2)):
            edges.add((left["id"], right["id"]))
    edges = sorted(tuple(sorted(e)) for e in edges)
    adjacency = [set() for _ in nodes]
    for a, b in edges:
        require(a != b, "self loop")
        adjacency[a].add(b)
        adjacency[b].add(a)

    # Second independently expressed predicate: every possible unordered pair.
    # Distinct words are quantified; shared endpoints do not create a loop.
    def should_be_adjacent(i, j):
        if i == j:
            return False
        ni, nj = nodes[i], nodes[j]
        if ni["kind"] == "A":
            return nj["kind"] != "A" and ni["support"][0] in nj["support"]
        if nj["kind"] == "A":
            return nj["support"][0] in ni["support"]
        merged = set(ni["support"]).union(nj["support"])
        for x in merged:
            for y in merged:
                if x != y and rho(x, y) < 4:
                    return False
        return True

    checked_pairs = 0
    for i in range(size):
        require(i not in adjacency[i], "loop in adjacency")
        for j in range(i + 1, size):
            expected = should_be_adjacent(i, j)
            require((j in adjacency[i]) == expected, "missing or spurious edge")
            require((i in adjacency[j]) == expected, "asymmetric adjacency")
            checked_pairs += 1
    require(checked_pairs == size * (size - 1) // 2, "incomplete adjacency audit")
    require(not any(b < 64 for a, b in edges), "A--A edge")

    breakdown = Counter()
    for a, b in edges:
        breakdown["-".join(sorted([nodes[a]["kind"], nodes[b]["kind"]]))] += 1
    require(breakdown == {"A-S": 64, "A-E": 960, "S-S": 704,
                          "E-S": 3840, "E-E": 3600}, "edge-type count mismatch")

    # Actual graph metric: full BFS from every one of the 608 nodes.
    distances = []
    bfs_relaxations = 0
    for start in range(size):
        row = [-1] * size
        row[start] = 0
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for nxt in adjacency[current]:
                bfs_relaxations += 1
                if row[nxt] == -1:
                    row[nxt] = row[current] + 1
                    queue.append(nxt)
        require(all(d >= 0 for d in row), "H disconnected")
        distances.append(row)
    # An independent shortest-distance certificate, beyond trusting BFS code:
    # symmetry, edge Lipschitz, and a descending adjacent vertex to every target.
    for start, row in enumerate(distances):
        require(row[start] == 0, "nonzero diagonal")
        for target in range(size):
            require(row[target] == distances[target][start], "asymmetric metric")
            if target != start:
                require(row[target] > 0 and
                        any(row[v] == row[target] - 1 for v in adjacency[target]),
                        "distance lacks descending-path certificate")
        for a, b in edges:
            require(abs(row[a] - row[b]) <= 1, "distance violates edge Lipschitz")

    # All 2016 distinct candidate pairs; actual strong-product distance is max.
    packing = []
    for a, b in combinations(range(64), 2):
        first = rho(a, b)
        second = distances[a][b]
        product = max(first, second)
        require(product >= 4, "product centers violate the p=3 packing condition")
        # This extra exact pattern tests the alleged length-two/three shortcuts.
        expected_h = 4 if first <= 3 else (2 if first == 4 else 3)
        require(second == expected_h, "unexpected exact A-center shortest path")
        packing.append({"a": a, "b": b, "d_q6": first,
                        "d_h": second, "d_product": product})
    require(len(packing) == 2016, "incomplete packing audit")

    # Same a is used in BOTH factors.  All 64*608 product targets are checked.
    witnesses = []
    reach = []
    first_ball = [{a for a in range(64) if rho(x, a) <= 2} for x in range(64)]
    for h in range(size):
        reachable = {a for a in range(64) if distances[h][a] <= 2}
        require(reachable, "no center label reachable from H vertex")
        reach.append(sorted(reachable))
        for x in range(64):
            common = first_ball[x].intersection(reachable)
            require(common, "no same-center radius-two covering witness")
            a = min(common)
            witnesses.append({"x": x, "h": h, "a": a,
                              "d_q6": rho(x, a), "d_h": distances[h][a]})
    require(len(witnesses) == 64 * size, "incomplete covering audit")

    # Check written sufficient label sets separately from actual BFS witnesses.
    for h, n in enumerate(nodes):
        supp = n["support"]
        if n["kind"] in ("A", "S"):
            a = supp[0]
            sufficient = {a} | {c for c in range(64) if rho(a, c) == 4}
        else:
            a, b = supp
            far = {c for c in range(64) if rho(a, c) >= 4 and rho(b, c) >= 4}
            require(len(far) == 6, "E pair does not have six common far words")
            sufficient = {a, b} | far
            require(len(sufficient) == 8, "wrong E sufficient label set")
        require(sufficient <= set(reach[h]), "written sufficient set not within H ball")
        for x in range(64):
            require(any(rho(x, a) <= 2 for a in sufficient),
                    "written sufficient first-label set fails to cover Q6")

    paths = {}
    paths["graph-independent.json"] = save(out / "graph-independent.json", {
        "nodes": nodes, "edges": [list(e) for e in edges],
        "adjacency": [sorted(v) for v in adjacency]})
    paths["distances-independent.json"] = save(out / "distances-independent.json", distances)
    paths["packing-independent.json"] = save(out / "packing-independent.json", packing)
    paths["coverage-independent.json"] = save(out / "coverage-independent.json", witnesses)
    paths["reachable-labels-independent.json"] = save(out / "reachable-labels-independent.json", reach)
    ended = utc()
    result = {"status": "OWN_EXACT_PASS_ROOT_COMPARISON_PENDING",
              "started_utc": started, "ended_utc": ended,
              "source_sha256": source_hash, "python": sys.version,
              "node_count": size, "node_type_counts": dict(Counter(n["kind"] for n in nodes)),
              "edge_count": len(edges), "edge_type_counts": dict(breakdown),
              "proper_unordered_adjacency_pairs_checked": checked_pairs,
              "bfs_rows": len(distances), "bfs_distance_entries": size * size,
              "bfs_relaxations": bfs_relaxations,
              "connected": True, "graph_diameter": max(map(max, distances)),
              "packing_pairs_checked": len(packing),
              "minimum_product_center_distance": min(p["d_product"] for p in packing),
              "same_center_covering_targets_checked": len(witnesses),
              "minimum_reachable_center_labels": min(map(len, reach)),
              "maximum_reachable_center_labels": max(map(len, reach)),
              "artifact_sha256": paths,
              "root_artifacts_read": False,
              "claim_scope": "Independent finite graph and exact candidate checks; not a Lean kernel proof or a priority claim."}
    result_hash = save(out / "result-independent.json", result)
    save(out / "status.json", {"status": result["status"], "ended_utc": ended,
                              "result_sha256": result_hash})
    print(json.dumps({**result, "result_sha256": result_hash}, ensure_ascii=False, sort_keys=True))


def compare_root_artifacts(out, root):
    # This entry point may be called only after the independent phase succeeds.
    started = utc()
    source_hash = digest(__file__)
    result = json.loads((out / "result-independent.json").read_text(encoding="utf-8"))
    require(result["status"] == "OWN_EXACT_PASS_ROOT_COMPARISON_PENDING", "own phase not PASS")
    for name, expected in result["artifact_sha256"].items():
        require(digest(out / name) == expected, "own artifact changed before comparison")
    save(out / "comparison-status.json", {"status": "IN_PROGRESS", "started_utc": started,
                                         "source_sha256": source_hash})
    own_graph = json.loads((out / "graph-independent.json").read_text(encoding="utf-8"))
    own_distances = json.loads((out / "distances-independent.json").read_text(encoding="utf-8"))
    own_cover = json.loads((out / "coverage-independent.json").read_text(encoding="utf-8"))
    # First ROOT data access occurs only in this later comparison phase.
    root_graph_sha = digest(root / "graph.json")
    root_certificate_sha = digest(root / "certificate.json")
    root_graph = json.loads((root / "graph.json").read_text(encoding="utf-8"))
    root_cert = json.loads((root / "certificate.json").read_text(encoding="utf-8"))
    require(set(root_graph) == {"nodes", "adjacency"}, "unexpected ROOT graph schema")
    require(set(root_cert) == {"h_center_to_all_distances", "same_center_cover_witness"},
            "unexpected ROOT certificate schema")
    require(len(root_graph["nodes"]) == 608 and len(root_graph["adjacency"]) == 608,
            "ROOT node/adjacency count mismatch")

    # Canonical support/type matching allows arbitrary ROOT vertex numbering.
    canonical = {(n["kind"], tuple(n["support"])): n["id"] for n in own_graph["nodes"]}
    root_to_own = []
    for n in root_graph["nodes"]:
        require(set(n) == {"kind", "support"}, "unexpected ROOT node fields")
        require(n["kind"] in ("A", "S", "E") and isinstance(n["support"], list),
                "invalid ROOT node kind/support")
        require(all(type(x) is int and 0 <= x < 64 for x in n["support"]),
                "ROOT support contains a non-Q6 word")
        require(n["support"] == sorted(set(n["support"])), "ROOT support not proper unordered set")
        key = (n["kind"], tuple(n["support"]))
        require(key in canonical, "ROOT node not in independent graph")
        root_to_own.append(canonical[key])
    require(set(root_to_own) == set(range(608)), "ROOT missing or duplicated canonical node")
    root_edges = set()
    for i, row in enumerate(root_graph["adjacency"]):
        require(isinstance(row, list) and len(row) == len(set(row)), "ROOT adjacency duplicate")
        for j in row:
            require(type(j) is int and 0 <= j < 608 and i != j, "ROOT loop or bad vertex")
            require(i in root_graph["adjacency"][j], "ROOT asymmetric graph")
            root_edges.add(tuple(sorted((root_to_own[i], root_to_own[j]))))
    require(root_edges == {tuple(e) for e in own_graph["edges"]},
            "ROOT canonical edge set differs from independent graph")

    # ROOT stores only the 64 A-center BFS rows; compare each of its 38912 entries
    # with the independently computed and separately metric-certified full BFS.
    root_dist = root_cert["h_center_to_all_distances"]
    require(len(root_dist) == 64, "ROOT center-distance row count mismatch")
    for a, row in enumerate(root_dist):
        require(len(row) == 608, "ROOT center-distance column count mismatch")
        for rh, d in enumerate(row):
            require(type(d) is int and d == own_distances[a][root_to_own[rh]],
                    "ROOT BFS entry differs from independent shortest path")

    # Verify every supplied ROOT same-center witness against OUR two metrics.
    # A witness need not equal our minimum valid choice, so record agreement too.
    root_witness = root_cert["same_center_cover_witness"]
    require(len(root_witness) == 608, "ROOT covering row count mismatch")
    witness_exact_agreements = 0
    for rh, row in enumerate(root_witness):
        h = root_to_own[rh]
        require(len(row) == 64, "ROOT covering column count mismatch")
        for x, a in enumerate(row):
            require(type(a) is int and 0 <= a < 64, "ROOT witness is not a Q6 center label")
            require(rho(x, a) <= 2 and own_distances[h][a] <= 2,
                    "ROOT witness fails SAME-center coverage using independent BFS")
            ow = own_cover[64 * h + x]
            require(ow["h"] == h and ow["x"] == x, "own coverage record layout mismatch")
            if a == ow["a"]:
                witness_exact_agreements += 1
    require(digest(root / "graph.json") == root_graph_sha and
            digest(root / "certificate.json") == root_certificate_sha,
            "ROOT artifacts changed during comparison")
    ended = utc()
    comparison = {"status": "INDEPENDENT_EXACT_REPLAY_AND_ROOT_COMPARISON_PASS",
                  "started_utc": started, "ended_utc": ended,
                  "source_sha256": source_hash,
                  "own_phase_source_sha256": result["source_sha256"],
                  "own_result_sha256": digest(out / "result-independent.json"),
                  "root_graph_sha256": root_graph_sha,
                  "root_certificate_sha256": root_certificate_sha,
                  "canonical_nodes_matched": 608, "canonical_edges_matched": len(root_edges),
                  "root_vertex_numbering_identical": root_to_own == list(range(608)),
                  "root_center_bfs_entries_matched": 64 * 608,
                  "root_same_center_witnesses_independently_validated": 64 * 608,
                  "root_witnesses_equal_own_minimum_choice": witness_exact_agreements,
                  "root_witnesses_different_but_valid": 64 * 608 - witness_exact_agreements,
                  "mustfix": 0,
                  "claim_scope": "Exact integer replay and certificate comparison only; no Lean or publication/priority claim."}
    comparison_hash = save(out / "comparison-independent.json", comparison)
    save(out / "comparison-status.json", {"status": comparison["status"],
                                         "ended_utc": ended, "comparison_sha256": comparison_hash})
    print(json.dumps({**comparison, "comparison_sha256": comparison_hash},
                     ensure_ascii=False, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["own", "compare"])
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    if args.phase == "own":
        independently_build_and_check(args.out)
    else:
        require(args.root is not None, "comparison needs ROOT artifacts path")
        compare_root_artifacts(args.out, args.root)


if __name__ == "__main__":
    main()
