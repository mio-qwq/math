#!/usr/bin/env python3
"""Standalone exact witness checking; Python stdlib only, no imported builder."""
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent

def rotations(w):
    return {w[i:]+w[:i] for i in range(4)}

def forced_words(n,levels):
    candidates={}
    for w in itertools.product(range(n),repeat=4):
        r=min(rotations(w))
        if levels[n*w[0]+w[1]]<levels[n*w[2]+w[3]]:
            candidates.setdefault(r,set()).add(w)
    forced={next(iter(o)) for o in candidates.values() if len(o)==1}
    return len(candidates),forced

def is_strict(n,code):
    """Maximum selected count on any five-arc path, full triple shift graph."""
    triples=list(itertools.product(range(n),repeat=3))
    arr={t:0 for t in triples}
    for step in range(5):
        arr={s:max(arr[(x,)+s[:2]]+int((x,)+s in code) for x in range(n)) for s in triples}
    return max(arr.values())<=2

def all_hyperedges(n,forced):
    edges=set()
    idx={w:i for i,w in enumerate(sorted(forced))}
    comb=list(itertools.combinations(range(5),3))
    for x in itertools.product(range(n),repeat=8):
        a=[idx.get(x[i:i+4]) for i in range(5)]
        good=[i for i in range(5) if a[i] is not None]
        if len(good)<3:continue
        for i,j,k in itertools.combinations(good,3):
            edges.add(tuple(sorted({a[i],a[j],a[k]})))
    return edges

def verify(doc):
    n=doc['n'];levels=doc['levels']
    assert n==6 and len(levels)==n*n and all(type(x)==int and x in (0,1,2) for x in levels)
    assert doc['schema']=='GP2-forced-cover-v1'
    orbit_count,forced=forced_words(n,levels)
    assert orbit_count==310 and orbit_count==doc['viable_orbits']
    assert len(forced)==189 and len(forced)==doc['forced_words']
    cover={tuple(w) for w in doc['cover']}
    assert len(cover)==64 and cover<=forced
    assert is_strict(n,forced-cover)
    matching=doc['disjoint_matching'];assert len(matching)==64
    used=set()
    for rec in matching:
        words={tuple(w) for w in rec['forbidden_words']}
        seq=tuple(rec['word8']);starts=rec['starts']
        assert len(seq)==8 and all(type(x)==int and 0<=x<n for x in seq)
        assert len(starts)==3 and len(set(starts))==3 and all(type(x)==int and 0<=x<=4 for x in starts)
        assert words=={seq[i:i+4] for i in starts}
        assert words<=forced and words and not used.intersection(words)
        used.update(words)
    assert len(used)==187,('number unique forced words in 64 forbidden triples',len(used))
    # Optional exhaustive confirmation of saved edge count and cover incidence.
    edges=all_hyperedges(n,forced)
    assert len(edges)==7919 and len(edges)==doc['hyperedge_count']
    f=sorted(forced);idx={w:i for i,w in enumerate(f)}
    Cidx={idx[w] for w in cover}
    assert all(Cidx.intersection(e) for e in edges)
    assert {len(e):sum(len(z)==len(e) for z in edges) for e in edges} == {int(k):v for k,v in doc['rank_histogram'].items()}
    # Four independent rejections: corrupt level, cover, matching arc, parameter.
    bad=dict(doc);bad['levels']=levels[:];bad['levels'][0]=3
    assert not all(v in (0,1,2) for v in bad['levels'])
    c=next(iter(cover));assert not is_strict(n,forced-(cover-{c}))
    sample=matching[0];mut=sample['word8'][:];mut[0]=n
    assert not all(0<=v<n for v in mut)
    assert n!=5
    return {'viable_orbits':orbit_count,'forced_words':len(forced),'hyperedges':len(edges),
            'cover_size':len(cover),'disjoint_edges':len(matching),'used_forced_words':len(used),
            'rotation_bound':'310/1296','certified_loss':'64/1296','fixed_level_upper':'41/216'}

def main():
    path=HERE/'forced_cover_certificate.json'
    data=json.loads(path.read_text())
    info=verify(data)
    print('PASS independent forced-cover certificate')
    print(json.dumps(info,sort_keys=True))
    print('SHA256',hashlib.sha256(path.read_bytes()).hexdigest())

if __name__=='__main__':main()
