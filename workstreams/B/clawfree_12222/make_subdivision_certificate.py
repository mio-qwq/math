"""Discovery-side certificate export. Verifier does not import this or probe."""
import json
from pathlib import Path
from itertools import product
from verify_subdivided import adjacency,check
# Local copy avoids importing probe and its top-level diagnostic output.
exec(Path(__file__).with_name('probe_subdivision.py').read_text().split('for L in range(2,13):')[0])
def canonical(c):
    names={0:0};n=1;out=[]
    for x in c:
        if x not in names:names[x]=n;n+=1
        out.append(names[x])
    return tuple(out)
reps=sorted({canonical(c) for c in rows})
assert len(reps)==42
out=[dict(boundary=c,words={str(L):extend(c,L) for L in (4,5,6)}) for c in reps]
assert all(all(r['words'].values()) for r in out)
Path(__file__).with_name('subdivision_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(canonical_boundaries=len(reps),base_words=3*len(reps))))
