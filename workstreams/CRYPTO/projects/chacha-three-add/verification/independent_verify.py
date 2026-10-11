#!/usr/bin/env python3
"""Blind independent word-enumeration and integer-threshold-sum verification.

Reads only this verification directory. It does not read discovery experiments
or proofs. No random trials are required: all executed numerical checks are exact.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent

def proposed(r, q):
    return (-Fraction(1,3*(1<<r))-Fraction(1,7*(1<<q))
            +Fraction(4,3*(1<<(3*r+2*q)))+Fraction(1,7*(1<<(3*r+q))))

def independent_threshold_sum(r, q):
    """Independent finite sum after integrating out the threshold variable S.

    B and V are independent uniform integers below M=2^(r+q).
    U=(B mod 2^r) xor floor(V/2^q). No closed-form lemma used here.
    """
    R, M = 1<<r, 1<<(r+q)
    total = 0
    for B in range(M):
        for V in range(M):
            U=(B & (R-1)) ^ (V>>q)
            total += (2*U+2-R)*(2*abs(B+V-M)-M)
    return Fraction(total, R*M**3)

def invoke(argv):
    start=time.monotonic()
    p=subprocess.run(argv, cwd=HERE, capture_output=True, text=True)
    return {"argv":argv,"exit_code":p.returncode,"elapsed_seconds":time.monotonic()-start,
            "stdout":p.stdout,"stderr":p.stderr}

def main():
    compiler=invoke(["g++","--version"])
    compile_result=invoke(["g++","-O3","-std=c++17","-Wall","-Wextra","-Werror",
                           str(HERE/"independent_word_enumerator.cpp"),"-o",str(HERE/"independent_word_enumerator")])
    if compile_result["exit_code"]:
        (HERE/"independent_run.json").write_text(json.dumps({"compile":compile_result},indent=2))
        raise RuntimeError(compile_result["stderr"])
    run_result=invoke([str(HERE/"independent_word_enumerator")])
    if run_result["exit_code"]: raise RuntimeError(run_result["stderr"])
    (HERE/"independent_word_counts.jsonl").write_text(run_result["stdout"])
    rows=[json.loads(x) for x in run_result["stdout"].splitlines()]
    direct=[x for x in rows if x["kind"]=="exhaustive"]
    accepted=[]
    for x in direct:
        n,r,q=x["n"],x["r"],x["q"]
        if r>=1 and q>=1 and r+q<n:
            i=r+q
            actual=Fraction(x["signed_sums"][i],x["samples"])
            threshold=independent_threshold_sum(r,q)
            expected=proposed(r,q)
            assert actual==threshold==expected, (x,actual,threshold,expected)
            accepted.append({"n":n,"r":r,"q":q,"i":i,"samples":x["samples"],
                             "signed_correlation":str(actual),"threshold_sum":str(threshold),
                             "formula":str(expected),"pass":True})
    # Distinct exact calculation at larger local widths, without enumerating words.
    sum_checks=[]
    for r in range(1,6):
        for q in range(1,6):
            actual=independent_threshold_sum(r,q)
            expected=proposed(r,q)
            assert actual==expected,(r,q,actual,expected)
            sum_checks.append({"r":r,"q":q,"pair_count":1<<(2*(r+q)),
                               "correlation":str(actual),"pass":True})
    # A zero second rotation is outside the theorem and the displayed formula fails.
    q0=next(x for x in direct if (x["n"],x["r"],x["q"])==(3,1,0))
    q0_actual=Fraction(q0["signed_sums"][1],q0["samples"])
    q0_expected=proposed(1,0)
    assert q0_actual!=q0_expected
    # Applying the candidate formula to a wrapped target is also invalid.
    wrap=next(x for x in direct if (x["n"],x["r"],x["q"])==(3,1,2))
    wrap_actual=Fraction(wrap["signed_sums"][0],wrap["samples"])
    wrap_expected=proposed(1,2)
    assert wrap_actual!=wrap_expected
    wrong=next(x for x in rows if x["kind"]=="right_rotation_negative_control")
    wrong_actual=Fraction(wrong["signed_sum"],wrong["samples"])
    assert wrong_actual!=proposed(1,2)
    standard=proposed(16,12)
    reported=Fraction(-47180567524833621,1180591620717411303424)
    assert standard==reported
    sign_example=accepted[0]
    assert Fraction(sign_example["signed_correlation"])<0
    output={
        "independence":"Derived from the supplied word-operation specification; no discovery files read.",
        "seed":"none; exhaustive / exact integer summation",
        "environment":{"python":sys.version,"platform":platform.platform(),"compiler":compiler["stdout"]},
        "source_sha256":{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in
                         [HERE/"independent_word_enumerator.cpp",HERE/"independent_verify.py"]},
        "compile":compile_result,
        "execution":{k:v for k,v in run_result.items() if k!="stdout"},
        "rfc8439":next(x for x in rows if x["kind"]=="rfc8439_section_2_1_1"),
        "all_rotation_word_enumerations":len(direct),
        "in_domain_exhaustive_cases":accepted,
        "independent_threshold_sum_cases":sum_checks,
        "negative_controls":[
            {"case":"q=0 outside hypothesis","actual":str(q0_actual),"misapplied_formula":str(q0_expected),"detected":True},
            {"case":"r+q=n, wrapped bit outside hypothesis","actual":str(wrap_actual),"misapplied_formula":str(wrap_expected),"detected":True},
            {"case":"right instead of left rotation","actual":str(wrong_actual),"left_formula":str(proposed(1,2)),"detected":True}],
        "standard":{"n":32,"r":16,"q":12,"i":28,"correlation":str(standard),
                    "decimal_correlation":float(standard),"equality_probability":str((1+standard)/2),
                    "signed_bias":str(standard/2),"reported_fraction_matches":True},
        "result":"PASS; finite numerical evidence plus separate independent written general proof"
    }
    (HERE/"independent_run.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({"result":"PASS","word_cases":len(direct),"in_domain_cases":len(accepted),
                      "threshold_cases":len(sum_checks),"standard":str(standard),
                      "negative_controls":output["negative_controls"]},indent=2))

if __name__=="__main__": main()
