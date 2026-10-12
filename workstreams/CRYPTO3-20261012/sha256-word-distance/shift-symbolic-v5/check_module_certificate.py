#!/usr/bin/env python3
"""Direct integer certificate checker; no elimination or builder import."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HASH = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"
MOD = 1 << 32


def require(condition,message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def original_matrix(support):
    variables = [[tag,j] for tag in ("d","F","G") for j in support]
    rows = []
    for t in range(16,64):
        full = {("d",t):1,("G",t-2):-1,("d",t-7):-1,("F",t-15):-1,("d",t-16):-1}
        rows.append([full.get(tuple(variable),0) for variable in variables])
    return variables,rows


def apply_operations(matrix,operations):
    value = [row[:] for row in matrix]
    for operation in operations:
        kind,*arguments = operation
        if kind == "swap":
            a,b = arguments
            require(0 <= a < 48 and 0 <= b < 48,"swap indices")
            value[a],value[b] = value[b],value[a]
        elif kind == "negate":
            (row,) = arguments
            require(0 <= row < 48,"negation index")
            value[row] = [-x for x in value[row]]
        elif kind == "add":
            target,source,factor = arguments
            require(0 <= target < 48 and 0 <= source < 48 and target != source,"row-add indices")
            require(isinstance(factor,int),"integer row addition")
            value[target] = [a + factor*b for a,b in zip(value[target],value[source])]
        else:
            raise ValueError("invalid elementary row operation")
    return value


def check_object(item,supports):
    sid = item["support_index"]
    require(sid in (9,12),"unexpected support")
    support = supports[sid]
    require(item["support"] == support,"support mismatch")
    variables,A = original_matrix(support)
    require(item["variables"] == variables,"variables mismatch")
    require(item["original_rows"] == A,"original recurrence row mismatch")
    require(item["original_recurrence_indices"] == list(range(16,64)),"incomplete original rows")
    operations = item["unit_row_operations"]
    R = apply_operations(A,operations)
    require(R == item["transformed_rows"],"row operation result mismatch")
    identity = [[int(i == j) for j in range(48)] for i in range(48)]
    U = apply_operations(identity,operations)
    require(U == item["integer_row_transform"],"transform matrix mismatch")
    # A second direct product check does not rely on the operation replay.
    require([[sum(U[r][k]*A[k][c] for k in range(48)) for c in range(39)] for r in range(48)] == R,
            "direct product U*A mismatch")
    pivots = item["pivot_columns"]
    require(pivots == sorted(set(pivots)),"pivot order")
    rank = len(pivots)
    require(item["integer_rank"] == rank,"rank mismatch")
    require(all(not any(row) for row in R[rank:]),"unprocessed nonzero rows")
    require(all(R[r][column] == int(r == j) for r in range(48) for j,column in enumerate(pivots)),
            "pivot columns are not unit identity")
    free = [j for j in range(39) if j not in pivots]
    require(item["free_columns"] == free,"free columns mismatch")
    target = [int(variable == ["d",15])-int(variable == (["d",8] if sid == 9 else ["G",13]))
              for variable in variables]
    require(item["boundary_target"] == target,"boundary target mismatch")
    residual = item["reduced_boundary_residual"]
    require(len(residual) == 39 and any(residual),"empty or malformed residual")
    require(all(residual[j] == 0 for j in pivots),"nonreduced residual")
    combination = item["target_minus_residual_original_row_combination"]
    require(len(combination) == 48,"row combination length")
    require([sum(combination[r]*A[r][j] for r in range(48)) for j in range(39)]
            == [target[j]-residual[j] for j in range(39)],"target residual row identity mismatch")
    require(item["boundary_residual_terms"] == [[*variables[j],c] for j,c in enumerate(residual) if c],
            "printed residual terms mismatch")
    integer_model = item["witness_integer_values"]
    model = item["witness_mod32_values"]
    require(len(integer_model) == len(model) == 39,"interface witness length")
    require([x % MOD for x in integer_model] == model,"integer versus modular witness mismatch")
    require(all(x != 0 for x in model),"active interface has zero value")
    require(all(dot(row,integer_model) == 0 for row in A),"integer witness violates a recurrence")
    require(all(dot(row,model) % MOD == 0 for row in A),"modular witness violates a recurrence")
    boundary = dot(target,model) % MOD
    require(boundary != 0,"witness does not separate boundary target")
    require(item["witness_boundary_integer"] == dot(target,integer_model),"integer boundary mismatch")
    require(item["witness_boundary_mod32"] == boundary,"modular boundary mismatch")
    # A separating witness proves nonmembership even without trusting elimination.
    require(dot(residual,model) % MOD == boundary,"residual does not separate")
    return {"support":sid,"rows":48,"variables":39,"unit_rank":rank,
            "free_variables":len(free),"boundary_residual_terms":item["boundary_residual_terms"],
            "separating_boundary":boundary,"all_39_active_interfaces_nonzero":True,
            "nonmembership_over_integers_and_mod32":True}


def negative_controls(data,supports):
    checks = []
    for label,damage in [
        ("alter_original_row",lambda o: o["original_rows"][0].__setitem__(0,o["original_rows"][0][0]+1)),
        ("alter_transform",lambda o: o["integer_row_transform"][0].__setitem__(0,o["integer_row_transform"][0][0]+1)),
        ("alter_residual_identity",lambda o: o["target_minus_residual_original_row_combination"].__setitem__(0,o["target_minus_residual_original_row_combination"][0]+1)),
        ("zero_active_interface",lambda o: o["witness_mod32_values"].__setitem__(0,0)),
        ("alter_boundary_target",lambda o: o["boundary_target"].__setitem__(0,1)),
    ]:
        item = copy.deepcopy(data["objects"][0])
        damage(item)
        try:
            check_object(item,supports)
        except ValueError as error:
            checks.append({"name":label,"rejected":True,"reason":str(error)})
        else:
            raise ValueError("damaged certificate accepted: "+label)
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate",type=Path,default=HERE/"MODULE_CERTIFICATE.json")
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    supportpath = ROOT/"supports-v2.json"
    require(digest(supportpath) == HASH,"support source changed")
    supports = json.loads(supportpath.read_text())["supports"]
    data = json.loads(args.certificate.read_text())
    require(data["source_support_sha256"] == HASH,"certificate support hash")
    require(data["modulus"] == MOD,"wrong modulus")
    require([x["support_index"] for x in data["objects"]] == [9,12],"object coverage")
    summary = [check_object(item,supports) for item in data["objects"]]
    result = {"schema":"crypto3-backward-boundary-module-check-v5",
              "status":"PASS","source_support_sha256":HASH,
              "certificate_sha256":digest(args.certificate),
              "checker_sha256":digest(Path(__file__).resolve()),
              "objects":summary,"negative_controls":negative_controls(data,supports),
              "builder_imported_or_executed":False,
              "frozen_v4_modified":False,
              "scope":"Exact linear-module nonmembership only. Actual word-pair derivative coupling and inverse time-shift truth remain unresolved.",
              "review_status":"new researcher-authored candidate, not independent-agent mathematical acceptance"}
    rendered = json.dumps(result,indent=2)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered,end="")


if __name__ == "__main__":
    main()
