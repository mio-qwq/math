#!/usr/bin/env python3
"""Ten-state local identities, rebuilt without importing frozen GP2 code."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "stage2" / "certificate.json"


def need(x, message):
    if not x:
        raise ValueError(message)


def common_rectangles(vertices, arcs):
    rectangles = set()
    for k in range(1, 1 << len(vertices)):
        incoming = tuple(i for i in range(len(vertices)) if k & (1 << i))
        outgoing = tuple(j for j in range(len(vertices)) if all(arcs[i][j] for i in incoming))
        if outgoing:
            closure = tuple(i for i in range(len(vertices)) if all(arcs[i][j] for j in outgoing))
            rectangles.add((closure, outgoing))
    return rectangles


def embedding(x, y, t):
    # The independently reviewed piecewise formula, with finite arguments.
    if t and x != 2:
        return (3-x, 5)
    if not t and y != 0:
        return (1, 5-y)
    return (2, 4)


def verify(doc):
    P = tuple(itertools.combinations(range(1, 6), 2))
    Q = tuple(itertools.combinations(range(1, 5), 2))
    R = tuple(itertools.combinations(range(1, 4), 2))
    heights = {p: tuple(sum(s <= t for s in p) for t in range(6)) for p in P}
    H = [[all(heights[q][t] >= heights[p][t-1] for t in range(1, 6)) for q in P] for p in P]
    M = [[all(heights[q][t] >= heights[p][t-1]+1 for t in range(1, 6)) for q in P] for p in P]
    need(doc["profiles"] == [list(p) for p in P], "ten-profile binding")
    need(doc["pair_types"] == [list(q) for q in Q], "six pair types")
    need(doc["letter_types"] == [list(r) for r in R], "three letter types")
    need(doc["allowed"] == [[int(v) for v in row] for row in H], "allowed height table")
    need(doc["marked"] == [[int(v) for v in row] for row in M], "marked height table")

    rects = []
    for a, b in Q:
        I = tuple(i for i, (s, t) in enumerate(P) if s >= a and t >= b)
        O = tuple(i for i, (s, t) in enumerate(P) if s <= a+1 and t <= b+1)
        rects.append((I, O))
    need(set(rects) == common_rectangles(P, H), "six maximal target rectangles")
    K = [[bool(set(O) & set(J)) for J, T in rects] for I, O in rects]
    rrects = []
    for a, b in R:
        I = tuple(i for i, (s, t) in enumerate(Q) if s >= a and t >= b)
        O = tuple(i for i, (s, t) in enumerate(Q) if s <= a+1 and t <= b+1)
        rrects.append((I, O))
    need(set(rrects) == common_rectangles(Q, K), "three maximal pair rectangles")
    need(all(set(O) & set(J) for I, O in rrects for J, T in rrects), "complete three-type graph")

    domains = 0
    domination_entries = 0
    for i, j in itertools.product(range(6), repeat=2):
        D = set(rects[i][1]) & set(rects[j][0])
        if not D:
            continue
        domains += 1
        a, b = Q[i]
        c, d = Q[j]
        active = set()
        if b == 4:
            active.add(P.index((a+1, 5)))
        if c == 1:
            active.add(P.index((1, d)))
        if b == 4 and c == 1:
            active.add(P.index((1, 5)))
        if not active:
            active.add(min(D))
        need(active <= D and len(active) <= 3, "active choices inside original domain")
        for p in D:
            need(any(all((not M[p][k] or M[q][k]) and (not M[k][p] or M[k][q])
                         for k in range(10)) for q in active), "marked row/column domination")
            domination_entries += 1

    cases = 0
    for x, y, z, t, u in itertools.product(range(3), range(3), range(3), range(2), range(2)):
        p, q = P.index(embedding(x, y, t)), P.index(embedding(y, z, u))
        need(H[p][q], "explicit five-profile assignment is not admissible")
        need(M[p][q] == bool(t and not u and x < z), "five-profile objective identity")
        cases += 1

    adjacent_profiles = [tuple(P[i] for i in (p, q, r))
                         for p, q, r in itertools.product(range(10), repeat=3)
                         if M[p][q] and M[q][r]]
    need(adjacent_profiles == [((4, 5), (1, 5), (1, 2))], "adjacency profile sequence")
    left_types, right_types = set(), set()
    for ri, (I, O) in enumerate(rrects):
        for qi in O:
            if P.index((4, 5)) in rects[qi][1]:
                left_types.add(R[ri])
        for qi in I:
            if P.index((1, 2)) in rects[qi][0]:
                right_types.add(R[ri])
    need(left_types == {(2, 3)} and right_types == {(1, 2)}, "adjacency endpoints")
    return {"allowed_arcs": sum(map(sum, H)), "marked_arcs": sum(map(sum, M)),
            "pair_arcs": sum(map(sum, K)), "triple_states": len(P),
            "pair_states": len(Q), "letter_states": len(R),
            "complete_letter_type_graph": True, "admissible_pair_domains": domains,
            "domination_entries": domination_entries, "five_profile_cases": cases,
            "unique_adjacent_profiles": adjacent_profiles,
            "adjacency_source_letter_type": list(next(iter(left_types))),
            "adjacency_target_letter_type": list(next(iter(right_types)))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = SOURCE.read_bytes()
    doc = json.loads(source)["ten_target"]
    report = verify(doc)
    controls = []
    for field in ("allowed", "marked"):
        bad = copy.deepcopy(doc)
        bad[field][0][0] ^= 1
        try:
            verify(bad)
        except ValueError as exc:
            controls.append({"damaged_field": field, "rejected": str(exc)})
        else:
            raise ValueError("damaged target table was accepted")
    report["negative_controls"] = controls
    report["source_certificate_sha256"] = hashlib.sha256(source).hexdigest()
    output = json.dumps(report, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output)
    print("PASS: ten-state local identities reconstructed independently")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
