"""Independent local graph/path checks, not a global colouring enumeration.

Only the Python standard library is used. No authored verifier is imported.
Run from any directory; output is written beside this script.
"""

from collections import Counter, deque
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import json
import re


REVIEW = Path(__file__).resolve().parent
SOURCE = REVIEW.parents[3] / "research/workstreams/ROOT/clawfree-11334-counterexample"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def diamond_ring(k):
    assert k >= 2
    edges = set()
    for i in range(k):
        a, b, p, q = (4 * i + j for j in range(4))
        for u, v in ((a, b), (a, p), (a, q), (b, p), (b, q),
                     (q, 4 * ((i + 1) % k) + 2)):
            assert u != v
            e = tuple(sorted((u, v)))
            assert e not in edges
            edges.add(e)
    neighbours = [set() for _ in range(4 * k)]
    for u, v in edges:
        neighbours[u].add(v)
        neighbours[v].add(u)
    assert len(edges) == 6 * k
    assert all(len(s) == 3 for s in neighbours)
    return neighbours, edges


def expand(core):
    labels = [(v, w) for v, ns in enumerate(core) for w in sorted(ns)]
    index = {vw: i for i, vw in enumerate(labels)}
    edges = set()
    for v, ns in enumerate(core):
        ports = [index[(v, w)] for w in ns]
        edges.update(tuple(sorted(e)) for e in combinations(ports, 2))
        for w in ns:
            edges.add(tuple(sorted((index[(v, w)], index[(w, v)]))))
    neighbours = [set() for _ in labels]
    for x, y in edges:
        neighbours[x].add(y)
        neighbours[y].add(x)
    return labels, index, neighbours, edges


def bfs_distances(graph):
    out = []
    for start in range(len(graph)):
        dist = {start: 0}
        queue = deque([start])
        while queue:
            x = queue.popleft()
            for y in sorted(graph[x]):
                if y not in dist:
                    dist[y] = dist[x] + 1
                    queue.append(y)
        assert len(dist) == len(graph)
        out.append([dist[x] for x in range(len(graph))])
    return out


def path_length(label_path, index, graph):
    ids = [index[vw] for vw in label_path]
    shortened = [ids[0]]
    for x in ids[1:]:
        if x != shortened[-1]:
            shortened.append(x)
    assert all(y in graph[x] for x, y in zip(shortened, shortened[1:]))
    return len(shortened) - 1


def local_tip_checks(k, core):
    # The six proper colourings of one diamond; 36 two-diamond local pairs.
    local = [(a, b, t, t) for a, b, t in permutations(range(3))]
    checked = 0
    for i in range(k):
        for tip_offset, adj_i, adjacent_tip in ((2, (i - 1) % k, 3),
                                                (3, (i + 1) % k, 2)):
            tip = 4 * i + tip_offset
            same_tip = 4 * i + (5 - tip_offset)
            for current in local:
                if current[tip_offset] != 2:
                    continue
                for neighbour in local:
                    if current[tip_offset] == neighbour[adjacent_tip]:
                        continue  # joining edge must be proper
                    colours = {4 * i + j: current[j] for j in range(4)}
                    colours.update({4 * adj_i + j: neighbour[j] for j in range(4)})
                    external = 4 * adj_i + adjacent_tip
                    assert core[tip] == {4 * i, 4 * i + 1, external}
                    for w in core[tip]:
                        if w != external:
                            witness = same_tip
                        else:
                            witness = next(x for x in (4 * adj_i, 4 * adj_i + 1)
                                           if colours[x] == 2)
                        assert witness != tip and witness in core[w]
                        assert colours[witness] == colours[tip] == 2
                    checked += 1
    return checked


def case(k):
    core, core_edges = diamond_ring(k)
    labels, index, graph, edges = expand(core)
    distance = bfs_distances(graph)
    assert len(graph) == 12 * k and len(edges) == 18 * k
    assert all(len(s) == 3 for s in graph)
    triangles = set()
    for x, ns in enumerate(graph):
        assert any(z in graph[y] for y, z in combinations(ns, 2))
        for y, z in combinations(ns, 2):
            if z in graph[y]:
                triangles.add(tuple(sorted((x, y, z))))
    expected = {tuple(sorted(index[(v, w)] for w in ns))
                for v, ns in enumerate(core)}
    assert triangles == expected
    triangle_edge_use = Counter(e for t in triangles for e in combinations(t, 2))
    assert max(triangle_edge_use.values()) == 1  # no shared edge, hence no diamond

    adjacent_tests = 0
    adjacent_hist = Counter()
    for u, v in core_edges:
        for s in core[u]:
            for t in core[v]:
                length = path_length([(u, s), (u, v), (v, u), (v, t)], index, graph)
                d = distance[index[(u, s)]][index[(v, t)]]
                assert d <= length <= 3
                adjacent_tests += 1
                adjacent_hist[d] += 1

    private_tests = 0
    private_hist = Counter()
    for v, ns in enumerate(core):
        for w in ns:
            for u in core[w] - {v}:
                for t in core[u]:
                    length = path_length([(v, w), (w, v), (w, u), (u, w), (u, t)],
                                         index, graph)
                    d = distance[index[(v, w)]][index[(u, t)]]
                    assert d <= length <= 4
                    private_tests += 1
                    private_hist[d] += 1

    return {
        "k": k, "core_vertices": len(core), "core_edges": len(core_edges),
        "expanded_vertices": len(graph), "expanded_edges": len(edges),
        "degree_set": sorted(set(map(len, graph))), "connected": True,
        "claw_free": True, "triangle_count": len(triangles), "diamond_free": True,
        "diameter": max(map(max, distance)),
        "adjacent_arbitrary_endpoint_tests": adjacent_tests,
        "adjacent_distance_histogram": dict(sorted(adjacent_hist.items())),
        "private_arbitrary_other_endpoint_tests": private_tests,
        "private_distance_histogram": dict(sorted(private_hist.items())),
        "tip_local_pair_tests": local_tip_checks(k, core),
    }


