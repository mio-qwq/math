#!/usr/bin/env python3
"""Exact bridge formulas, raw-word adjacency, local subset and original BFS checks."""
from collections import defaultdict, deque
from fractions import Fraction
from itertools import permutations, product
from math import prod
from pathlib import Path
import argparse
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "stage2"))
import ten_state  # inherited label constructor; not the adjacency/deletion oracle


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fixture(case):
    n = case["alphabet"]
    require(type(n) is int and n >= 1, "alphabet binding")
    raw = case["weights"]
    require(len(raw) == n and all(type(x) is int and x >= 0 for x in raw)
            and sum(raw) > 0, "weight binding")
    if case["kind"] == "explicit":
        code = {tuple(word) for word in case["words"]}
    elif case["kind"] in ("blowup", "valid_blowup"):
        require(n % 2 == 0, "blowup alphabet binding")
        q = n // 2
        code = {w for w in product(range(n), repeat=4)
                if tuple(int(a >= q) for a in w) in ((0, 0, 0, 1), (0, 0, 1, 1))}
        if case["kind"] == "valid_blowup":
            code = {w for w in code if all(w[i] != w[i + 1] for i in range(3))}
    else:
        raise ValueError("unknown fixture")
    require(all(len(w) == 4 and all(type(a) is int and 0 <= a < n for a in w)
                for w in code), "word/alphabet binding")
    mu = [Fraction(x, sum(raw)) for x in raw]
    return n, code, mu


def strict_dp(n, code):
    states = tuple(product(range(n), repeat=3))
    values = {s: 0 for s in states}
    for _ in range(5):
        following = {s: 0 for s in states}
        for s, value in values.items():
            for a in range(n):
                w = s + (a,)
                following[w[1:]] = max(following[w[1:]], value + int(w in code))
        values = following
    maximum = max(values.values())
    require(maximum <= 2, "not strict: occurrences exceed two")
    if n <= 3:
        literal = max(sum(w[i:i+4] in code for i in range(5))
                      for w in product(range(n), repeat=8))
        require(literal == maximum, "strict DP/literal mismatch")
    return maximum


def formula_and_components(n, code, mu):
    incoming, outgoing = defaultdict(set), defaultdict(set)
    for w in code:
        incoming[w[1:]].add(w)
        outgoing[w[:3]].add(w)
    active = set(incoming).intersection(outgoing)
    word_weight = {w: prod(mu[a] for a in w) for w in code}
    triple_weight = {s: prod(mu[a] for a in s) for s in active}
    p = sum(word_weight.values(), Fraction())
    left = {s: sum((mu[w[0]] for w in incoming[s]), Fraction()) for s in active}
    right = {s: sum((mu[w[3]] for w in outgoing[s]), Fraction()) for s in active}
    d = sum((triple_weight[s] * min(left[s], right[s]) for s in active), Fraction())
    b = sum(triple_weight.values(), Fraction())
    adj_formula = sum((triple_weight[s] * left[s] * right[s] for s in active), Fraction())

    # Rebuild adjacency by literal suffix/prefix comparison, without the tables.
    arcs = {(u, v) for u in code for v in code if u[1:] == v[:3]}
    require(all(u != v for u, v in arcs), "selected loop")
    graph = {w: set() for w in code}
    for u, v in arcs:
        graph[u].add(v)
        graph[v].add(u)
    unseen = set(code)
    components = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        stack, component = [start], {start}
        while stack:
            for v in graph[stack.pop()]:
                if v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    stack.append(v)
        components.append(component)
    predicted = {frozenset(incoming[s] | outgoing[s]) for s in active}
    actual = {frozenset(c) for c in components if len(c) > 1}
    require(predicted == actual and len(predicted) == len(active), "component partition")
    for s in active:
        require(not incoming[s].intersection(outgoing[s]), "bridge sides overlap")
        internal = {(u, v) for u, v in arcs if u in incoming[s] | outgoing[s]
                    and v in incoming[s] | outgoing[s]}
        require(internal == set(product(incoming[s], outgoing[s])), "component not complete")

    best = Fraction()
    tested_subsets = 0
    retained = {w for w in code if not graph[w]}
    for component in components:
        if len(component) == 1:
            best += word_weight[next(iter(component))]
            continue
        words = sorted(component)
        maximum = Fraction()
        for mask in range(1 << len(words)):
            selected = {w for i, w in enumerate(words) if mask >> i & 1}
            tested_subsets += 1
            if all(not (u in selected and v in selected) for u, v in arcs):
                maximum = max(maximum, sum((word_weight[w] for w in selected), Fraction()))
        best += maximum
    for s in active:
        a = sum((word_weight[w] for w in incoming[s]), Fraction())
        c = sum((word_weight[w] for w in outgoing[s]), Fraction())
        retained.update(incoming[s] if a >= c else outgoing[s])
    require(all(not (u in retained and v in retained) for u, v in arcs), "retained adjacency")
    require(best == p-d == sum((word_weight[w] for w in retained), Fraction()),
            "weighted independent optimum")
    literal_adj = sum((prod(mu[a] for a in w) for w in product(range(n), repeat=5)
                       if w[:4] in code and w[1:] in code), Fraction())
    require(literal_adj == adj_formula, "adjacency probability identity")
    require(d*d <= b*literal_adj, "bridge Cauchy cost")
    return {"p": p, "deletion": d, "independent_density": best, "bridge_mass": b,
            "adjacency_probability": literal_adj, "bridge_components": len(active),
            "isolated_words": sum(not graph[w] for w in code), "arcs": len(arcs),
            "local_subsets_checked": tested_subsets,
            "cost_square_slack": b*literal_adj-d*d}, (active, left, right)


