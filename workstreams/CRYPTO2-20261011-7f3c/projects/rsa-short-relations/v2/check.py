#!/usr/bin/env python3
"""Exact scope checks and actual Lean elaboration; no external Python packages."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent

def convergents(a, b):
    p0, p1, q0, q1 = 0, 1, 1, 0
    while b:
        c, rem = divmod(a, b)
        p0, p1 = p1, c*p1+p0
        q0, q1 = q1, c*q1+q0
        yield p1, q1
        a, b = b, rem

def recover(N, e):
    # Receives public values only, never the polynomial or the test private key.
    answers = []
    for d, k in convergents(N, e):
        if k == 0 or (e*d-1) % k:
            continue
        phi = (e*d-1)//k
        total = N-phi+1
        disc = total*total-4*N
        if disc < 0:
            continue
        z = math.isqrt(disc)
        if z*z == disc and (total+z) % 2 == 0:
            p, q = (total+z)//2, (total-z)//2
            if p > 1 and q > 1 and p*q == N:
                answers.append(dict(d=d, k=k, p=p, q=q))
    return answers

def exact_checks():
    fixture = HERE.parent/'evidence/general/synthetic.json'
    data = json.loads(fixture.read_text())
    cases = []
    for case in data['cases']:
        N, e = (int(case['public'][x]) for x in ('N', 'e'))
        expected = {x:int(v) for x,v in case['expected'].items()}
        answers = recover(N, e)
        assert any(a['d'] == expected['d'] and a['k'] == expected['k']
                   and {a['p'],a['q']} == {expected['p'],expected['q']} for a in answers)
        k, d, Y = expected['k'], expected['d'], int(case['Y'])
        assert 3*k*k*Y < e and 0 <= N*k-e*d and 2*k*(N*k-e*d)<e
        cases.append(dict(degree=case['m'], answers=answers))
    # Removing the shortness bound makes the lifting conclusion false.
    e,N,k,s,d,r,t,u,X,Y,T = 3,3,1,1,1,1,3,2,1,1,3
    assert 1+k*(N-s)==e*d and e*u==r*N+t
    assert 0<k<=X and 0<r and 1<=s<=Y and r*Y<=T and -T<=t<=T
    assert math.gcd(k,d)==1 and not 3*X*T<e and u*k!=r*d
    # Coprimality is essential for the standalone gcd_recovery lemma.
    k,d,r,u = 2,2,1,1
    assert u*k==r*d and r//math.gcd(r,u)!=k
    # A strict small-multiple interval cannot be replaced by a closed interval.
    assert 3%3==0 and -3<=3<=3 and 3!=0
    return dict(cases=cases, negative_mathematical_controls=3,
                fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--lean-root', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args=ap.parse_args()
    root=args.lean_root.resolve()
    env=os.environ.copy()
    env.update(LEAN_SYSROOT=str(root), LAKE_HOME=str(root),
               PATH=str(root/'bin')+os.pathsep+env.get('PATH',''))
    source=(HERE/'lean/lakefile.lean').read_text()
    assert 'sorry' not in source and '\naxiom ' not in source
    records=[]
    for name, extra, good in [
        ('positive','',True),
        ('false-conclusion','\nexample : (2 : Int) = 3 := by decide\n',False),
    ]:
        with tempfile.TemporaryDirectory(prefix='rsa-scope-') as tmp:
            path=Path(tmp)
            (path/'lakefile.lean').write_text(source+extra)
            command=[str(root/'bin/lake'),'--reconfigure','env','true']
            p=subprocess.run(command,cwd=path,env=env,capture_output=True,text=True,timeout=60)
            output=(p.stdout+p.stderr).replace(tmp,'<temporary-checkout>')
            assert (p.returncode==0)==good, output
            if good:
                assert output.count('depends on axioms:')==8
                for line in output.splitlines():
                    if 'depends on axioms:' in line:
                        assert line.endswith('[propext, Classical.choice, Quot.sound]'), line
            else:
                assert 'false' in output.lower() or 'failed' in output.lower(), output
            records.append(dict(name=name, command=command, exit_code=p.returncode, output=output))
    version=subprocess.run([str(root/'bin/lake'),'--version'],env=env,capture_output=True,text=True,check=True).stdout.strip()
    result=dict(schema='rsa-scope-audit-v2',python=platform.python_version(),platform=platform.platform(),
                lean_version=version,source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                exact=exact_checks(),lean_runs=records)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: 8 Lean declarations, axiom audit, rejected false theorem, public-only CF recovery, 3 mathematical negative controls')

if __name__=='__main__':
    main()
