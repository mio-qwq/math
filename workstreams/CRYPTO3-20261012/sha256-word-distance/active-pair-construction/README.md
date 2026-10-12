# Support-0 active-pair construction modules

**Candidate mathematical reduction and bounded construction failure.**
No full active-pair assignment or actual distance-13 schedule is known
from this work. The global lower bound remains 13. This directory has
not yet received a separate independent-agent review.

The complete result is in `PROOF.md`:

- All 48 original modular difference recurrences on frozen support 0
  reduce exactly to 24 nontrivial interface equations, retaining the
  distinct initial and terminal boundaries.
- A reversed-sigma1-image chain, with three free modular translations,
  parameterizes all R-chain relations. A left boundary, two middle
  actual-pair modules and a right boundary give an exact necessary and
  sufficient condition for a full difference assignment.
- For any fixed input XOR mask, prescribed modular word/sigma
  differences define an exactly checkable affine binary fibre.
- One natural seed-mask construction is impossible: original equations
  45 and 54 require `G_52=F_30`, but the proposed masks force disjoint
  modulo-8 residue sets `{1,7}` and `{3,5}`. This stops that construction;
  it does not exclude support 0.

The prospective mechanism and its fixed scope were recorded in
`MECHANISM.md` before each bounded calculation. No SAT/SMT solver was
used, no timeout was extended, and no other seed family was searched.

## Evidence and reproduction

`ANALYSIS.json` records all 48 equations and exact seed-fibre diagnostics.
`FIXED-MASK-RUN.json` gives the affine certificates and the one terminal
contradiction. `VERIFICATION.json` records direct original output-bit
checks and eight rejected damaged controls. This second implementation
is by the discoverer and is not described as independent review.

Run the standard-library-only checker:

```sh
python -B verify.py --negative
```

To replay all three small computations and compare their JSON outputs
without changing the saved evidence:

```sh
python -B reproduce.py
```

`RUNS.json` records the actual commands, source/output hashes and exit
codes. `provenance.json` binds the exact external support and base-lift
versions. `SHA256.json` binds all files in this directory other than
itself. The existing `mechanism/` and `base-review/` packages were not
changed by this investigation.

An actual schedule still requires the separate base interpolation and
all ten original base-lift residual equations. The module criterion
does not imply that any specified fibre is nonempty, or that any
completed difference assignment has a base lift.
