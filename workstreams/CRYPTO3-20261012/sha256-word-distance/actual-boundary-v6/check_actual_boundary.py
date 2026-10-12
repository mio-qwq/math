#!/usr/bin/env python3
"""Direct-bit independent-of-generator verification of the v6 local result."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MOD = 1 << 32
MASK = MOD-1
SUPPORT_HASH = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"
# Every nonzero original support-12 row, in the convention E_t=0.
EXPECTED_ROWS = {
    17:[["G",15,-1],["d",10,-1]],
    18:[["d",18,1],["d",11,-1]],
    20:[["d",20,1],["G",18,-1],["d",13,-1]],
    22:[["G",20,-1],["d",15,-1]],
    25:[["d",18,-1],["F",10,-1]],
    26:[["d",26,1],["F",11,-1],["d",10,-1]],
    27:[["d",20,-1],["d",11,-1]],
    28:[["d",28,1],["G",26,-1],["F",13,-1]],
    29:[["d",29,1],["d",13,-1]],
    30:[["G",28,-1],["F",15,-1]],
    31:[["G",29,-1],["d",15,-1]],
    33:[["d",26,-1],["F",18,-1]],
    34:[["d",34,1],["d",18,-1]],
    35:[["d",28,-1],["F",20,-1]],
    36:[["G",34,-1],["d",29,-1],["d",20,-1]],
    41:[["d",34,-1],["F",26,-1]],
    42:[["d",42,1],["d",26,-1]],
    43:[["d",43,1],["F",28,-1]],
    44:[["G",42,-1],["F",29,-1],["d",28,-1]],
    45:[["G",43,-1],["d",29,-1]],
    49:[["d",42,-1],["F",34,-1]],
    50:[["d",43,-1],["d",34,-1]],
    57:[["d",57,1],["F",42,-1]],
    58:[["F",43,-1],["d",42,-1]],
    59:[["G",57,-1],["d",43,-1]],
}


def require(value,message):
    if not value:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bit_sigma(x,which):
    a,b,s = (7,18,3) if which == 0 else (17,19,10)
    y = 0
    for j in range(32):
        bit = ((x >> ((j+a) % 32)) & 1) ^ ((x >> ((j+b) % 32)) & 1)
        if j+s < 32:
            bit ^= (x >> (j+s)) & 1
        y |= bit << j
    return y


def v2(x):
    require(x != 0,"valuation of zero")
    return (x & -x).bit_length()-1


def original_rows(support):
    rows = {}
    for t in range(16,64):
        row = [[name,j,coef] for name,j,coef in
               [["d",t,1],["G",t-2,-1],["d",t-7,-1],["F",t-15,-1],["d",t-16,-1]]
               if j in support]
        if row:
            rows[t] = row
    require(rows == EXPECTED_ROWS,"readable original-row substitution mismatch")
    return rows


def actual_pair(item):
    x,y = item["x"],item["y"]
    require(0 <= x < MOD and 0 <= y < MOD and x != y,"invalid actual words")
    expected = {"x":x,"y":y,"difference":(y-x) % MOD,
                "F":(bit_sigma(y,0)-bit_sigma(x,0)) % MOD,
                "G":(bit_sigma(y,1)-bit_sigma(x,1)) % MOD,"input_xor":x^y}
    require(item == expected,"actual pair derivative mismatch")
    return expected


def verify(data):
    basis = [int(x,16) for x in data["f_inverse_basis_hex"]]
    require(len(basis) == 32,"inverse basis size")
    require(all(bit_sigma(column,0) == 1 << i for i,column in enumerate(basis)),"inverse basis equation")
    def inverse_f(x):
        value = 0
        for i in range(32):
            if x >> i & 1:
                value ^= basis[i]
        return value
    comparisons,survivors,empty = 0,0,[]
    high_certificate = []
    require(len(data["strata"]) == 32,"incomplete power strata")
    for k,stored in enumerate(data["strata"]):
        require(stored["power_bit"] == k,"stratum order")
        masks = [sum(1 << j for j in range(k,end+1)) for end in range(k,32)]
        fvals = [v2(bit_sigma(x,0)) for x in masks]
        ivals = [v2(inverse_f(x)) for x in masks]
        require(stored["forward_run_valuation"] == fvals,"forward interval valuations")
        require(stored["inverse_output_run_valuation"] == ivals,"inverse interval valuations")
        matching = []
        for u in range(k,32):
            for w in range(k,32):
                comparisons += 1
                if fvals[u-k] == ivals[w-k]:
                    matching.append([u,w,fvals[u-k]])
        require(stored["surviving_endpoint_triples"] == matching,"endpoint cover mismatch")
        survivors += len(matching)
        if not matching:
            empty.append(k)
        if k >= 22:
            require(all(value == k-18 for value in fvals),"high input interval least bit")
            require(all(value < k-18 for value in ivals),"high inverse output interval obstruction")
            high_certificate.append({"k":k,"forward_valuation":k-18,"inverse_valuation_max":max(ivals),
                                     "inverse_run_words_hex":[f"{inverse_f(x):08x}" for x in masks]})
    require(comparisons == data["comparison_count"] == 11440,"comparison budget or cover")
    require(empty == data["empty_power_bits"] == list(range(22,32)),"empty high-power strata")
    require(survivors == data["total_surviving_endpoint_triples"] == 3675,"survivor count")
    fixture = data["analytic_conservation_fixture"]
    pairs = {j:actual_pair(item) for j,item in fixture["pairs_by_index"].items()}
    require(set(pairs) == {"13","29","26","42"},"fixture pair index coverage")
    P,Q,U,V = (pairs[j] for j in ("13","29","26","42"))
    require(P["difference"] == Q["difference"] == fixture["common_c"],"actual c-pair difference")
    require(U["difference"] == V["difference"] == fixture["common_b"],"actual b-pair difference")
    require(P["F"] + Q["F"] == MOD,"opposed sigma0 derivatives")
    require(U["G"] + V["G"] == MOD,"opposed sigma1 derivatives")
    require((P["F"]+Q["F"]+U["G"]+V["G"]) % MOD == 0,"actual conservation equation")
    expected_auxiliary = {"a":(-U["F"]) % MOD,"e":(P["F"]+U["G"]) % MOD,
                          "k":(-Q["G"]) % MOD,"d57":V["F"],
                          "sigma0_sum_c_pairs":(P["F"]+Q["F"]) % MOD,
                          "sigma1_sum_b_pairs":(U["G"]+V["G"]) % MOD,
                          "reverse_boundary_target":(-P["G"]-Q["G"]) % MOD}
    for key,value in expected_auxiliary.items():
        require(fixture[key] == value,"auxiliary actual value: "+key)
    require(all(fixture[key] != 0 for key in ("a","e","k","d57","reverse_boundary_target")),
            "zero local auxiliary or boundary")
    require(bit_sigma(MASK,0) == (1 << 29)-1,"sigma0 complement constant")
    require(bit_sigma(MASK,1) == (1 << 22)-1,"sigma1 complement constant")
    require(Q["x"] == MASK^P["y"] and Q["y"] == MASK^P["x"],"c complement-reverse")
    require(V["x"] == MASK^U["y"] and V["y"] == MASK^U["x"],"b complement-reverse")
    require(P["F"] == 1 << 29 and U["G"] == 1 << 22,"analytic fixture chosen images")
    return {"power_comparisons":comparisons,"surviving_endpoint_triples":survivors,
            "excluded_signed_power_bits":empty,"high_power_certificate":high_certificate,
            "actual_pairs_checked":4,"actual_reverse_boundary":fixture["reverse_boundary_target"]}


def full_pair_gate(fixture,support):
    require(set(map(int,fixture["pairs_by_index"])) == set(support),
            "four-pair fixture omits nine active pairs and is not a complete support model")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",type=Path,default=HERE/"MASK_EXPERIMENT.json")
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    supportpath = ROOT/"supports-v2.json"
    require(digest(supportpath) == SUPPORT_HASH,"support source changed")
    support = json.loads(supportpath.read_text())["supports"][12]
    rows = original_rows(set(support))
    data = json.loads(args.data.read_text())
    require(data["experiment_plan_sha256"] == digest(HERE/"EXPERIMENT_PLAN.md"),"pre-experiment plan hash")
    summary = verify(data)
    negative = []
    for label,damage in [
        ("alter_inverse_column",lambda d:d["f_inverse_basis_hex"].__setitem__(0,"185744e8")),
        ("omit_high_power_stratum",lambda d:d["strata"].pop()),
        ("incorrect_empty_stratum",lambda d:d["empty_power_bits"].pop()),
        ("damage_actual_word",lambda d:d["analytic_conservation_fixture"]["pairs_by_index"]["13"].__setitem__("y",0x290AFDCC)),
        ("damage_actual_G",lambda d:d["analytic_conservation_fixture"]["pairs_by_index"]["29"].__setitem__("G",0)),
    ]:
        altered = copy.deepcopy(data)
        damage(altered)
        try:
            verify(altered)
        except ValueError as error:
            negative.append({"name":label,"rejected":True,"reason":str(error)})
        else:
            raise ValueError("damaged finite evidence accepted: "+label)
    try:
        full_pair_gate(data["analytic_conservation_fixture"],support)
    except ValueError as error:
        negative.append({"name":"promote_local_fixture_to_complete_support", "rejected":True,"reason":str(error)})
    else:
        raise ValueError("partial fixture accepted as a full support")
    output = {"schema":"crypto3-actual-boundary-local-proof-check-v6","status":"PASS",
              "data_sha256":digest(args.data),"checker_sha256":digest(Path(__file__).resolve()),
              "source_support_sha256":SUPPORT_HASH,
              "original_48_row_reduction":{"nonzero_rows":rows,"zero_rows":[t for t in range(16,64) if t not in rows]},
              "verified_summary":summary,"negative_controls":negative,
              "discovery_generator_imported_or_executed":False,
              "scope":"necessary high signed-power stratum exclusion and actual four-pair conservation counterfixture; actual inverse shift remains unresolved",
              "independent_agent_acceptance":False}
    rendered = json.dumps(output,indent=2)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered,end="")


if __name__ == "__main__":
    main()
