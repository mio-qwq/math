#!/usr/bin/env python3
"""Definition-level checks for the support-12 row-57 merge lemma."""

import argparse
import hashlib
import importlib.util
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "support12-base-lift-v8" / "base_completion.py"
EXPECTED_BASE_SHA256 = "ffb18eab959097258633a69fbc23556d0f3fbf09bc80cf4d0deefc0fe7d89365"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_base():
    if sha256(BASE) != EXPECTED_BASE_SHA256:
        raise AssertionError("base_completion.py provenance mismatch")
    spec = importlib.util.spec_from_file_location("accepted_base_completion", BASE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dependencies(base):
    deps = [None] * 64
    for i in set(base.SUPPORT) | set(base.PARAMETERS):
        deps[i] = {i}
    for t, target in base.ORDER:
        positions = (t, t - 2, t - 7, t - 15, t - 16)
        assert [i for i in positions if deps[i] is None] == [target]
        deps[target] = set().union(*(deps[i] for i in positions if i != target))
    assert all(item is not None for item in deps)
    return deps


def h57(base, words):
    return (base.sigma1(words[55]) + words[50] + base.sigma0(words[42])
            + words[41]) & base.MASK


def check_context(base, active, params, replacements):
    words, residuals = base.complete(active, params)
    h = h57(base, words)
    assert residuals[57] == (active[57] - h) & base.MASK
    for replacement in replacements:
        changed = dict(active)
        changed[57] = replacement
        other, other_residuals = base.complete(changed, params)
        delta = (replacement - active[57]) & base.MASK
        assert other[:57] == words[:57]
        assert other_residuals[33] == residuals[33]
        assert other_residuals[57] == (residuals[57] + delta) & base.MASK
        forced = dict(active)
        forced[57] = h
        _, forced_residuals = base.complete(forced, params)
        assert forced_residuals[57] == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    base = load_base()

    deps = dependencies(base)
    affected_by_57 = [i for i, item in enumerate(deps) if 57 in item]
    assert affected_by_57 == [57, 59, 61, 63]
    r33_sources = set().union(deps[33], deps[31], deps[26], deps[18], deps[17])
    r57_tail_sources = set().union(deps[55], deps[50], deps[42], deps[41])
    assert 57 not in r33_sources
    assert 57 not in r57_tail_sources

    contexts = []
    for fill in (0, base.MASK, 0xAAAAAAAA, 0x55555555):
        contexts.append(({i: fill for i in base.SUPPORT},
                         {i: fill for i in base.PARAMETERS}))
    rng = random.Random(0xBA5E57)
    for _ in range(32):
        contexts.append(({i: rng.getrandbits(32) for i in base.SUPPORT},
                         {i: rng.getrandbits(32) for i in base.PARAMETERS}))
    replacements = (0, 1, 0x12345678, 0x80000000, base.MASK)
    for active, params in contexts:
        check_context(base, active, params, replacements)

    z = 1
    projected_b = (base.sigma1(z) - base.sigma1(0)) & base.MASK
    forced_h = 0x12345678
    pointwise_b = (base.sigma1((forced_h + z) & base.MASK)
                   - base.sigma1(forced_h)) & base.MASK
    assert projected_b == 0x0000A000
    assert pointwise_b == 0xFFFFA000
    assert pointwise_b != projected_b

    # Direct algebraic row-57 difference check with shared inactive words.
    for _ in range(64):
        w41, w50, w55 = (rng.getrandbits(32) for _ in range(3))
        u42, v42 = rng.getrandbits(32), rng.getrandbits(32)
        hu = (base.sigma1(w55) + w50 + base.sigma0(u42) + w41) & base.MASK
        hv = (base.sigma1(w55) + w50 + base.sigma0(v42) + w41) & base.MASK
        assert (hv - hu) & base.MASK == (base.sigma0(v42) - base.sigma0(u42)) & base.MASK

    result = {
        "status": "PASS",
        "claim_scope": "row-57 sink elimination and exact pointwise endpoint merge only",
        "base_source": str(BASE.relative_to(HERE.parent)),
        "base_source_sha256": sha256(BASE),
        "dependency_sources_affected_by_u57": affected_by_57,
        "deterministic_contexts": len(contexts),
        "u57_replacements_per_context": len(replacements),
        "row57_pair_identity_trials": 64,
        "negative_control": {
            "z": "0x00000001",
            "projected_witness_base": "0x00000000",
            "projected_b": f"0x{projected_b:08x}",
            "forced_base": f"0x{forced_h:08x}",
            "pointwise_b": f"0x{pointwise_b:08x}",
            "projection_is_insufficient": pointwise_b != projected_b,
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
