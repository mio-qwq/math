# support12 base interpolation: independent PRE-AUTHOR review

This directory independently reconstructs a five-anchor, two-residual base
coordinate chart for support 12.  The result is exact and definition-based,
but only states an interpolation equivalence for specified first active-word
values.  It neither solves the residual equations nor constructs a pair of
messages.

The derivation and checker were frozen before author contact.  See
`INDEPENDENT_PROOF.md` and run `check_independent.py` from the repository
root.  The only imported data are the frozen support indices in
`../supports-v2.json`; no author program is imported.
