#!/usr/bin/env python3
"""Author's separate definition-based dependency check; standard library only."""
import argparse
from collections import Counter,defaultdict
import copy
import hashlib
import json
from pathlib import Path
import platform
import time

HERE=Path(__file__).resolve().parent
MASK=(1<<32)-1
SUPPORT_HASH='02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf'


def require(condition,message):
    if not condition:raise ValueError(message)


def bit_rows(a,b,s):
    result=[]
    for j in range(32):
        row=(1<<((j+a)%32))^(1<<((j+b)%32))
        if j+s<32:row^=1<<(j+s)
        result.append(row)
    return result


F_ROWS=bit_rows(7,18,3)
G_ROWS=bit_rows(17,19,10)


def apply_rows(rows,x):
    return sum(((row & x).bit_count()%2)<<i for i,row in enumerate(rows))


def rank(rows):
    basis={}
    for row in rows:
        while row:
            lead=row.bit_length()-1
            if lead in basis:row^=basis[lead]
            else:
                basis[lead]=row
                break
    return len(basis)


def complete_kernel(original_rows,basis,expected_rank):
    require(rank(original_rows)==expected_rank,'original-row rank')
    require(len(basis)==32-expected_rank,'kernel dimension')
    require(rank(basis)==len(basis),'kernel basis independence')
    require(all((r&b).bit_count()%2==0 for r in original_rows for b in basis),'kernel membership')
    vals=[0]
    for b in basis:vals += [v^b for v in vals]
    require(len(set(vals))==len(vals),'complete distinct kernel span')
    return vals


