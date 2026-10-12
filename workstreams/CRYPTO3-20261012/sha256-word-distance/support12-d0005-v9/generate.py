#!/usr/bin/env python3
"""Generate the fixed-D reciprocal sigma0 CNF and a DRUP proof.

The only non-stdlib dependency is python-sat, used solely as the proof-
producing solver.  ``check.py`` does not import it.
"""

from pathlib import Path
import hashlib
import importlib.metadata
import json
import platform

MASK = (1 << 32) - 1
D = 0x00050000
A = 0x40406E02
T = 0x1FFD913E


class Builder:
    def __init__(self):
        self.nvars = 0
        self.names = {}
        self.clauses = []

    def vars(self, stem, count):
        out = []
        for i in range(count):
            self.nvars += 1
            self.names[f"{stem}{i}"] = self.nvars
            out.append(self.nvars)
        return out

    def forbid(self, variables, values):
        # Clause false on exactly the supplied Boolean assignment.
        self.clauses.append([(-v if b else v) for v, b in zip(variables, values)])

    def relation(self, variables, predicate):
        for bits in product_bits(len(variables)):
            if not predicate(*bits):
                self.forbid(variables, bits)


def product_bits(n):
    for value in range(1 << n):
        yield tuple((value >> i) & 1 for i in range(n))


def bit(value, i):
    return (value >> i) & 1


def add_constant(builder, source, constant, stem):
    """Return bits for source+constant mod 2^32, with ripple carries."""
    target = builder.vars(stem, 32)
    carries = builder.vars(stem + "carry", 33)
    builder.clauses.append([-carries[0]])
    for i in range(32):
        k = bit(constant, i)

        def full(x, c, y, cn, k=k):
            total = x + c + k
            return y == (total & 1) and cn == (total >> 1)

        builder.relation([source[i], carries[i], target[i], carries[i + 1]], full)
    return target, carries


def xor_output(builder, inputs, output):
    def parity(*values):
        return values[-1] == (sum(values[:-1]) & 1)

    builder.relation(list(inputs) + [output], parity)


def sigma_bits(builder, source, stem, rotations, shift):
    out = builder.vars(stem, 32)
    for i in range(32):
        inputs = [source[(i + r) % 32] for r in rotations]
        if i + shift < 32:
            inputs.append(source[i + shift])
        xor_output(builder, inputs, out[i])
    return out


def equate(builder, left, right):
    for u, v in zip(left, right):
        builder.clauses.append([-u, v])
        builder.clauses.append([u, -v])


def build_reciprocal():
    b = Builder()
    x = b.vars("x", 32)
    y, carry_a = add_constant(b, x, A, "y")
    sx = sigma_bits(b, x, "sx", (7, 18), 3)
    sy = sigma_bits(b, y, "sy", (7, 18), 3)
    sx_plus_d, carry_d = add_constant(b, sx, D, "sd")
    equate(b, sx_plus_d, sy)
    return b, {
        "x": x, "y": y, "sigma0_x": sx, "sigma0_y": sy,
        "carry_A": carry_a, "sigma0_x_plus_D": sx_plus_d,
        "carry_D": carry_d,
    }


def build_third_image():
    b = Builder()
    x = b.vars("x", 32)
    y, carry_d = add_constant(b, x, D, "y")
    sx = sigma_bits(b, x, "sx", (7, 18), 3)
    sy = sigma_bits(b, y, "sy", (7, 18), 3)
    gx = sigma_bits(b, x, "gx", (17, 19), 10)
    gy = sigma_bits(b, y, "gy", (17, 19), 10)
    sx_target, carry_f = add_constant(b, sx, (-A) & MASK, "sf")
    gx_target, carry_g = add_constant(b, gx, (-T) & MASK, "gt")
    equate(b, sx_target, sy)
    equate(b, gx_target, gy)
    return b, {
        "x": x, "y": y, "sigma0_x": sx, "sigma0_y": sy,
        "sigma1_x": gx, "sigma1_y": gy, "carry_D": carry_d,
        "sigma0_x_minus_A": sx_target, "carry_minus_A": carry_f,
        "sigma1_x_minus_T": gx_target, "carry_minus_T": carry_g,
    }


def dimacs(builder):
    lines = [f"p cnf {builder.nvars} {len(builder.clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in builder.clauses)
    return "\n".join(lines) + "\n"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def emit_unsat(root, stem, builder):
    from pysat.solvers import Solver

    cnf_data = dimacs(builder).encode()
    (root / f"{stem}.cnf").write_bytes(cnf_data)

    # Glucose emits a deletion-free DRUP trace through python-sat.
    with Solver(name="glucose4", bootstrap_with=builder.clauses,
                with_proof=True) as solver:
        sat = solver.solve()
        proof_lines = solver.get_proof()
    if sat is not False or proof_lines is None:
        raise RuntimeError("expected proof-producing UNSAT")
    normalized = []
    deletion_lines = 0
    for line in proof_lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("d "):
            deletion_lines += 1
            continue
        if not line.endswith(" 0") and line != "0":
            line += " 0"
        normalized.append(line)
    proof_data = ("\n".join(normalized) + "\n").encode()
    (root / f"{stem}.drup").write_bytes(proof_data)
    return {
        "cnf": {"variables": builder.nvars, "clauses": len(builder.clauses),
                "sha256": sha256(cnf_data)},
        "proof": {"format": "deletion-free DRUP",
                  "added_clauses": len(normalized),
                  "discarded_deletion_lines": deletion_lines,
                  "sha256": sha256(proof_data)},
    }


def main():
    root = Path(__file__).resolve().parent
    reciprocal, reciprocal_groups = build_reciprocal()
    third, third_groups = build_third_image()
    reciprocal_record = emit_unsat(root, "reciprocal", reciprocal)
    third_record = emit_unsat(root, "third_image", third)

    metadata = {
        "schema": "support12-d0005-reciprocal-v9",
        "status": "two UNSAT claims with independently checked DRUP certificates",
        "constants": {"D": f"{D:08x}", "A": f"{A:08x}",
                      "T": f"{T:08x}"},
        "claims": {
            "reciprocal": {
                "meaning": "no x has sigma0(x+A)-sigma0(x)=D modulo 2^32",
                **reciprocal_record,
                "variable_groups": reciprocal_groups,
            },
            "third_image": {
                "meaning": (
                    "no x has d=D, sigma0 derivative=-A and "
                    "sigma1 derivative=-T modulo 2^32"
                ),
                **third_record,
                "variable_groups": third_groups,
            },
        },
        "runtime": {
            "python": platform.python_version(),
            "python_sat": importlib.metadata.version("python-sat"),
            "solver": "Glucose4 bundled by python-sat (proof generation only)",
            "command": (
                "PYTHONPATH=/workspace/scratch/b1d6bae025af/crypto3-deps "
                "python -B workstreams/CRYPTO3-20261012/sha256-word-distance/"
                "support12-d0005-v9/generate.py"
            ),
        },
        "source_sha256": {
            "generate.py": sha256(Path(__file__).read_bytes()),
            "check.py": sha256((root / "check.py").read_bytes()),
        },
    }
    (root / "CERTIFICATE.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": metadata["status"],
                      "reciprocal": reciprocal_record,
                      "third_image": third_record}, sort_keys=True))


if __name__ == "__main__":
    main()
