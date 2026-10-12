#!/usr/bin/env python3
"""Deterministic symbolic audit of the support-12 18-word normal form.

The core checks are universal term identities in the additive word algebra.
The frozen v10 seeded run is replayed only as a separately labelled auxiliary
transcription test; it is not used to establish any identity.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MOD = 1 << 32

REFERENCES = {
    "support12-full-factor-v9/PROOF.md":
        "efba27236a949965e8689462703b4ed675a0484c0c5a84302b621c59d9bd0395",
    "support12-full-factor-v9/manifest.json":
        "a0438580b430fdd031cecd0ea07c87363c5c942f5f8fc3848864ba1a51ae6b98",
    "support12-full-factor-review-v8/REVIEW_V9.md":
        "04cd55432d18f2abb3dbca2d16f651ceb4451ac550048c5b0e84db4c82da63e8",
    "support12-base-lift-v8/PROOF.md":
        "40305b2a0ec9dc1d5776626cbde09cbaddb857cc24e627f6dabec20c7ee4ab3a",
    "support12-base-lift-v8/base_completion.py":
        "ffb18eab959097258633a69fbc23556d0f3fbf09bc80cf4d0deefc0fe7d89365",
    "support12-base-lift-v8/SHA256.json":
        "374732f8fee671cd7290d7596ab7f0cb85bb83502b3c94a124d7a78280802dc6",
    "support12-base-review-v8/REVIEW.md":
        "8c3ab0fb544c487e065316149fcf791630062aea5bc359a3ead53f748e033527",
    "support12-base-residual-v9/PROOF.md":
        "d9fcb05b5bd21bd7b34fd16fdd6df61c9d6a351dc4b83bd63b6d1b91c5dc808c",
    "support12-base-residual-v9/SHA256.json":
        "cbdfa2fd8d76c4e7bc511f10c30d15b43763144dfd1eac6fff758e1d5ee6546f",
    "support12-base-residual-review-v9/REVIEW.md":
        "92017f34d561a9db3a4220c1c1f67fff429b54ff378ef3134cc900b239330cf0",
    "support12-base-residual-review-v9/SHA256.json":
        "1ee4aa1318a6306dfc23c4f56426824f9d49eb87f0808adcd8a74058d36838a1",
    "support12-base-factor-normal-v10/CANDIDATE.md":
        "4a6ddf2d14ab042af43e8d4c66fbcea02487c92badae0ef8573c4c4ff0b6888b",
    "support12-base-factor-normal-v10/verify_candidate.py":
        "15248aa67277df653d4383e27d8437d218cb1c1b2d915da8d27ded4d41b8c124",
    "support12-base-factor-normal-v10/RUN.json":
        "409e57b7aac5f3e2485c7027318c6532a35275a951222455bf74777647658139",
    "support12-base-factor-normal-v10/SHA256.json":
        "9c780d8164782c0a8bb7e6efc159d1ac01fe27fe9df6d2bb020b2470b3b6a7ea",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze_key(value):
    if isinstance(value, tuple):
        return [freeze_key(item) for item in value]
    return value


@dataclass(frozen=True)
class Expr:
    """Canonical finite Z/(2^32)-linear combination of normalized atoms."""

    terms: tuple

    @staticmethod
    def from_dict(data):
        cleaned = tuple(sorted(
            ((term, coefficient % MOD) for term, coefficient in data.items()
             if coefficient % MOD),
            key=lambda item: repr(item[0]),
        ))
        return Expr(cleaned)

    def as_dict(self):
        return dict(self.terms)

    def __add__(self, other):
        other = coerce(other)
        data = self.as_dict()
        for term, coefficient in other.terms:
            data[term] = (data.get(term, 0) + coefficient) % MOD
        return Expr.from_dict(data)

    def __sub__(self, other):
        return self + (-coerce(other))

    def __neg__(self):
        return Expr.from_dict({term: -coefficient for term, coefficient in self.terms})

    def serial(self):
        return [[freeze_key(term), coefficient] for term, coefficient in self.terms]


ZERO = Expr(())


def coerce(value):
    if isinstance(value, Expr):
        return value
    if isinstance(value, int):
        return Expr.from_dict({("const",): value}) if value % MOD else ZERO
    raise TypeError(value)


def var(name):
    return Expr.from_dict({("var", name): 1})


def fn(name, *arguments):
    normalized = tuple(tuple(argument.terms) for argument in map(coerce, arguments))
    return Expr.from_dict({("fn", name, normalized): 1})


def D0(x, d):
    return fn("D0", x, d)


def D1(x, d):
    return fn("D1", x, d)


def S0(x):
    return fn("sigma0", x)


def S1(x):
    return fn("sigma1", x)


def I0(x):
    return fn("inverse_sigma0", x)


def I1(x):
    return fn("inverse_sigma1", x)


def contains(expr, variable_name):
    needle = ("var", variable_name)

    def visit_term(term):
        if term == needle:
            return True
        if term and term[0] == "fn":
            return any(visit_expr(Expr(arguments)) for arguments in term[2])
        return False

    def visit_expr(value):
        return any(visit_term(term) for term, _ in value.terms)

    return visit_expr(expr)


def substitute(expr, mapping):
    def sub_term(term):
        if term[0] == "var" and term[1] in mapping:
            return mapping[term[1]]
        if term[0] == "fn":
            args = [substitute(Expr(arguments), mapping) for arguments in term[2]]
            return fn(term[1], *args)
        return Expr.from_dict({term: 1})

    result = ZERO
    for term, coefficient in expr.terms:
        atom = sub_term(term)
        for _ in range(coefficient if coefficient < 8 else 0):
            result = result + atom
        if coefficient >= 8:
            result = result + Expr.from_dict(
                {key: coefficient * value for key, value in atom.terms}
            )
    return result


def load_base():
    path = ROOT / "support12-base-lift-v8" / "base_completion.py"
    spec = importlib.util.spec_from_file_location("frozen_base_v8", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def derive_values(x):
    A = var("A")
    B = -D0(x[10], A)
    C = -D1(x[43], -B)
    K = -D1(x[29], C)
    P = D0(x[11], B)
    Q = D0(x[13], C)
    L = D0(x[15], K)
    S = D1(x[26], P + A)
    W = D0(x[29], C)
    Z = D0(x[42], P + A)
    return dict(A=A, B=B, C=C, K=K, P=P, Q=Q, L=L, S=S, W=W, Z=Z)


def factor_residuals(v, x, H):
    A, B, C, K = (v[name] for name in ("A", "B", "C", "K"))
    P, Q, L, S, W, Z = (v[name] for name in ("P", "Q", "L", "S", "W", "Z"))
    return {
        "10F": D0(x[10], A) + B,
        "11F": D0(x[11], B) - P,
        "13F": D0(x[13], C) - Q,
        "15F": D0(x[15], K) - L,
        "15G": D1(x[15], K) + A,
        "18F": D0(x[18], B) + P + A,
        "18G": D1(x[18], B) + B + C,
        "20F": D0(x[20], -B) + Q + S,
        "20G": D1(x[20], -B) + K,
        "26F": D0(x[26], P + A) + B,
        "26G": D1(x[26], P + A) - S,
        "28F": D0(x[28], Q + S) + B,
        "28G": D1(x[28], Q + S) + L,
        "29F": D0(x[29], C) - W,
        "29G": D1(x[29], C) + K,
        "34F": D0(x[34], B) + P + A,
        "34G": D1(x[34], B) - B + C,
        "42F": D0(x[42], P + A) - Z,
        "42G": D1(x[42], P + A) + W + Q + S,
        "43F": D0(x[43], -B) + P + A,
        "43G": D1(x[43], -B) + C,
        "57G": D1(H, Z) - B,
    }


def reduced_residuals(v, x, H):
    """Build the thirteen displayed NF equations independently."""
    A, B, C, K = (v[name] for name in ("A", "B", "C", "K"))
    P, Q, L, S, W, Z = (v[name] for name in ("P", "Q", "L", "S", "W", "Z"))
    return {
        "15G": D1(x[15], K) + A,
        "18F": D0(x[18], B) + P + A,
        "18G": D1(x[18], B) + B + C,
        "20F": D0(x[20], -B) + Q + S,
        "20G": D1(x[20], -B) + K,
        "26F": D0(x[26], P + A) + B,
        "28F": D0(x[28], Q + S) + B,
        "28G": D1(x[28], Q + S) + L,
        "34F": D0(x[34], B) + P + A,
        "34G": D1(x[34], B) - B + C,
        "42G": D1(x[42], P + A) + W + Q + S,
        "43F": D0(x[43], -B) + P + A,
        "57G": D1(H, Z) - B,
    }


def symbolic_base_chart(base):
    support = tuple(base.SUPPORT)
    parameters = tuple(base.PARAMETERS)
    words = [None] * 64
    for index in support:
        words[index] = var("U57") if index == 57 else var(f"X{index}")
    for index in parameters:
        words[index] = var(f"P{index}")

    for t, target in base.ORDER:
        inputs = ((t - 2, S1, I1), (t - 7, lambda x: x, lambda x: x),
                  (t - 15, S0, I0), (t - 16, lambda x: x, lambda x: x))
        unknown = [position for position in (t,) + tuple(i[0] for i in inputs)
                   if words[position] is None]
        assert unknown == [target]
        if target == t:
            value = ZERO
            for position, function, _ in inputs:
                value = value + function(words[position])
            words[target] = value
        else:
            others = ZERO
            inverse = None
            for position, function, inv in inputs:
                if position == target:
                    inverse = inv
                else:
                    others = others + function(words[position])
            words[target] = inverse(words[t] - others)

    r33 = words[33] - S1(words[31]) - words[26] - S0(words[18]) - words[17]
    r57 = words[57] - S1(words[55]) - words[50] - S0(words[42]) - words[41]
    H = S1(words[55]) + words[50] + S0(words[42]) + words[41]
    return words, r33, r57, H


def sign_class(expr):
    direct = json.dumps(expr.serial(), sort_keys=True, separators=(",", ":"))
    negative = json.dumps((-expr).serial(), sort_keys=True, separators=(",", ":"))
    return min(direct, negative)


def main():
    checked_hashes = {}
    for relative, expected in REFERENCES.items():
        path = ROOT / relative
        actual = sha256(path)
        assert actual == expected, (relative, actual, expected)
        checked_hashes[relative] = actual

    base = load_base()
    assert tuple(base.SUPPORT) == (10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57)
    assert tuple(base.PARAMETERS) == (9, 12, 14, 19, 22)
    assert tuple(base.RESIDUAL_INDICES) == (33, 57)

    x = {index: var(f"X{index}") for index in base.SUPPORT if index != 57}
    words, r33, r57, H = symbolic_base_chart(base)
    assert not contains(H, "U57")
    assert not contains(r33, "U57")
    assert r57 == var("U57") - H
    assert substitute(r57, {"U57": H}) == ZERO
    assert H == substitute(H, {"U57": ZERO})
    assert r33 == substitute(r33, {"U57": ZERO})

    v = derive_values(x)
    residuals = factor_residuals(v, x, H)
    eliminated = ("10F", "11F", "13F", "15F", "26G", "29F", "29G", "42F", "43G")
    retained = ("15G", "18F", "18G", "20F", "20G", "26F", "28F", "28G",
                "34F", "34G", "42G", "43F", "57G")
    assert len(residuals) == 22
    assert all(residuals[name] == ZERO for name in eliminated)
    assert all(residuals[name] != ZERO for name in retained)
    assert set(eliminated).isdisjoint(retained)
    assert set(eliminated) | set(retained) == set(residuals)
    reduced = reduced_residuals(v, x, H)
    assert tuple(reduced) == retained
    assert all(residuals[name] == reduced[name] for name in retained)

    A, B, C, K = (v[name] for name in ("A", "B", "C", "K"))
    P, Q, S, Z = (v[name] for name in ("P", "Q", "S", "Z"))
    distinct = (A, B, C, K, P + A, Q + S, Z)
    d_table = {
        10: A, 11: B, 13: C, 15: K, 18: B, 20: -B,
        26: P + A, 28: Q + S, 29: C, 34: B,
        42: P + A, 43: -B, 57: Z,
    }
    assert len({sign_class(item) for item in distinct}) == 7
    assert {sign_class(item) for item in d_table.values()} == {
        sign_class(item) for item in distinct
    }
    assert all(item != ZERO for item in distinct)

    # Exact 42 -> 57 cascade: the definition of Z is the word-42 F value,
    # the factor table sets d57=Z, the base chart forces X57=H, and retained
    # 57G is precisely D1(H,Z)=B.
    assert v["Z"] == D0(x[42], v["P"] + v["A"])
    assert d_table[57] == v["Z"]
    assert residuals["57G"] == D1(H, v["Z"]) - v["B"]

    # Frozen candidate sampling is replayed only as non-proof auxiliary data.
    candidate = ROOT / "support12-base-factor-normal-v10" / "verify_candidate.py"
    frozen_run = json.loads((candidate.parent / "RUN.json").read_text())
    completed = subprocess.run(
        [sys.executable, "-B", str(candidate)], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    auxiliary = json.loads(completed.stdout)
    assert auxiliary == frozen_run

    result = {
        "schema": "support12-base-factor-normal-proof-v11-symbolic-run-v1",
        "status": "PASS",
        "python": platform.python_version(),
        "reference_hashes_checked": checked_hashes,
        "symbolic_core": {
            "method": "canonical normalized term DAG over the additive word group",
            "random_sampling_used_for_proof": False,
            "original_factor_derivative_equations": len(residuals),
            "definitionally_zero_equations": list(eliminated),
            "retained_equations": list(retained),
            "retained_equation_count": len(retained),
            "base_residual_equations": ["R33=0"],
            "free_word_count": 18,
            "free_words": ["A"] + [f"X{i}" for i in base.SUPPORT if i != 57]
                          + [f"P{i}" for i in base.PARAMETERS],
            "exact_support_nonzero_classes": 7,
            "u57_absent_from_H": True,
            "u57_absent_from_R33": True,
            "R57_identity": "R57=U57-H",
            "forced_u57": "H",
            "cascade": "Z=D0(X42,P+A)=d57; D1(H,Z)=B",
        },
        "auxiliary_v10_seeded_run": {
            "status": "PASS_EXACT_FROZEN_REPLAY_NON_PROOF",
            "seed": frozen_run["seed"],
            "trials": frozen_run["trials"],
            "u57_sink_control_trials": frozen_run["u57_sink_control_trials"],
        },
        "scope": (
            "Complete author-written bidirectional equivalence proof audit for the "
            "18-word support-12 normal form; no feasibility, message-pair, "
            "distance-14, independent-review, human-review, or Lean claim."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
