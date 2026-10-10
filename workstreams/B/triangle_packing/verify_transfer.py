"""Verify the finite universal-language invariant using Boolean matrices.
Independent implementation from the bitmask discovery arithmetic. This is
B's self-verification; no separate reviewer or Lean run is implied.
"""
from itertools import permutations
from pathlib import Path
import json,hashlib,copy,sys

def product(A,B):
 return tuple(tuple(any(A[i][k] and B[k][j] for k in range(6)) for j in range(6)) for i in range(6))
def union(A,B):return tuple(tuple(A[i][j] or B[i][j] for j in range(6)) for i in range(6))
def diagonal(A):return any(A[i][i] for i in range(6))
def decode(row):
 assert len(row)==12 and all(type(x) is int and 0<=x<64 for x in row)
 ms=[tuple(tuple(bool(x & 2**j) for j in range(6)) for x in row[k:k+6]) for k in (0,6)]
 return tuple(ms)

def verify(cert):
 pairs=list(permutations(range(3),2));I=tuple(tuple(i==j for j in range(6)) for i in range(6));Z=tuple((False,)*6 for _ in range(6))
 # Check original local packing rule on the three-vertex path, not a hardcoded table.
 def legal(a,b,c):
  word=(a,b,c);radii=(1,2,2)
  return all(word[i]!=word[j] or j-i>radii[word[i]] for i in range(3) for j in range(i+1,3))
 P=tuple(tuple(b==bb and legal(a,b,c) for bb,c in pairs) for a,b in pairs)
 power=I;R={}
 for step in range(1,12):
  power=product(power,P)
  if step>=3:
   L=step-1
   R[L]=tuple(tuple(power[i][j] and not(L==2 and 0 in pairs[i] and 0 in pairs[j]) for j in range(6)) for i in range(6))
 J=tuple((True,)*6 for _ in range(6));assert power==J and product(J,P)==J
 E=tuple(tuple(0 not in a and 0 not in b for b in pairs) for a in pairs)
 states=[decode(row) for row in cert['states']];S=set(states)
 assert len(states)==len(S) and (I,Z) in S
 transitions=0
 for A,B in S:
  assert diagonal(A) or diagonal(B)
  for L in range(2,11):
   C=product(A,R[L]);D=product(B,R[L])
   if L==4:D=union(D,product(A,E))
   assert (C,D) in S,('not closed',L)
   transitions+=1
 return {'result':'PASS','invariant_states':len(S),'verified_transitions':transitions,'long_gap_relation':'all-ones from length10 onward','universal_trace_condition':True}

def main():
 p=Path(__file__).with_name('transfer_certificate.json');cert=json.loads(p.read_text());out=verify(cert);tests=[]
 bad=copy.deepcopy(cert);bad['states']=bad['states'][:-1]
 try:verify(bad)
 except AssertionError:tests.append('missing invariant state rejected')
 else:raise AssertionError('bad certificate accepted')
 bad=copy.deepcopy(cert);bad['states'].append([0]*12)
 try:verify(bad)
 except AssertionError:tests.append('zero-trace invariant state rejected')
 else:raise AssertionError('bad certificate accepted')
 out.update(negative_controls=tests,certificate_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),python=sys.version)
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
