#!/usr/bin/env python3
"""Exact support relaxation. Requires NumPy; certificates use only integer bytes."""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import zlib
import numpy as np

def sig(x, a, b, s):
    mask=(1<<32)-1
    rr=lambda t: ((x>>t)|(x<<(32-t)))&mask
    return rr(a)^rr(b)^(x>>s)

def inverse_columns(a,b,s):
    cols=[sig(1<<i,a,b,s) for i in range(32)]
    rows=[sum(((cols[j]>>i)&1)<<j for j in range(32)) | (1<<(32+i)) for i in range(32)]
    for j in range(32):
        p=next(i for i in range(j,32) if (rows[i]>>j)&1)
        rows[j],rows[p]=rows[p],rows[j]
        for i in range(32):
            if i!=j and (rows[i]>>j)&1:
                rows[i]^=rows[j]
    assert all((rows[i]&0xffffffff)==1<<i for i in range(32))
    return [sum(((rows[i]>>(32+j))&1)<<i for i in range(32)) for j in range(32)]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    masks=np.arange(65536,dtype=np.uint32)
    count=sum((masks>>j)&1 for j in (0,1,9,14))
    nxt=masks>>1
    # V[t,mask] is minimum number of active words t..63 after the given window.
    V=np.zeros((49,65536),dtype=np.uint8)
    for row in range(47,-1,-1):
        c0=V[row+1,nxt].astype(np.uint16)
        c1=1+V[row+1,nxt|32768].astype(np.uint16)
        c0[count==1]=255
        c1[count==0]=255
        V[row]=np.minimum(c0,c1)
    weights=np.array([i.bit_count() for i in range(65536)],dtype=np.uint16)
    total=weights+V[0]
    start=1+int(np.argmin(total[1:]))
    bound=int(total[start])
    state=start
    support=[i for i in range(16) if (state>>i)&1]
    for row in range(48):
        c=sum((state>>j)&1 for j in (0,1,9,14))
        for bit in (0,1):
            if c+bit==1:
                continue
            ns=(state>>1)|(bit<<15)
            if int(V[row,state])==bit+int(V[row+1,ns]):
                if bit:
                    support.append(16+row)
                state=ns
                break
        else:
            raise AssertionError('no optimal successor')
    raw=V.tobytes()
    cert=dict(schema='sha256-word-support-relaxation-v1',bound=bound,
              state_encoding='bit j is W[t-16+j] active',shape=[49,65536],
              potential_sha256=hashlib.sha256(raw).hexdigest(),
              potentials_zlib_base64=base64.b64encode(zlib.compress(raw,9)).decode(),
              support_witness=support,
              sigma_inverse_columns=[inverse_columns(7,18,3),inverse_columns(17,19,10)])
    args.output.write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({k:v for k,v in cert.items() if k not in ('potentials_zlib_base64','sigma_inverse_columns')}))
    print('certificate_bytes',args.output.stat().st_size)

if __name__=='__main__':
    main()
