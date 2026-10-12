# Independent review: fixed-K affine carry proof

**Accepted for the exact fixed-mask local theorem.** See `REVIEW.md`
for the statement, exact author hashes, independent reconstruction,
comparison and scope. No entire message-schedule support or global
distance improvement is claimed by this review alone.

Before reading the author package, the reviewer reconstructed the
original three modular equations with explicit carry-sign variables,
generated all 132 necessary masks from a wider 19-bit mask universe,
and obtained 132 explicit original-row XOR contradictions. The exact
pre-author files are bound by `PRE-AUTHOR-CHECKPOINT.json`.

After the author package froze, the reviewer checked its complete mask
partition, all ten contradiction templates, and all 384 premise uses.
For each premise, `COMPARISON.json` supplies an explicit XOR of original
rows from one independent modular subsystem. All 396 corresponding
author/independent affine projections are equivalent. The earlier
SAT/CNF/RUP artifacts and exploratory matrix code are not dependencies.

## Reproduce

The standard-library-only replay leaves saved evidence and author files
unchanged:

```sh
python -B reproduce.py
```

The four actual commands and their source/output hashes, exit codes
and JSON comparisons are recorded in `RUNS.json`. `SHA256.json` binds
this review package. The full proof receipt is `RECEIPT.json`.

`INDEPENDENT-VERIFICATION.json` includes the modular final-carry
boundary and eight rejected controls. `COMPARISON.json` adds four
rejected controls. `AUTHOR-CHECKER-RERUN.json` is an actual replay of
the frozen author's checker, including its 14 rejected controls.

This is independent AI-agent review, not external human peer review or
Lean formalization. Historical priority is not certified here.
