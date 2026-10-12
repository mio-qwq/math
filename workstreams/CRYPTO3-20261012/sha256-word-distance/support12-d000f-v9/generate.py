#!/usr/bin/env python3
"""Build and solve the exact fixed-D selected-four-pair CNF.

python-sat/Glucose is used only to produce a DRUP trace.  The frozen
checker is deliberately stdlib-only.
"""

from pathlib import Path
import hashlib
import importlib.metadata
import json
import platform
import time

MASK = (1 << 32) - 1
D = 0x000F0000


def bits(n):
    for packed in range(1 << n):
        yield tuple((packed >> i) & 1 for i in range(n))


class Circuit:
    def __init__(self):
        self.top = 0
        self.clauses = []
        self.groups = {}

    def fresh(self, stem, count=32):
        ans = list(range(self.top + 1, self.top + count + 1))
        self.top += count
        self.groups[stem] = ans
        return ans

    def relation(self, variables, predicate):
        for values in bits(len(variables)):
            if not predicate(values):
                self.clauses.append([
                    -var if value else var
                    for var, value in zip(variables, values)
                ])

    def add_const(self, left, constant, stem):
        right = self.fresh(stem)
        carry = self.fresh(stem + "_carry", 33)
        self.clauses.append([-carry[0]])
        for i in range(32):
            k = (constant >> i) & 1
            self.relation(
                [left[i], carry[i], right[i], carry[i + 1]],
                lambda v, k=k: (v[2], v[3]) ==
                ((v[0] + v[1] + k) & 1, (v[0] + v[1] + k) >> 1),
            )
        return right

    def add_words(self, left, right, stem):
        out = self.fresh(stem)
        carry = self.fresh(stem + "_carry", 33)
        self.clauses.append([-carry[0]])
        for i in range(32):
            self.relation(
                [left[i], right[i], carry[i], out[i], carry[i + 1]],
                lambda v: (v[3], v[4]) ==
                ((v[0] + v[1] + v[2]) & 1,
                 (v[0] + v[1] + v[2]) >> 1),
            )
        return out

    def equal(self, left, right):
        for a, b in zip(left, right):
            self.clauses.extend(([-a, b], [a, -b]))

    def sigma(self, source, rotations, shift, stem):
        out = self.fresh(stem)
        for i in range(32):
            inputs = [source[(i + n) % 32] for n in rotations]
            if i + shift < 32:
                inputs.append(source[i + shift])
            self.relation(
                inputs + [out[i]],
                lambda v: v[-1] == (sum(v[:-1]) & 1),
            )
        return out

    def sigma0(self, source, stem):
        return self.sigma(source, (7, 18), 3, stem)

    def sigma1(self, source, stem):
        return self.sigma(source, (17, 19), 10, stem)


def derivative_context(c, source, name):
    shifted = c.add_const(source, D, name + "_plus_D")
    s0 = c.sigma0(source, name + "_s0")
    s0d = c.sigma0(shifted, name + "_s0D")
    s1 = c.sigma1(source, name + "_s1")
    s1d = c.sigma1(shifted, name + "_s1D")
    return shifted, s0, s0d, s1, s1d


def build():
    """Encode the criterion entirely over 32-bit modular addition."""
    c = Circuit()
    x = c.fresh("x")
    y = c.fresh("y")
    z = c.fresh("z")
    A = c.fresh("A")

    _, x0, x0d, x1, x1d = derivative_context(c, x, "x")
    # A = F_D(x), GX = G_D(x), T = GX + D.
    x0_plus_A = c.add_words(x0, A, "x_s0_plus_A")
    c.equal(x0_plus_A, x0d)
    GX = c.fresh("GX")
    x1_plus_GX = c.add_words(x1, GX, "x_s1_plus_GX")
    c.equal(x1_plus_GX, x1d)
    T = c.add_const(GX, D, "T")

    _, y0, y0d, y1, y1d = derivative_context(c, y, "y")
    # F_D(y)=A and G_D(y)=T+D.
    y0_plus_A = c.add_words(y0, A, "y_s0_plus_A")
    c.equal(y0_plus_A, y0d)
    T_plus_D = c.add_const(T, D, "T_plus_D")
    y1_plus_TD = c.add_words(y1, T_plus_D, "y_s1_plus_TD")
    c.equal(y1_plus_TD, y1d)

    _, z0, z0d, z1, z1d = derivative_context(c, z, "z")
    # F_D(z)=-A and G_D(z)=-T, equivalently endpoint identities.
    z0d_plus_A = c.add_words(z0d, A, "z_s0D_plus_A")
    c.equal(z0d_plus_A, z0)
    z1d_plus_T = c.add_words(z1d, T, "z_s1D_plus_T")
    c.equal(z1d_plus_T, z1)

    return c


