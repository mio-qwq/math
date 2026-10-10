from search import *
exec(open(ROOT+'/endpoints.py').read().split('log=open')[0])
log=open(ROOT+'/leaves.jsonl','w',buffering=1);i=0
for k in range(1,6):
 for types in [('triangle','leaf'),('square','leaf'),('leaf','leaf')]:
  ranges=[range(2,7) for _ in range(k)]
  ranges[-1]=range(1,7)
  if types[0]=='leaf':ranges[0]=range(1,7)
  for ls in itertools.product(*ranges):
   if ls[0]!=1 and ls[-1]!=1:continue
   if types[0]==types[1] and ls>ls[::-1]:continue
   g=endchain(ls,types);assert g.valid();status,nodes,r=solve(g,5)
   row=dict(i=i,family='endchain',lengths=ls,ends=types,n=len(g.a),status=status,nodes=nodes)
   if r:verify(g,r)
   log.write(json.dumps(row)+'\n');i+=1
   if status!='SAT':print(row,flush=True)
   if status=='UNSAT':
    row['adjacency']=[sorted(a) for a in g.a];json.dump(row,open(ROOT+'/candidate.json','w'),indent=2);sys.exit()
print('LEAF DONE',i,flush=True)
for line in open(ROOT+'/runs.jsonl'):
 row=json.loads(line);g=globals()[row['family']](row['lengths']);s,n,r=solve(g,5);assert s=='SAT';verify(g,r)
print('REPLAY VERIFIED 4376',flush=True)
# Small exceptional components: cycles, paths and K2,3.
for n in range(1,101):
 for cyclic in [False,True]:
  if cyclic and n<3:continue
  g=Graph()
  for _ in range(n):g.v()
  for v in range(n-1):g.e(v,v+1)
  if cyclic:g.e(0,n-1)
  s,nd,r=solve(g,5);assert s=='SAT';verify(g,r)
g=Graph()
for _ in range(5):g.v()
for x in [0,1]:
 for y in [2,3,4]:g.e(x,y)
assert g.valid();s,nd,r=solve(g);assert s=='SAT';colors=verify(g,r)
json.dump(dict(family='K2,3',adjacency=[sorted(a) for a in g.a],coloring=colors),open(ROOT+'/example.json','w'),indent=2)
print('EXCEPTIONS VERIFIED',flush=True)
