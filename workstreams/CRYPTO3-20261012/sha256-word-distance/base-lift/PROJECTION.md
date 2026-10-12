# Actual-base completion for SHA-256 support 0

Status: candidate exact reduction, with a complete written elimination proof
and definition-based evaluator checks; independent-agent review pending.
This is not a new word-distance bound, real equality pair, attack or
historical-priority claim.

This note separates two exact conditions which were combined in the old
full-schedule SMT model.  It concerns the FIPS 180-4 32-bit recurrence,
arbitrary base words, and the frozen support

```
S = {2,9,10,16,23,24,30,37,38,44,51,52,58}.
```

No zero-base assumption or relaxed replacement of modular addition is used.
Definitions are [FIPS 180-4, Sections 4.1.2 and 6.2.2](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf).
The support is frozen in CRYPTO2 commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`,
`projects/sha256-schedule-distance/v2/supports.json`, index 0.

## Exact completion reduction

Suppose two unequal words `(u_i,v_i)` are prescribed for every `i in S`.
Put `delta_i=v_i-u_i`, `F_i=sigma0(v_i)-sigma0(u_i)`, and
`G_i=sigma1(v_i)-sigma1(u_i)` on S; put all three quantities zero outside S.
All operations on differences are modulo `2^32`.

The prescribed pairs extend to two actual schedules with support exactly S
if and only if both conditions below hold:

1. All 48 standard difference equations hold:
   `delta_t = G_(t-2)+delta_(t-7)+F_(t-15)+delta_(t-16)`.
2. There is one actual base schedule W satisfying `W_i=u_i` for every
   `i in S`.

Proof. Necessity follows by subtraction and projection.  Conversely,
given the base schedule from condition 2, define W' by replacing its
coordinates on S with v and leaving every other coordinate unchanged.
Subtracting the 48 proposed W' recurrences from the corresponding W
recurrences reduces precisely to condition 1.  Thus W' satisfies all
48 actual recurrences and has the prescribed exact support.  The input
blocks differ because S contains 2,9,10.  No base equation was dropped.

Condition 2 is the surjectivity/interpolation question for the projection
`M -> (E(M)_i)_(i in S)`.  It cannot be declared automatic without proof,
nor may it be declared an additional obstruction before its image is known.

## A bounded mechanism to test before solving values

Each standard recurrence is invertible in each of its five words: the
identity coefficients permit direct subtraction, and both small sigmas
are permutations.  Prescribing the 13 active words and three additional
inactive words leaves 48 words unknown and 48 recurrence equations.

If an elimination order repeatedly finds an equation with exactly one
unknown word and eventually solves all 48 unknowns, every equation was
used exactly once and arbitrary prescribed values admit a unique completion.
That would establish surjectivity for this projection with three free
word parameters, without any SMT search or probability assumption.

The finite structural test considers the `binomial(51,3)=20,825` choices
of three additional coordinate anchors.  It propagates known-coordinate
sets only; it does not enumerate word values, support models or message
pairs.  Success must supply the full equation/unknown order, then verify
the resulting algebraic evaluator directly.  Failure only rules out this
single-equation elimination mechanism with three coordinate anchors;
it does not disprove actual completion or surjectivity.

### Outcome and stop for this mechanism

The exact structural test completed all 20,825 anchor sets.  None completed
the schedule; the maximum known-coordinate count was 21.  One maximizing
anchor triple is `{17,18,31}`, from which only five further coordinates
are obtained.  `coordinate_elimination.json` records the complete count
histogram and an explicit partial order.  This settles only this bounded
elimination question.  No larger anchor search or SMT timeout extension
is justified by it.

## An exact completion with ten residual equations

There is nevertheless an explicit elimination which moves all unresolved
conditions into ten original recurrence equations.  It uses the 13 active
coordinates and these 13 additional, inactive coordinates:

```
P = {0,1,3,4,5,7,8,11,12,15,29,43,57}.
```

For arbitrary word values on `S union P`, the following order assigns
every other coordinate uniquely.  Each listed pair is `(recurrence t,
coordinate solved)`.  In every step four words of that five-word equation
have already been assigned.  `sigma0` and `sigma1` are inverted when the
unknown is their argument; no inversion of a modular sum is assumed.

| Step group | Equation/unknown pairs |
|---|---|
| Alternate residue-3 words and intervening residue-1 words | `(17,17), (24,22), (31,31), (38,36), (45,45), (52,50), (59,59)` |
| Residue-0 words from the prescribed residue-2 outputs | `(16,14), (23,21), (30,28), (37,35), (44,42), (51,49), (58,56)` |
| Residue-4 forward equations | `(18,18), (25,25), (32,32), (39,39), (46,46), (53,53), (60,60)` |
| Residue-5 forward equations | `(19,19), (26,26), (33,33), (40,40), (47,47), (54,54), (61,61)` |
| Solve the three missing residue-6 boundary words | `(21,6), (22,20), (20,13)` |
| Remaining residue-6 forward equations | `(27,27), (34,34), (41,41), (48,48), (55,55), (62,62)` |
| Last output | `(63,63)` |

These are 38 distinct equations and 38 distinct new coordinates.  Together
with the initial 26 coordinates they fill all 64 words.  The ten unused
equations are exactly

```
T = {28,29,35,36,42,43,49,50,56,57}.
```

**Completion theorem.** Let `C(u,p)` be the 64-word sequence produced by
this order, where u gives values on S and p gives values on P.  Define

```
R_t(u,p) = C_t - sigma1(C_(t-2)) - C_(t-7)
               - sigma0(C_(t-15)) - C_(t-16),   t in T.
