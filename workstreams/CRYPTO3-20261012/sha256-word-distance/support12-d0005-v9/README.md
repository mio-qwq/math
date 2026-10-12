# support12 fixed-D branch `00050000`

This package corrects a sign/orientation error in a proposed three-pair
fixture and freezes two proof-producing local exclusions:

1. the correct third joint-image point `(D,-A,-T)` is absent;
2. the reciprocal sigma0 edge `A -> D` is absent.

Both are exact 32-bit modular statements with independently rebuilt CNFs and
stdlib-only deletion-free DRUP checking.  They exclude only the displayed
fixed branch, not every A at this D and not the full support or message
problem.  The mathematical details and precise scope are in `PROOF.md`.

Replay from repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d0005-v9/check.py
```

Regeneration, requiring the separately installed python-sat dependency:

```sh
PYTHONPATH=/workspace/scratch/b1d6bae025af/crypto3-deps python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d0005-v9/generate.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d0005-v9/check.py --write
```

`CERTIFICATE.json` records the exact runtime, commands, formula sizes,
variable groups and proof hashes.  `RUN.json` is the frozen checker output.
