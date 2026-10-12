# Replay

Run from the repository root.

## Trusted certificate check

This needs Python 3 and its standard library only:

```bash
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d000f-v9/check.py
```

Expected terminal status is JSON containing:

```text
"status": "PASS"
"clauses_checked": 3951
"final_empty": true
```

To reproduce the frozen `RUN.json` receipt:

```bash
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d000f-v9/check.py --write
```

## Regenerate CNF and proof

The generation dependency used for the frozen run was `python-sat
1.9.dev15`; it was installed in the already isolated dependency directory
shown below.  The native proof-producing module digest is recorded in
`CERTIFICATE.json`.

```bash
PYTHONPATH=/workspace/scratch/b1d6bae025af/crypto3-deps \
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d000f-v9/generate.py

python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d000f-v9/check.py --write
```

Regeneration is not required to validate the frozen proof.  If another
Glucose build emits a different valid trace, its digest may differ even
though the stdlib checker still accepts it.

