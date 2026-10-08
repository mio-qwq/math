"""Independent exact reconstruction checker, with no solver import/search.

Accepts valid cover/pruning certificates; it does not certify optimality or
trust the construction trace. Explicit checks remain active under python -O.
The optional integration self-test invokes the separate constructor to obtain
candidates, but check() and the normal certificate CLI never import it.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pairs(data, n, m):
    require(isinstance(data, list), "pairs must be a list")
    out = set()
    for entry in data:
        require(isinstance(entry, list) and len(entry) == 2 and
                all(type(v) is int for v in entry), "invalid pair")
        a, b = entry
        require(0 <= a < n and 0 <= b < m, "pair outside coordinate domain")
        require((a, b) not in out, "duplicate pair")
        out.add((a, b))
    return out


def cluster_relation(relation):
    """Independent characterization: intersecting left neighborhoods coincide."""
    neighborhoods = {}
    for a, b in relation:
        neighborhoods.setdefault(a, set()).add(b)
    rows = list(neighborhoods.values())
    return all(not (u & v) or u == v for u in rows for v in rows)


def node(tag, a, b):
    return f"{tag}:{a}:{b}"


def check(cert):
    require(cert.get("schema") == "compatible-pair-costs-certificate-v1", "unknown schema")
    raw = cert["instance"]
    require(raw.get("format") == "compatible-pair-costs-v1", "unknown instance format")
    dims = raw["sizes"]
    require(set(dims) == {"P", "I", "S", "J"}, "incorrect size keys")
    require(all(type(n) is int and n >= 0 for n in dims.values()), "invalid dimensions")
    psize, isize, ssize, jsize = (dims[k] for k in ("P", "I", "S", "J"))
    E = pairs(raw["E"], psize, isize)
    F = pairs(raw["F"], ssize, jsize)
    R = pairs(raw["R"], psize, jsize)
    C = pairs(raw["C"], isize, ssize)
    structured = cert["structured_relation"]
    require(structured in ("E", "F"), "invalid structured relation")
    require(cluster_relation(E if structured == "E" else F), "relation is not a block union")
    shapes = {"R": (psize, jsize), "C": (isize, ssize),
              "H": (psize, ssize), "Z": (isize, jsize)}
    require(set(raw["costs"]) == set(shapes), "incorrect costs keys")
    costs = {}
    for tag, (n, m) in shapes.items():
        matrix = raw["costs"][tag]
        require(isinstance(matrix, list) and len(matrix) == n, "incorrect cost row count")
        require(all(isinstance(row, list) and len(row) == m for row in matrix),
                "incorrect cost column count")
        values = {}
        for a, row in enumerate(matrix):
            for b, value in enumerate(row):
                require(type(value) is str, "cost must be a rational string")
                amount = Fraction(value)
                require(amount >= 0, "negative pair cost")
                values[a, b] = amount
        costs[tag] = values
    H, Z, edges = set(), set(), set()
    active_r, active_c = set(), set()
    for p, j in R:
        for i, s in C:
            if (p, i) in E and (s, j) in F:
                H.add((p, s))
                Z.add((i, j))
                active_r.add((p, j))
                active_c.add((i, s))
                edges.add((node("R", p, j), node("C", i, s)))
                require(costs["R"][p, j] * costs["C"][i, s] <=
                        costs["H"][p, s] * costs["Z"][i, j], "local constraint failed")
    for i, j in Z:
        for p, jj in R:
            if jj == j and (p, i) in E:
                edges.add((node("R", p, j), node("ZR", i, j)))
        for ii, s in C:
            if ii == i and (s, j) in F:
                edges.add((node("ZL", i, j), node("C", i, s)))
    weights = {node("R", p, j): costs["R"][p, j] for p, j in R}
    weights.update({node("C", i, s): costs["C"][i, s] for i, s in C})
    for i, j in Z:
        weights[node("ZL", i, j)] = weights[node("ZR", i, j)] = costs["Z"][i, j]
    require(isinstance(cert["cover"], list) and all(type(v) is str for v in cert["cover"]),
            "invalid cover")
    cover = set(cert["cover"])
    require(len(cover) == len(cert["cover"]) and cover <= set(weights), "bad cover vertex")
    incident = {v for edge in edges for v in edge}
    require(cover <= incident, "isolated vertex selected")
    require(all(a in cover or b in cover for a, b in edges), "uncovered graph edge")
    kept_r = {(p, j) for p, j in R if node("R", p, j) not in cover}
    kept_c = {(i, s) for i, s in C if node("C", i, s) not in cover}
    require(pairs(cert["retained_R"], psize, jsize) == kept_r, "incorrect retained R")
    require(pairs(cert["retained_C"], isize, ssize) == kept_c, "incorrect retained C")
    require(R - active_r <= kept_r and C - active_c <= kept_c, "isolated originals lost")
    require(all((p, i) not in E or (s, j) not in F for p, j in kept_r for i, s in kept_c),
            "retained originals conflict")
    U = set()
    for i, j in Z:
        r_covered = any(jj == j and (p, i) in E for p, jj in kept_r)
        c_covered = any(ii == i and (s, j) in F for ii, s in kept_c)
        if not r_covered and not c_covered:
            U.add((i, j))
    require(pairs(cert["uncovered"], isize, jsize) == U, "incorrect actual uncovered set")
    hmass = sum((costs["H"][v] for v in H), Fraction(0))
    zmass = sum((costs["Z"][v] for v in Z), Fraction(0))
    umass = sum((costs["Z"][v] for v in U), Fraction(0))
    ctotal = sum((weights[v] for v in cover), Fraction(0))
    deletion = sum((costs["R"][v] for v in R - kept_r), Fraction(0))
    deletion += sum((costs["C"][v] for v in C - kept_c), Fraction(0))
    require(ctotal <= hmass + zmass, "cover bound failed")
    require(deletion <= hmass + umass, "pruning bound failed")
    actual = {"H_mass": hmass, "Z_mass": zmass, "cover_cost": ctotal,
              "deletion_cost": deletion, "uncovered_mass": umass}
    require(set(cert["claims"]) == set(actual), "incorrect claim fields")
    for key, value in actual.items():
        require(type(cert["claims"][key]) is str and Fraction(cert["claims"][key]) == value,
                f"incorrect {key}")
    return {key: str(value) for key, value in actual.items()}


def self_test(example_output=None):
    import copy
    import hashlib
    import itertools
    import random
    from pathlib import Path
    import compatible_pair_costs as constructor

    Q = Fraction
    def raw(dims, E, F, R, C, x, y, h, z):
        return {"format": "compatible-pair-costs-v1", "sizes": dict(zip("PISJ", dims)),
                "E": [list(v) for v in sorted(E)], "F": [list(v) for v in sorted(F)],
                "R": [list(v) for v in sorted(R)], "C": [list(v) for v in sorted(C)],
                "costs": {k: [[str(v) for v in row] for row in mat]
                          for k, mat in zip(("R", "C", "H", "Z"), (x, y, h, z))}}

    all2 = set(itertools.product(range(2), repeat=2))
    diag = {(0, 0), (1, 1)}
    path = {(0, 0), (1, 0), (1, 1)}
    fixtures = [
        ("tight_nonproduct", raw((2, 2, 1, 1), path, {(0, 0)}, {(0, 0), (1, 0)},
                                 {(0, 0), (1, 0)}, [[4], [1]], [[1], [1]],
                                 [[1], [1]], [[4], [1]])),
        ("zero_h_positive_R", raw((1, 1, 1, 1), {(0, 0)}, {(0, 0)}, {(0, 0)},
                                     {(0, 0)}, [[1]], [[0]], [[0]], [[0]])),
        ("zero_R_positive_C", raw((1, 1, 1, 1), {(0, 0)}, {(0, 0)}, {(0, 0)},
                                     {(0, 0)}, [[0]], [[1]], [[0]], [[0]])),
        ("extra_corner_copy", raw((2, 2, 2, 2), {(0, 0), (1, 0)}, all2, diag,
                                  {(0, 0)}, [[8, 0], [0, 1]], [[1, 0], [0, 0]],
                                  [[2, 0], [1, 0]], [[4, 1], [0, 0]])),
        ("isolated_originals", raw((2, 2, 2, 2), {(0, 0)}, all2, all2, all2,
                                    [[1, 1], [5, 7]], [[1, 1], [8, 9]],
                                    [[1, 1], [0, 0]], [[1, 1], [0, 0]])),
        ("symmetric_E_blocks", raw((2, 2, 2, 2), diag, path, all2, all2,
                                    [[1, 1], [1, 1]], [[1, 1], [1, 1]],
                                    [[1, 1], [1, 1]], [[1, 1], [1, 1]])),
        ("two_F_blocks", raw((2, 2, 2, 2), all2, diag, all2, all2,
                              [[1, 1], [1, 1]], [[1, 1], [1, 1]],
                              [[1, 1], [1, 1]], [[1, 1], [1, 1]])),
        ("empty_P_domain", raw((0, 2, 1, 2), set(), {(0, 0), (0, 1)}, set(),
                                {(0, 0), (1, 0)}, [], [[3], [2]], [], [[1, 1], [1, 1]])),
    ]
    examples = []
    for name, data in fixtures:
        certificate = constructor.solve(data)
        check(certificate)
        examples.append({"name": name, "certificate": certificate})
    tight = examples[0]["certificate"]
    require(tight["claims"] == {"H_mass": "2", "Z_mass": "5", "cover_cost": "7",
                                "deletion_cost": "3", "uncovered_mass": "1"}, "tight fixture mismatch")
    require(examples[5]["certificate"]["structured_relation"] == "E", "symmetric branch not used")
    gap = examples[3]["certificate"]
    require(gap["uncovered"] == [[0, 1]] and "ZR:0:1" in gap["cover"],
            "extra selected corner / actual U distinction not exercised")

    rng = random.Random(20261008)
    relations = [set(v for k, v in enumerate(sorted(all2)) if mask >> k & 1) for mask in range(16)]
    clustered = [rel for rel in relations if cluster_relation(rel)]
    general_paths = [rel for rel in relations if not cluster_relation(rel)]
    zero_corners = 0
    nonempty_cases = 0
    orientation_counts = {"E": 0, "F": 0}
    for test in range(400):
        if test % 2:
            E, F = rng.choice(clustered), rng.choice(general_paths)
        else:
            E, F = rng.choice(relations), rng.choice(clustered)
        R = {v for v in sorted(all2) if rng.randrange(4)}
        C = {v for v in sorted(all2) if rng.randrange(4)}
        x = [[Q(rng.randrange(9), rng.randrange(1, 6)) for j in range(2)] for p in range(2)]
        y = [[Q(rng.randrange(9), rng.randrange(1, 6)) for s in range(2)] for i in range(2)]
        z = [[Q(rng.randrange(1, 9), rng.randrange(1, 6)) for j in range(2)] for i in range(2)]
        h = [[Q(0) for s in range(2)] for p in range(2)]
        conflicts = [(p, j, i, s) for p, j in R for i, s in C if (p, i) in E and (s, j) in F]
        nonempty_cases += bool(conflicts)
        for i, j in sorted({(i, j) for p, j, i, s in conflicts}):
            if all(x[p][j] * y[i][s] == 0 for p, jj, ii, s in conflicts if (ii, jj) == (i, j)) and rng.randrange(2):
                z[i][j] = Q(0)
                zero_corners += 1
        for p, j, i, s in conflicts:
            if z[i][j] > 0:
                h[p][s] = max(h[p][s], x[p][j] * y[i][s] / z[i][j])
        for p, s in sorted({(p, s) for p, j, i, s in conflicts}):
            h[p][s] += Q(rng.randrange(3), 4)
        certificate = constructor.solve(raw((2, 2, 2, 2), E, F, R, C, x, y, h, z))
        check(certificate)
        orientation_counts[certificate["structured_relation"]] += 1

    mutations = []
    def mutate(fn, original=tight):
        certificate = copy.deepcopy(original)
        fn(certificate)
        mutations.append(certificate)
    mutate(lambda c: c["claims"].update(cover_cost="0"))
    mutate(lambda c: c["cover"].remove("ZR:0:0"))
    mutate(lambda c: c["cover"].append(c["cover"][0]))
    mutate(lambda c: c["instance"]["costs"]["H"][0].__setitem__(0, "0"))
    mutate(lambda c: c["retained_R"].append([1, 0]))
    mutate(lambda c: c.update(uncovered=[]))
    mutate(lambda c: c.update(structured_relation="E"))
    mutate(lambda c: c["instance"]["costs"]["R"][0].__setitem__(0, "-1"))
    mutate(lambda c: c["instance"]["E"].append(c["instance"]["E"][0]))
    mutate(lambda c: c["cover"].append("R:1:0"), examples[4]["certificate"])
    for certificate in mutations:
        try:
            check(certificate)
        except ValueError:
            pass
        else:
            raise ValueError("mutated certificate was accepted")
    unsupported = raw((2, 2, 2, 2), path, path, all2, all2,
                      [[1, 1], [1, 1]], [[1, 1], [1, 1]], [[1, 1], [1, 1]], [[1, 1], [1, 1]])
    try:
        constructor.solve(unsupported)
    except ValueError:
        pass
    else:
        raise ValueError("unsupported relations accepted")
    if example_output is not None:
        Path(example_output).write_text(json.dumps({"format": "compatible-pair-costs-example-suite-v1",
                                                   "cases": examples}, indent=2, sort_keys=True) + "\n",
                                        encoding="utf-8")
    source_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                     for path in (Path(__file__), Path(constructor.__file__))}
    return {"status": "PASS", "date": "2026-10-08", "seed": 20261008,
            "written_examples_checked": len(examples), "bounded_generated_cases": 400,
            "generated_cases_by_orientation": orientation_counts,
            "generated_cases_with_conflicts": nonempty_cases, "zero_Z_corners_checked": zero_corners,
            "mutated_certificates_rejected": len(mutations), "unsupported_structure_rejected": 1,
            "source_sha256": source_hashes, "python_version": sys.version.split()[0],
            "scope": "Fresh bounded exact Fraction checks, no general enumeration. General theorem has a written proof, not a Lean formalization. Certificate checking proves feasibility and the stated bounds, not optimality."}


def main():
    if len(sys.argv) in (2, 3) and sys.argv[1] == "--self-test":
        print(json.dumps(self_test(sys.argv[2] if len(sys.argv) == 3 else None), sort_keys=True))
        return
    require(len(sys.argv) == 2, "usage: check_compatible_pair_costs.py CERTIFICATE_OR_SUITE")
    with open(sys.argv[1], encoding="utf-8") as stream:
        raw = json.load(stream)
    if raw.get("format") == "compatible-pair-costs-example-suite-v1":
        require(isinstance(raw["cases"], list), "invalid cases")
        results = [{"name": item["name"], **check(item["certificate"])} for item in raw["cases"]]
    else:
        results = [check(raw)]
    print(json.dumps({"status": "ACCEPT", "cases": results}, sort_keys=True))


if __name__ == "__main__":
    main()
