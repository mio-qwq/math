# Independent review of the width-18 lemma

Accepted in `REVIEW.md`: a necessary condition on three actual ordered
word pairs, not a support exclusion or distance-13 message construction.
This is independent AI-assisted mathematical review, not human peer
review or Lean verification.

Read-only reproduction, from this directory:

```sh
python -B check_rows_independent.py
```

The checker uses only the standard library and prints JSON to stdout;
it does not import the author's checker or run large enumerations.
`VERIFICATION.json` freezes the actual result, `RUN.json` the execution,
`RECEIPT.json` the exact reviewed source and scope, and `SHA256.json`
the remaining review artifacts. The source proof is hash-pinned in the
receipt rather than modified by this review.
