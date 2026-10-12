#!/usr/bin/env python3
"""Stdlib-only certificate checker: verifies inequalities, does not optimize."""
import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path
import zlib

def require(ok, why):
    if not ok:
        raise ValueError(why)

def sigma_bits(x, kind):
    # Direct output-bit equations from FIPS, no rotation implementation reuse.
    a,b,s = ((7,18,3),(17,19,10))[kind]
    bits=[(x>>i)&1 for i in range(32)]
    out=0
    for i in range(32):
        v=bits[(i+a)%32]^bits[(i+b)%32]
        if i+s<32:
            v ^= bits[i+s]
        out |= v<<i
    return out

def check(cert):
    require(cert['schema']=='sha256-word-support-relaxation-v1','schema')
    require(cert['shape']==[49,65536],'shape')
    require(cert['state_encoding']=='bit j is W[t-16+j] active','state encoding')
    inv=cert['sigma_inverse_columns']
    require(len(inv)==2 and all(len(a)==32 for a in inv),'inverse shape')
    for kind,cols in enumerate(inv):
        for i,x in enumerate(cols):
            require(type(x) is int and 0<=x<2**32,'inverse word')
            require(sigma_bits(x,kind)==1<<i,'right inverse column')
    # Exact contradiction for the specific zero-base lifting attempt in PROOF.md.
    v=inv[0][31]
    require(v==0x94857ee6,'zero-base forced word')
    lhs=sigma_bits((-sigma_bits(v,1))%(2**32),0)
    rhs=sigma_bits(1<<31,1)
    require(lhs==0xabacb99f and rhs==0x00205000 and lhs!=rhs,'zero-base obstruction')
    raw=zlib.decompress(base64.b64decode(cert['potentials_zlib_base64'],validate=True))
    require(len(raw)==49*65536,'potential size')
    require(hashlib.sha256(raw).hexdigest()==cert['potential_sha256'],'potential hash')
    table=memoryview(raw)
    require(not any(table[48*65536:]),'terminal potential')
    bound=cert['bound']
    require(type(bound) is int and 1<=bound<=64,'bound type/range')
    for state in range(1,65536):
        require(state.bit_count()+table[state]>=bound,'initial lower bound')
    edges=0
    for row in range(48):
        cur=table[row*65536:(row+1)*65536]
        nxt=table[(row+1)*65536:(row+2)*65536]
        for state in range(65536):
            # At step t, source distances are 2,7,15,16 from the FIPS recurrence.
            active=sum(bool(state & (1<<(16-distance))) for distance in (2,7,15,16))
            for newbit in (0,1):
                if active+newbit==1:
                    continue
                successor=(state//2)+newbit*32768
                require(cur[state]<=newbit+nxt[successor],'transition lower bound')
                edges+=1
    supp=cert['support_witness']
    require(supp==sorted(set(supp)) and all(type(t) is int and 0<=t<64 for t in supp),'support')
    require(len(supp)==bound and any(t<16 for t in supp),'support weight/nonzero')
    active=set(supp)
    for t in range(16,64):
        require(sum(j in active for j in (t,t-2,t-7,t-15,t-16))!=1,'support recurrence')
    return dict(bound=bound,verified_transition_inequalities=edges,
                interpretation='universal actual-word lower bound; sharp only in support relaxation')

def negative_checks(cert):
    changed=[]
    c=copy.deepcopy(cert);c['bound']+=1;changed.append(c)
    c=copy.deepcopy(cert);c['sigma_inverse_columns'][0][0]^=1;changed.append(c)
    c=copy.deepcopy(cert);c['support_witness']=list(range(13));changed.append(c)
    c=copy.deepcopy(cert);c['potential_sha256']='0'*64;changed.append(c)
    c=copy.deepcopy(cert)
    raw=bytearray(zlib.decompress(base64.b64decode(c['potentials_zlib_base64'])))
    raw[0]=255  # Hash-consistent corruption: must fail a Bellman inequality.
    c['potential_sha256']=hashlib.sha256(raw).hexdigest()
    c['potentials_zlib_base64']=base64.b64encode(zlib.compress(raw)).decode()
    changed.append(c)
    reasons=[]
    for c in changed:
        try:
            check(c)
        except ValueError as e:
            reasons.append(str(e))
        else:
            raise ValueError('negative control was accepted')
    return reasons

def main():
    ap=argparse.ArgumentParser();ap.add_argument('certificate',type=Path)
    ap.add_argument('--negative',action='store_true');args=ap.parse_args()
    cert=json.loads(args.certificate.read_text())
    result=check(cert)
    if args.negative:
        result['rejected_controls']=negative_checks(cert)
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    main()
