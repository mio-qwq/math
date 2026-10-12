# Independent base-projection review

`REVIEW.md` accepts the two exact reductions in the hash-pinned
`base-lift/PROJECTION.md`: prescribed-pair lifting conditional on a
genuine interpolating base, and the explicit 38-equation completion
with ten remaining original residuals. No surjectivity or equality-pair
claim is accepted or implied.

The reviewer reconstructed the mathematics and a different elimination
order before inspecting the author proof or evaluator. That initial
state is pinned in `PRE-AUTHOR-CHECKPOINT.json`.

Reproduce the definition-based review:

```sh
python -B verify_independent.py --author-directory ../base-lift --frozen-supports PATH/TO/FROZEN/v2/supports.json
```

`VERIFICATION.json` records the successful independent run and its
negative controls. `AUTHOR-VERIFIER-RERUN.json` is a separate replay of
the original author checker, matching the frozen author output exactly.
`RUNS.json` records the observed exits and hashes. `RECEIPT.json` pins
the accepted scope and versions; `SHA256.json` freezes the review files.
