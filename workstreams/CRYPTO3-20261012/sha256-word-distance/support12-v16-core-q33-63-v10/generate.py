#!/usr/bin/env python3
"""Generate exact selected-three-pair CNFs and deletion-free DRUP traces."""

import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import platform
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "support12-v16-core-batch-v9" / "generate.py"
BASE_SHA256 = "475bb1171d77ba2fd957f50025c335e4fdf7ee8d7bab2b86f7fcf9cd6055c3a0"
QS = tuple(range(33, 64, 2))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_base():
    if digest(BASE.read_bytes()) != BASE_SHA256:
        raise AssertionError("frozen circuit generator changed")
    spec = importlib.util.spec_from_file_location("v16_core_base", BASE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    from pysat.solvers import Solver
    import pysolvers

    base = load_base()
    records = {}
    for q in QS:
        delta = q << 16
        tag = f"d{q:04x}"
        circuit = base.build(delta)
        cnf = base.dimacs(circuit)
        (HERE / f"{tag}.cnf").write_bytes(cnf)
        started = time.monotonic()
        with Solver(name="glucose4", bootstrap_with=circuit.clauses,
                    with_proof=True) as solver:
            result = solver.solve()
            raw_proof = solver.get_proof()
        seconds = time.monotonic() - started
        record = {
            "q": q,
            "D": f"{delta:08x}",
            "cnf": {"variables": circuit.top,
                    "clauses": len(circuit.clauses),
                    "sha256": digest(cnf)},
            "solver_seconds": seconds,
        }
        if result is False and raw_proof is not None:
            additions, deletions = [], 0
            for raw in raw_proof:
                line = raw.strip()
                if not line:
                    continue
                if line.startswith("d "):
                    deletions += 1
                    continue
                if line != "0" and not line.endswith(" 0"):
                    line += " 0"
                additions.append(line)
            proof = ("\n".join(additions) + "\n").encode()
            (HERE / f"{tag}.drup").write_bytes(proof)
            record.update({
                "status": "UNSAT candidate; DRUP generated",
                "proof": {"format": "deletion-free DRUP",
                          "added_clauses": len(additions),
                          "discarded_deletion_lines": deletions,
                          "sha256": digest(proof)},
            })
        else:
            record["status"] = "UNKNOWN: no checkable proof generated"
            record["solver_result_discovery_only"] = str(result)
        records[str(q)] = record
    complete = all("proof" in row for row in records.values())
    meta = {
        "schema": "support12-v16-selected-core-q33-63-v10",
        "status": ("all sixteen author proof candidates generated" if complete
                   else "partial; one or more q values UNKNOWN"),
        "q_values": list(QS),
        "definition": {
            "D": "q*2^16", "A": "F_D(x)", "T": "G_D(x)+D",
            "encoded_constraints": ["F_D(y)=A", "G_D(y)=T+D",
                                    "F_D(z)=-A", "G_D(z)=-T"],
        },
        "records": records,
        "runtime": {
            "python": platform.python_version(),
            "python_sat": importlib.metadata.version("python-sat"),
            "solver": "Glucose4 bundled by python-sat; generation only",
            "solver_binary": str(Path(pysolvers.__file__)),
            "solver_binary_sha256": digest(Path(pysolvers.__file__).read_bytes()),
            "command": ("PYTHONPATH=/workspace/scratch/b1d6bae025af/crypto3-deps "
                        "python -B workstreams/CRYPTO3-20261012/sha256-word-distance/"
                        "support12-v16-core-q37-43-v10/generate.py"),
        },
        "source_sha256": {"generate.py": digest(Path(__file__).read_bytes()),
                          "base_generate.py": BASE_SHA256},
        "scope": ("sixteen fixed D values in a selected local subsystem only; "
                  "not all v2(D)=16, not the complete support-12 graph, and "
                  "not messages"),
    }
    (HERE / "CERTIFICATE.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": meta["status"], "records": records},
                     sort_keys=True))


if __name__ == "__main__":
    main()
