"""Small exact obstruction probe, not an upper-bound certificate by itself."""
from itertools import combinations,product

def dist(x,y):
 if x==y:return 0
 for k in (3,2,1):
  if x[-k:]==y[:k]:return 4-k
 return 4

def bad(triple):
 a,b,c=triple
 return any(dist(x,y)+dist(y,z)==dist(x,z) for x,y,z in ((a,b,c),(a,c,b),(b,a,c),(b,c,a),(c,a,b),(c,b,a)))

def windows(cycle):return [tuple(cycle[(i+j)%len(cycle)] for j in range(4)) for i in range(len(cycle))]
cycle=tuple(range(8));base=windows(cycle);known={base[0],base[4]};zeros=set(base)-known
groups=[]
for i in range(8):
 ws=windows(cycle[:i]+cycle[i+1:])
 assert len(set(ws)&known)==1
 g=[w for w in ws if w not in set(base)]
 assert len(g)==3
 groups.append(g)
words=sorted(known|{w for g in groups for w in g});idx={w:i for i,w in enumerate(words)}
forbidden=[]
for tri in combinations(words,3):
 if bad(tri):forbidden.append(sum(1<<idx[w] for w in tri))
knownmask=sum(1<<idx[w] for w in known)
solutions=[]
for choices in product(range(3),repeat=8):
 mask=knownmask|sum(1<<idx[groups[i][ch]] for i,ch in enumerate(choices))
 if all(mask&t!=t for t in forbidden):solutions.append(choices)
print({'words':len(words),'forbidden_triples':len(forbidden),'all_even_solutions':len(solutions),'first':solutions[:1]})
if solutions:
 print('witness',[groups[i][ch] for i,ch in enumerate(solutions[0])])
