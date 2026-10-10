"""Reserved scope: exact boundary extension probes, not universal theorem yet."""
from itertools import combinations
from collections import deque
from pathlib import Path
import json
SEQ=[1,2,2,2,2]
def build(n,edges):
 A=[set() for _ in range(n)]
 for u,v in edges:A[u].add(v);A[v].add(u)
 return A

def expand(n,E):
 A=[set() for _ in range(3*n)];used=[0]*n;edges=[]
 for v in range(n):edges.extend(combinations(range(3*v,3*v+3),2))
 for u,v in E:
  x=3*u+used[u];used[u]+=1;y=3*v+used[v];used[v]+=1;edges.append((x,y))
 return build(3*n,edges),[3*v+used[v] for v in range(n) if used[v]<3]

def solve(A,pre):
 n=len(A);D=[]
 for s in range(n):
  ds=[99]*n;ds[s]=0;q=deque([s])
  while q:
   u=q.popleft()
   for v in A[u]:
    if ds[v]==99:ds[v]=ds[u]+1;q.append(v)
  D.append(ds)
 colors=dict(pre);nodes=0
 def rec():
  nonlocal nodes
  nodes+=1
  if len(colors)==n:return [colors[v] for v in range(n)]
  choices={v:[c for c in range(5) if all(c!=cc or D[v][u]>SEQ[c] for u,cc in colors.items())] for v in range(n) if v not in colors}
  v=min(choices,key=lambda x:len(choices[x]))
  for c in choices[v]:
   colors[v]=c;ans=rec()
   if ans is not None:return ans
   del colors[v]
  return None
 return rec(),nodes

def main():
 D=build(7,[(0,1),(0,2),(1,2),(1,3),(2,4),(3,5),(3,6),(4,5),(4,6),(5,6)])
 B,free=expand(2,[(0,1),(0,1)]);Broot=free[0]
 T,free=expand(3,[(0,1),(0,1),(0,2),(1,2)]);Troot=free[0]
 cases=[('diamond_loop_cap',D,0),('parallel_pendant_cap',B,Broot),('parallel_same_neighbor_cap',T,Troot)]
 out=[]
 for name,A,root in cases:
  outside=len(A);A=[s.copy() for s in A]+[{root}];A[root].add(outside)
  for a,b in [(0,1),(1,0),(1,2)]:
   col,nodes=solve(A,{root:a,outside:b})
   row={'name':name,'root':root,'outside':outside,'edges':[(u,v) for u,ns in enumerate(A) for v in ns if u<v],'pre':[a,b],'colors':col,'nodes':nodes}
   out.append(row);print(json.dumps({'name':name,'pre':[a,b],'result':'SAT' if col is not None else 'UNSAT','nodes':nodes}),flush=True)
 Path(__file__).with_name('cap_witnesses.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
