"""Replay the root-proposed five-job counterexample through independent callbacks."""
import json
from pathlib import Path
from eager_independent_audit import Machine,run_eager_policy
parents=[set(),set(),set(),set(),{3}]
traces=[]
for u in range(1,5):
    m=Machine(parents,0,True)
    out=run_eager_policy(5,0,m.read,m.issue,initial_chunk_size=u)
    assert out['cycles']==3
    traces.append({'offset':u,'trace':m.trace,'result':out})
m=Machine(parents,0,False)
m.issue((0,1,3));m.issue((2,4))
assert len(m.done)==5
result={'status':'PASS','B':4,'W':3,'L':0,'N':5,'edges':[[3,4]],'offsets':traces,
        'optimal_trace':m.trace,'optimum':2,'lower_bound':'ceil(5/3)=2','mean_cost':3,
        'ratio':'3/2','scope':'specified fixed implementation only; isolated instance, no additive-constant conclusion'}
(Path(__file__).resolve().parent/'evidence/eager-five-job-counterexample.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: four offsets cost three, independent feasible witness and work bound give optimum two')