def hierarchy_bounds(n, code, mu, bridge_data):
    _, eta, kappa, gamma = ten_state.from_code(n, code)
    require(all(p in ten_state.P for p in gamma.values()), "P10 binding")
    for a, b in product(range(n), repeat=2):
        q = kappa[a, b]
        require(eta[b][0] <= q[0] <= eta[a][0]+1 and
                eta[b][1] <= q[1] <= eta[a][1]+1, "letter/pair domain")
    for a, b, c in product(range(n), repeat=3):
        p = gamma[a, b, c]
        require(kappa[b, c][0] <= p[0] <= kappa[a, b][0]+1 and
                kappa[b, c][1] <= p[1] <= kappa[a, b][1]+1, "pair/triple domain")
    for a, b, c, d in code:
        p, q = gamma[a, b, c], gamma[b, c, d]
        require(p[1] == 5 and q[0] == 1 and q[1] <= p[0]+1, "selected marked arc")
    active, left, right = bridge_data
    x = sum((mu[a] for a in range(n) if eta[a] == (1, 2)), Fraction())
    z = sum((mu[a] for a in range(n) if eta[a] == (2, 3)), Fraction())
    for s in active:
        require(gamma[s] == (1, 5), "active bridge profile")
        require(eta[s[0]] != (1, 2) and eta[s[2]] != (2, 3), "bridge endpoint types")
        require(left[s] <= z and right[s] <= x, "bridge free-letter masses")
    b = sum((prod(mu[a] for a in s) for s in active), Fraction())
    adj = sum((prod(mu[a] for a in s)*left[s]*right[s] for s in active), Fraction())
    deletion = sum((prod(mu[a] for a in s)*min(left[s], right[s]) for s in active), Fraction())
    require(b <= (1-x)*(1-z) and adj <= b*x*z and deletion <= b*min(x,z),
            "10/6/3 mass bounds")
    return {"r0_mass": x, "r2_mass": z,
            "bridge_endpoint_slack": (1-x)*(1-z)-b,
            "adjacency_mass_slack": b*x*z-adj,
            "deletion_mass_slack": b*min(x,z)-deletion}


def original_gp(n, selected):
    vertices = [w for w in product(range(n), repeat=4)
                if all(w[i] != w[i+1] for i in range(3))]
    neighbors = {w: [w[1:]+(a,) for a in range(n) if a != w[-1]] for w in vertices}
    require(selected.issubset(neighbors), "Kautz selected vertex binding")
    distances = {}
    for source in selected:
        dist = {source: 0}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in neighbors[u]:
                if v not in dist:
                    dist[v] = dist[u]+1
                    queue.append(v)
        distances[source] = dist
    tested = 0
    for u, v, w in permutations(selected, 3):
        require(distances[u][v]+distances[v][w] != distances[u][w],
                "original shortest directed path contains three selected vertices")
        tested += 1
    return {"vertices": len(vertices), "arcs": sum(map(len, neighbors.values())),
            "selected": len(selected), "ordered_selected_triples": tested}


def compute_case(case):
    n, code, mu = fixture(case)
    maximum = strict_dp(n, code)
    record, bridge_data = formula_and_components(n, code, mu)
    record.update(hierarchy_bounds(n, code, mu, bridge_data))
    record.update({"words": len(code), "strict_maximum": maximum})
    if case["kind"] == "valid_blowup":
        record["original_gp_bfs"] = original_gp(n, code)
    return {k: str(v) if isinstance(v, Fraction) else v for k, v in record.items()}


def verify(data):
    require(data["schema"] == "GP2-bridge-deletion-v1", "schema")
    records = {}
    for case in data["cases"]:
        result = compute_case(case)
        require(result == case["expected"], "certificate result binding: "+case["name"])
        records[case["name"]] = result
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--derive", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    data = json.loads((root/"bridge_deletion_certificate.json").read_text())
    if args.derive:
        print(json.dumps({case["name"]: compute_case(case) for case in data["cases"]},
                         sort_keys=True, indent=2))
        return
    records = verify(data)
    rejected = []
    for damage in ("selected loop", "negative weight", "wrong deletion", "wrong alphabet",
                   "wrong BFS graph size", "wrong Cauchy slack"):
        bad = json.loads(json.dumps(data))
        case = bad["cases"][0]
        if damage == "selected loop": case["words"].append([0, 0, 0, 0])
        if damage == "negative weight": case["weights"][0] = -1
        if damage == "wrong deletion": case["expected"]["deletion"] = "1"
        if damage == "wrong alphabet": case["alphabet"] += 1
        if damage == "wrong BFS graph size":
            bad["cases"][7]["expected"]["original_gp_bfs"]["vertices"] += 1
        if damage == "wrong Cauchy slack": case["expected"]["cost_square_slack"] = "1"
        try:
            verify(bad)
        except ValueError as error:
            rejected.append({"damage": damage, "reason": str(error)})
        else:
            raise RuntimeError("tampered bridge input accepted")
    print(json.dumps({"status": "PASS", "cases": records,
                      "negative_controls": rejected,
                      "scope": "Exact weighted deletion and hierarchy costs, not a new lambda_4 bound."},
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
