#!/usr/bin/env python3
"""Direct-bit validation, without importing either discovery program.

This is a second implementation by the discoverer, not independent
research review. All arithmetic is fixed to the original 32-bit words.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

N = 1 << 32
M = N - 1
L = (1 << 31) - 1
HERE = Path(__file__).resolve().parent
SUPPORT_HASH = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"
S = (2, 9, 10, 16, 23, 24, 30, 37, 38, 44, 51, 52, 58)
Q = tuple(2 + 14 * j for j in range(5))
P = tuple(9 + 14 * j for j in range(4))
R = tuple(10 + 14 * j for j in range(4))
COMMON = set(Q[1:]) | set(P)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sigma(x, a, b, s):
    require(type(x) is int and 0 <= x < N, "not a 32-bit word")
    bits = [(x >> j) & 1 for j in range(32)]
    return sum((bits[(i + a) % 32] ^ bits[(i + b) % 32]
                ^ (bits[i + s] if i + s < 32 else 0)) << i for i in range(32))


def f(x):
    return sigma(x, 7, 18, 3)


def g(x):
    return sigma(x, 17, 19, 10)


def rows_for(kind):
    if kind == "d":
        return [1 << i for i in range(32)]
    a, b, s = (7, 18, 3) if kind == "F" else (17, 19, 10)
    return [(1 << ((i + a) % 32)) ^ (1 << ((i + b) % 32))
            ^ ((1 << (i + s)) if i + s < 32 else 0) for i in range(32)]


def diff(pair):
    a, b = pair
    return [(b - a) % N, (f(b) - f(a)) % N, (g(b) - g(a)) % N]


def rank(values):
    # Low-pivot elimination, distinct from the discovery high-pivot code.
    pivots = {}
    for word in values:
        while word:
            bit = (word & -word).bit_length() - 1
            if bit in pivots:
                word ^= pivots[bit]
            else:
                pivots[bit] = word
                break
    return len(pivots)


def span(basis):
    require(len(basis) <= 10, "certificate exceeds this fixed check's bound")
    return [xor_selected(basis, subset) for subset in range(1 << len(basis))]


def xor_selected(words, subset):
    value = 0
    for j, word in enumerate(words):
        if subset >> j & 1:
            value ^= word
    return value


def original_equations():
    result = []
    for t in range(16, 64):
        raw = [[1, "d", t], [-1, "G", t - 2], [-1, "d", t - 7],
               [-1, "F", t - 15], [-1, "d", t - 16]]
        result.append({"t": t, "terms": [v for v in raw if v[2] in S]})
    return result


def canonical(terms):
    result = {}
    for sign, kind, index in terms:
        key = "D" if kind == "d" and index in COMMON else kind + str(index)
        result[key] = result.get(key, 0) + sign
    return {k: v for k, v in result.items() if v}


def check_equations(analysis):
    equations = original_equations()
    require(analysis["equations"] == equations, "all 48 original equations required")
    require(analysis["support"] == list(S), "wrong support")
    require(analysis["nontrivial_equations"] == 24, "wrong nontrivial count")
    nonzero = [e for e in equations if e["terms"]]
    require(len(nonzero) == 24, "raw nontrivial count")
    chain = [9, 16, 23, 30, 37, 44, 51, 58]
    require(set(chain) == COMMON and len(set(chain)) == 8, "common-D path vertices")
    by_t = {e["t"]: e["terms"] for e in equations}
    for left, right in zip(chain, chain[1:]):
        require(by_t[right] == [[1, "d", right], [-1, "d", left]], "D path edge")

    expected = {17: {"d10": -1, "F2": -1},
                18: {"G16": -1, "d2": -1}}
    for j in range(3):
        expected[24 + 14 * j] = {"d" + str(R[j + 1]): 1,
                                 "F" + str(P[j]): -1}
        expected[31 + 14 * j] = {"d" + str(R[j + 1]): -1,
                                 "F" + str(Q[j + 1]): -1}
        expected[32 + 14 * j] = {"G" + str(Q[j + 2]): -1, "D": -1}
        expected[25 + 14 * j] = {"G" + str(P[j + 1]): -1,
                                 "F" + str(R[j]): -1, "D": -1}
        expected[26 + 14 * j] = {"G" + str(R[j + 1]): -1,
                                 "d" + str(R[j]): -1}
    actual = {e["t"]: canonical(e["terms"]) for e in equations
              if canonical(e["terms"])}
    require(actual == expected and len(actual) == 17, "exact module equations")
    require(by_t[45] == [[-1, "d", 38], [-1, "F", 30]], "t45 source")
    require(by_t[54] == [[-1, "G", 52], [-1, "d", 38]], "t54 source")
    return {"original_equations": 48, "identities": 24,
            "common_D_tree_edges": 7, "remaining_module_equations": 17,
            "mask_obstruction_sources": [45, 54]}


def constraints(alpha, requirements):
    result = []
    for kind, target in requirements.items():
        fun = {"d": lambda x: x, "F": f, "G": g}[kind]
        mask = fun(alpha)
        c = (mask - target) % N
        require(c % 2 == 0, "inconsistent output parity")
        c //= 2
        require(c & (L ^ (mask & L)) == 0, "unavailable changed sign")
        rows = rows_for(kind)
        for bit in range(31):
            if mask >> bit & 1:
                result.append({"kind": kind, "bit": bit,
                               "row": rows[bit], "rhs": (c >> bit) & 1})
    return result


def check_solution(sol):
    alpha = sol["input_xor_mask"]
    requirements = sol["requirements"]
    if sol["status"] == "empty" and sol["reason"] in ("parity", "unavailable_sign_bit"):
        kind = sol["kind"]
        require(kind in requirements, "unknown contradiction map")
        fun = {"d": lambda x: x, "F": f, "G": g}[kind]
        mask = fun(alpha)
        target = requirements[kind]
        require(sol["output_mask"] == mask and sol["target"] == target, "contradiction data")
        c = (mask - target) % N
        if sol["reason"] == "parity":
            require(c % 2 == 1, "false parity contradiction")
        else:
            require(c % 2 == 0, "wrong sign contradiction parity")
            c //= 2
            bit = sol["impossible_bit"]
            require(sol["required_sign_word"] == c, "wrong sign word")
            require(0 <= bit < 31 and c >> bit & 1 and not (mask >> bit & 1),
                    "false unavailable-sign contradiction")
        return []
    correct = constraints(alpha, requirements)
    rows = sol["rows"]
    key = lambda r: (r["kind"], r["bit"], r["row"], r["rhs"])
    require(sorted(rows, key=key) == sorted(correct, key=key), "complete original bit rows")
    if sol["status"] == "empty":
        require(sol["reason"] == "linear_conflict", "unknown failure")
        coefficient = rhs = 0
        indices = sol["combination"]
        require(len(indices) == len(set(indices)), "duplicate conflict index")
        for j in indices:
            require(0 <= j < len(rows), "conflict index range")
            coefficient ^= rows[j]["row"]
            rhs ^= rows[j]["rhs"]
        require(coefficient == 0 and rhs == 1, "false affine contradiction")
        return []
    require(sol["status"] == "nonempty", "unknown fibre status")
    basis, particular = sol["basis"], sol["particular"]
    require(sol["dimension"] == len(basis) == rank(basis), "bad basis dimension")
    require(sol["rank"] == rank(r["row"] for r in rows) == 32 - len(basis), "incomplete basis")
    for r in rows:
        require((r["row"] & particular).bit_count() % 2 == r["rhs"], "invalid particular")
        for b in basis:
            require((r["row"] & b).bit_count() % 2 == 0, "basis leaves fibre")
    pairs = [[particular ^ z, particular ^ z ^ alpha] for z in span(basis)]
    for pair in pairs:
        values = dict(zip(("d", "F", "G"), diff(pair)))
        require(all(values[k] == v for k, v in requirements.items()), "direct pair mismatch")
    return pairs


def check_analysis_fibre(item):
    a, b = item["seed"]
    require(diff([a, b]) == item["seed_interface"], "incorrect seed interface")
    alpha = a ^ b
    require(item["xor_mask"] == alpha, "incorrect seed mask")
    rows = []
    for kind in item["preserve"]:
        fun = {"d": lambda x: x, "F": f, "G": g}[kind]
        mask = fun(alpha)
        rows.extend(rows_for(kind)[i] for i in range(31) if mask >> i & 1)
    basis = item["basis"]
    require(rank(basis) == len(basis) == item["dimension"] == 32 - rank(rows), "fibre basis rank")
    require(all((r & z).bit_count() % 2 == 0 for r in rows for z in basis), "homogeneous fibre")
    pairs = [[a ^ z, b ^ z] for z in span(basis)]
    values = sorted({tuple(diff(pair)) for pair in pairs})
    require(item["pair_count"] == len(pairs), "fibre pair count")
    require(item["distinct_interfaces"] == [list(v) for v in values], "fibre output values")


def verify_data(analysis, probe):
    equation_summary = check_equations(analysis)
    for item in analysis["fibres"].values():
        check_analysis_fibre(item)
    q_seed, p_seed = [0x00305680, 0x88abc2db], [0x96e4e732, 0x1f60538d]
    require(analysis["fibres"]["q_dG"]["seed"] == q_seed, "wrong Q seed")
    require(analysis["fibres"]["p_dF"]["seed"] == p_seed, "wrong P seed")
    D, qF, qG = diff(q_seed)
    pD, pF, _ = diff(p_seed)
    require(D != 0 and pD == D and (qF + pF) % N == 0 and (qG + D) % N == 0,
            "seed coupled equations")
    qmask, pmask = q_seed[0] ^ q_seed[1], p_seed[0] ^ p_seed[1]
    rmask = f(qmask)
    require(probe["D"] == D, "wrong construction D")
    require(probe["masks"] == {"Q": qmask, "P": pmask, "R": rmask}, "wrong construction masks")
    qsol = probe["q_fibre"]
    require(qsol["input_xor_mask"] == qmask and qsol["requirements"] == {"d": D, "G": -D % N},
            "wrong Q fibre target")
    qpairs = check_solution(qsol)
    require(probe["q_pairs"] == qpairs and len(qpairs) == 32, "incomplete Q fibre")
    a_values = sorted({-diff(pair)[1] % N for pair in qpairs})
    require(a_values == probe["q_A_values"] and len(a_values) == 16, "incomplete Q interface set")
    p_solutions = probe["p_opposite_F_fibres"]
    require(len(p_solutions) == len(a_values), "missing P target")
    viable = {}
    for A, sol in zip(a_values, p_solutions):
        require(sol["input_xor_mask"] == pmask and sol["requirements"] == {"d": D, "F": A},
                "wrong P target")
        ppairs = check_solution(sol)
        if ppairs:
            viable[str(A)] = [{"pair": p, "G": diff(p)[2]} for p in ppairs]
    require(viable == probe["p_viable_interfaces"], "incomplete viable P set")
    require(list(viable) == [str(0xbef39c7d)] and len(viable[str(0xbef39c7d)]) == 4,
            "changed P result")
    terminal = probe["terminal_R3_fibres"]
    require(len(terminal) == len(viable) ** 2 == 1, "terminal cross product incomplete")
    for sol in terminal:
        A1, A2 = sol["A1"], sol["A2"]
        require(str(A1) in viable and str(A2) in viable, "wrong terminal A values")
        require(sol["input_xor_mask"] == rmask and sol["requirements"] == {"d": A2, "G": -A1 % N},
                "wrong terminal constraints")
        require(not check_solution(sol) and sol["status"] == "empty", "terminal not excluded")
    require(probe["terminal_surviving_interfaces"] == 0 and
            probe["result"] == "restricted_family_excluded_at_terminal_R3", "wrong scoped result")

    left_mask, right_mask = f(qmask), g(rmask)
    require((left_mask, right_mask) == (0x4314a785, 0xc722ccc1), "mask composition")
    residues = lambda mask: sorted({((x ^ (mask & 7)) - x) % 8 for x in range(8)})
    left, right = residues(left_mask), residues(right_mask)
    require(left == [3, 5] and right == [1, 7] and not set(left) & set(right), "mod8 obstruction")
    return {"equation_check": equation_summary, "Q_pairs": len(qpairs),
            "Q_F_values": len(a_values), "P_target_fibres": len(p_solutions),
            "P_surviving_pairs": 4, "terminal_interfaces": len(terminal),
            "terminal_survivors": 0, "left_mod8": left, "right_mod8": right}


def sample_chain():
    pairs = [None, None, None, [0x129f8735, 0xe1264a98]]
    shifts = [0x84613278, 0x3182beac, 0xd810bcfe]
    for j in (2, 1, 0):
        v, w = pairs[j + 1]
        pairs[j] = [(g(w) + shifts[j]) % N, (g(v) + shifts[j]) % N]
    return pairs, shifts


def check_chain(pairs):
    require(all(a != b for a, b in pairs), "chain inactive pair")
    for j in range(3):
        require((diff(pairs[j + 1])[2] + diff(pairs[j])[0]) % N == 0, "reversed-image chain")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    source = (HERE.parent / "supports-v2.json").read_bytes()
    require(hashlib.sha256(source).hexdigest() == SUPPORT_HASH, "frozen support hash")
    require(json.loads(source)["supports"][0] == list(S), "frozen support 0")
    for kind in ("F", "G"):
        require(rank(rows_for(kind)) == 32, "sigma is not bijective")
        fun = f if kind == "F" else g
        for j in range(32):
            actual = fun(1 << j)
            encoded = sum(((r >> j) & 1) << i for i, r in enumerate(rows_for(kind)))
            require(actual == encoded, "original bit row mismatch")
    analysis = json.loads((HERE / "ANALYSIS.json").read_text())
    probe = json.loads((HERE / "FIXED-MASK-RUN.json").read_text())
    report = verify_data(analysis, probe)
    pairs, shifts = sample_chain()
    check_chain(pairs)
    require([((pairs[j][0] - g(pairs[j + 1][1])) % N) for j in range(3)] == shifts,
            "chain translation recovery")
    report["reversed_image_chain_example"] = {"pairs": pairs, "shifts": shifts,
                                               "scope": "R chain only, not a full assignment"}
    report["sigma_ranks"] = {"f": 32, "g": 32}
    report["negative_controls"] = []
    if args.negative:
        def rejected(name, action):
            try:
                action()
            except (ValueError, KeyError, IndexError):
                report["negative_controls"].append({"name": name, "rejected": True})
            else:
                raise ValueError("negative control accepted: " + name)

        bad = copy.deepcopy(analysis)
        bad["fibres"]["q_dG"]["seed"][1] ^= 1
        rejected("damaged_seed_word", lambda: verify_data(bad, probe))
        bad = copy.deepcopy(analysis)
        bad["equations"] = [e for e in bad["equations"] if e["t"] != 18]
        rejected("omitted_initial_boundary", lambda: verify_data(bad, probe))
        badp = copy.deepcopy(probe)
        badp["q_fibre"]["basis"][0] ^= 1
        rejected("damaged_affine_basis", lambda: verify_data(analysis, badp))
        badp = copy.deepcopy(probe)
        badp["q_A_values"].pop()
        rejected("omitted_interface_value", lambda: verify_data(analysis, badp))
        badp = copy.deepcopy(probe)
        badp["masks"]["R"] ^= 2
        rejected("wrong_R_mask", lambda: verify_data(analysis, badp))
        badp = copy.deepcopy(probe)
        badp["terminal_R3_fibres"][0]["impossible_bit"] = 0
        rejected("false_contradiction_bit", lambda: verify_data(analysis, badp))
        q, qp = 0x00305680, 0x88abc2db
        rejected("wrong_sigma1_rotation", lambda: require(
            (sigma(qp, 18, 19, 10) - sigma(q, 18, 19, 10) + qp - q) % N == 0,
            "wrong rotation fails local seed"))
        damaged_chain = copy.deepcopy(pairs)
        damaged_chain[1][1] ^= 1
        rejected("damaged_reversed_image_chain", lambda: check_chain(damaged_chain))
    report.update(status="pass", checker="direct output-bit reconstruction; no discovery imports",
                  independent_agent_review=False, uses_sat_or_smt=False,
                  complete_active_assignment_found=False, actual_schedule_pair_found=False)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
