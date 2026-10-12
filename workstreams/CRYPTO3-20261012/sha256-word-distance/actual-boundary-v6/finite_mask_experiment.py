#!/usr/bin/env python3
"""One pre-budgeted 11,440-case exact screen; no SMT or full schedules."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASK = (1 << 32) - 1
F_INVERSE_HEX = [
    "185744e9", "30ae89d2", "615d13a4", "daed63a1", "9cd03a8e", "08fdcc39", "11fb9872", "23f730e4",
    "5fb92521", "bf724a42", "57ee6948", "afdcd290", "76b358ec", "f531f531", "c36917ae", "b78f9679",
    "4615d13e", "947ce695", "19a4740f", "2b1facf7", "4e681d07", "84877ee7", "385344eb", "70a689d6",
    "f91a5745", "c36917af", "b78f967b", "4615d13a", "8c2ba274", "290afdcd", "4a42bf73", "94857ee6",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sigma(word,which):
    first,second,shift = (7,18,3) if which == 0 else (17,19,10)
    def rotate(count):
        return ((word >> count) | (word << (32-count))) & MASK
    return rotate(first) ^ rotate(second) ^ (word >> shift)


def inverse_f(word):
    answer = 0
    for bit,column in enumerate(F_INVERSE_HEX):
        if word >> bit & 1:
            answer ^= int(column,16)
    return answer


def valuation(word):
    assert word
    return (word & -word).bit_length()-1


def interval(k,end):
    return ((1 << (end+1))-1) ^ ((1 << k)-1)


def pair(x,y):
    return {"x":x,"y":y,"difference":(y-x)&MASK,
            "F":(sigma(y,0)-sigma(x,0))&MASK,
            "G":(sigma(y,1)-sigma(x,1))&MASK,
            "input_xor":x^y}


def complement_reverse(x,y):
    return pair(MASK^y,MASK^x)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    for bit,column in enumerate(F_INVERSE_HEX):
        assert sigma(int(column,16),0) == 1 << bit
    strata = []
    comparisons = 0
    for k in range(32):
        forward = [valuation(sigma(interval(k,end),0)) for end in range(k,32)]
        backward = [valuation(inverse_f(interval(k,end))) for end in range(k,32)]
        matches = []
        for i,left in enumerate(forward):
            for j,right in enumerate(backward):
                comparisons += 1
                if left == right:
                    matches.append([k+i,k+j,left])
        strata.append({"power_bit":k,"forward_run_valuation":forward,
                       "inverse_output_run_valuation":backward,"surviving_endpoint_triples":matches})
    assert comparisons == 11440
    p13 = pair(0,inverse_f(1 << 29))
    p29 = complement_reverse(p13["x"],p13["y"])
    # A pre-existing exact inverse basis value of sigma1 at bit22; verify directly.
    g_inverse_bit22 = 0x8DDD55AD
    assert sigma(g_inverse_bit22,1) == 1 << 22
    p26 = pair(0,g_inverse_bit22)
    p42 = complement_reverse(p26["x"],p26["y"])
    fixture = {"pairs_by_index":{"13":p13,"29":p29,"26":p26,"42":p42},
               "common_c":p13["difference"],"common_b":p26["difference"],
               "a":(-p26["F"])&MASK,"e":(p13["F"]+p26["G"])&MASK,
               "k":(-p29["G"])&MASK,"d57":p42["F"],
               "sigma0_sum_c_pairs":(p13["F"]+p29["F"])&MASK,
               "sigma1_sum_b_pairs":(p26["G"]+p42["G"])&MASK,
               "reverse_boundary_target":(-p13["G"]-p29["G"])&MASK,
               "scope":"four actual word pairs satisfying equal-difference and conservation subset; other nine active pairs and base message NOT provided"}
    assert p13["difference"] == p29["difference"] != 0
    assert p26["difference"] == p42["difference"] != 0
    assert fixture["sigma0_sum_c_pairs"] == fixture["sigma1_sum_b_pairs"] == 0
    assert all(fixture[name] != 0 for name in ("a","e","k","d57","reverse_boundary_target"))
    result = {"schema":"crypto3-actual-boundary-prebudgeted-mask-screen-v6",
              "experiment_plan_sha256":digest(HERE/"EXPERIMENT_PLAN.md"),
              "source_sha256":digest(Path(__file__).resolve()),
              "f_inverse_basis_hex":F_INVERSE_HEX,
              "f_inverse_basis_provenance":{"source":"active-pair-review/INDEPENDENT_RUN.json",
                                            "sha256":"7e951e4ac3b5e26c5eb73ef4895be2e35c9daa79ecd98ff510db0d9159077001"},
              "comparison_count":comparisons,"strata":strata,
              "empty_power_bits":[s["power_bit"] for s in strata if not s["surviving_endpoint_triples"]],
              "total_surviving_endpoint_triples":sum(len(s["surviving_endpoint_triples"]) for s in strata),
              "analytic_conservation_fixture":fixture,
              "no_sat_or_unknown_replay":True,
              "real_inverse_shift_unresolved":True}
    rendered = json.dumps(result,indent=2)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered,end="")


if __name__ == "__main__":
    main()
