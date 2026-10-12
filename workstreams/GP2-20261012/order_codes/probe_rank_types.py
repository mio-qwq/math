#!/usr/bin/env python3
"""Discovery only: strict codes determined by relative order of four letters.

Every selected four-window must have four different letters. Violations with
global repeats can be perturbed to distinct real letters, preserving every
strict comparison within each selected window. Thus eight-letter permutations
capture all violations for this particular class. This is not a bound on
arbitrary window codes.
"""
import itertools
import json
from pathlib import Path


def rank(word):
    order = {v: i for i, v in enumerate(sorted(word))}
    return tuple(order[v] for v in word)


def main():
    patterns = list(itertools.permutations(range(4)))
    index = {p: i for i, p in enumerate(patterns)}
    bad = {}
    triples = list(itertools.combinations(range(5), 3))
    for word in itertools.permutations(range(8)):
        indices = [index[rank(word[t:t+4])] for t in range(5)]
        for pos in triples:
            mask = sum(1 << i for i in set(indices[t] for t in pos))
            bad.setdefault(mask, (word, pos))
    minimal = [b for b in sorted(bad, key=lambda b: (b.bit_count(), b))
               if not any(a != b and a & b == a for a in bad)]
    alive = [i for i in range(24) if (1 << i) not in bad]
    feasible = []
    for k in range(len(alive), -1, -1):
        for choice in itertools.combinations(alive, k):
            mask = sum(1 << i for i in choice)
            if not any(mask & b == b for b in minimal):
                feasible.append(choice)
        if feasible:
            break
    report = {
        "scope": "relative-order four-letter templates only",
        "rank_patterns": [list(p) for p in patterns],
        "distinct_8letter_permutations": 40320,
        "minimal_forbidden_sets": [
            {"pattern_indices": [i for i in range(24) if b >> i & 1],
             "word": bad[b][0], "positions": bad[b][1]}
            for b in minimal],
        "allowed_single_patterns": alive,
        "maximum_patterns": k,
        "optimal_index_sets": feasible,
        "density_fraction": [k, 24],
    }
    target = Path(__file__).with_name("rank_discovery.json")
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"patterns_surviving_singletons": len(alive),
                      "minimal_constraints": len(minimal),
                      "maximum_patterns": k,
                      "number_of_maxima": len(feasible),
                      "first_maximum": [patterns[i] for i in feasible[0]],
                      "report": str(target)}, indent=2))


if __name__ == "__main__":
    main()
