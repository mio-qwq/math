"""Small discovery calculation; not an independent original-adjacency verifier.

Enumerates the 877 equality partitions of seven cyclic letters.  For each
partition it computes the largest possible number of selected window
OCCURRENCES subject to the original directed GP constraints on DISTINCT words.
The metric here is the proved overlap formula; independent replay must use BFS.
"""

from collections import Counter
from itertools import permutations
import json
from pathlib import Path


def partitions(n):
    def rec(xs, high):
        if len(xs) == n:
            yield tuple(xs)
            return
        for z in range(high + 2):
            yield from rec(xs + [z], max(z, high))
    yield from rec([0], 0)


def distance(u, v):
    if u == v:
        return 0
    for shift in range(1, 4):
        if u[shift:] == v[:-shift]:
            return shift
    return 4


def solve(xs):
    windows = [tuple(xs[(i + j) % 7] for j in range(4)) for i in range(7)]
    mult = Counter(w for w in windows if all(w[j] != w[j+1] for j in range(3)))
    words = sorted(mult)
    conflicts = set()
    for i, j, k in permutations(range(len(words)), 3):
        if distance(words[i], words[j]) + distance(words[j], words[k]) == distance(words[i], words[k]):
            conflicts.add((1 << i) | (1 << j) | (1 << k))
    best = 0
    witness = []
    for mask in range(1 << len(words)):
        if any(mask & c == c for c in conflicts):
            continue
        value = sum(mult[w] for i, w in enumerate(words) if mask >> i & 1)
        if value > best:
            best = value
            witness = [list(w) for i, w in enumerate(words) if mask >> i & 1]
    return best, witness


def main():
    counts = Counter()
    coefficients = Counter()
    exceptional = []
    for xs in partitions(7):
        best, witness = solve(xs)
        k = max(xs) + 1
        counts[k, best] += 1
        excess = max(0, best * (best - 2))
        coefficients[k] += excess
        if excess:
            exceptional.append(dict(pattern=list(xs), alphabet_size=k,
                                    max_occurrences=best, twice_excess=excess,
                                    witness=witness))
    out = dict(kind="discovery only; overlap metric", pattern_count=sum(counts.values()),
               capacity_counts=[dict(alphabet_size=k, max_occurrences=n, count=c)
                                for (k,n),c in sorted(counts.items())],
               twice_excess_coefficients=dict(sorted(coefficients.items())),
               exceptional_patterns=exceptional)
    Path(__file__).with_name("collision_discovery.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k != "exceptional_patterns"}, indent=2))


if __name__ == "__main__":
    main()
