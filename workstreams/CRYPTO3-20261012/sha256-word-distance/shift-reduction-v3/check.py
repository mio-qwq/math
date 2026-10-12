#!/usr/bin/env python3
"""Independent, definition-based checker for an exact temporal-window support reduction.

No solver, guessed witnesses, or trust in the previous v2 enumerator is used.
The 15 patterns and their completeness are inherited; only the implications
between explicitly supplied supports are certified here.
"""
import argparse, hashlib, json, random
from pathlib import Path
MASK = (1 << 32) - 1
ROOT = Path(__file__).resolve().parent
SOURCE_DIGEST = '02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf'
# Implication: if support `src` is attained, support `dst` is attained by
# shifting the actual pair of expanded schedules LEFT `shift` time steps.
IMPLICATIONS = [(0,9,1),(1,0,1),(2,0,2),(4,0,3),
                (6,12,1),(13,12,2),(7,12,3)]
# Support 0 also implies support 1,2,4 via a backwards common-prefix extension.
RIGHT_SHIFTS = [(0,1,1),(0,2,2),(0,4,3)]


def rotr(x,k): return ((x >> k) | (x << (32-k))) & MASK

def f(x): return rotr(x,7)^rotr(x,18)^(x>>3)

def g(x): return rotr(x,17)^rotr(x,19)^(x>>10)

def schedule(msg,length=67):
    assert len(msg)==16
    a=[x & MASK for x in msg]
    for t in range(16,length):
        a.append((g(a[t-2])+a[t-7]+f(a[t-15])+a[t-16])&MASK)
    return a


def left_window_check(support, target, shift):
    """Purely sufficient support propagation: all future dependencies are zero."""
    active=set(support)
    assert min(active)>=shift
    # This test is deliberately algebraically stronger than possible
    # cancellation: all nonzero terms are absent, so no cancellation presumed.
    tested=[]
    for t in range(64,64+shift):
        lags=(t-2,t-7,t-15,t-16)
        hits=sorted(set(lags)&active)
        tested.append({'t':t,'lags':list(lags),'active_dependencies':hits})
        if hits:return False,tested
    return {i-shift for i in active}==set(target),tested


def right_window_check(support, target, shift):
    active=set(support)
    tested=[]
    for t in range(15,15-shift,-1):
        # Solve W[t-16] by subtracting the other four terms from W[t].
        rhs_indices=(t,t-2,t-7,t-15)
        hits=sorted(set(rhs_indices)&active)
        tested.append({'t':t,'new_shared_index':t-16,
                       'rhs_indices':list(rhs_indices), 'active_dependencies':hits})
        if hits: return False,tested
        # Because there are no hits, the reconstructed negative word agrees
        # for both inputs, so t-16 must not be added to active.
    in_window={i+shift for i in active if i<=63-shift}
    return (in_window==set(target) and max(active)<=63-shift),tested


def self_test_windows():
    rng=random.Random(0xC3A52026)
    passed=0
    for sample in range(15):
        a=[rng.getrandbits(32) for _ in range(16)]
        b=[rng.getrandbits(32) for _ in range(16)]
        if a==b:b[0]^=1
        A=schedule(a);B=schedule(b)
        for shift in (1,2,3):
            # This is a true 16-word rescheduling, not a difference-only model.
            assert schedule(A[shift:shift+16],64)==A[shift:shift+64]
            assert schedule(B[shift:shift+16],64)==B[shift:shift+64]
            passed+=1
        if sample==0:
            altered=A[:]
            altered[64]^=1
            assert schedule(A[1:17],64)!=altered[1:65]
            # Destroying recurrence after position 63 is detected, not accepted.
    return passed


def main():
    p=ROOT/'supports-v2.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==SOURCE_DIGEST
    obj=json.loads(p.read_text())
    supports=[tuple(s) for s in obj['supports']]
    assert len(supports)==15 and all(len(s)==13 for s in supports)
    positive=[]
    for src,dst,shift in IMPLICATIONS:
        ok,proof=left_window_check(supports[src],supports[dst],shift)
        assert ok,(src,dst)
        positive.append({'direction':'left', 'source':src,'target':dst,'shift':shift,'tail':proof})
    for src,dst,shift in RIGHT_SHIFTS:
        ok,proof=right_window_check(supports[src],supports[dst],shift)
        assert ok,(src,dst)
        positive.append({'direction':'right','source':src,'target':dst,'shift':shift,'prefix':proof})
    # Inherited v2 exclusions are precisely 3 and 14. Every other support
    # must belong to the target representatives or be reducible to one.
    remaining=set(range(15))-{3,14}
    representatives={5,8,9,10,11,12}
    assert remaining == representatives | {src for src,_,_ in IMPLICATIONS}
    assert not(representatives & {src for src,_,_ in IMPLICATIONS})
    # Additional consistency: support 3 would shift to excluded support 14
    # if it were realizable, by dropping index 1 and forcing index 64 active.
    source3=set(supports[3]); target14=set(supports[14]); shift=2
    assert 1 in source3 and 57 in source3
    assert {62,49,48}.isdisjoint(source3)
    assert {63,58,50,49}.isdisjoint(source3)
    expected={i-shift for i in source3 if i>=shift}|{64-shift}
    assert expected==target14 and (64-shift) in target14
    sample_shifts=self_test_windows()
    # Negative controls are tests of our criterion, NOT claims that an
    # actual schedule with the corrupted support exists.
    bad1=set(supports[1])|{57}   # d57 can feed t64
    assert not left_window_check(bad1,supports[0],1)[0]
    bad2=set(supports[0])|{15}   # newly inferred W[-1] need not be shared
    assert not right_window_check(bad2,supports[1],1)[0]
    bad3=list(supports[7]);bad3.remove(60);bad3.append(59)
    assert not left_window_check(bad3,supports[12],3)[0]
    bad4=set(supports[0])|{11}   # backwards t13 uses G11
    assert not right_window_check(bad4,supports[4],3)[0]
    bad5=set(supports[0])|{57}   # forward t64 fails to vanish
    assert not left_window_check(bad5,supports[9],1)[0]
    result={'schema':'crypto3-window-reduction-v3',
        'standard':'FIPS 180-4 SHA-256 small sigma word schedule',
        'source_supports_sha256':SOURCE_DIGEST,
        'implications':positive,
        'representative_supports':sorted(representatives),
        'left_window_tests':sample_shifts,'negative_controls':5,
        'excluded_support_implication':'3 implies 14 by left shift 2 (drops index 1; d64=d57 != 0)',
        'new_full_support_exclusions':0,'status':'PASS'}
    print(json.dumps(result,sort_keys=True,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--save',action='store_true',help='Save the exact checked reduction as RESULTS.json')
    opts=parser.parse_args()
    result=main()
    if opts.save:(ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
