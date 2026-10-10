from search import *
def endchain(ls,types):
 g=Graph()
 def end(kind):
  if kind=='triangle':return g.triangle()
  if kind=='square':return g.square()[0]
  return g.v()
 l=end(types[0]);ss=[g.square() for _ in range(len(ls)-1)];r=end(types[1]);ends=[(None,l)]+ss+[(r,None)]
 for i,L in enumerate(ls):g.path(ends[i][1],ends[i+1][0],L)
 return g

def verify(g,ds):
 colors=[d.bit_length() for d in ds]
 for s,c in enumerate(colors):
  assert 1<=c<=4
  seen={s};front=[s]
  for depth in range(c):
   nxt=[]
   for u in front:
    for v in g.a[u]:
     if v not in seen:
      seen.add(v);nxt.append(v);assert colors[v]!=c,(s,v,c)
   front=nxt
 return colors
log=open(ROOT+'/endpoints.jsonl','a',buffering=1);i=0
for k in range(1,7):
 for ls in itertools.product(range(2,7),repeat=k):
  for types in itertools.combinations_with_replacement(['triangle','square','leaf'],2):
   if types[0]==types[1] and ls>ls[::-1]:continue
   g=endchain(ls,types);assert g.valid();t=time.time();status,nodes,r=solve(g,5)
   row=dict(i=i,family='endchain',lengths=ls,ends=types,n=len(g.a),status=status,nodes=nodes,seconds=time.time()-t)
   if r:verify(g,r)
   log.write(json.dumps(row)+'\n');i+=1
   if i%10000==0 or status!='SAT':print(row,flush=True)
   if status=='UNSAT':
    row['adjacency']=[sorted(a) for a in g.a];json.dump(row,open(ROOT+'/candidate.json','w'),indent=2);sys.exit()
print('ALL DONE',i)
