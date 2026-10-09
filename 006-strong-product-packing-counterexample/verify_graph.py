"""Exact replay of one explicit simple connected graph; no conjecture search."""
from collections import deque
from hashlib import sha256
from pathlib import Path
import json
import sys
from datetime import datetime, timezone


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def bfs(adj, start):
    dist = [-1] * len(adj)
    dist[start] = 0
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + 1
                queue.append(w)
    return dist


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python verifier.py NEW_OUTPUT_DIRECTORY")
    out = Path(sys.argv[1])
    if out.exists():
        raise SystemExit("Preserve previous output; supply a fresh directory.")
    out.mkdir(parents=True)
    start = datetime.now(timezone.utc).isoformat()
    hd = [[(a ^ b).bit_count() for b in range(64)] for a in range(64)]
    g = [[b for b in range(64) if hd[a][b] == 1] for a in range(64)]
    g_dist = [bfs(g, a) for a in range(64)]
    assert g_dist == hd, "Actual Q6 graph distance must equal six-bit Hamming distance."
    pairs = [(a, b) for a in range(64) for b in range(a + 1, 64) if hd[a][b] == 4]
    assert len(pairs) == 480
    nodes = ([{"kind": "A", "support": [a]} for a in range(64)]
             + [{"kind": "S", "support": [a]} for a in range(64)]
             + [{"kind": "E", "support": [a, b]} for a, b in pairs])
    assert len(nodes) == 608
    adj = [set() for _ in nodes]

    def edge(v, w):
        assert v != w
        adj[v].add(w)
        adj[w].add(v)

    for a in range(64):
        edge(a, 64 + a)
    for k, (a, b) in enumerate(pairs):
        edge(a, 128 + k)
        edge(b, 128 + k)
    for v in range(64, len(nodes)):
        for w in range(v + 1, len(nodes)):
            if all(a == b or hd[a][b] >= 4
                   for a in nodes[v]["support"] for b in nodes[w]["support"]):
                edge(v, w)
    h = [sorted(neighbors) for neighbors in adj]
    assert all(v not in h[v] for v in range(608))
    assert all(v in h[w] for v in range(608) for w in h[v])
    assert all(w >= 64 for v in range(64) for w in h[v]), "No A-A edges."
    dist_h = [bfs(h, a) for a in range(64)]
    assert all(d >= 0 for d in dist_h[0]), "H must really be connected."
    assert all(all(d >= 0 for d in row) for row in dist_h)
    failures = []
    minimum = None
    for a in range(64):
        for b in range(a + 1, 64):
            product_distance = max(g_dist[a][b], dist_h[a][b])
            minimum = product_distance if minimum is None else min(minimum, product_distance)
            if product_distance < 4:
                failures.append([a, b, g_dist[a][b], dist_h[a][b]])
    assert not failures, failures
    balls = [sum(1 << x for x in range(64) if g_dist[x][a] <= 2) for a in range(64)]
    witness = []
    for v in range(608):
        close_labels = [a for a in range(64) if dist_h[a][v] <= 2]
        union = 0
        for a in close_labels:
            union |= balls[a]
        assert union == (1 << 64) - 1, [v, nodes[v], close_labels, union]
        witness.append([next(a for a in close_labels if g_dist[x][a] <= 2) for x in range(64)])
    # Explicitly recheck the same center for every one of the 64*608 targets.
    assert all(g_dist[x][witness[v][x]] <= 2 and dist_h[witness[v][x]][v] <= 2
               for v in range(608) for x in range(64))
    graph = {"nodes": nodes, "adjacency": h}
    cert = {"h_center_to_all_distances": dist_h, "same_center_cover_witness": witness}
    graph_bytes = (canonical(graph) + "\n").encode("utf8")
    cert_bytes = (canonical(cert) + "\n").encode("utf8")
    (out / "graph.json").write_bytes(graph_bytes)
    (out / "certificate.json").write_bytes(cert_bytes)
    summary = {
        "status": "EXACT_FINITE_GRAPH_REPLAY_PASS",
        "start_utc": start, "end_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "parameters": {"d": 2, "p": 3},
        "G_vertices": 64, "G_edges": sum(map(len, g)) // 2,
        "G_actual_graph_distances_equal_hamming": True,
        "H_vertices": 608, "H_edges": sum(map(len, h)) // 2,
        "H_simple_undirected_connected": True,
        "H_degree_range": [min(map(len, h)), max(map(len, h))],
        "H_center_to_any_max_distance": max(map(max, dist_h)),
        "product_center_count": 64, "checked_unordered_center_pairs": 2016,
        "minimum_product_center_distance": minimum,
        "checked_same_center_targets": 64 * 608,
        "uncovered_targets": 0, "packing_violations": 0,
        "graph_sha256": sha256(graph_bytes).hexdigest(),
        "certificate_sha256": sha256(cert_bytes).hexdigest(),
        "factor_nonexistence_scope": "existing all-subsets Q6PackingDomination proof; not reproved by this replay",
        "claim_scope": "Exact actual-graph replay; mathematical proof and Lean verification are recorded separately in README.md",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
