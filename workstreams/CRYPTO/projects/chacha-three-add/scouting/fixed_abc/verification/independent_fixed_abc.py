#!/usr/bin/env python3
"""Independent distribution calibration: fixed a,b,c and uniform d.

Written from original word operations before reading the discovery fixed_abc
implementation. Only seven deterministic small-word input settings are used;
there is no search over a,b,c and no 32-bit original-input enumeration.
"""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]


def rol(x, r, n):
    r %= n
    return ((x << r) | (x >> (n-r))) & ((1 << n)-1)


def original_counts(n, r, q, a, b, c):
    mask = (1 << n)-1
    counts = [0] * n
    for d in range(1 << n):
        s = (a+b) & mask
        t = rol(d ^ s, r, n)
        u = (c+t) & mask
        y = rol(b ^ u, q, n)
        w = (s+y) & mask
        linear_s = a ^ b
        linear_t = rol(d ^ linear_s, r, n)
        linear_u = c ^ linear_t
        linear_y = rol(b ^ linear_u, q, n)
        linear_w = linear_s ^ linear_y
        error = w ^ linear_w
        for i in range(n):
            counts[i] += -1 if ((error >> i) & 1) else 1
    return counts


def threshold_sum(n, r, q, i, a, b, c):
    # Independent U summation, with output bits assembled explicitly instead
    # of using the original-word rotation helper or the joint-state recurrence.
    j, k = (i-q) % n, (i-r-q) % n
    ni, nj, nk = 1 << i, 1 << j, 1 << k
    carry_i = int((a % ni) + (b % ni) >= ni)
    carry_k = int((a % nk) + (b % nk) >= nk)
    constant_phase = carry_i ^ carry_k
    s_low = (a+b) % ni
    numerator = 0
    for u in range(1 << n):
        y_low = 0
        for output_bit in range(i):
            source_bit = (output_bit-q) % n
            y_low |= (((b >> source_bit) ^ (u >> source_bit)) & 1) << output_bit
        borrow = int(u % nj < c % nj)
        final_carry = int(s_low + y_low >= ni)
        numerator += -1 if constant_phase ^ borrow ^ final_carry else 1
    return Fraction(numerator, 1 << n)


