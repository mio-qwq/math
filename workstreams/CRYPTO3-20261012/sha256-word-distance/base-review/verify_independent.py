#!/usr/bin/env python3
"""Independent review of the exact support-0 interpolation reduction."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import types

# Reconstruct was written and checkpointed before author files were read.
sys.dont_write_bytecode=True
import reconstruct as ref

PROOF_HASH='436a80b20ae6d98a6d8a6b68248449ed047e212aaff8c9f6eb41a8ba73a76b9f'
CODE_HASH='1215aa82a6abe196fe2396803a5a7565042e7862c35a434ed2be0b4bfc156955'
SUPPORT_HASH='02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf'


def require(ok,message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_words(words):
    return hashlib.sha256(b''.join(w.to_bytes(4,'big') for w in words)).hexdigest()


def load_candidate(path):
    module=types.ModuleType('reviewed_base_completion')
    module.__file__=str(path)
    exec(compile(path.read_text(),str(path),'exec'),module.__dict__)
    return module


def structural(candidate):
    require(tuple(candidate.SUPPORT)==ref.S,'support coordinates')
    require(tuple(candidate.PARAMETERS)==ref.P,'parameter coordinates')
    require(tuple(candidate.RESIDUAL_INDICES)==ref.EXPECTED_T,'residual coordinates')
    known=set(ref.S)|set(ref.P);used=set();new=[]
    for t,target in candidate.ORDER:
        require(type(t) is int and 16<=t<64 and t not in used,'unique original equation')
        missing={i for i,_,_ in ref.terms(t)}-known
        require(missing=={target},'exactly one new coordinate')
        require(target not in known,'fresh target')
        used.add(t);known.add(target);new.append(target)
    require(known==set(range(64)) and len(used)==38,'all 64 coordinates completed')
    require(set(range(16,64))-used==set(ref.EXPECTED_T),'exact unused equation set')
    return used,new


def check_sigma_maps(candidate):
    tested=0
    for kind,forward,inverse in ((0,candidate.sigma0,candidate.INV0),
                                (1,candidate.sigma1,candidate.INV1)):
        require(forward(0)==inverse(0)==0,'sigma zero')
        for i in range(32):
            x=1<<i
            require(forward(x)==ref.apply_rows(ref.FORWARD[kind],x),'original sigma basis')
            require(inverse(x)==ref.apply_rows(ref.INVERSE[kind],x),'original inverse basis')
            require(forward(inverse(x))==inverse(forward(x))==x,'sigma inverse composition')
            tested+=1
    return tested


def all_residuals(words):
    require(len(words)==64 and all(type(w) is int and 0<=w<ref.MODULUS for w in words),
            'complete unsigned word sequence')
    return {t:ref.residual(words,t) for t in range(16,64)}


def completion(candidate,anchors,steps,used):
    a={i:anchors[i] for i in ref.S};p={i:anchors[i] for i in ref.P}
    actual,returned=candidate.complete(a,p)
    rebuilt=ref.fill(anchors,steps)
    require(actual==rebuilt,'agreement of distinct completion orders')
    require(all(actual[i]==w for i,w in anchors.items()),'all 26 anchors retained')
    raw=all_residuals(actual)
    require(all(raw[t]==0 for t in used),'all 38 solved original equations')
    require(returned=={t:raw[t] for t in ref.EXPECTED_T},'exact original residual vector')
    require((not any(returned.values()))==(actual==ref.expand(actual[:16])),
            'zero residuals iff original forward expansion')
    return actual,returned


def common_word_formulas():
    U=lambda j:7*j
    V=lambda j:1+7*j
    D=lambda j:5+7*j
    Q=lambda j:6+7*j
    checked=0
    for j in range(4,9):
        proposed=[
            (7*j,[(U(j),'identity',1),(U(j-1),'identity',-1),
                   (D(j-1),'sigma1',-1),(D(j-3),'identity',-1),(Q(j-3),'sigma0',-1)]),
            (7*j+1,[(V(j),'identity',1),(V(j-1),'identity',-1),
                     (Q(j-1),'sigma1',-1),(Q(j-3),'identity',-1),(U(j-2),'sigma0',-1)])]
        for t,terms in proposed:
            require(t in ref.EXPECTED_T and sorted(terms)==sorted(ref.terms(t)),
                    'common-word residual rewrite')
            require(all(0<=i<64 and i not in ref.S for i,_,_ in terms),
                    'common-word coordinates are inactive')
            checked+=1
    return checked


def lifting_identity(base):
    # Deliberately choose arbitrary active replacements, not a feasible
    # sparse pair. This checks the exact residual-subtraction identity.
    altered=list(base)
    for i in ref.S:
        altered[i]=(base[i]+(0x01020305*(i+1)))&ref.WORD_MASK
        require(altered[i]!=base[i],'active replacement')
    d=[(b-a)&ref.WORD_MASK for a,b in zip(base,altered)]
    f=[(ref.transform('sigma0',b)-ref.transform('sigma0',a))&ref.WORD_MASK
       for a,b in zip(base,altered)]
    g=[(ref.transform('sigma1',b)-ref.transform('sigma1',a))&ref.WORD_MASK
       for a,b in zip(base,altered)]
    proposed={t:(d[t]-g[t-2]-d[t-7]-f[t-15]-d[t-16])&ref.WORD_MASK
              for t in range(16,64)}
    difference={t:(ref.residual(altered,t)-ref.residual(base,t))&ref.WORD_MASK
                for t in range(16,64)}
    require(proposed==difference,'all 48 exact lifting identities')
    require(any(proposed.values()),'arbitrary replacements must not be mistaken for a witness')
    return {'verified_equation_identities':48,'exact_changed_support':list(ref.S),
            'nonzero_replacement_residuals':[t for t,v in proposed.items() if v],
            'interpretation':'rejected sparse candidate; verifies algebraic identity only'}


def main(author,frozen_supports):
    require(digest(author/'PROJECTION.md')==PROOF_HASH,'exact reviewed proof version')
    require(digest(author/'base_completion.py')==CODE_HASH,'exact reviewed evaluator version')
    require(digest(frozen_supports)==SUPPORT_HASH,'frozen support version')
    require(tuple(json.loads(frozen_supports.read_text())['supports'][0])==ref.S,'frozen support zero')
    manifest=json.loads((author/'SHA256.json').read_text())['files']
    for name,sha in manifest.items():
        require(digest(author/name)==sha,'author manifest integrity: '+name)
    candidate=load_candidate(author/'base_completion.py')
    used,new=structural(candidate)
    sigma_cases=check_sigma_maps(candidate)
    steps,left=ref.chart()
    require(used=={s['recurrence'] for s in steps},'same equation set under distinct orders')
    fixtures=[
        [ref.WORD_MASK]*16,
        [0x80000000 if i%2==0 else 0x7fffffff for i in range(16)],
        [(0x13579bdf+i*0x01010101)&ref.WORD_MASK for i in range(16)],
        [int.from_bytes(hashlib.sha256(('CR3-base-review-fixture-'+str(i)).encode()).digest()[:4],'big')
         for i in range(16)]]
    roundtrips=[]
    bases=[]
    for message in fixtures:
        base=ref.expand(message);bases.append(base)
        anchors={i:base[i] for i in set(ref.S)|set(ref.P)}
        actual,res=completion(candidate,anchors,steps,used)
        require(actual==base and not any(res.values()),'independent genuine-base roundtrip')
        roundtrips.append({'input_words':message,'completed_words_sha256':digest_words(actual),
                          'all_64_words_match':True,'all_48_raw_equations_zero':True})
    arbitrary=[]
    for seed in (0x6a09e667,0xbb67ae85):
        anchors={i:((seed*(i+3))^(0x3c6ef372+i*i))&ref.WORD_MASK for i in set(ref.S)|set(ref.P)}
        actual,res=completion(candidate,anchors,steps,used)
        arbitrary.append({'seed':seed,'all_38_used_equations_zero':True,
                          'anchors_retained':True,'completed_words_sha256':digest_words(actual),
                          'nonzero_residual_indices':[t for t,v in res.items() if v]})
    bad_anchors={i:bases[0][i] for i in set(ref.S)|set(ref.P)}
    bad_anchors[16]^=1
    changed,remaining=completion(candidate,bad_anchors,steps,used)
    require(any(remaining.values()),'changed anchor leaves a real residual obstruction')
    reasons=[]
    tests=[]
    a={i:bases[0][i] for i in ref.S};p={i:bases[0][i] for i in ref.P}
    missing=dict(a);missing.pop(16)
    tests.append(('missing active anchor',lambda:candidate.complete(missing,p)))
    malformed=dict(p);malformed[0]=1<<32
    tests.append(('out-of-range word',lambda:candidate.complete(a,malformed)))
    boolword=dict(p);boolword[0]=True
    tests.append(('non-integer Boolean word',lambda:candidate.complete(a,boolword)))
    for label,fn in tests:
        try:fn()
        except ValueError as e:reasons.append({'control':label,'rejection':str(e)})
        else:raise ValueError('invalid input accepted: '+label)
    clone=load_candidate(author/'base_completion.py')
    clone.ORDER=((17,16),)+clone.ORDER[1:]
    try:structural(clone)
    except ValueError as e:reasons.append({'control':'wrong elimination target','rejection':str(e)})
    else:raise ValueError('corrupted order accepted')
    clone=load_candidate(author/'base_completion.py')
    clone.RESIDUAL_INDICES=clone.RESIDUAL_INDICES[:-1]
    try:structural(clone)
    except ValueError as e:reasons.append({'control':'omitted residual equation','rejection':str(e)})
    else:raise ValueError('missing residual accepted')
    clone=load_candidate(author/'base_completion.py')
    clone.sigma0=lambda word:clone.rotr(word,8)^clone.rotr(word,18)^(word>>3)
    try:check_sigma_maps(clone)
    except ValueError as e:reasons.append({'control':'wrong sigma0 rotation constant','rejection':str(e)})
    else:raise ValueError('wrong sigma constant accepted')
    corrupt=list(bases[0]);corrupt[13]^=1
    require(any(all_residuals(corrupt).values()),'damaged completed word rejected by raw recurrence')
    reasons.append({'control':'damaged completed word','rejection':'nonzero original recurrence'})
    return {'schema':'independent-sha256-base-projection-review-v1','passed':True,
            'proof_sha256':PROOF_HASH,'evaluator_sha256':CODE_HASH,'frozen_support_sha256':SUPPORT_HASH,
            'manifest_files_verified':len(manifest),'sigma_basis_and_inverse_checks':sigma_cases,
            'reviewer_sigma_inverse_compositions':128,'author_assignments_verified':len(new),
            'reviewer_assignments_verified':len(steps),'same_equation_set_different_order':True,
            'residual_indices':left,'common_word_formulas_verified':common_word_formulas(),
            'genuine_base_roundtrips':roundtrips,'arbitrary_26_anchor_completions':arbitrary,
            'damaged_anchor_control':{'all_38_constructed_equations_zero':True,
                                      'nonzero_remaining_equations':[t for t,v in remaining.items() if v]},
            'negative_controls':reasons,'lifting_identity':lifting_identity(bases[2]),
            'scope':'Independent written/evaluator review of two exact reductions; no projection surjectivity claim; no sparse pair found'}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--author-directory',type=Path,required=True)
    p.add_argument('--frozen-supports',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(main(a.author_directory,a.frozen_supports),indent=2,sort_keys=True))
