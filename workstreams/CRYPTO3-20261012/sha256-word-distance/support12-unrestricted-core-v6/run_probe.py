#!/usr/bin/env python3
"""A single unrestricted exact QF_BV probe; writes into a new output directory."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import time
import z3

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    words = {name: z3.BitVec(name, 32) for name in ("x", "xp", "y", "yp", "r", "rp")}
    def f(word):
        return z3.RotateRight(word, 7) ^ z3.RotateRight(word, 18) ^ z3.LShR(word, 3)
    def g(word):
        return z3.RotateRight(word, 17) ^ z3.RotateRight(word, 19) ^ z3.LShR(word, 10)
    d = words["xp"] - words["x"]
    fx, fy, fr = [f(words[a+"p"]) - f(words[a]) for a in ("x", "y", "r")]
    gx, gy, gr = [g(words[a+"p"]) - g(words[a]) for a in ("x", "y", "r")]
    equations = [d != 0, words["yp"]-words["y"] == d,
                 words["rp"]-words["r"] == -d, fx == fy, fx == fr,
                 gy-gx == d+d, gy-gr == d]
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=15000)
    solver.add(*equations)
    smt = solver.to_smt2()
    (args.out_dir / "MODEL.smt2").write_text(smt, encoding="utf-8")
    began = datetime.now(timezone.utc).isoformat()
    clock = time.perf_counter()
    answer = solver.check()  # Exactly one check call; no retry or seed sweep.
    elapsed = time.perf_counter()-clock
    result = {"schema": "CRYPTO3-unrestricted-actual-three-pair-probe-v6",
              "object": "Actual six-word necessary local core only; no base schedule.",
              "solver_result": str(answer), "accepted_conclusion": None,
              "started_utc": began, "ended_utc": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": elapsed, "timeout_ms": 15000,
              "solver_check_calls": 1, "logic": "QF_BV", "solver": "Z3",
              "z3_version": z3.get_version_string(), "z3_full_version": z3.get_full_version(),
              "python_version": platform.python_version(),
              "z3_python_module": str(Path(z3.__file__).resolve()),
              "z3_python_module_sha256": digest(Path(z3.__file__)),
              "model_smt2_sha256": digest(args.out_dir / "MODEL.smt2"),
              "probe_script_sha256": digest(Path(__file__)),
              "plan_sha256": digest(HERE / "PLAN.md"),
              "verifier_script_sha256": digest(HERE / "verify_model.py"),
              "named_word_variables": list(words), "raw_free_bits": 192,
              "nonzero_constraint": "xp-x != 0", "assertions": 7,
              "statistics": str(solver.statistics())}
    if answer == z3.sat:
        model = solver.model()
        values = {name: model.eval(word, model_completion=True).as_long()
                  for name, word in words.items()}
        witness = {"schema": "CRYPTO3-actual-three-pair-model-v6",
                   "words": values, "derived_D": (values["xp"]-values["x"]) % (1 << 32),
                   "scope": "Solver candidate requiring independent arithmetic verification; not a schedule."}
        (args.out_dir / "MODEL.json").write_text(json.dumps(witness, indent=2, sort_keys=True)+"\n")
        result["model_json_sha256"] = digest(args.out_dir / "MODEL.json")
        result["acceptance_state"] = "SAT candidate; separate direct arithmetic verification required."
    elif answer == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
        result["acceptance_state"] = "Unresolved. No extension, repeat query, or seed sweep."
    else:
        result["acceptance_state"] = "Unverified solver UNSAT; no independently checked certificate."
        result["proof_certificate"] = None
    (args.out_dir / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