def four_state_correlation(n, r, q, i, a, b, c):
    if not (n >= 1 and 0 <= r < n and 0 <= q < n and 0 <= i < n):
        raise ValueError("parameters outside word/rotation/bit domain")
    if not all(0 <= x < (1 << n) for x in (a, b, c)):
        raise ValueError("fixed word outside n-bit domain")
    s = (a+b) & ((1 << n)-1)
    alpha = s ^ a ^ b
    j, k = (i-q) % n, (i-r-q) % n
    phase = ((alpha >> i) ^ (alpha >> k)) & 1
    if i >= q:
        prefix_length = q
        overlap_length = j
        unit = 1 << prefix_length
        prefix_carry_count = s % unit
        counts = [unit-prefix_carry_count, prefix_carry_count, 0, 0]
        start_u, start_s = 0, q
        support = {"case": "i>=q", "independent_prefix": "final-addition carry",
                   "prefix_U_interval": [n-q, n], "overlap_U_interval": [0, j]}
    else:
        prefix_length = n-q
        overlap_length = i
        unit = 1 << prefix_length
        prefix_borrow_count = c % unit
        counts = [unit-prefix_borrow_count, 0, prefix_borrow_count, 0]
        start_u, start_s = prefix_length, 0
        support = {"case": "i<q", "independent_prefix": "middle-addition borrow",
                   "prefix_U_interval": [0, prefix_length], "overlap_U_interval": [prefix_length, j]}
    initial_counts = counts[:]
    for offset in range(overlap_length):
        u_position, s_position = start_u+offset, start_s+offset
        c_bit = (c >> u_position) & 1
        b_bit = (b >> u_position) & 1
        s_bit = (s >> s_position) & 1
        following = [0, 0, 0, 0]
        for state, count in enumerate(counts):
            borrow, carry = divmod(state, 2)
            for u_bit in (0, 1):
                next_borrow = int(c_bit+borrow > u_bit)
                y_bit = b_bit ^ u_bit
                next_carry = int(s_bit+y_bit+carry >= 2)
                following[2*next_borrow+next_carry] += count
        counts = following
    denominator = 1 << (prefix_length+overlap_length)
    assert sum(counts) == denominator
    numerator = counts[0]-counts[1]-counts[2]+counts[3]
    if phase:
        numerator = -numerator
    return Fraction(numerator, denominator), {
        "j": j, "k": k, "constant_phase": phase, "S": s, "first_carry_word": alpha,
        "prefix_length": prefix_length, "overlap_length": overlap_length,
        "initial_integer_counts": initial_counts, "terminal_integer_counts": counts,
        "denominator_before_reduction": denominator, **support}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    # Selected before discovery-code disclosure. The settings cover both
    # support orders, zero rotation, no overlap, borrow phases, and zero words.
    settings = [(1,0,0,1,1,1), (3,1,0,3,5,2), (3,2,2,3,1,6),
                (4,1,3,5,7,9), (4,2,2,7,9,13), (5,4,2,13,17,23), (3,1,1,0,0,0)]
    report = {"started_utc": datetime.now(timezone.utc).isoformat(),
              "command": [sys.executable, str(Path(__file__).resolve())],
              "environment": {"python": sys.version, "platform": platform.platform()},
              "source_sha256": sha(Path(__file__).resolve()),
              "independence": "Original definition and parent task specification only; discovery fixed_abc proof, code, and results not read before this run.",
              "random_seed": None, "settings": settings,
              "parameter_search_over_fixed_words": False}
    try:
        comparisons = []
        raw_counts = []
        for n,r,q,a,b,c in settings:
            direct = original_counts(n,r,q,a,b,c)
            raw_counts.append({"n":n,"r":r,"q":q,"a":a,"b":b,"c":c,
                               "samples":1 << n,"signed_sums":direct})
            for i in range(n):
                original = Fraction(direct[i],1 << n)
                threshold = threshold_sum(n,r,q,i,a,b,c)
                dp, detail = four_state_correlation(n,r,q,i,a,b,c)
                assert original == threshold == dp, (n,r,q,i,a,b,c,original,threshold,dp)
                comparisons.append({"n":n,"r":r,"q":q,"i":i,"a":a,"b":b,"c":c,
                                    "correlation":str(dp),"pass":True,"state_details":detail})
        phase_value, detail = four_state_correlation(3,2,2,0,3,1,6)
        assert detail["constant_phase"] == 1 and phase_value == -1

        old_uniform = PROJECT / "verification/independent_word_counts.jsonl"
        old_fixed = PROJECT / "verification/general_fixed_word_counts.jsonl"
        uniform = next(json.loads(line) for line in old_uniform.read_text().splitlines()
                       if (lambda x: x.get("kind") == "exhaustive" and
                           (x["n"],x["r"],x["q"]) == (3,1,1))(json.loads(line)))
        fixed = next(json.loads(line) for line in old_fixed.read_text().splitlines()
                     if (lambda x: (x["n"],x["r"],x["q"],x["a"]) == (3,1,1,0))(json.loads(line)))
        uniform_value = Fraction(uniform["signed_sums"][2],uniform["samples"])
        fixed_a_value = Fraction(fixed["signed_sums"][2],fixed["samples"])
        fixed_abc_value, _ = four_state_correlation(3,1,1,2,0,0,0)
        assert (uniform_value,fixed_a_value,fixed_abc_value) == (Fraction(-3,16),Fraction(1,8),Fraction(1))
        report.update({"status":"pass","exit_code":0,"fixed_settings":len(settings),
                       "original_d_inputs_enumerated":sum(1 << row[0] for row in settings),
                       "bit_comparisons":len(comparisons),"raw_original_word_counts":raw_counts,
                       "comparisons":comparisons,
                       "constant_phase_negative_control":{"n":3,"r":2,"q":2,"i":0,
                           "a":3,"b":1,"c":6,"correct":"-1","omitting_constant_phase":"1"},
                       "distribution_control":{"n":3,"r":1,"q":1,"i":2,
                           "uniform_all_words":str(uniform_value),
                           "fixed_a_zero_other_words_uniform":str(fixed_a_value),
                           "fixed_abc_zero_d_uniform":str(fixed_abc_value)},
                       "frozen_data_sha256":{str(p):sha(p) for p in (old_uniform,old_fixed)},
                       "claim_status":"L0 distribution calibration; no novelty or attack claim"})
    except Exception as exc:
        report.update({"status":"failed","exit_code":1,"error":repr(exc)})
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (HERE / "independent_run.json").write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ("status","fixed_settings","original_d_inputs_enumerated",
                      "bit_comparisons","constant_phase_negative_control","distribution_control")},indent=2))


if __name__ == "__main__":
    main()
