"""Independent classification/dual checks against pre-disclosure rank data."""
import json
from pathlib import Path
from independent_probe import ROTATIONS, envelope, project_rows
HERE=Path(__file__).resolve().parent
prior=json.loads((HERE/'independent_projection_results.json').read_text())
bad={tuple(c['I']):c for c in prior['deficient_triples']}
expected={}
for lane,(a,b) in enumerate(ROTATIONS):
    for k in (1,2):
        shape={0,(k*a)%64,(k*b)%64}
        assert len(shape)==3
        for pivot in shape:
            s=(-pivot)%64
            I=tuple(sorted((s+v)%64 for v in shape))
            t=sorted({s} if k==1 else {s,(s+a)%64,(s+b)%64})
            assert I not in expected
            expected[I]={'lane':lane,'k':k,'s':s,'t_columns':t}
            T=envelope(I)
            assert set(t)<=set(T)
            image=0
            for row in project_rows([],t,lane):image^=row
            assert image==sum(1<<j for j in I)
            free_image=0
            for row in project_rows(I,t,lane):free_image^=row
            assert free_image==0
assert set(expected)==set(bad)
for I,w in expected.items():
    c=bad[I];n=c['rows_per_lane']
    assert c['ranks']==[n-(i==w['lane']) for i in range(5)]
result={'normalized_supports_checked':prior['normalized_triples_checked'],
        'exceptional_normalized_supports':len(bad),'translation_orbits':10,
        'all_exceptions_equal_ten_claimed_shapes':True,
        'all_dual_characters_supported_in_envelope':True,
        'all_L_transpose_duals_equal_three_source_bits':True,
        'all_exceptional_projection_codimensions_one':True,
        'witnesses':[{'I':I,**w} for I,w in sorted(expected.items())]}
(HERE/'independent_triple_classification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='witnesses'},indent=2))
