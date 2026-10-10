#!/usr/bin/env python3
"""Direct exact verification of the cubic triangle-expansion 3-template certificate."""
from itertools import permutations, product

edges = {
    'x': ('A', 'B', 0), 'y': ('B', 'C', 1), 't': ('C', 'A', 2),
    'e0': ('C', 'X0', 0), 'e1': ('A', 'X1', 1), 'e2': ('B', 'X2', 2),
}
templates = [
    ('x','y','t','e0','e1','e2'),
    ('t','x','y','e0','e1','e2'),
    ('t','e0','e1','x','y','e2'),
]

def local_sequences(order):
    assert set(order) == set(edges) and len(order) == 6
    assert [x for x in order if x.startswith('e')] == ['e0','e1','e2']
    seq = {v: [] for v in ['A','B','C','X0','X1','X2']}
    for edge in order:
        a,b,c = edges[edge]
        seq[a].append(c)
        seq[b].append(c)
    return {v: tuple(seq[v]) for v in ('A','B','C')}

def main():
    patterns = [local_sequences(x) for x in templates]
    assert [p['B'] for p in patterns] == [(0,1,2)] * 3
    assert len({p['A'] for p in patterns}) == 3
    assert len({p['C'] for p in patterns}) == 3
    assert all(len({p['A'],p['B'],p['C']}) == 3 for p in patterns)
    colors = list(permutations(range(3)))
    good = 0
    for neighbor_C,neighbor_A,neighbor_B in product(colors, colors,
            [x for x in colors if x != (0,1,2)]):
        assert any(p['C'] != neighbor_C and p['A'] != neighbor_A
                   and p['B'] != neighbor_B for p in patterns)
        good += 1
    assert good == 180
    try:
        local_sequences(('x','y','t','e1','e0','e2'))
    except AssertionError:
        pass
    else:
        raise AssertionError('invalid external order accepted')
    print('PASS three explicit edge-order certificates; 180/180 admissible outside patterns; negative test')

if __name__ == '__main__':
    main()
