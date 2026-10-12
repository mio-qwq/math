#!/usr/bin/env python3
"""V6 post-freeze controls and compressed evidence checks, no author imports."""
import datetime
import hashlib
import itertools
import json
import lzma
import pathlib
import check_independent as own

HERE=pathlib.Path(__file__).resolve().parent
AUTHOR=HERE.parent/'support12-boundary-v6'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def solution(basis):
    value=0
    for pivot,row in sorted(basis.items()):
        if (row>>96)^((row&value).bit_count()%2):value|=1<<pivot
    assert all(((row&value).bit_count()%2)==(row>>96) for row in basis.values())
    return [value>>32*i&own.M for i in range(3)]

def twin_witness(k,h,a,b):
    fa,fb=a[3],b[3]
    ga,gb=a[4],b[4]
    D=(k<<17)+(h<<31)
    if (ga&0x3fffff)+(gb&0x3fffff)<2*(k<<17) or (fa-fb)&1 or (gb-ga-2*D)&1:return None
    eqs=[own.equation_templates(fa,fb,((fa-fb)//2)&((1<<31)-1),-1,
                               own.FR,[r<<32 for r in own.FR]),
         own.equation_templates(gb,ga,((gb-ga-2*D)//2)&((1<<31)-1),-1,
                               [r<<32 for r in own.GR],own.GR)]
    stack=[(0,(0,0),own.fixed_input_basis((a,b,(0,0,0,0,0))))]
    while stack:
        step,cs,bs=stack.pop()
        if step==62:
            x,y,_=solution(bs);xp=(x+D)&own.M;yp=(y+D)&own.M
            assert x^xp==a[0] and y^yp==b[0]
            fx=(own.sigma0(xp)-own.sigma0(x))&own.M
            fy=(own.sigma0(yp)-own.sigma0(y))&own.M
            gx=(own.sigma1(xp)-own.sigma1(x))&own.M
            gy=(own.sigma1(yp)-own.sigma1(y))&own.M
            assert fx==fy and (gy-gx)&own.M==(2*D)&own.M
            return {'x':f'{x:08x}','xp':f'{xp:08x}',
                    'y':f'{y:08x}','yp':f'{yp:08x}',
                    'F':f'{fx:08x}','Gx':f'{gx:08x}','Gy':f'{gy:08x}'}
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
    assert all(digest(HERE.parent/n)==h for n,h in dependencies.items())
    previous=HERE.parent/'support12-review-v5'
    old_manifest=json.loads((previous/'SHA256.json').read_text())['files']
    assert all(digest(previous/n)==h for n,h in old_manifest.items())
    assert json.loads((previous/'REVIEW_RECEIPT.json').read_text())['status']=='ACCEPT'
    assert all(own.GR[j]>>17==0 for j in range(22,30))
    assert own.GR[30]==(1<<15)|(1<<17)
    assert own.GR[31]==(1<<16)|(1<<18)
    assert 3*(1<<23)<1<<31
    representatives=[(k,h,(k<<17)+(h<<31)) for k in range(1,32,2) for h in (0,1)]
    assert len({d for k,h,d in representatives})==32
    assert all(d&-d==1<<17 for k,h,d in representatives)
    signed={(sign*(k<<17)+(h<<31))&own.M
            for k,h,d in representatives for sign in (-1,1)}
    assert len(signed)==64
    assert signed=={d for k,h,d in representatives}|{(-d)&own.M for k,h,d in representatives}
    no_lift={d for k,h,d in representatives if h==0}
    assert no_lift|{(-d)&own.M for d in no_lift}!=signed
    summaries=[]
    raw_hashes={}
    total_receipts=total_pairs=total_thirds=raw_bytes=xz_bytes=0
    all_controls=[]
    for k,h,D in representatives:
        cases=own.masks(k,h)
        for alpha,forced,_,beta,gamma in cases:
            assert alpha&((1<<17)-1)==0 and alpha>>17&1
            assert forced>>31==0 and beta==own.sigma0(alpha) and gamma==own.sigma1(alpha)
            assert beta>>31==1 and gamma>>30&1 and gamma&0x3fc00000==0
        filename=f'CASE-{k}-{h}.json.xz'
        compressed=(AUTHOR/filename).read_bytes();raw=lzma.decompress(compressed)
        build=json.loads((AUTHOR/f'BUILD-{k}-{h}.json').read_text())
        raw_sha=hashlib.sha256(raw).hexdigest();xz_sha=hashlib.sha256(compressed).hexdigest()
        assert raw_sha==build['raw_json_sha256'] and xz_sha==build['xz_sha256']==manifest[filename]
        assert len(raw)==build['raw_bytes'] and len(compressed)==build['xz_bytes']
        raw_hashes[filename[:-3]]={'raw_sha256':raw_sha,'raw_bytes':len(raw),
                                 'xz_sha256':xz_sha,'xz_bytes':len(compressed)}
        raw_bytes+=len(raw);xz_bytes+=len(compressed)
        data=json.loads(raw)
        assert data['definition']['q']==k and data['definition']['h']==h and data['definition']['D']==f'{D:08x}'
        assert data['definition']['bits']==32 and not data['witnesses']
        assert data['kernel_sha256']==dependencies['support12-v4/check.py']
        assert data['v4_manifest_sha256']==dependencies['support12-v4/manifest.json']
        classes={orientation:[
            {'alpha':f'{a:08x}',
             'input_rows':[[f'{1<<bit:08x}',(v^(fm if orientation=='negative' else 0))>>bit&1]
                           for bit in range(17,31) if fm>>bit&1]}
            for a,fm,v,_,_ in cases]
            for orientation in ('positive','negative')}
        assert data['input_classes']==classes
        pairs=[(f'{a[0]:08x}',f'{b[0]:08x}') for a,b in itertools.product(cases,repeat=2)]
        assert [(c['alpha_x'],c['alpha_y']) for c in data['cases']]==pairs
        own_survivors=[]
        for a,b in itertools.product(cases,repeat=2):
            witness=twin_witness(k,h,a,b)
            if witness is not None:
                own_survivors.append({'alpha_x':f'{a[0]:08x}','alpha_y':f'{b[0]:08x}',
                                      'actual_twin_witness':witness})
        assert [(c['alpha_x'],c['alpha_y']) for c in own_survivors]==[
            (c['alpha_x'],c['alpha_y']) for c in data['cases'] if c['g_leaves']]
        bank=data['conflict_row_bank']
        for receipt in bank:
            coefficients=constant=0
            for c,b in receipt:
                w=int(c,16);assert 0<=w<1<<96 and b in (0,1)
                coefficients^=w;constant^=b
            assert coefficients==0 and constant==1
        thirdcount=0
        for c in data['cases']:
            assert all(0<=i<len(bank) for i in c['f_conflicts']+c['g_conflicts'])
            third=c['third_pair']
            assert len(third)==c['g_leaves']*len(cases)
            for ordinal in range(c['g_leaves']):
                subset=[r for r in third if r['branch']==ordinal]
                assert sorted(r['alpha_r'] for r in subset)==sorted(f'{a[0]:08x}' for a in cases)
            for r in third:
                assert r.get('g_leaves',0)==0
                refs=([r['input_conflict']] if 'input_conflict' in r else r['f_conflicts']+r['g_conflicts'])
                assert all(0<=i<len(bank) for i in refs)
            thirdcount+=len(third)
        twinbranches=sum(c['g_leaves'] for c in data['cases'])
        assert build['summary']['mask_pairs']==len(pairs)
        assert build['summary']['twin_branches']==twinbranches
        assert build['summary']['third_masks_checked']==thirdcount
        assert build['summary']['xor_conflict_proofs']==len(bank)
        total_receipts+=len(bank);total_pairs+=len(pairs);total_thirds+=thirdcount
        summaries.append({'q':k,'h':h,'mask_classes_each_orientation':len(cases),
                          'twin_mask_cases':len(pairs),'actual_feasible_twin_mask_pairs':own_survivors,
                          'author_twin_branches':twinbranches,'third_mask_tests':thirdcount,
                          'direct_XOR_receipts':len(bank)})
        if bank:
            broken=[list(r) for r in bank[0]];broken[0][1]^=1
            total=0
            for c,b in broken:total^=int(c,16)|(b<<96)
            assert total!=1<<96
    assert total_pairs==111718 and total_thirds==7068 and total_receipts==10914
    assert sum(s['author_twin_branches'] for s in summaries)==142
    assert raw_bytes==20167680 and xz_bytes==360716
    # Neither the ordinary bound nor the common quarter lift is valid modulo N.
    delta=1<<17;Q=1<<30;P=1<<31
    plus=own.sigma1(delta);minus=(-plus)&own.M;low=plus&0x3fffff
    assert plus==Q+low and plus>1<<22
    assert minus%P==(Q-low)%P
    assert minus!=(Q-low)&own.M and (minus-(Q-low))&own.M==P
    # Sigma1 output-mask bit31 is a meaningful constant at the original modulus.
    gamma=own.sigma1(3*delta)
    assert gamma>>31==1 and gamma!=gamma&0x7fffffff
    assert (gamma-(gamma&0x7fffffff))&own.M==P
    all_controls=['dropping h lift omits32 signed residues',
                  'common quarter identity valid only mod2^31',
                  'ordinary full-output width bound rejected',
                  'discarding sigma1 beta31 constant changes original derivative',
                  'corrupt receipt RHS rejected per nonempty case',
                  'actual native-mod2^32 twin witnesses checked for every feasible mask pair']
    return {'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'author_hashes':frozen,'manifest_files_verified':len(manifest),
            'author_dependencies_verified':dependencies,
            'accepted_v5_review_manifest_sha256':digest(previous/'SHA256.json'),
            'accepted_v5_receipt_sha256':digest(previous/'REVIEW_RECEIPT.json'),
            'case_count':32,'signed_residues':64,'mask_pair_cases':total_pairs,
            'third_mask_tests':total_thirds,'direct_XOR_receipts':total_receipts,
            'raw_json_bytes':raw_bytes,'compressed_bytes':xz_bytes,
            'raw_case_hashes':raw_hashes,'case_summaries':summaries,'controls':all_controls,
            'scope':'independent fullmodN theorem model; complete XZ/raw evidence, input cubes, case coverage and direct row identities; author branch-edge statistics not independently reconstructed'}

if __name__=='__main__':
    report=run()
    (HERE/'CONTROLS_COMPARISON_RUN.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'case_count':32,'mask_pair_cases':report['mask_pair_cases'],
                      'third_mask_tests':report['third_mask_tests'],'raw_json_bytes':report['raw_json_bytes'],
                      'compressed_bytes':report['compressed_bytes'],'direct_XOR_receipts':report['direct_XOR_receipts']}))
