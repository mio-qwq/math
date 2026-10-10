from collections import deque
from itertools import combinations, permutations
import json

def distances(n,d):
    D=[]
    for start in range(n):
        row=[n+1]*n; row[start]=0; queue=deque([start])
        while queue:
            x=queue.popleft()
            for k in range(1,d+1):
                y=(x+k)%n
                if row[y]>n:
                    row[y]=row[x]+1; queue.append(y)
        D.append(row)
    return D

def gp(S,D):
    return all(D[x][z] != D[x][y]+D[y][z] for x,y,z in permutations(S,3))

def check(n,d):
    D=distances(n,d)
    assert all(D[x][y]==((y-x)%n+d-1)//d for x in range(n) for y in range(n))
    blockers={}
    for i,j,k in combinations(range(n),3):
        if not gp((i,j,k),D):
            blockers.setdefault(k,[]).append((1<<i)|(1<<j))
    best=[0]; count=[0]; projected=[0]
    # Translation symmetry allows restricting to sets containing 0.
    def visit(S,mask,start):
        count[0]+=1; best[0]=max(best[0],len(S))
        R=[0]+[(x-1)%d+1 for x in S[1:]]
        K=[0]+[(x-1)//d for x in S[1:]]
        assert R==sorted(set(R)),(n,d,S,R)
        assert gp(R,D),(n,d,S,R)
        assert all(D[S[i]][S[j]]==D[R[i]][R[j]]+K[j]-K[i] for i in range(len(S)) for j in range(len(S)) if i!=j),(n,d,S,R,K)
        projected[0]+=1
        for k in range(start,n):
            if all(mask & pair != pair for pair in blockers.get(k,[])):
                visit(S+[k],mask|(1<<k),k+1)
    visit([0],1,1)
    a=(n-1)%d+1
    predicted=max(a,d//a+1)
    assert best[0]==predicted,(n,d,best,predicted)
    for i,j,k in combinations(range(d+1),3):
        assert gp((i,j,k),D)==((k-i<a) or (j-i>=a and k-j>=a)),(n,d,a,i,j,k)
    return {'n':n,'d':d,'a':a,'gp':best[0],'anchored_gp_sets':count[0],'projection_checks':projected[0]}

results=[]
for n in range(3,23):
    for d in range(2,n):
        a=(n-1)%d+1
        if a==1:continue
        results.append(check(n,d))
print(json.dumps({'cases':len(results),'anchored_gp_sets':sum(r['anchored_gp_sets'] for r in results),'max_n':22,'results':results},indent=2))