```

All values are modulo `2^32`.  Then the set of actual base schedules
whose S-projection equals u is in bijection with

```
{ p in (Z/(2^32))^13 : R_t(u,p)=0 for every t in T }.
```

Proof. By induction on the displayed order, exactly one value of the new
word satisfies that step's recurrence.  Thus `C(u,p)` satisfies all 38
used equations for every assignment, and it satisfies the remaining ten
if and only if all ten residuals vanish.  Every actual schedule with
S-projection u supplies p by projection onto P.  The same induction
reconstructs that schedule exactly, proving surjectivity of this parameter
description onto the set of completions.  Different p give different
schedules because the corresponding P-coordinates are retained.  This is
the claimed bijection.

Combined with the earlier difference/completion reduction, this is an
exact two-stage feasibility formulation for independently prescribed
active word pairs.  The second stage is a single-base system of ten
word equations in thirteen word parameters.  Neither stage alone is a
real equality witness.

### Explicit common-word coupling

For clarity set `U_j=W_(7j)`, `V_j=W_(1+7j)`, `D_j=W_(5+7j)` and
`Q_j=W_(6+7j)`.  Every one of these coordinates is outside S, hence shared
by a proposed pair of schedules.  The ten residual conditions are the
following five pairs, for `j=4,5,6,7,8`:

```
U_j-U_(j-1) = sigma1(D_(j-1)) + D_(j-3) + sigma0(Q_(j-3)),
V_j-V_(j-1) = sigma1(Q_(j-1)) + Q_(j-3) + sigma0(U_(j-2)).
```

They are not independent free-variable equations: every U,V,D,Q on the
right and left is the specific function of `(u,p)` produced above.  The
active words influence these common words through the 38 solved equations.
This gives an explicit location for the base-word coupling omitted by a
pure independent-active-pair difference model.  No claim is made that
these conditions are inconsistent, automatically soluble, or independent
as equations over the ring.  Counting words does not establish a fiber
size or a success probability.

## Verification purpose and limit

`base_completion.py` implements the displayed elimination.  Its verifier
first checks the entire order symbolically at coordinate level, including
that T is the exact complement of the used equation set.  For a small
fixed collection of nonzero 16-word inputs it then independently expands
the FIPS recurrence bit by bit, extracts `(u,p)`, reconstructs the schedule
and compares every word and all 48 original equations.  Damaged anchors
and a damaged completed word test rejection by the original recurrence.

These tests validate the evaluator and the exact decomposition.  They do
not search for support-0 pairs or prove that all independent-pair solutions
lift.  The theoretical completion theorem is the elimination induction;
the samples do not stand in for its quantifiers.

Actual verification: four prescribed nonzero input fixtures round-tripped
all 64 words, and all 48 standard equations held in each case.  Damaging
active anchor 16 by one bit still satisfied the 38 constructed equations
but violated all ten residual equations in the chosen fixture.  A separate
completed-word corruption was also rejected by the raw recurrence.  Both
programs exited 0.  Exact source hashes, environment and outputs appear in
`RUNS.json` and `verification.json`.

The old `lift_probe.py` already imposed both complete schedules directly;
it was read and was not rerun.  The present result is an explicit inversion
and residual decomposition of that exact mathematical model, intended to
make future base-lift obligations precise.  It supplies no measured solver
speedup.  No word-value search is appended merely to extend an old timeout.

