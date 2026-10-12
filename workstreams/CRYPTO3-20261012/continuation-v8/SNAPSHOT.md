# CRYPTO3 stage-8 checkpoint

Recovery base: `22c0853b24e3f7cbcb43738a8b4fc2170fa60ce6` on
`partner/dist-CRYPTO3-20261012`.  The global result remains a lower bound of
**13** for the real 32-bit modular-addition SHA-256 message expansion.  This
stage supplies neither a distance-13 message pair nor a proof of distance at
least 14.

## Independently accepted support-12 factorisation

For the true zero-based support identifier 12,

```
S={10,11,13,15,18,20,26,28,29,34,42,43,57},
```

all 48 original difference rows are now factored exactly.  There are 25
nonzero rows and 23 identities.  Integer unit elimination gives rank 25 and
free rank 14 over `Z/(2^32)`, with no field division or hidden two-power
torsion.  Four boundary-private derivative coordinates can be absorbed into
their own factors, leaving an exact connected system of ten shared scalars
and thirteen actual same-word-pair conditions: nine full joint `(d,F,G)`
memberships, three exact `(d,F)` projections and one exact `(d,G)`
projection.

The corrected author proof is in `sha256-word-distance/support12-full-factor-v9/`.
The blind review in `support12-full-factor-review-v8/` derives a different
normal form first, then verifies all 48 rows, all 39 coordinate forms under
an explicit integral change of basis, the unit operations, source binding
and damage controls.  It accepts exactly this independent-active-pair
factor theorem.  It does not assert that the thirteen factors are jointly
feasible or arise from two common base messages.

## Preserved rejection and failure mechanism

The first author object `support12-full-factor-v8/` is immutable and
**rejected** for the claimed target.  It used

```
supports[11]={10,11,15,18,20,26,27,28,29,34,42,43,57}
```

while labelling it support 12, replacing the required position 13 by 27.
Seven original rows change.  Its internal checks passed because generator,
certificate and checker shared the same wrong active constant; both wrong
and correct objects coincidentally have the same 25/23 row counts and
rank/free-rank values.  The independent review records `REJECT` for v8 and
`ACCEPT` for corrected v9.  V9 adds explicit zero-based source binding and
two object-damage controls that recreate the failure.

## Independently accepted actual-base completion chart

For arbitrary prescribed first-word values on the true support 12, five
inactive anchors

```
P={9,12,14,19,22}
```

uniquely determine the other 46 coordinates through 46 distinct original
recurrences.  The only unused original rows are 33 and 57.  Projection onto
the five anchors is therefore an exact bijection between genuine schedules
with the prescribed support coordinates and the common zeros of the two
word residuals `R_33` and `R_57`.

The independent reviewer froze a different five-anchor chart before author
contact, obtained the same two residual rows, exhausted all 272,052 anchor
sets of sizes zero through four, and confirmed that the author's set is the
first lexicographic five-anchor success at trial 1,498,469.  Both small-sigma
inverse matrices, all reverse steps, actual-schedule round trips and damage
controls pass.  This is an exact interpolation equivalence, not a proof that
the two residual equations have a common zero.

## Independently accepted fixed-residue obstruction

At the concrete residual `D=0x00010000`, the first two fibres in the already
accepted selected joint-image core cannot satisfy

```
F_D(x)=F_D(y) mod 2^32,
G_D(y)-G_D(x)=2D mod 2^31.
```

The finite proof partitions every input into sixteen exact addition-XOR
classes.  Across all 256 class pairs, the full sigma0 equality leaves 414
affine branches, the sigma1 equation through bit 29 leaves 20, and bit 30
eliminates all 20 by an odd-carry parity contradiction.  A real four-word
boundary fixture satisfies the system modulo `2^30`, showing that the last
bit is necessary.  An independent implementation reconstructs the class
cover, `414 -> 20 -> 0` frontier, a different boundary fixture, reversal
bijection and damage controls.  Pair reversal also excludes
`D=0xffff0000`.

This removes only the two signed numerical residues `+/-2^16`.  It does not
exclude the other exact-valuation-16 residues or the complete support.

## Stopped bounded query

A separately preregistered QF_BV query retained thirteen independent actual
word pairs, all 48 original difference rows and exact `v2(d18)=16`.  Z3
4.15.3 made one check at a fixed 30,000 ms limit and returned `unknown`
with reason `timeout` after 30.147937709996768 seconds.  There is no model or
UNSAT certificate, and the model verifier was not run.  The query omits
base completion.  It is not retried or extended, and the stage replay checks
only its frozen bytes and stopping receipt.

## Remaining target

The sharpest exact support-12 formulation is now two-layered: first solve or
exclude the accepted ten-scalar/thirteen-factor independent-pair system;
then satisfy the independently accepted two-residual base chart for the
chosen first endpoints.  The fixed signed `2^16` residues are excluded, but
the remaining exact-valuation strata are open.  Any future negative solver
result still requires a checkable certificate; any local factor witness
still requires the two base residuals before it is a message pair.

No result in this stage changes another representative support, creates a
Lean formalisation, or constitutes external human review, publication,
historical priority, a paper, DOI or Release.

Replay the new stage with only Python's standard library:

```sh
python -B workstreams/CRYPTO3-20261012/continuation-v8/replay.py
```

The replay validates prior frozen manifests, runs the new independent gates
in an isolated copy, and checks the stopped-query receipt without invoking
Z3 or repeating older large enumerations.
