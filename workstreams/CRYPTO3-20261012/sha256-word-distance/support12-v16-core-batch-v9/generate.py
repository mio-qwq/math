#!/usr/bin/env python3
"""Generate fixed-D selected-three-pair CNFs and Glucose DRUP traces."""

from pathlib import Path
import hashlib
import importlib.metadata
import json
import platform
import time

QS = (5, 13, 21, 23, 25, 27)


class Circuit:
    def __init__(self, delta):
        self.delta = delta
        self.top = 0
        self.clauses = []

    def fresh(self, count=32):
        result = list(range(self.top + 1, self.top + count + 1))
        self.top += count
        return result

    def relation(self, variables, accepts):
        for packed in range(1 << len(variables)):
            values = tuple((packed >> i) & 1 for i in range(len(variables)))
            if not accepts(values):
                self.clauses.append([
                    -variable if value else variable
                    for variable, value in zip(variables, values)
                ])

    def add_const(self, source, constant):
        target, carry = self.fresh(), self.fresh(33)
        self.clauses.append([-carry[0]])
        for i in range(32):
            k = (constant >> i) & 1
            self.relation(
                [source[i], carry[i], target[i], carry[i + 1]],
                lambda v, k=k: (v[2], v[3]) ==
                ((v[0] + v[1] + k) & 1, (v[0] + v[1] + k) >> 1),
            )
        return target

    def add_word(self, left, right):
        target, carry = self.fresh(), self.fresh(33)
        self.clauses.append([-carry[0]])
        for i in range(32):
            self.relation(
                [left[i], right[i], carry[i], target[i], carry[i + 1]],
                lambda v: (v[3], v[4]) ==
                ((v[0] + v[1] + v[2]) & 1,
                 (v[0] + v[1] + v[2]) >> 1),
            )
        return target

    def equal(self, left, right):
        for a, b in zip(left, right):
            self.clauses.extend(([-a, b], [a, -b]))

    def sigma(self, source, rotations, shift):
        target = self.fresh()
        for i in range(32):
            inputs = [source[(i + r) % 32] for r in rotations]
            if i + shift < 32:
                inputs.append(source[i + shift])
            self.relation(
                inputs + [target[i]],
                lambda v: v[-1] == (sum(v[:-1]) & 1),
            )
        return target

    def context(self, source):
        shifted = self.add_const(source, self.delta)
        return (self.sigma(source, (7, 18), 3),
                self.sigma(shifted, (7, 18), 3),
                self.sigma(source, (17, 19), 10),
                self.sigma(shifted, (17, 19), 10))


def build(delta):
    c = Circuit(delta)
    x, y, z, A = c.fresh(), c.fresh(), c.fresh(), c.fresh()
    x0, x0d, x1, x1d = c.context(x)
    word = c.add_word(x0, A)
    c.equal(word, x0d)
    GX = c.fresh()
    word = c.add_word(x1, GX)
    c.equal(word, x1d)
    T = c.add_const(GX, delta)

    y0, y0d, y1, y1d = c.context(y)
    word = c.add_word(y0, A)
    c.equal(word, y0d)
    TD = c.add_const(T, delta)
    word = c.add_word(y1, TD)
    c.equal(word, y1d)

    z0, z0d, z1, z1d = c.context(z)
    word = c.add_word(z0d, A)
    c.equal(word, z0)
    word = c.add_word(z1d, T)
    c.equal(word, z1)
    return c


def dimacs(circuit):
    return (f"p cnf {circuit.top} {len(circuit.clauses)}\n" +
            "".join(" ".join(map(str, clause)) + " 0\n"
                    for clause in circuit.clauses)).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    from pysat.solvers import Solver
    import pysolvers

    root = Path(__file__).resolve().parent
    records = {}
    for q in QS:
        delta = q << 16
        tag = f"d{q:04x}"
        circuit = build(delta)
        cnf = dimacs(circuit)
        (root / f"{tag}.cnf").write_bytes(cnf)
        started = time.monotonic()
        with Solver(name="glucose4", bootstrap_with=circuit.clauses,
                    with_proof=True) as solver:
            result = solver.solve()
            raw_proof = solver.get_proof()
        seconds = time.monotonic() - started
        record = {
            "q": q,
            "D": f"{delta:08x}",
            "cnf": {"variables": circuit.top, "clauses": len(circuit.clauses),
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
            (root / f"{tag}.drup").write_bytes(proof)
            record.update({
                "status": "UNSAT candidate; DRUP generated",
                "proof": {"format": "deletion-free DRUP",
                          "added_clauses": len(additions),
                          "discarded_deletion_lines": deletions,
                          "sha256": digest(proof)},
            })
        else:
            record["status"] = "UNKNOWN: no independently checkable proof generated"
            record["solver_result_discovery_only"] = str(result)
        records[str(q)] = record

    complete = all("proof" in record for record in records.values())
    meta = {
        "schema": "support12-v16-selected-core-batch-v9",
        "status": ("all six author proof candidates generated" if complete else
                   "partial; one or more q values UNKNOWN"),
        "q_values": list(QS),
        "definition": {
            "D": "q*2^16",
            "A": "F_D(x)",
            "T": "G_D(x)+D",
            "encoded_constraints": [
                "F_D(y)=A", "G_D(y)=T+D",
                "F_D(z)=-A", "G_D(z)=-T",
            ],
        },
        "implication": (
            "each certified core exclusion also excludes its fixed-D selected "
            "four-pair criterion after adding F_A(u)=D"
        ),
        "records": records,
        "runtime": {
            "python": platform.python_version(),
            "python_sat": importlib.metadata.version("python-sat"),
            "solver": "Glucose4 bundled by python-sat; generation only",
            "solver_binary": str(Path(pysolvers.__file__)),
            "solver_binary_sha256": digest(Path(pysolvers.__file__).read_bytes()),
            "command": (
                "PYTHONPATH=/workspace/scratch/b1d6bae025af/crypto3-deps "
                "python -B workstreams/CRYPTO3-20261012/sha256-word-distance/"
                "support12-v16-core-batch-v9/generate.py"
            ),
        },
        "source_sha256": {
            "generate.py": digest(Path(__file__).read_bytes()),
            "check.py": digest((root / "check.py").read_bytes()),
        },
        "scope": (
            "six fixed D values in a selected local subsystem only; not all "
            "v2(D)=16, not the complete support-12 graph, and not messages"
        ),
    }
    (root / "CERTIFICATE.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": meta["status"], "records": records},
                     sort_keys=True))


if __name__ == "__main__":
    main()
