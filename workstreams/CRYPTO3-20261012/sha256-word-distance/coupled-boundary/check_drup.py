#!/usr/bin/env python3
"""RUP-only proof checking; deletions may safely be ignored by monotonicity.

The optional emitted hints allow a second, simpler verifier to avoid using
this watch-list implementation. No SAT library is imported here.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent


def read_cnf(path):
    clauses=[]
    n=None
    for line in path.read_text().splitlines():
        if line.startswith('c') or not line.strip():
            continue
        if line.startswith('p '):
            _,kind,variables,count=line.split()
            assert kind=='cnf'
            n=int(variables)
            expected=int(count)
        else:
            values=list(map(int,line.split()))
            assert values[-1]==0 and 0 not in values[:-1]
            assert all(abs(x)<=n for x in values[:-1])
            clauses.append(values[:-1])
    assert len(clauses)==expected
    return n,clauses


class RUP:
    def __init__(self,n,clauses):
        self.n=n
        self.clauses=[[]]
        self.watch=defaultdict(list)
        self.units=[]
        for c in clauses:
            self.add(c)

    def add(self,clause):
        c=list(dict.fromkeys(clause))
        idx=len(self.clauses)
        self.clauses.append(c)
        if len(c)<2:
            self.units.append(idx)
        else:
            self.watch[c[0]].append(idx)
            self.watch[c[1]].append(idx)
        return idx

    def check(self,clause):
        value=[0]*(self.n+1)
        trail=[]
        hints=[]
        def assign(lit):
            v=1 if lit>0 else -1
            old=value[abs(lit)]
            if old:
                return old==v
            value[abs(lit)]=v
            trail.append(lit)
            return True
        def val(lit):
            return value[abs(lit)]*(1 if lit>0 else -1)
        for lit in clause:
            if not assign(-lit):
                return hints
        for idx in self.units:
            c=self.clauses[idx]
            if not c:
                return hints+[idx]
            if val(c[0])<=0:
                hints.append(idx)
                if not assign(c[0]):
                    return hints
        head=0
        while head<len(trail):
            false=-trail[head]
            head+=1
            watched=self.watch[false]
            j=0
            while j<len(watched):
                idx=watched[j]
                c=self.clauses[idx]
                if c[0]==false:
                    c[0],c[1]=c[1],c[0]
                assert c[1]==false
                if val(c[0])>0:
                    j+=1
                    continue
                replacement=None
                for k in range(2,len(c)):
                    if val(c[k])>=0:
                        replacement=k
                        break
                if replacement is not None:
                    c[1],c[replacement]=c[replacement],c[1]
                    watched[j]=watched[-1]
                    watched.pop()
                    self.watch[c[1]].append(idx)
                    continue
                hints.append(idx)
                if val(c[0])<0:
                    return hints
                assert assign(c[0])
                j+=1
        raise ValueError('clause is not RUP: '+str(clause))


def verify(cnf,proof,hint_path=None):
    n,clauses=read_cnf(cnf)
    checker=RUP(n,clauses)
    additions=deletions=0
    empty=False
    out=hint_path.open('w') if hint_path else None
    try:
        for line in proof.read_text().splitlines():
            if not line.strip():
                continue
            if line.startswith('d '):
                deletions+=1
                continue
            tokens=list(map(int,line.split()))
            assert tokens[-1]==0 and 0 not in tokens[:-1]
            clause=tokens[:-1]
            assert all(abs(x)<=n for x in clause)
            hints=checker.check(clause)
            idx=checker.add(clause)
            additions+=1
            if out:
                out.write(json.dumps([idx,clause,hints],separators=(',',':'))+'\n')
            if not clause:
                empty=True
        assert empty,'no derived empty clause'
    finally:
        if out:
            out.close()
    return {'status':'PASS','variables':n,'input_clauses':len(clauses),
            'checked_rup_additions':additions,'ignored_deletions':deletions,
            'derived_empty_clause':empty}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cnf',type=Path,default=HERE/'boundary.cnf')
    parser.add_argument('--proof',type=Path,default=HERE/'boundary.drup')
    parser.add_argument('--emit-hints',action='store_true')
    args=parser.parse_args()
    start=time.monotonic()
    result=verify(args.cnf,args.proof,HERE/'boundary.rup.jsonl' if args.emit_hints else None)
    result['seconds']=time.monotonic()-start
    result['cnf_sha256']=hashlib.sha256(args.cnf.read_bytes()).hexdigest()
    result['proof_sha256']=hashlib.sha256(args.proof.read_bytes()).hexdigest()
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
