#!/usr/bin/env python3
"""Post-freeze comparison and controls; imports only the independent engine."""
import datetime
import hashlib
import itertools
import json
import pathlib
import check_independent as own

HERE=pathlib.Path(__file__).resolve().parent
AUTHOR=HERE.parent/'support12-extension-v5'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def solution(basis):
    value=0
    for pivot,row in sorted(basis.items()):
        rhs=row>>96
        parity=(row&value).bit_count()%2
        if rhs^parity:value|=1<<pivot
    assert all(((row&value).bit_count()%2)==(row>>96) for row in basis.values())
    return [value>>32*i&own.M for i in range(3)]

def twin_witness(k,a,b):
    fa,fb=a[3],b[3]
    ga,gb=a[4],b[4]
    D=k<<18
    if ga+gb<2*D or (fa-fb)&1 or (gb-ga-2*D)&1:return None
    eqs=[own.equation_templates(fa,fb,((fa-fb)//2)&((1<<31)-1),-1,
                               own.FR,[r<<32 for r in own.FR]),
         own.equation_templates(gb,ga,((gb-ga-2*D)//2)&((1<<31)-1),-1,
                               [r<<32 for r in own.GR],own.GR)]
    stack=[(0,(0,0),own.fixed_input_basis((a,b,(0,0,0,0,0))))]
    while stack:
        step,cs,bs=stack.pop()
        if step==62:
            x,y,_=solution(bs)
            xp=(x+D)&own.M;yp=(y+D)&own.M
            assert x^xp==a[0] and y^yp==b[0]
            fx=(own.sigma0(xp)-own.sigma0(x))&own.M
            fy=(own.sigma0(yp)-own.sigma0(y))&own.M
            gx=(own.sigma1(xp)-own.sigma1(x))&own.M
            gy=(own.sigma1(yp)-own.sigma1(y))&own.M
            assert fx==fy and (gy-gx)&own.M==2*D
            return {'x':f'{x:08x}','xp':f'{xp:08x}','y':f'{y:08x}',
                    'yp':f'{yp:08x}','F':f'{fx:08x}',
                    'Gx':f'{gx:08x}','Gy':f'{gy:08x}'}
        bit,which=divmod(step,2)
        for nxt,rows in eqs[which][bit][cs[which]]:
            nb=bs.copy()
            if not all(own.insert(nb,r,v) for r,v in rows):continue
            nc=list(cs);nc[which]=nxt
            stack.append((step+1,tuple(nc),nb))
    return None

def run():
    frozen=json.loads((HERE/'FIRST_AUTHOR_CONTACT.json').read_text())['sha256']
    assert all(digest(AUTHOR/n)==h for n,h in frozen.items())
    manifest=json.loads((AUTHOR/'manifest.json').read_text())['files']
    assert all(digest(AUTHOR/n)==h for n,h in manifest.items())
    dependencies=json.loads((AUTHOR/'AUTHOR-RECEIPT.json').read_text())['dependencies']
    assert all(digest((AUTHOR/n).resolve())==h for n,h in dependencies.items())
    previous=HERE.parent/'support12-review-v4'
    old_manifest=json.loads((previous/'SHA256.json').read_text())['files']
    assert all(digest(previous/n)==h for n,h in old_manifest.items())
    assert json.loads((previous/'REVIEW_RECEIPT.json').read_text())['status']=='ACCEPT'
    # Definition-based universal width identities, including the top bit.
    assert all(own.GR[j]>>18==0 for j in range(22,31))
    assert own.GR[31]==(1<<16)|(1<<18)
    assert 3*(1<<23)<1<<32
    cert=json.loads((AUTHOR/'CERTIFICATE.json').read_text())
    assert cert['definition']['new_odd_representatives']==list(range(1,16,2))
    assert [c['q'] for c in cert['cases']]==list(range(1,16,2))
    summary=[]
    total_thirds=0
    for k,stored in zip(range(1,16,2),cert['cases']):
        cases=own.masks(k)
        for alpha,_,_,_,gamma in cases:
            assert alpha&((1<<18)-1)==0 and alpha>>18&1
            actual=own.sigma1(alpha)
            assert actual>>31==1 and actual&0x7fc00000==0
            assert gamma==actual&0x7fffffff
        classes={}
        for orientation in ('positive','negative'):
            classes[orientation]=[
                {'alpha':f'{a:08x}',
                 'input_rows':[[f'{1<<bit:08x}',(v^(fm if orientation=='negative' else 0))>>bit&1]
                               for bit in range(18,31) if fm>>bit&1]}
                for a,fm,v,_,_ in cases]
        assert cert['input_classes'][str(k)]==classes
        pairs=[(f'{a[0]:08x}',f'{b[0]:08x}') for a,b in itertools.product(cases,repeat=2)]
        assert [(c['alpha_x'],c['alpha_y']) for c in stored['cases']]==pairs
        assert stored['q']==k and stored['delta']==f'{k<<18:08x}'
        assert stored['positive_masks']==stored['negative_masks']==len(cases)
        assert stored['mask_pairs']==len(pairs)
        own_survivors=[]
        for a,b in itertools.product(cases,repeat=2):
            witness=twin_witness(k,a,b)
            if witness is not None:
                own_survivors.append({'alpha_x':f'{a[0]:08x}','alpha_y':f'{b[0]:08x}',
                                      'actual_twin_witness':witness})
        assert [(c['alpha_x'],c['alpha_y']) for c in own_survivors]==[
            (c['alpha_x'],c['alpha_y']) for c in stored['cases'] if c['g_leaves']]
        thirdcount=0
        for c in stored['cases']:
            rows=c['third_pair']
            assert len(rows)==c['g_leaves']*len(cases)
            for ordinal in range(c['g_leaves']):
                subset=[r for r in rows if r['branch']==ordinal]
                assert sorted(r['alpha_r'] for r in subset)==sorted(f'{a[0]:08x}' for a in cases)
            assert all(r.get('g_leaves',0)==0 for r in rows)
            thirdcount+=len(rows)
        total_thirds+=thirdcount
        summary.append({'k':k,'mask_classes_each_orientation':len(cases),
                        'complete_twin_mask_pairs':len(pairs),'feasible_twin_mask_pairs':own_survivors,
                        'stored_twin_branches':sum(c['g_leaves'] for c in stored['cases']),
                        'third_mask_tests_checked':thirdcount})
    assert sum(s['complete_twin_mask_pairs'] for s in summary)==12245
    assert total_thirds==612
    for receipt in cert['conflict_row_bank']:
        coefficients=constant=0
        for c,b in receipt:
            w=int(c,16);assert 0<=w<1<<96 and b in (0,1)
            coefficients^=w;constant^=b
        assert coefficients==0 and constant==1
    mutated=[list(r) for r in cert['conflict_row_bank'][0]];mutated[0][1]^=1
    total=0
    for c,b in mutated:total^=int(c,16)|(b<<96)
    assert total!=1<<96
    # Dropping the half-word offset is detected on a genuine actual input pair.
    D=1<<18;x=0;xp=D
    actual=(own.sigma1(xp)-own.sigma1(x))&own.M
    low=(own.sigma1(xp)&((1<<22)-1))-(own.sigma1(x)&((1<<22)-1))
    assert actual!=low&own.M and actual==((1<<31)+low)&own.M
    # Reverse the third pair: the modular offset remains H, the low derivative negates.
    reverse=(own.sigma1(x)-own.sigma1(xp))&own.M
    assert reverse==((1<<31)-low)&own.M
    assert (actual+reverse)&own.M==0
    return {'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'author_hashes':frozen,'manifest_files_verified':len(manifest),
            'author_dependencies_verified':dependencies,
            'accepted_v4_review_manifest_sha256':digest(previous/'SHA256.json'),
            'accepted_v4_receipt_sha256':digest(previous/'REVIEW_RECEIPT.json'),
            'width_proof_sha256':digest(HERE.parent/'width-reduction-v5/PROOF.md'),
            'width_checker_sha256':digest(HERE.parent/'width-reduction-v5/check.py'),
            'cases':summary,'third_mask_tests_checked':total_thirds,
            'direct_XOR_receipts_checked':len(cert['conflict_row_bank']),
            'controls':['nonzero half-word offset directly required',
                        'negative orientation retains same H offset',
                        'corrupt receipt RHS detected',
                        'actual twin witnesses for every independently feasible mask pair'],
            'scope':'independent theorem model + complete coverage/row identities; author branch-edge counts are not independently matched'}

if __name__=='__main__':
    report=run()
    (HERE/'CONTROLS_COMPARISON_RUN.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
