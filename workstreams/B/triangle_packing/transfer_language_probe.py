from transfer_probe import states,P,mul,diag,rs
from collections import deque
I=tuple(1<<i for i in range(6));gens={L:rs[L] for L in range(2,11)}
seen={I:0};queue=[I];edges={};parents={}
for A in queue:
 edges[A]={L:mul(A,R) for L,R in gens.items()}
 for L,B in edges[A].items():
  parents.setdefault(B,set()).add(A)
  if B not in seen:seen[B]=len(seen);queue.append(B)
bad={A for A in queue if not diag(A)};live=set(bad);q=list(bad)
for A in q:
 for B in parents.get(A,()):
  if B not in live:live.add(B);q.append(B)
print('STATES',len(seen),'BAD',len(bad),'CAN REACH BAD',len(live))
active=set();done=set();words=[]
def dfs(A,prefix):
 if A in active:raise ValueError(('LIVE CYCLE',prefix))
 if A in bad:words.append(prefix)
 active.add(A)
 for L,B in edges[A].items():
  if B in live:dfs(B,prefix+(L,))
 active.remove(A)
if I in live:dfs(I,())
print('ALL BAD WORDS',words)
