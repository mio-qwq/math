#!/usr/bin/env python3
"""Seeded substitution audit for the support-12 base/factor normal form.

This is a sign/transcription checker for a candidate exact reduction.  Random
testing is not a proof of the universally quantified equivalence.
"""

import argparse
import hashlib
import importlib.util
import json
import platform
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "support12-base-lift-v8" / "base_completion.py"
BASE_SHA256 = "ffb18eab959097258633a69fbc23556d0f3fbf09bc80cf4d0deefc0fe7d89365"
MASK = (1 << 32) - 1
SEED = 0x0C012E57
TRIALS = 10_000
PAIR_INDICES = (10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43)

ELIMINATED = (
    "10F", "11F", "13F", "15F", "26G", "29F", "29G", "42F", "43G",
)
RETAINED = (
    "15G", "18F", "18G", "20F", "20G", "26F", "28F", "28G",
    "34F", "34G", "42G", "43F", "57G",
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_base():
    actual = sha256(BASE)
    if actual != BASE_SHA256:
        raise AssertionError(f"base provenance mismatch: {actual}")
    spec = importlib.util.spec_from_file_location("frozen_support12_base", BASE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add(*values):
    return sum(values) & MASK


def neg(value):
    return (-value) & MASK


def delta0(base, x, d):
    return (base.sigma0(add(x, d)) - base.sigma0(x)) & MASK


def delta1(base, x, d):
    return (base.sigma1(add(x, d)) - base.sigma1(x)) & MASK


def derive(base, root_a, x):
    """Definitionally eliminate b,c,k,p,q,l,s,w,z in that order."""
    a = root_a
    b = neg(delta0(base, x[10], a))
    c = neg(delta1(base, x[43], neg(b)))
    k = neg(delta1(base, x[29], c))
    p = delta0(base, x[11], b)
    q = delta0(base, x[13], c)
    l = delta0(base, x[15], k)
    s = delta1(base, x[26], add(p, a))
    w = delta0(base, x[29], c)
    z = delta0(base, x[42], add(p, a))
    return {"a": a, "b": b, "c": c, "k": k, "p": p,
            "q": q, "l": l, "s": s, "w": w, "z": z}


def h_and_r33(base, x, anchors):
    active = {index: x[index] for index in PAIR_INDICES}
    active[57] = 0  # H and R33 are independently certified not to depend on it.
    words, residuals = base.complete(active, anchors)
    h = add(base.sigma1(words[55]), words[50], base.sigma0(words[42]), words[41])
    return h, residuals[33]


def original_residuals(base, v, x, h):
    a, b, c, k = (v[name] for name in ("a", "b", "c", "k"))
    p, q, l, s, w, z = (v[name] for name in ("p", "q", "l", "s", "w", "z"))
    targets = {
        10: (a, neg(b), None),
        11: (b, p, None),
        13: (c, q, None),
        15: (k, l, neg(a)),
        18: (b, neg(add(p, a)), neg(add(b, c))),
        20: (neg(b), neg(add(q, s)), neg(k)),
        26: (add(p, a), neg(b), s),
        28: (add(q, s), neg(b), neg(l)),
        29: (c, w, neg(k)),
        34: (b, neg(add(p, a)), add(b, neg(c))),
        42: (add(p, a), z, neg(add(w, q, s))),
        43: (neg(b), neg(add(p, a)), neg(c)),
    }
    residuals = {}
    for index, (d, f_target, g_target) in targets.items():
        if f_target is not None:
            residuals[f"{index}F"] = (delta0(base, x[index], d) - f_target) & MASK
        if g_target is not None:
            residuals[f"{index}G"] = (delta1(base, x[index], d) - g_target) & MASK
    residuals["57G"] = (delta1(base, h, z) - b) & MASK
    return residuals


def reduced_residuals(base, v, x, h):
    """The thirteen equations left after the nine definitional pivots."""
    a, b, c, k = (v[name] for name in ("a", "b", "c", "k"))
    p, q, l, s, w, z = (v[name] for name in ("p", "q", "l", "s", "w", "z"))
    return {
        "15G": add(delta1(base, x[15], k), a),
        "18F": add(delta0(base, x[18], b), p, a),
        "18G": add(delta1(base, x[18], b), b, c),
        "20F": add(delta0(base, x[20], neg(b)), q, s),
        "20G": add(delta1(base, x[20], neg(b)), k),
        "26F": add(delta0(base, x[26], add(p, a)), b),
        "28F": add(delta0(base, x[28], add(q, s)), b),
        "28G": add(delta1(base, x[28], add(q, s)), l),
        "34F": add(delta0(base, x[34], b), p, a),
        "34G": (delta1(base, x[34], b) - b + c) & MASK,
        "42G": add(delta1(base, x[42], add(p, a)), w, q, s),
        "43F": add(delta0(base, x[43], neg(b)), p, a),
        "57G": (delta1(base, h, z) - b) & MASK,
    }


def support_values(v):
    return (v["a"], v["b"], v["c"], v["k"],
            add(v["p"], v["a"]), add(v["q"], v["s"]), v["z"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=TRIALS)
    parser.add_argument("--seed", type=lambda value: int(value, 0), default=SEED)
    args = parser.parse_args()
    if args.trials <= 0:
        raise ValueError("trials must be positive")

    base = load_base()
    rng = random.Random(args.seed)
    sentinel_checks = 0
    for trial in range(args.trials):
        root_a = rng.getrandbits(32)
        x = {index: rng.getrandbits(32) for index in PAIR_INDICES}
        anchors = {index: rng.getrandbits(32) for index in base.PARAMETERS}
        values = derive(base, root_a, x)
        h, r33 = h_and_r33(base, x, anchors)
        original = original_residuals(base, values, x, h)
        reduced = reduced_residuals(base, values, x, h)

        assert tuple(original) == (
            "10F", "11F", "13F", "15F", "15G", "18F", "18G",
            "20F", "20G", "26F", "26G", "28F", "28G", "29F",
            "29G", "34F", "34G", "42F", "42G", "43F", "43G", "57G",
        )
        assert all(original[name] == 0 for name in ELIMINATED)
        assert tuple(reduced) == RETAINED
        assert all(original[name] == reduced[name] for name in RETAINED)
        assert len(support_values(values)) == 7
        assert 0 <= r33 <= MASK

        # A bounded control rechecks the accepted sink-coordinate property in
        # the exact contexts generated here, without turning sampling into a
        # universal proof claim.
        if trial < 64:
            active = {index: x[index] for index in PAIR_INDICES}
            active[57] = 0xA5A5A5A5
            other_words, other_residuals = base.complete(active, anchors)
            other_h = add(base.sigma1(other_words[55]), other_words[50],
                          base.sigma0(other_words[42]), other_words[41])
            assert other_h == h and other_residuals[33] == r33
            active[57] = h
            _, forced_residuals = base.complete(active, anchors)
            assert forced_residuals[33] == r33 and forced_residuals[57] == 0
            sentinel_checks += 1

    pivots = {
        "10F": "definitionally_zero_by_B",
        "11F": "definitionally_zero_by_P",
        "13F": "definitionally_zero_by_Q",
        "15F": "definitionally_zero_by_L",
        "26G": "definitionally_zero_by_S",
        "29F": "definitionally_zero_by_W",
        "29G": "definitionally_zero_by_K",
        "42F": "definitionally_zero_by_Z",
        "43G": "definitionally_zero_by_C",
    }
    mapping = {name: pivots.get(name, name) for name in tuple(original)}
    result = {
        "schema": "support12-base-factor-normal-v10-substitution-run-v1",
        "status": "PASS_CANDIDATE_SYMBOLIC_CHECK_ONLY",
        "python": platform.python_version(),
        "base_source": "../support12-base-lift-v8/base_completion.py",
        "base_source_sha256": sha256(BASE),
        "seed": f"0x{args.seed:08x}",
        "trials": args.trials,
        "original_factor_derivative_equations": len(original),
        "definitionally_eliminated_equations": len(ELIMINATED),
        "retained_factor_derivative_equations": len(reduced),
        "additional_base_equation": "R33=0",
        "reduced_equalities_including_R33": len(reduced) + 1,
        "original_free_words_after_u57_sink_elimination": 27,
        "definitionally_eliminated_scalar_words": 9,
        "reduced_free_words": 18,
        "exact_support_nonzero_tests": 7,
        "u57_sink_control_trials": sentinel_checks,
        "equation_mapping": mapping,
        "scope": (
            "Seeded word-arithmetic substitution audit of a candidate exact "
            "normal form; not a complete proof, SAT/UNSAT result, message pair, "
            "independent review, or Lean formalization."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
