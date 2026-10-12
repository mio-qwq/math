#!/usr/bin/env python3
"""Post-freeze source, high-mask, original-row and four-pair fixture audit.

Imports only the reviewer's independent sigma0/inverse checker. No author
program is executed, and the 11440 endpoint discovery comparisons are
not repeated.
"""
import copy
import datetime
import hashlib
import json
import pathlib
import check_independent as own

HERE=pathlib.Path(__file__).resolve().parent
AUTHOR=HERE.parent/'actual-boundary-v6'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def g(x):return own.rot(x,17)^own.rot(x,19)^(x>>10)

def original_rows(support):
    return {str(t):row for t in range(16,64)
            if (row:=[[kind,i,c] for kind,i,c in [('d',t,1),('G',t-2,-1),
                 ('d',t-7,-1),('F',t-15,-1),('d',t-16,-1)] if i in support])}

def pair(item):
    x=item['x'];y=item['y']
    assert 0<=x<own.N and 0<=y<own.N and x!=y
    expected={'x':x,'y':y,'difference':(y-x)&own.M,
              'F':(own.f(y)-own.f(x))&own.M,
              'G':(g(y)-g(x))&own.M,'input_xor':x^y}
    assert item==expected
    return expected

def fixture_check(fixture,support):
    actual={int(j):pair(item) for j,item in fixture['pairs_by_index'].items()}
    assert set(actual)=={13,29,26,42}
    p,q,u,v=(actual[j] for j in (13,29,26,42))
    assert p['difference']==q['difference']==fixture['common_c']!=0
    assert u['difference']==v['difference']==fixture['common_b']!=0
    assert (p['F']+q['F'])&own.M==0
    assert (u['G']+v['G'])&own.M==0
    assert (p['F']+q['F']+u['G']+v['G'])&own.M==0
    a=(-u['F'])&own.M;e=(p['F']+u['G'])&own.M
    k=(-q['G'])&own.M;z=v['F'];boundary=(-p['G']-q['G'])&own.M
    assert [fixture[s] for s in ('a','e','k','d57','reverse_boundary_target')]==[a,e,k,z,boundary]
    assert all(x!=0 for x in (a,e,k,z,boundary))
    assert boundary==0xffd519ca
    assert fixture['sigma0_sum_c_pairs']==fixture['sigma1_sum_b_pairs']==0
    assert own.f(own.M)==0x1fffffff and g(own.M)==0x003fffff
    assert q['x']==own.M^p['y'] and q['y']==own.M^p['x']
    assert v['x']==own.M^u['y'] and v['y']==own.M^u['x']
    assert p['F']==0x20000000 and u['G']==0x00400000
    assert (p['G']+q['G'])&own.M==2*(p['G']&0x3fffff)
    assert (u['F']&~own.f(own.M))==0
    # Only these two original rows use provided actual pair differences alone.
    assert q['difference']-p['difference']==0       # E29
    assert v['difference']-u['difference']==0       # E42
    # These other five identities use explicitly defined interface auxiliaries;
    # the corresponding word pairs at15,28,34,57 are still absent.
    assert (e-u['G']-p['F'])&own.M==0              # E28
    assert (-q['G']-k)&own.M==0                   # E31
    assert (-a-u['F'])&own.M==0                   # E41
    assert (-v['G']-q['F']-e)&own.M==0            # E44
    assert (z-v['F'])&own.M==0                    # E57
    assert 0 not in support and 8 not in support
    # Inverse row15: d_-1=d15-G13-d8-F0, together with E31.
    assert (k-p['G'])&own.M==boundary
    missing=sorted(set(support)-set(actual))
    assert missing==[10,11,15,18,20,28,34,43,57]
    assert len(missing)==9
    return {'actual_pairs':actual,'author_auxiliary':{'a':a,'b':u['difference'],
              'c':p['difference'],'e':e,'k':k,'z':z},
            'reviewer_auxiliary':{'a':u['difference'],'b':a},
            'original_rows_using_only_actual_pair_differences':[29,42],
            'additional_rows_using_defined_auxiliary_interfaces':[28,31,41,44,57],
            'inverse_boundary_target':f'{boundary:08x}','missing_actual_pairs':missing,
            'scope':'actual four-pair conservation subsystem only; no complete25row actual support or message blocks'}

