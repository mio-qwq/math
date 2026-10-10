from pathlib import Path
import json
p=Path(__file__).with_name('check_independent.py')
src=p.read_text().split('\nresults=[]')[0]
ns={}; exec(src,ns)
results=[]
for n in range(2,17):
    for d in range(1,n):
        if d==1 or (n-1)%d==0:
            results.append(ns['check'](n,d))
D=ns['distances'](8,3)
assert not ns['gp']([0,1,3],D)
assert ns['gp']([0,2],D)
controls=[]
for label,modified in [('wrong_prediction',src.replace('predicted=max(a,d//a+1)','predicted=max(a,d//a+1)+1')),('broken_distance',src.replace('return D','D[0][1] = 99\n    return D'))]:
    ns2={};exec(modified,ns2)
    try:ns2['check'](8,3)
    except AssertionError:controls.append({'name':label,'detected':True})
    else:raise AssertionError('negative control not detected: '+label)
print(json.dumps({'boundary_cases':len(results),'anchored_gp_sets':sum(r['anchored_gp_sets'] for r in results),'negative_controls':controls,'results':results},indent=2))
