# Exact support-12 base-completion reduction

Status: complete author-written elimination proof and definition-based
implementation checks.  Independent-agent acceptance is separate.  This is
not a support witness, a distance-13 construction, a distance-14 proof or a
claim that the remaining equations are soluble.

All arithmetic is in `R=Z/(2^32)`.  The SHA-256 small sigmas are the FIPS
180-4 maps

```
f(x)=ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x).
```

They are binary linear permutations.  The verifier reconstructs inverse
bases and checks all 64 compositions on standard basis vectors.  Thus each
message-schedule recurrence

```
W[t] = g(W[t-2]) + W[t-7] + f(W[t-15]) + W[t-16]
```

is uniquely reversible in any one of its five coordinates.

## Coordinate chart

For support 12 let

```
S = {10,11,13,15,18,20,26,28,29,34,42,43,57}
P = {9,12,14,19,22}.
```

The finite coordinate-only search exhausts all 20,825 inactive three-anchor
sets and all 249,900 inactive four-anchor sets without finding a complete
single-row peeling order.  At five anchors its first lexicographic success
is P.  Starting with arbitrary words on `S union P`, the following pairs
`(row t, coordinate solved)` uniquely assign every remaining coordinate:

```
(26,24) (28,21) (29,27) (34,32) (36,36) (43,41)
(27,25) (41,39) (25,23) (30,30) (39,37) (44,44)
(37,35) (42,40) (35,33) (40,38) (45,45) (38,31)
(46,46) (47,47) (48,48) (49,49) (50,50) (51,51)
(52,52) (53,53) (54,54) (55,55) (56,56) (58,58)
(59,59) (60,60) (61,61) (62,62) (63,63) (31,16)
(32,17) (24,8) (23,7) (22,6) (21,5) (20,4)
(19,3) (18,2) (17,1) (16,0).
```

These are 46 distinct rows and 46 distinct newly assigned coordinates.
The unused original rows are exactly `T={33,57}`.

Let `C(u,p)` denote the resulting 64-word sequence for values `u` on S and
`p` on P.  Define, for `t in T`,

```
R_t(u,p) = C_t - g(C_(t-2)) - C_(t-7)
                - f(C_(t-15)) - C_(t-16).
```

Equivalently the two remaining constraints are

```
R_33 = C_33 - g(C_31) - C_26 - f(C_18) - C_17,
R_57 = C_57 - g(C_55) - C_50 - f(C_42) - C_41.
```

## Bijection theorem

For every prescribed 13-tuple `u in R^S`, projection onto P is a bijection
between

```
{actual SHA-256 schedules W : W_i=u_i for all i in S}
```

and

```
{p in R^P : R_33(u,p)=R_57(u,p)=0}.
```

**Proof.**  Fix `(u,p)`.  Induct through the displayed order.  At each step
the target is the only unassigned coordinate in that original recurrence.
If it occurs with identity coefficient, modular subtraction gives its unique
value; if it is an input of f or g, subtraction followed by the checked
inverse permutation gives its unique value.  Therefore C exists uniquely,
retains exactly the prescribed S and P coordinates, and satisfies all 46
used original rows.  It is an actual schedule exactly when the complementary
rows 33 and 57 also vanish.

Conversely, let W be an actual schedule with S-projection u and set
`p=W|P`.  Induction through the same order shows that every coordinate
constructed by `C(u,p)` equals the corresponding coordinate of W, since W
satisfies the selected row and its solution is unique.  Hence `C(u,p)=W`.
Projection recovers p, so the two maps are inverse.  This proves the
bijection.  In particular, five parameters versus two equations is only an
exact parametrization; it does not prove either residual has a common zero.

## Relation to the active-pair problem

Suppose actual unequal pairs `(u_i,v_i)` on S already satisfy all 48 exact
modular difference recurrences, with sigma differences computed from the
same endpoints.  As in the independently accepted base-lift reduction, they
extend to two genuine schedules with exact support S iff u has an actual
base completion.  The theorem above makes that last statement equivalent to
the existence of `p in R^5` satisfying the two displayed residual equations.
Once such p exists, replace C's S-coordinates by v and retain every inactive
coordinate; subtraction by the assumed difference equations proves the
second sequence is also an actual schedule.

Thus support 12 has an exact two-residual base-lift obligation.  The result
does not supply the required active endpoint pairs or solve the residuals.
The exhaustive failure for three/four anchors concerns only this peeling
mechanism and is not a lower bound on every possible algebraic chart.

## Verification

`verify_completion.py` computes the FIPS functions independently from their
output bits, checks the coordinate dependencies and inverse bases, and then
round-trips four deterministic plus twelve seeded-random nonzero 16-word
messages through all 64 coordinates.  All 48 original rows are checked
directly.  Flipping active coordinate 10 preserves the 46 constructed rows
but is rejected by a residual; separately corrupting constructed coordinate
31 is rejected by used original rows.  These examples validate the evaluator
and controls; the universally quantified claim is the elimination proof.

