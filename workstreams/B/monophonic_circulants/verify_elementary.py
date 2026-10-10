"""Check the elementary proof's finite arithmetic, separately from BFS verifier."""
from itertools import combinations
import json
U=set(range(15))
forbidden=[{5},{1,2},{1,7},{2,4},{3,6},{4,7},{1,3,4},{2,6,7}]
def symmetric(P):return P|{(-x)%15 for x in P}
for P in forbidden:
 S=symmetric(P)
 assert any((a+b)%15 in S for a in S for b in S)
pairs={(1,3):{5,7,8,10},(3,4):{2,5,10,13},(2,6):{1,5,10,14},(6,7):{4,5,10,11},(1,4):{6,9},(1,6):{4,11},(4,6):{1,14},(2,3):{7,8},(2,7):{3,12},(3,7):{2,13}}
allowed={(),*( (i,) for i in (1,2,3,4,6,7)),*pairs,(1,4,6),(2,3,7)}
assert len(allowed)==19
for mask in range(128):
 P={i+1 for i in range(7) if mask>>i&1}
 restricted=not any(F<=P for F in forbidden)
 assert restricted==(tuple(sorted(P)) in allowed)
 S=symmetric(P)
 triangle_free=not any((a+b)%15 in S for a in S for b in S)
 assert triangle_free==restricted
for pair,missing in pairs.items():
 S=symmetric(set(pair));R={0}|S|{(a+b)%15 for a in S for b in S}
 assert U-R==missing and missing
for P in ({1,4,6},{2,3,7}):
 S=symmetric(P)
 assert {0}|S|{(a+b)%15 for a in S for b in S}==U
 assert {(s+5)%15 for s in S}==S and not {5,10}&S
# Corrupt the first missing-distance claim; it must not equal the real complement.
S=symmetric({1,3});assert U-({0}|S|{(a+b)%15 for a in S for b in S})!={5,7,8}
print(json.dumps(dict(status='PASS',masks=128,necessary_forbidden_patterns=8,allowed_sets=19,pair_sumset_rows=10,survivors=2,rejected_corrupt_table=1)))
