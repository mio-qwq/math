"""Freeze a closed matrix invariant for all words of at least two connectors."""
import json
from pathlib import Path
root=Path(__file__).parent;raw=json.loads((root/'five_relations.json').read_text());R={int(k):tuple(v) for k,v in raw['relations'].items() if int(k)<=16}
def mul(A,B):
 out=[]
 for row in A:
  val=0
  while row:
   bit=row&-row;row-=bit;val|=B[bit.bit_length()-1]
  out.append(val)
 return tuple(out)
seen={mul(A,B) for A in R.values() for B in R.values()};queue=list(seen)
for A in queue:
 for B in R.values():
  C=mul(A,B)
  if C not in seen:seen.add(C);queue.append(C)
assert all(any(row>>i&1 for i,row in enumerate(A)) for A in seen)
import zlib,base64,hashlib
data=json.dumps({'matrices':[list(A) for A in sorted(seen)]},separators=(',',':')).encode()
(root/'five_invariant.json').write_text(json.dumps({'encoding':'base64(zlib(UTF-8 JSON))','decoded_sha256':hashlib.sha256(data).hexdigest(),'data':base64.b64encode(zlib.compress(data,9)).decode()},indent=2)+'\n')
print('Matrices',len(seen))