def certificate_alignment():
    cert = json.loads((SOURCE / "counterexample.json").read_text(encoding="utf-8"))
    lean = (SOURCE / "ClawFree11334.lean").read_text(encoding="utf-8")
    core, core_edges = diamond_ring(3)
    labels, index, graph, edges = expand(core)
    assert cert["n"] == len(graph) == 36
    assert set(map(tuple, cert["edges"])) == edges
    assert set(map(tuple, cert["core_edges"])) == core_edges
    assert list(map(tuple, cert["labels"])) == labels
    assert cert["palette"] == [1, 1, 3, 3, 4]
    partner_match = re.search(r"def partner[^\n]*:= !\[([0-9,]+)\]", lean)
    assert partner_match
    lean_partner = list(map(int, partner_match.group(1).split(",")))
    expected_partner = [index[(w, v)] for v, w in labels]
    assert lean_partner == expected_partner
    lean_core = lean.split("def coreEdges", 1)[1].split("def coreAdjacent", 1)[0]
    assert {tuple(map(int, m)) for m in re.findall(r"\((\d+),\s*(\d+)\)", lean_core)} == core_edges
    lean_edges = lean.split("theorem graph_matches_edges", 1)[1].split("def ClawFree", 1)[0]
    directed = {tuple(map(int, m)) for m in re.findall(r"\((\d+),\s*(\d+)\)", lean_edges)}
    expected_directed = edges | {(v, u) for u, v in edges}
    assert directed == expected_directed
    pair_tests = 0
    for x in range(36):
        for y in range(36):
            from_lean_definition = (x // 3 == y // 3 and x != y) or lean_partner[x] == y
            assert from_lean_definition == (y in graph[x]) == ((x, y) in directed)
            pair_tests += 1
    return {"labels_match": True, "core_edges_match": True, "expanded_edges_match": True,
            "partner_match": True, "palette_match": True, "all_vertex_pair_tests": pair_tests}


def negative_controls():
    core, _ = diamond_ring(3)
    labels, index, graph, _ = expand(core)
    distance = bfs_distances(graph)
    # The external-tip witness can really have distance exactly four.
    path = [(2, 11), (11, 2), (11, 8), (8, 11), (8, 9)]
    assert path_length(path, index, graph) == 4
    d = distance[index[path[0]]][index[path[-1]]]
    assert d == 4
    even_controls = []
    for k in (2, 4):
        even_core, _ = diamond_ring(k)
        colours = []
        for i in range(k):
            t = i % 2
            colours.extend([2, 1 - t, t, t])
        assert all(colours[v] != colours[w] for v, ns in enumerate(even_core) for w in ns)
        private_witnesses = {v: next(w for w in even_core[v]
                                    if {u for u in even_core[w] if colours[u] == 2} == {v})
                             for v in range(4 * k) if colours[v] == 2}
        assert private_witnesses == {4 * i: 4 * i + 1 for i in range(k)}
        even_controls.append({"k": k, "core_colours": colours,
                              "proper_and_C_private": True,
                              "C_private_witnesses": private_witnesses,
                              "original_packing_existence_not_tested": True})
    # These local colourings illustrate that high-point uniqueness is not a triangle fact.
    local_multiple_high = [[0, 2, 3], [2, 3, 4]]
    assert all(len(set(c)) == 3 for c in local_multiple_high)
    return {"distance_four_path": path, "distance_four_actual_BFS": d,
            "same_C_pair_allowed_at_radius_three": d > 3,
            "same_C_pair_forbidden_at_radius_four": not d > 4,
            "even_ring_controls": even_controls,
            "local_triangle_multi_high_examples": local_multiple_high,
            "multi_high_examples_are_only_local_not_global": True}


def main():
    started = datetime.now(timezone.utc).isoformat()
    names = ["PROOF.md", "ClawFree11334.lean", "counterexample.json",
             "verify_counterexample.py", "lean-audit.json", "HISTORY.md"]
    inputs = {name: digest(SOURCE / name) for name in names}
    assert inputs["ClawFree11334.lean"] == "afad6d3313c93fd5681be0ba0e25d302c73d019448681cb4c6552f8a0e0765b2"
    assert inputs["counterexample.json"] == "7d1cdd61f032185728ffac6a6b0b6a79c611e0a36341a78eb35610df55b95ccd"
    result = {"status": "PASS", "started_utc": started,
              "script_sha256": digest(Path(__file__)), "input_sha256": inputs,
              "scope": "Small explicit constructors, BFS and two-diamond local checks; no global colouring enumeration or Lean execution",
              "cases": [case(k) for k in (2, 3, 4, 5, 7)],
              "certificate_alignment": certificate_alignment(),
              "negative_controls": negative_controls(),
              "finished_utc": datetime.now(timezone.utc).isoformat()}
    out = REVIEW / "independent-bfs-results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(out),
                      "k_cases": [x["k"] for x in result["cases"]],
                      "adjacent_tests": sum(x["adjacent_arbitrary_endpoint_tests"] for x in result["cases"]),
                      "private_tests": sum(x["private_arbitrary_other_endpoint_tests"] for x in result["cases"]),
                      "local_tip_tests": sum(x["tip_local_pair_tests"] for x in result["cases"]),
                      "certificate_pair_tests": result["certificate_alignment"]["all_vertex_pair_tests"]}))


if __name__ == "__main__":
    main()