def dimacs(c):
    return (f"p cnf {c.top} {len(c.clauses)}\n" +
            "".join(" ".join(map(str, clause)) + " 0\n"
                    for clause in c.clauses)).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    from pysat.solvers import Solver
    import pysolvers

    root = Path(__file__).resolve().parent
    c = build()
    cnf = dimacs(c)
    (root / "fourpair.cnf").write_bytes(cnf)

    started = time.monotonic()
    with Solver(name="glucose4", bootstrap_with=c.clauses,
                with_proof=True) as solver:
        result = solver.solve()
        trace = solver.get_proof()
    elapsed = time.monotonic() - started
    if result is not False or trace is None:
        raise RuntimeError(f"expected proof-producing UNSAT, got {result!r}")

    additions = []
    deletions = 0
    for raw in trace:
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
    (root / "fourpair.drup").write_bytes(proof)

    metadata = {
        "schema": "support12-d000f-selected-four-pair-v9",
        "status": "selected three-pair core UNSAT candidate with deletion-free DRUP certificate",
        "constant_D": f"{D:08x}",
        "criterion": {
            "A": "F_D(x)", "T": "G_D(x)+D",
            "constraints": [
                "F_D(y)=A", "G_D(y)=T+D",
                "F_D(z)=-A", "G_D(z)=-T", "F_A(u)=D",
            ],
        },
        "encoded_necessary_subsystem": [
            "A=F_D(x)", "T=G_D(x)+D",
            "F_D(y)=A", "G_D(y)=T+D",
            "F_D(z)=-A", "G_D(z)=-T",
        ],
        "implication": (
            "UNSAT of the encoded selected three-pair core implies UNSAT of "
            "the full selected four-pair criterion, whose additional condition "
            "is F_A(u)=D"
        ),
        "cnf": {"variables": c.top, "clauses": len(c.clauses),
                "sha256": digest(cnf)},
        "proof": {"format": "deletion-free DRUP",
                  "added_clauses": len(additions),
                  "discarded_deletion_lines": deletions,
                  "sha256": digest(proof)},
        "groups": c.groups,
        "runtime": {
            "python": platform.python_version(),
            "python_sat": importlib.metadata.version("python-sat"),
            "solver": "Glucose4 bundled by python-sat (proof generation only)",
            "seconds": elapsed,
            "command": (
                "PYTHONPATH=/workspace/scratch/b1d6bae025af/crypto3-deps "
                "python -B workstreams/CRYPTO3-20261012/sha256-word-distance/"
                "support12-d000f-v9/generate.py"
            ),
            "solver_binary": str(Path(pysolvers.__file__)),
            "solver_binary_sha256": digest(Path(pysolvers.__file__).read_bytes()),
        },
        "source_sha256": {
            "generate.py": digest(Path(__file__).read_bytes()),
            "check.py": digest((root / "check.py").read_bytes()),
        },
        "scope": (
            "fixed D selected four-pair local system only; not the complete "
            "support-12 factor graph and not a SHA-256 message pair"
        ),
    }
    (root / "CERTIFICATE.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"result": result, "seconds": elapsed,
                      "cnf": metadata["cnf"], "proof": metadata["proof"]},
                     sort_keys=True))


if __name__ == "__main__":
    main()
