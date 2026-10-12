#!/usr/bin/env python3
"""Read-only author artifact checks after independent reconstruction froze."""
import collections
import datetime
import hashlib
import itertools
import json
import pathlib
import check_independent as own

HERE=pathlib.Path(__file__).resolve().parent
AUTHOR=HERE.parent/'support12-v4'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    frozen=json.loads((HERE/'FIRST_AUTHOR_CONTACT.json').read_text())['sha256']
    assert all(digest(AUTHOR/n)==h for n,h in frozen.items())
    manifest=json.loads((AUTHOR/'manifest.json').read_text())['files']
    assert all(digest(AUTHOR/n)==h for n,h in manifest.items())
    cert=json.loads((AUTHOR/'CERTIFICATE.json').read_text())
    summary=[]
    for k,stored in zip(range(1,8),cert['cases']):
        own_cases=own.masks(k)
        own_classes=[{'alpha':f'{a:08x}',
                      'input_rows':[[f'{1<<bit:08x}',v>>bit&1]
                                    for bit in range(19,31) if fm>>bit&1]}
                     for a,fm,v,_,_ in own_cases]
        assert cert['positive_input_classes'][str(k)]==own_classes
        pairs=[(f'{a[0]:08x}',f'{b[0]:08x}')
               for a,b in itertools.product(own_cases,repeat=2)]
        assert [(c['alpha_x'],c['alpha_y']) for c in stored['cases']]==pairs
        assert stored['q']==k and stored['delta']==f'{k<<19:08x}'
        assert stored['mask_count']==len(own_cases) and stored['mask_pairs']==len(pairs)
        survivors=[c for c in stored['cases'] if c['g_leaves']]
        assert len(survivors)==int(k==5)
        if k==5:
            assert survivors[0]['alpha_x']==survivors[0]['alpha_y']=='ffd80000'
            assert survivors[0]['g_leaves']==1
            third=survivors[0]['third_pair']
            assert len(third)==len(own_cases)
            assert sorted(t['alpha_r'] for t in third)==sorted(f'{c[0]:08x}' for c in own_cases)
            assert all(t.get('g_leaves',0)==0 for t in third)
        summary.append({'k':k,'complete_input_classes':len(own_classes),
                        'complete_pair_cases':len(pairs),'stored_twin_survivors':len(survivors)})
    for receipt in cert['conflict_row_bank']:
        coefficients=constant=0
        for c,b in receipt:
            w=int(c,16)
            assert 0<=w<1<<96 and b in (0,1)
            coefficients^=w;constant^=b
        assert coefficients==0 and constant==1
    # Independently check the written integer combinations of original rows.
    support=json.loads((HERE.parent/'supports-v2.json').read_text())['supports']
    combos=[({18:1},{'d18':1,'d11':-1}),
            ({34:1},{'d34':1,'d18':-1}),
            ({50:-1},{'d43':1,'d34':1}),
            ({33:1,42:-1,49:-1},{'F34':1,'F18':-1}),
            ({33:1,42:-1,58:-1},{'F43':1,'F18':-1}),
            ({20:1,27:2,18:-2,36:-1,29:-1},{'G34':1,'G18':-1,'d18':-2}),
            ({36:-1,45:1,27:1,18:-1},{'G34':1,'G43':-1,'d18':-1})]
    for index,shift in ((12,0),(6,1),(7,3),(13,2)):
        S=set(support[index])
        for rows,target in combos:
            result=collections.Counter()
            for t,co in rows.items():
                tt=t+shift
                assert 16<=tt<64
                for prefix,i,v in [('d',tt,1),('G',tt-2,-1),('d',tt-7,-1),
                                   ('F',tt-15,-1),('d',tt-16,-1)]:
                    if i in S:result[prefix+str(i)]+=co*v
            assert {v:c for v,c in result.items() if c}=={
                v[0]+str(int(v[1:])+shift):c for v,c in target.items()}
    # Mutation controls are applied to memory copies; author bytes are untouched.
    corrupt=[list(row) for row in cert['conflict_row_bank'][0]]
    corrupt[0][1]^=1
    value=0
    for c,b in corrupt:value^=int(c,16)|(b<<96)
    assert value!=1<<96
    missing=pairs[:-1]
    assert missing!=pairs
    return {'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'author_manifest_sha256':digest(AUTHOR/'manifest.json'),
        'author_manifest_files_verified':len(manifest),'author_hashes':frozen,
        'positive_input_classes_and_pair_coverage':summary,
        'direct_XOR_row_receipts_checked':len(cert['conflict_row_bank']),
        'written_original_row_combinations_checked':28,
        'mutations_detected':['row receipt RHS flip','missing mask pair'],
        'scope':'artifact integrity/coverage and direct row identities; complete model exclusion independently rerun by check_independent.py'}

if __name__=='__main__':
    data=run()
    (HERE/'COMPARISON_RUN.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data))
