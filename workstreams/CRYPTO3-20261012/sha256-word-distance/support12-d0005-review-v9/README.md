# support12 d0005 independent review v9

This directory contains the frozen independent review of the fixed
`D=00050000, A=40406e02, T=1ffd913e` candidate.  All three requested
verdicts are ACCEPT within the narrow scope stated in `REVIEW.md`.

Replay the independent construction and frozen output:

```sh
PYTHONPATH=/workspace/scratch/b1d6bae025af/crypto3-deps \
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d0005-review-v9/independent.py
```

Replay the author comparison (about two minutes on the review host):

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d0005-review-v9/compare_author.py
```