def run():
    contact=json.loads((HERE/'FIRST_AUTHOR_CONTACT.json').read_text())['sha256']
    assert all(digest(AUTHOR/n)==h for n,h in contact.items())
    manifest=json.loads((AUTHOR/'SHA256.json').read_text())['files']
    assert all((AUTHOR/n).stat().st_size==meta['bytes'] and digest(AUTHOR/n)==meta['sha256']
               for n,meta in manifest.items())
    freeze=json.loads((HERE/'PRE_AUTHOR_FREEZE.json').read_text())['independent_files']
    assert all(digest(HERE/n)==h for n,h in freeze.items())
    evidence=json.loads((AUTHOR/'MASK_EXPERIMENT.json').read_text())
    author_run=json.loads((AUTHOR/'CHECK_RUN.json').read_text())
    rows,inverse=own.inverse_rows()
    columns=[own.finv(1<<j,inverse) for j in range(32)]
    assert evidence['f_inverse_basis_hex']==[f'{r:08x}' for r in columns]
    high=[]
    for k in range(22,32):
        stored=evidence['strata'][k]
        assert stored['power_bit']==k
        masks=[own.interval(k,e) for e in range(k,32)]
        forward=[(own.f(a)&-own.f(a)).bit_length()-1 for a in masks]
        inv_masks=[own.finv(a,inverse) for a in masks]
        backward=[(a&-a).bit_length()-1 for a in inv_masks]
        assert forward==[k-18]*(32-k)
        assert stored['forward_run_valuation']==forward
        assert stored['inverse_output_run_valuation']==backward
        assert all(j<k-18 for j in backward) and not stored['surviving_endpoint_triples']
        high.append({'k':k,'forward_valuation':k-18,'inverse_valuation_max':max(backward),
                     'inverse_run_words_hex':[f'{a:08x}' for a in inv_masks]})
    assert evidence['empty_power_bits']==list(range(22,32))
    assert author_run['verified_summary']['high_power_certificate']==high
    support_path=HERE.parent/'supports-v2.json'
    support=set(json.loads(support_path.read_text())['supports'][12])
    reconstructed=original_rows(support)
    assert len(reconstructed)==25
    assert author_run['original_48_row_reduction']['nonzero_rows']==reconstructed
    zeros=[t for t in range(16,64) if str(t) not in reconstructed]
    assert len(zeros)==23 and author_run['original_48_row_reduction']['zero_rows']==zeros
    # Elimination of E28 and E44 gives exactly the four-derivative conservation row.
    totals={}
    for t in (28,44):
        for name,i,c in reconstructed[str(t)]:totals[name+str(i)]=totals.get(name+str(i),0)+c
    assert {name:c for name,c in totals.items() if c}=={
        'G26':-1,'F13':-1,'G42':-1,'F29':-1}
    fixture=fixture_check(evidence['analytic_conservation_fixture'],support)
    assert author_run['verified_summary']['actual_reverse_boundary']==int(fixture['inverse_boundary_target'],16)
    # Mutations occur only in memory, never on the author's frozen bytes.
    bad_word=copy.deepcopy(evidence['analytic_conservation_fixture'])
    bad_word['pairs_by_index']['13']['y']^=1
    try:fixture_check(bad_word,support)
    except AssertionError:pass
    else:raise AssertionError('corrupt actual word accepted')
    bad_G=copy.deepcopy(evidence['analytic_conservation_fixture'])
    bad_G['pairs_by_index']['29']['G']=0
    try:fixture_check(bad_G,support)
    except AssertionError:pass
    else:raise AssertionError('corrupt actual G accepted')
    assert set(fixture['actual_pairs'])!=support
    try:assert author_run['verified_summary']['high_power_certificate'][:-1]==high
    except AssertionError:pass
    else:raise AssertionError('missing high certificate stratum accepted')
    structure=HERE.parent/'support12-structure-review-v7/manifest.json'
    structure_hash=digest(structure)
    assert structure_hash=='fb056bb7063b075f6a98e4eea05329267e60e00e7554184ea75e4f5b7b2d0d14'
    context={'accepted_structure_review_manifest_sha256':structure_hash,
       'accepted_structure_author_proof_sha256':digest(HERE.parent/'support12-structure-v7/PROOF.md'),
       'overlap':'Accepted D valuation<=16 already excludes high signed powers in author a=reviewer b. Accepted reciprocal signature upperbound23 covers author b=reviewer a powersk>=24; exact signedpowerk22,23 remains additional.',
       'structure_signature_table_replayed':False,
       'old11440_discovery_comparisons_replayed':False}
    return {'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'author_hashes':contact,'manifest_files_verified':len(manifest),
            'sigma0_inverse_basis_columns_checked':32,'high_interval_masks_checked':55,
            'original_rows_total':48,'nonzero_rows':reconstructed,'zero_rows':zeros,
            'fixture':fixture,'symbol_mapping':{'reviewer a':'author b=-checkpoint A',
                'reviewer b':'author a=checkpoint D'},'overlap_context':context,
            'negative_controls':['actual word mutation rejected','actual G mutation rejected',
                 'missing ninth actual-pair set prevents full-support promotion',
                 'missing high stratum detected'],'unreviewed_supplementary_scope':
            'Low-k stored endpoint candidates and complete11440 traversal remain author-only statistics; not premises of the accepted high-power theorem.'}

if __name__=='__main__':
    report=run()
    (HERE/'COMPARISON_FIXTURE_RUN.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'original_rows':48,'nonzero_rows':25,
                      'inverse_masks':55,'actual_pairs':4,'fixture_boundary':report['fixture']['inverse_boundary_target']}))
