#!/usr/bin/env python3
"""Exact sharpness: a third size-two partition can obstruct red/blue splitting."""
from itertools import product
from balanced_partitions import balanced_colouring, verify_balance

P=((0,1),(2,3))
S=((0,2),(1,3))
T=((0,3),(1,2))
for A,B in ((P,S),(P,T),(S,T)):
    c=balanced_colouring(A,B)
    assert verify_balance(A,B,c)
    assert all({c[x] for x in block}=={0,1} for block in A+B)

assert not any(all(abs(sum(bits[x]==0 for x in block)-sum(bits[x]==1 for x in block)) <= 1
                   for block in P+S+T)
               for bits in product((0,1),repeat=4))
# The three pair partitions cover all six edges of K4 and would require
# a proper vertex 2-colouring of K4, which is impossible.
c=balanced_colouring([[0]],[[0]])
assert abs(sum(c[x]==0 for x in (0,))-sum(c[x]==1 for x in (0,)))==1
print('PASS every two of P,S,T simultaneously split, all three impossible (16 assignments)')
print('PASS singleton discrepancy-one lower bound')
