#!/usr/bin/env python3
"""Transparent Tseitin encoding of three exact 32-bit modular equalities."""
import argparse
import hashlib
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
K = 0xfbca7000


class Circuit:
    def __init__(self):
        self.n = 0
        self.clauses = []
        self.gates = []
        self.inputs = {}

    def fresh(self):
        self.n += 1
        return self.n

    def word(self, name):
        bits = [self.fresh() for _ in range(32)]
        self.inputs[name] = bits
        return bits

    def gate(self, op, a, b):
        z = self.fresh()
        if op == 'xor':
            self.clauses += [[-a,-b,-z],[a,b,-z],[a,-b,z],[-a,b,z]]
        elif op == 'and':
            self.clauses += [[-a,-b,z],[a,-z],[b,-z]]
        elif op == 'or':
            self.clauses += [[a,b,-z],[-a,z],[-b,z]]
        else:
            raise ValueError(op)
        self.gates.append([op,a,b,z])
        return z

    def add(self, a, b):
        carry = self.zero
        output = []
        for i in range(32):
            ab = self.gate('xor',a[i],b[i])
            output.append(self.gate('xor',ab,carry))
            if i < 31:
                t = self.gate('and',a[i],b[i])
                u = self.gate('and',ab,carry)
                carry = self.gate('or',t,u)
        return output

    def sigma(self, x, a, b, shift):
        return [self.gate('xor',self.gate('xor',x[(i+a)%32],x[(i+b)%32]),
                          x[i+shift] if i+shift < 32 else self.zero)
                for i in range(32)]

    def equal(self, a, b):
        for x,y in zip(a,b):
            self.clauses += [[-x,y],[x,-y]]


def build():
    c = Circuit()
    q,p,pp = [c.word(name) for name in ['q','p','p_prime']]
    c.zero = c.fresh()
    c.clauses.append([-c.zero])
    qp = [-q[i] if (K>>i)&1 else q[i] for i in range(32)]
    gq = c.sigma(q,17,19,10)
    gqp = c.sigma(qp,17,19,10)
    c.equal(c.add(q,gq),c.add(qp,gqp))
    c.equal(c.add(pp,q),c.add(p,qp))
    fpp = c.sigma(pp,7,18,3)
    fqp = c.sigma(qp,7,18,3)
    fp = c.sigma(p,7,18,3)
    fq = c.sigma(q,7,18,3)
    c.equal(c.add(fpp,fqp),c.add(fp,fq))
    return c


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--solve',action='store_true')
    args=parser.parse_args()
    c=build()
    raw='p cnf %d %d\n'%(c.n,len(c.clauses))
    raw+=''.join(' '.join(map(str,x))+' 0\n' for x in c.clauses)
    (HERE/'boundary.cnf').write_text(raw)
    (HERE/'circuit.json').write_text(json.dumps({'schema':'crypto3-coupled-circuit-v1','K':K,
        'variables':c.n,'inputs':c.inputs,'zero':c.zero,'gates':c.gates},indent=2)+'\n')
    result={'variables':c.n,'clauses':len(c.clauses),'cnf_sha256':hashlib.sha256(raw.encode()).hexdigest()}
    if args.solve:
        import pysat
        from pysat.solvers import Solver
        start=time.monotonic()
        with Solver(name='g3',bootstrap_with=c.clauses,with_proof=True) as s:
            s.conf_budget(200000)
            answer=s.solve_limited()
            result.update({'solver':'Glucose3','pysat':pysat.__version__,'conflict_budget':200000,
                           'answer':str(answer),'seconds':time.monotonic()-start,'statistics':s.accum_stats()})
            if answer is False:
                proof='\n'.join(s.get_proof())+'\n'
                (HERE/'boundary.drup').write_text(proof)
                result['proof_sha256']=hashlib.sha256(proof.encode()).hexdigest()
                result['proof_lines']=len(proof.splitlines())
            elif answer is True:
                result['model']=s.get_model()
        (HERE/'SOLVER_RUN.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
