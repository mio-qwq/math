#!/usr/bin/env python3
"""Discovery only: strict codes supported on four distinct index symbols.

Floating solver bounds are not proof certificates. Printed witnesses must
be checked from the literal window definition before use.
"""
import argparse
import itertools
import json
import time


def complete_search(n, seconds):
    """Integer-only search for one representative of every rotation orbit.

    A timeout certifies nothing. A returned witness still gets an independent
    literal-window check in the acceptance checker.
    """
    start = time.monotonic()
    words, bad = constraints(n)
    index = {w: i for i, w in enumerate(words)}
    representatives = sorted({min(w[j:]+w[:j] for j in range(4)) for w in words})
    orbits = [[index[w[j:]+w[:j]] for j in range(4)] for w in representatives]
    word_orbit = {w: o for o, group in enumerate(orbits) for w in group}
    incidence = [[] for _ in words]
    for edge in bad:
        for v in edge:
            incidence[v].append(edge)
    nodes = 0

    def search(alive, chosen, pending):
        nonlocal nodes
        nodes += 1
        if time.monotonic()-start > seconds:
            raise TimeoutError
        while pending:
            v = pending.pop()
            if v in chosen:
                continue
            if v not in alive:
                return None
            chosen.add(v)
            banned = set(orbits[word_orbit[v]])-{v}
            for edge in incidence[v]:
                remaining = [w for w in edge if w not in chosen]
                if not remaining:
                    return None
                if len(remaining) == 1:
                    banned.add(remaining[0])
            if banned & chosen:
                return None
            removed = banned & alive
            alive.difference_update(removed)
            for o in {word_orbit[w] for w in removed}:
                group = [w for w in orbits[o] if w in alive]
                if not group:
                    return None
                if len(group) == 1 and group[0] not in chosen:
                    pending.append(group[0])
        choices = [[w for w in group if w in alive] for group in orbits
                   if not any(w in chosen for w in group)]
        if not choices:
            return sorted(chosen)
        group = min(choices, key=len)
        for v in group:
            result = search(alive.copy(), chosen.copy(), [v])
            if result is not None:
                return result
        return None

    try:
        selected = search(set(range(len(words))), set(), [index[(0,1,2,3)]])
        status = 'witness' if selected is not None else 'exhausted'
    except TimeoutError:
        selected, status = None, 'timeout'
    return {'scope': 'discovery; independently check any returned witness',
            'n': n, 'status': status, 'nodes': nodes, 'constraints': len(bad),
            'selected': [] if selected is None else [list(words[i]) for i in selected],
            'seconds': time.monotonic()-start}


def constraints(n):
    words = list(itertools.permutations(range(n), 4))
    index = {w: i for i, w in enumerate(words)}
    bad = set()
    # Every forbidden triple has positive gaps h,k and h+k <= 4.
    for h, k in ((1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (3, 1)):
        for v in words:
            left = [u for u in words if u[h:] == v[:4-h]]
            right = [w for w in words if v[k:] == w[:4-k]]
            for u in left:
                for w in right:
                    bad.add(tuple(sorted(set((index[u], index[v], index[w])))))
    # If two windows coincide, both are still selected occurrences; the
    # corresponding inequality forbids selecting their distinct word set.
    return words, sorted(bad)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    parser.add_argument('--seconds', type=float, default=40)
    parser.add_argument('--complete', action='store_true')
    parser.add_argument('--force-adjacent', action='store_true')
    args = parser.parse_args()
    if args.complete:
        print(json.dumps(complete_search(args.n, args.seconds), indent=2))
        return
    import numpy as np
    from scipy.optimize import milp, Bounds, LinearConstraint
    from scipy.sparse import coo_matrix
    start = time.monotonic()
    words, bad = constraints(args.n)
    rows, cols = [], []
    for i, edge in enumerate(bad):
        rows.extend([i]*len(edge))
        cols.extend(edge)
    mat = coo_matrix((np.ones(len(rows)), (rows, cols)),
                     shape=(len(bad), len(words))).tocsc()
    lower = np.zeros(len(words))
    if args.force_adjacent:
        if args.n < 5:
            raise ValueError('forced five-index adjacency requires n >= 5')
        lower[words.index((0,1,2,3))] = 1
        lower[words.index((1,2,3,4))] = 1
    result = milp(-np.ones(len(words)), integrality=np.ones(len(words)),
                  bounds=Bounds(lower, 1),
                  constraints=LinearConstraint(mat, -np.inf,
                                                [len(e)-1 for e in bad]),
                  options={'time_limit': args.seconds})
    selected = [] if result.x is None else [i for i,x in enumerate(result.x) if x > .5]
    print(json.dumps({'scope': 'solver discovery, not certified upper bound',
                      'n': args.n, 'force_adjacent': args.force_adjacent,
                      'words': len(words), 'constraints': len(bad),
                      'status': result.message, 'value': len(selected),
                      'solver_dual': getattr(result, 'mip_dual_bound', None),
                      'selected': [list(words[i]) for i in selected],
                      'seconds': time.monotonic()-start}, indent=2))


if __name__ == '__main__':
    main()
