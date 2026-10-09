"""Replay the seven-core certificate using Python's standard library only.

Checks fixed rational values and the integer graph recipe. Does not solve
an LP, enumerate graphs, instantiate a large graph, or prove the written
classification of all depth profiles.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def check():
    certificate = Path(__file__).resolve().parents[1] / 'results' / 'seven-core-substitution-exact.json'
    data = json.loads(certificate.read_text(encoding='utf-8'))
    assert data['outer_steps'] == [1, 2]
    assert data['deep_clusters'] == [0, 3]
    p = list(map(F, data['normalized_sizes']))
    q = list(map(F, data['dual_row_weights']))
    gamma = F(data['sharp_ratio'])
    assert len(p) == len(q) == 7
    assert all(x > 0 for x in p + q)
    assert sum(p) == sum(q) == 1
    c = [F(5, 16) if i in {0, 3} else F(1, 4) for i in range(7)]
    matrix = [[c[i] if i == j else F(1) if (j-i) % 7 in {1, 2} else F(0)
               for j in range(7)] for i in range(7)]
    assert data['internal_degree_ratios'] == [str(x) if x.denominator != 1 else f'{x}/1' for x in c]
    assert [[F(x) for x in row] for row in data['matrix']] == matrix
    primal = [sum(matrix[i][j]*p[j] for j in range(7)) for i in range(7)]
    dual = [sum(q[i]*matrix[i][j] for i in range(7)) for j in range(7)]
    assert primal == dual == [gamma]*7
    assert gamma == F(260889, 805108)
    assert F(21, 64)-gamma == F(data['gap_below_Grzesik_k3_threshold']) == F(52593, 12881728)
    assert F(1, 3)-gamma == F(data['gap_below_CH_triangle_threshold']) == F(22441, 2415324)
    assert gamma < F(21, 64) < F(1, 3)

    depths = [2 if i in {0, 3} else 1 for i in range(7)]
    assert all(sum(2**depths[(i+j) % 7] for j in range(3)) <= 8 for i in range(7))
    order = 16*201277
    sizes = [order*x for x in p]
    assert all(x.denominator == 1 and x > 0 for x in sizes)
    sizes = [int(x) for x in sizes]
    assert sum(sizes) == order
    factors = [sizes[i] // 4**depths[i] for i in range(7)]
    assert all(factors[i] > 0 and factors[i]*4**depths[i] == sizes[i] for i in range(7))
    internal = [factors[i]*((4**depths[i]-1)//3) for i in range(7)]
    outdegrees = [internal[i]+sizes[(i+1) % 7]+sizes[(i+2) % 7] for i in range(7)]
    indegrees = [internal[i]+sizes[(i-1) % 7]+sizes[(i-2) % 7] for i in range(7)]
    assert outdegrees == [1043556]*7
    assert F(outdegrees[0], order) == gamma
    assert indegrees[0] == 1072996
    assert len(set(indegrees)) > 1  # Only out-regularity is established.
    return {'pass': True, 'method': 'exact Fraction substitutions, no optimization',
            'primal_rows_checked': 7, 'dual_columns_checked': 7,
            'order': order, 'cluster_orders': sizes, 'internal_blow_up_factors': factors,
            'outdegrees': outdegrees, 'indegrees': indegrees, 'sharp_ratio': str(gamma),
            'graph_classification': 'written proof, not asserted by this arithmetic checker'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