def first_impossible(masks):
    carries=[0]
    for j in range(32):
        count=sum((m>>j)&1 for m in masks)
        outgoing=set()
        for carry in carries:
            for signed_sum in range(-count,count+1,2):
                total=carry+signed_sum
                if total%2==0:outgoing.add(total//2)
        if not outgoing:return j
        carries=list(outgoing)
    return None


def original_equation(support,t):
    return [[k,i,c] for k,i,c in [('d',t,1),('g',t-2,-1),
        ('d',t-7,-1),('f',t-15,-1),('d',t-16,-1)] if i in support]


def combination(equations,weights):
    terms=defaultdict(int)
    for t,mul in weights.items():
        require(int(t) in equations,'combination references checked recurrence')
        for k,i,c in equations[int(t)]:terms[(k,i)]+=mul*c
    return {k:v for k,v in terms.items() if v}


def verify(cert):
    require(cert['schema']=='supports10-11-two-pair-joint-valuation-v1','schema')
    require(cert['definitions']=={'bits':32,'f_rotations':[7,18],'f_shift':3,
        'g_rotations':[17,19],'g_shift':10},'original sigma definitions')
    require(cert['k']==16,'theorem stratum')
    supports_file=HERE.parent/'supports-v2.json'
    require(hashlib.sha256(supports_file.read_bytes()).hexdigest()==SUPPORT_HASH,
            'frozen support identity')
    require(cert['source_support_sha256']==SUPPORT_HASH,'certificate source identity')
    supports=json.loads(supports_file.read_text())['supports']
    K=[int(v,16) for v in cert['kernel_X_basis']]
    X=complete_kernel([1<<j for j in range(16)]+G_ROWS[:16],K,cert['kernel_X_rank'])
    require(len(X)==2 and K==[0x44ab0000],'unique nonzero X mask')
    gamma=apply_rows(F_ROWS,K[0])
    require(gamma==int(cert['FX_xor_mask'],16),'actual F mask')
    Y=complete_kernel(F_ROWS[:16],[int(v,16) for v in cert['kernel_Y_basis']],
                      cert['kernel_Y_rank'])
    require(len(Y)==cert['first_candidates']==65536,'complete Y mask count')
    survivors=[];hist=Counter()
    for L in Y:
        bit=first_impossible([L,gamma])
        if bit is None:survivors.append(L)
        else:hist[str(bit)]+=1
    require(hist==Counter(cert['first_empty_histogram']),'full first carry histogram')
    require(sorted(survivors)==[int(v,16) for v in cert['first_survivors']],
            'complete first carry survivor cover')
    require(len(survivors)==5,'exact survivor count')
    for m in (1,2):
        failures={}
        for L in survivors:
            bit=first_impossible([apply_rows(F_ROWS,L),(m*K[0])&MASK,
                                  apply_rows(G_ROWS,K[0])])
            require(bit is not None,'second carry actual relaxed contradiction')
            failures[f'{L:08x}']=bit
        require(failures==cert['second_first_empty_bits'][str(m)],'second first-empty bits')
    require([(b['support_index'],b['m']) for b in cert['bridges']]==[(10,1),(11,2)],
            'exact support application scope')
    for bridge in cert['bridges']:
        support=set(supports[bridge['support_index']]);m=bridge['m']
        require(bridge['active_indices']==[18,26,34] and all(i in support for i in [18,26,34]),
                'actual pair and E activity')
        eqs={}
        for row in bridge['equations']:
            t=row['t'];require(16<=t<64,'original recurrence range')
            actual=original_equation(support,t)
            require(actual==row['terms'],'original recurrence substitution')
            eqs[t]=actual
        require(combination(eqs,bridge['core1_combination'])=={('d',26):1,('f',18):1},
                'core dY+FX exact identity')
        require(combination(eqs,bridge['core2_combination'])==
                {('f',26):1,('d',18):m,('g',18):1},'core FY+m*dX+GX exact identity')
        require(combination(eqs,bridge['E_combination'])==
                {('d',34):1,('d',18):-m,('g',18):-1},'E actual recurrence identity')
    require([v['m'] for v in cert['boundary_fixtures']]==[1,2],'both local sharpness scopes')
    for fixture in cert['boundary_fixtures']:
        words=fixture['words'];m=fixture['m']
        x,xp,y,yp=[words[k] for k in ['x','x_prime','y','y_prime']]
        require(all(0<=v<=MASK for v in [x,xp,y,yp]),'unsigned fixture words')
        A=(xp-x)&MASK;C=(apply_rows(G_ROWS,xp)-apply_rows(G_ROWS,x))&MASK
        E=(m*A+C)&MASK
        require(x!=xp and y!=yp and A and E,'nonzero actual fixture differences')
        require({'A':A,'C':C,'E':E}==fixture['interfaces'],'fixture actual interfaces')
        require((yp-y+apply_rows(F_ROWS,xp)-apply_rows(F_ROWS,x))&MASK==0,
                'first original fixture equation')
        require((apply_rows(F_ROWS,yp)-apply_rows(F_ROWS,y)+E)&MASK==0,
                'second original fixture equation')
        require((A|E)&0x7fff==0 and (A|E)&0x8000!=0,'local minimum valuation exactly 15')
    return {'status':'PASS','original_recurrences':11,'Y_masks':65536,
            'first_survivors':5,'second_contradictions':10,'actual_local_fixtures':2,
            'scope':'author finite-dependency replay; no full schedule or independent-agent acceptance'}


def negative_controls(cert):
    mutations=[
        ('wrong_sigma',lambda d:d['definitions'].__setitem__('f_shift',4)),
        ('wrong_X_rank',lambda d:d.__setitem__('kernel_X_rank',30)),
        ('wrong_X_mask',lambda d:d['kernel_X_basis'].__setitem__(0,'44ab0001')),
        ('missing_Y_basis',lambda d:d['kernel_Y_basis'].pop()),
        ('missing_survivor',lambda d:d['first_survivors'].pop()),
        ('wrong_carry_bit',lambda d:d['second_first_empty_bits']['2'].__setitem__('4804ddd6',26)),
        ('wrong_bridge_m',lambda d:d['bridges'][1].__setitem__('m',1)),
        ('missing_active_d11',lambda d:d['bridges'][1]['equations'][2]['terms'].pop()),
        ('wrong_E_combination',lambda d:d['bridges'][1]['E_combination'].__setitem__('18',1)),
        ('damaged_fixture_word',lambda d:d['boundary_fixtures'][0]['words'].__setitem__('x',0)),
        ('false_fixture_interface',lambda d:d['boundary_fixtures'][1]['interfaces'].__setitem__('E',0)),
    ]
    rejected=[]
    for name,mutation in mutations:
        damaged=copy.deepcopy(cert);mutation(damaged)
        try:verify(damaged)
        except (ValueError,KeyError):rejected.append(name)
        else:raise ValueError('negative control accepted: '+name)
    return rejected


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--negative',action='store_true')
    parser.add_argument('--save',action='store_true');args=parser.parse_args()
    start=time.monotonic();cert=json.loads((HERE/'CERTIFICATE.json').read_text())
    result=verify(cert)
    if args.negative:result['negative_controls_rejected']=negative_controls(cert)
    result.update({'python':platform.python_version(),'elapsed_s':time.monotonic()-start,
        'source_sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest()
                         for f in ['PROOF.md','CERTIFICATE.json','check.py']},
        'support_sha256':SUPPORT_HASH})
    if args.save:(HERE/'CHECK_RUN.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
