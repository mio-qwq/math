# Replay

Run from the repository root.

## Check the frozen certificates

Only Python 3's standard library is required:

```bash
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-core-batch-v9/check.py
```

The top-level result must contain `"status": "PASS"`; each of the six
records must also contain `"status": "PASS"` and
`"final_empty": true`.

To reproduce `RUN.json`:

```bash
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-core-batch-v9/check.py --write
```

## Regenerate formulas and proofs

The frozen generation run used Python 3.12.14 and `python-sat 1.9.dev15`.
The native solver-module digest and individual runtimes are recorded in
`CERTIFICATE.json`.

```bash
PYTHONPATH=/workspace/scratch/b1d6bae025af/crypto3-deps \
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-core-batch-v9/generate.py

python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-core-batch-v9/check.py --write
```

Regeneration is not part of the trusted verification path.  A different
Glucose build may emit a byte-different valid proof; such a trace must be
checked and frozen under its own digest.

