#!/usr/bin/env python3
"""Independent standard-library checks for endpoint and sampling statements.

This file imports no checker, certificate, optimizer, or model implementation
from the main workstream. Universal validity is covered by REVIEW.md; finite
checks here test identities, the explicit witness, and sampling semantics.
"""

from collections import Counter
from fractions import Fraction
from itertools import permutations, product
import json


class Rejected(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Rejected(message)


WORDS5 = """
0123 0124 0132 0134 0213 0214 0231 0234 0241 0243
0312 0314 0321 0324 0412 0413 0431 0432 1034 1042
1234 1324 1423 1432 2014 2034 2134 3014 3042 3124
"""
CODE5 = frozenset(tuple(map(int, word)) for word in WORDS5.split())
GAPS = ((1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (3, 1))


def rotations(word):
    return tuple(word[i:] + word[:i] for i in range(4))


def check_code(code, alphabet_size, injective=False):
    require(type(alphabet_size) is int and alphabet_size > 0,
            "alphabet must have a positive integer size")
    for word in code:
        require(len(word) == 4, "wrong word length")
        require(all(type(x) is int and 0 <= x < alphabet_size for x in word),
                "letter outside alphabet")
        if injective:
            require(len(set(word)) == 4, "noninjective selected index word")


def check_strict_by_overlaps(code, alphabet_size, injective=False):
    """Exclude all three selected windows of total span at most four.

    Compatible neighboring pairs determine a consistent concatenation, so
    testing the six positive gap pairs is equivalent to the literal A^8
    definition, even when words/letters repeat. No dynamic program is used.
    """
    check_code(code, alphabet_size, injective)
    predecessor = {gap: {word: [] for word in code} for gap in (1, 2, 3)}
    successor = {gap: {word: [] for word in code} for gap in (1, 2, 3)}
    counts = {}
    for gap in (1, 2, 3):
        counts[gap] = 0
        for left in code:
            for right in code:
                if left[gap:] == right[:4-gap]:
                    successor[gap][left].append(right)
                    predecessor[gap][right].append(left)
                    counts[gap] += 1
    for first_gap, second_gap in GAPS:
        for middle in code:
            require(not (predecessor[first_gap][middle]
                         and successor[second_gap][middle]),
                    "three compatible selected windows")
    return {str(gap): counts[gap] for gap in (1, 2, 3)}


def normalize(integer_weights):
    require(all(type(x) is int and x >= 0 for x in integer_weights),
            "invalid probability weight")
    total = sum(integer_weights)
    require(total > 0, "zero total probability")
    return tuple(Fraction(x, total) for x in integer_weights)


def probability(word, weights):
    result = Fraction(1)
    for letter in word:
        result *= weights[letter]
    return result


def no_qp(word):
    # Type 0=L, 1=R, 2=H, 3=N; all are coordinate types, not unique letters.
    return all(not (word[i] in (1, 2) and word[(i+1) % 4] in (0, 2))
               for i in range(4))


def endpoint_ie(weights, adjacent_pair_coefficient=4):
    l, r, h, _ = weights
    u, v = l+h, r+h
    return (1 - 4*u*v + adjacent_pair_coefficient*u*v*h
            + 2*u*u*v*v - 4*u*v*h*h + h**4)


def endpoint_nonnegative(weights):
    l, r, h, n = weights
    return (l**4 + r**4
            + 4*n*(l**3+r**3+l*l*r+l*r*r+h*(l*l+r*r+l*r))
            + n*n*(6*(l*l+r*r)+8*l*r+8*h*(l+r)+2*h*h)
            + 4*n**3*(l+r+h) + n**4)


def endpoint_checks():
    all_words = tuple(product(range(4), repeat=4))
    allowed = tuple(word for word in all_words if no_qp(word))
    coefficients = Counter(tuple(word.count(i) for i in range(4))
                           for word in allowed)
    require(len(all_words) == 256 and len(allowed) == 81,
            "unexpected endpoint type count")
    vectors = 0
    zero_mass_vectors = 0
    for integers in product(range(4), repeat=4):
        if sum(integers) == 0:
            continue
        weights = normalize(integers)
        raw = sum((probability(word, weights) for word in allowed), Fraction(0))
        require(raw == endpoint_ie(weights), "inclusion-exclusion mismatch")
        require(raw == endpoint_nonnegative(weights), "nonnegative form mismatch")
        l, r, h, n = weights
        require(raw >= l**4+r**4+2*h*h*n*n+4*h*n**3+n**4,
                "nonnegative lower bound failed")
        if n == 0:
            require(raw == l**4+r**4, "n=0 formula failed")
        vectors += 1
        zero_mass_vectors += int(0 in integers)
    return {
        "all_type_words": len(all_words), "no_qp_type_words": len(allowed),
        "exact_weight_vectors": vectors, "vectors_with_zero_weights": zero_mass_vectors,
        "coefficient_table_l_r_h_n": [
            {"powers": list(powers), "coefficient": count}
            for powers, count in sorted(coefficients.items(), reverse=True)
        ],
    }


def certificate5_checks():
    require(len(CODE5) == 30, "five-letter witness cardinality")
    overlaps = check_strict_by_overlaps(CODE5, 5, injective=True)
    orbits = {min(rotations(word)) for word in permutations(range(5), 4)}
    occupancy = Counter(min(rotations(word)) for word in CODE5)
    require(len(orbits) == 30 and set(occupancy) == orbits,
            "missing injective rotation orbit")
    require(set(occupancy.values()) == {1}, "repeated occupied orbit")
    restrictions = []
    for omitted in range(5):
        code4 = frozenset(word for word in CODE5 if omitted not in word)
        require(len(code4) == 6, "four-letter restriction cardinality")
        check_strict_by_overlaps(code4, 5, injective=True)
        restrictions.append(len(code4))
    adjacency = tuple(word for word in permutations(range(5), 5)
                      if word[:4] in CODE5 and word[1:] in CODE5)
    require(len(adjacency) == 4, "injective adjacency count")
    require((0, 1, 2, 3, 4) in adjacency, "missing stated adjacency witness")
    return {
        "alphabet_size": 5, "selected_words": 30,
        "occupied_injective_rotation_orbits": len(orbits),
        "gap_pair_combinations_checked": [list(pair) for pair in GAPS],
        "compatible_ordered_pairs_by_gap": overlaps,
        "four_letter_restriction_sizes": restrictions,
        "injective_adjacency_count": len(adjacency),
        "injective_adjacency_words": ["".join(map(str, word)) for word in adjacency],
        "rho5": "1/4", "rho4": "1/4",
        "normalized_adj5": "1/30",
    }


def validate_motif(k, queries):
    require(type(k) is int and k >= 0, "invalid motif order")
    for query in queries:
        require(len(query) == 4 and len(set(query)) == 4,
                "motif query must have four distinct indices")
        require(all(type(x) is int and 0 <= x < k for x in query),
                "motif query index outside range")


def motif_truth(code, letters, queries, formula):
    return bool(formula(tuple(tuple(letters[i] for i in query) in code
                              for query in queries)))


def motif_checks():
    # These are two inherited strict patterns, not a newly claimed construction.
    code = frozenset(((0, 0, 0, 1), (0, 0, 1, 1)))
    check_strict_by_overlaps(code, 2)
    weights = normalize((2, 3))
    index_size = 5
    motifs = (
        ("selected", 4, ((0, 1, 2, 3),), lambda z: z[0]),
        ("adjacent", 5, ((0, 1, 2, 3), (1, 2, 3, 4)), lambda z: z[0] and z[1]),
        ("xor_adjacent", 5, ((0, 1, 2, 3), (1, 2, 3, 4)), lambda z: z[0] != z[1]),
        ("empty_rotation", 4, rotations((0, 1, 2, 3)), lambda z: not any(z)),
        ("shared_indices_with_negation", 5,
         ((0, 1, 2, 3), (1, 2, 3, 4), (4, 3, 0, 1)),
         lambda z: (z[0] and not z[1]) or z[2]),
    )
    index_words = tuple(permutations(range(index_size), 4))
    samples = []
    for image in product(range(2), repeat=index_size):
        inverse = frozenset(word for word in index_words
                            if tuple(image[i] for i in word) in code)
        check_strict_by_overlaps(inverse, index_size, injective=True)
        samples.append((inverse, probability(image, weights)))
    result = []
    for name, k, queries, formula in motifs:
        validate_motif(k, queries)
        raw_probability = sum(
            (probability(letters, weights) for letters in product(range(2), repeat=k)
             if motif_truth(code, letters, queries, formula)), Fraction(0))
        injections = tuple(permutations(range(index_size), k))
        expected_count = Fraction(0)
        for inverse, mass in samples:
            count = sum(motif_truth(inverse, injection, queries, formula)
                        for injection in injections)
            expected_count += mass * count
        require(expected_count == len(injections)*raw_probability,
                "joint Boolean motif transfer mismatch")
        result.append({"name": name, "k": k, "injections": len(injections),
                       "product_probability": str(raw_probability),
                       "expected_count": str(expected_count)})
    return {"sampled_alphabet_maps": len(samples), "motifs": result}


def rejects(action):
    try:
        action()
    except Rejected:
        return True
    return False


def negative_controls():
    uniform = normalize((1, 1, 1, 1))
    actual_endpoint = sum((probability(word, uniform)
                           for word in product(range(4), repeat=4) if no_qp(word)),
                          Fraction(0))
    controls = {
        "changed_endpoint_coefficient": lambda: require(
            endpoint_ie(uniform, 5) == actual_endpoint, "damaged coefficient"),
        "negative_probability_weight": lambda: normalize((1, -1, 1, 1)),
        "zero_total_probability": lambda: normalize((0, 0, 0, 0)),
        "selected_constant_loop": lambda: check_strict_by_overlaps(
            CODE5 | {(0, 0, 0, 0)}, 5),
        "second_selected_rotation": lambda: check_strict_by_overlaps(
            CODE5 | {(1, 2, 3, 0)}, 5),
        "noninjective_index_word": lambda: check_code(
            CODE5 | {(0, 1, 2, 2)}, 5, injective=True),
        "repeated_index_motif_query": lambda: validate_motif(4, ((0, 0, 1, 2),)),
        "damaged_adjacency_count": lambda: require(
            sum(word[:4] in CODE5 and word[1:] in CODE5
                for word in permutations(range(5))) == 5, "damaged adjacency"),
    }
    outcomes = {name: rejects(action) for name, action in controls.items()}
    require(all(outcomes.values()), "a damaged input was accepted")
    return outcomes


def main():
    result = {
        "review_kind": "independent AI and exact standard-library checks",
        "scope": "endpoint identities; strict order-five witness; Boolean motif semantics",
        "endpoint": endpoint_checks(),
        "five_letter_certificate": certificate5_checks(),
        "joint_motif_transfer": motif_checks(),
        "negative_controls_rejected": negative_controls(),
        "status": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
