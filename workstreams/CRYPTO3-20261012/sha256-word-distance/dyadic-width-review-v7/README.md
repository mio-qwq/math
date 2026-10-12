# Independent acceptance of the dyadic width screen

**Accepted for exact k=v2(D) from 10 through 18.** The statement is a
necessary screen on actual ordered word pairs. It is not a whole-support
exclusion, a feasible-core witness or a new global distance bound.

`INDEPENDENT_PROOF.md`, `check_independent.py`, their successful output
and `PRE-AUTHOR-CHECKPOINT.json` were frozen before reading the author's
files. `REVIEW.md` subsequently accepts the exact pinned author proof.
`SOURCE_COMPARISON.json` records comparison of the author's entire finite
certificate with the independently reconstructed rows and case budgets.
No author checker is imported or executed by either review program.

Both commands are read-only, from this directory:

```sh
python -B check_independent.py
python -B compare_author.py
```

The first reconstructs all g rows, checks the joint integer norm and lift
coverage, checks 162 boundary lift fixtures and 486 actual-pair fixtures
with their reversed decompositions, and rejects four malformed controls.
Those pair fixtures test identities; none is asserted to satisfy the
complete three-pair core. The quantified theorem is the written argument.
The second checks frozen source identities and exact certificate equality.

At k=10 the crucial estimate is the shared-term bound 4*(2^22-1),
strictly below the modulus 2^24. At k=9 it no longer forces the multiple
to be zero, and the same signed-domain formula becomes vacuous. These
limits and the correct reversal of the lift h are recorded explicitly.

`RUN.json` and `COMPARISON-RUN.json` record actual execution.
`RECEIPT.json` pins scope and sources; `SHA256.json` freezes the other
review files. This is independent AI-assisted review, not Lean or human
peer review, and supplies no historical-originality claim.
