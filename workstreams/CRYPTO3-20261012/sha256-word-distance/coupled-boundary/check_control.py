#!/usr/bin/env python3
"""Positive and damaged controls for the unrestricted local word equations."""
import argparse
import copy
import json
from pathlib import Path

MASK=(1<<32)-1
HERE=Path(__file__).resolve().parent


def sigma(x,a,b,c):
    out=0
    for i in range(32):
        bit=((x>>((i+a)%32))^(x>>((i+b)%32)))&1
        if i+c<32:
            bit^=(x>>(i+c))&1
        out|=bit<<i
    return out


def check(data,rotations=(17,19,10)):
    assert data['schema']=='crypto3-unrestricted-local-control-v1'
    assert rotations==(17,19,10),'standard sigma1 constants'
    q,qp,p,pp=[data[key] for key in ['q','q_prime','p','p_prime']]
    assert all(type(x) is int and 0<=x<=MASK for x in [q,qp,p,pp]),'word range'
    g=lambda x:sigma(x,*rotations)
    f=lambda x:sigma(x,7,18,3)
    D=(qp-q)&MASK; Gq=(g(qp)-g(q))&MASK
    Fq=(f(qp)-f(q))&MASK; Fp=(f(pp)-f(p))&MASK
    assert D!=0 and ((pp-p)&MASK)==D,'equal nonzero input differences'
    assert (Gq+D)&MASK==0,'sigma1 cancellation'
    assert (Fq+Fp)&MASK==0,'opposite sigma0 derivatives'
    assert D&0xfff,'not in excluded low12 stratum'
    for key,value in [('D_hex',D),('Gq_hex',Gq),('Fq_hex',Fq),('Fp_hex',Fp),
                      ('q_xor_q_prime_hex',q^qp)]:
        assert data[key]==f'{value:08x}','recorded '+key
    assert q^qp!=0xfbca7000,'not the excluded fixed XOR mask'
    return {'D':f'{D:08x}','input_xor':f'{q^qp:08x}'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--negative',action='store_true')
    args=parser.parse_args()
    data=json.loads((HERE/'UNRESTRICTED_CONTROL.json').read_text())
    result=check(data)
    controls=[]
    if args.negative:
        wrong_input=copy.deepcopy(data); wrong_input['p_prime']^=1
        wrong_output=copy.deepcopy(data); wrong_output['Gq_hex']='778493a4'
        wrong_mask=copy.deepcopy(data); wrong_mask['q_xor_q_prime_hex']='fbca7000'
        for name,bad,const in [('damaged input',wrong_input,(17,19,10)),
                               ('damaged sigma output',wrong_output,(17,19,10)),
                               ('wrong XOR scope',wrong_mask,(17,19,10)),
                               ('wrong rotation',data,(17,18,10))]:
            try:
                check(bad,const)
            except AssertionError as e:
                controls.append({'case':name,'rejected':True,'reason':str(e)})
            else:
                raise AssertionError('accepted damaged control')
    print(json.dumps({'status':'PASS','local_positive_control':result,
                      'negative_controls':controls,'full_schedule_claimed':False},sort_keys=True))


if __name__=='__main__':
    main()
