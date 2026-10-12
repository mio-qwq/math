# Independent proof of actual-schedule time translation

This reconstruction was written from FIPS 180-4 and the frozen fifteen
supports before reading `shift-reduction-v3/PROOF.md`. It does not import
or execute the discoverer's checker. The object is the expansion of any
two distinct sixteen-word vectors over R = Z/(2^32), with no padding,
IV, fixed base block or random-message restriction.

## 1. The original and inverse recurrence

Let f(x) = ROTR7(x) XOR ROTR18(x) XOR SHR3(x), and
g(x) = ROTR17(x) XOR ROTR19(x) XOR SHR10(x). In the original expansion,

    W_t = g(W_(t-2)) + W_(t-7) + f(W_(t-15)) + W_(t-16),  16 <= t < 64.

All sums and differences below are in R. These are the original small
sigmas and schedule of NIST FIPS 180-4 Sections 4.1.2 and 6.2.2:
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf .

Extend forwards by this recurrence for all t >= 16. Extend backwards,
in the order j = -1, -2, ..., by

    W_j = W_(j+16) - g(W_(j+14)) - W_(j+9) - f(W_(j+1)).             (1)

Every right-hand index exceeds j, so it is already known. Equation (1)
is exactly the original recurrence at t = j+16 solved for the oldest
word, whose coefficient is one. It imposes no extra constraint on the
original sixteen words. It makes the original forward recurrence true
at each t <= 15 as well. We therefore obtain one unique sequence on all
integer indices satisfying the same recurrence at every integer t.

For every integer r, define V_i = W_(i+r) for 0 <= i < 64. Its first
sixteen words are an arbitrary allowed input, and for 16 <= i < 64 its
recurrence is the recurrence of W at i+r. Consequently V is exactly
the original 64-word expansion of its own first sixteen words. In
particular, an inverse-created prefix is not an assertion that the
original SHA algorithm normally computes negative indices: it is a
construction of a different legal input block.

## 2. Distinct initial blocks remain distinct

Suppose two extended sequences agree on sixteen consecutive positions
r,...,r+15. Forward induction forces agreement at all later positions.
Equation (1), applied successively below r, forces agreement at all
earlier positions. They therefore agree at the original positions
0,...,15. Contrapositively, if the original input blocks differ, every
translated initial block differs. This holds for arbitrary shifts and
requires no sigma invertibility, no probability argument, and no
support hypothesis. It also shows that the sixteen-word state
transition is a bijection.

The finite support checks additionally record at least one active index
below 16 for every map accepted below. This is a redundant concrete
check of distinctness for these maps, not a replacement for the lemma.

## 3. Boundary differences must be proved, not presumed

For a pair W,W', let d_j = W'_j-W_j,
F_j = f(W'_j)-f(W_j), G_j = g(W'_j)-g(W_j). If d_j=0,
then F_j=G_j=0. Subtracting original recurrences gives

    d_t = G_(t-2) + d_(t-7) + F_(t-15) + d_(t-16),                 (2)
    d_j = d_(j+16) - G_(j+14) - d_(j+9) - F_(j+1).                 (3)

For a left shift of size r>0, only the new old-coordinate tail
64,...,63+r needs to be determined; original active indices below r
are deleted. For a right shift of size k>0, only the prefix
-1,...,-k needs to be determined; original active indices above
63-k are deleted. One may conclude a new word is equal when all four
predecessor word pairs are equal. This conclusion is applied in the
appropriate induction order, including predecessors created in an
earlier extension step. It is not valid merely because the original
last words or the original first words are equal.

## 4. Seven left shifts with equal new tails

Denote the frozen support at index s by S_s. The following maps use
V_i = W_(i+r). The boundary rows are exact instances of (2).

| Source s | r | Target | Tail indices whose differences are zero |
|---|---:|---:|---|
| 0 | 1 | 9 | 64 |
| 1 | 2 | 9 | 64,65 |
| 2 | 3 | 9 | 64,65,66 |
| 4 | 4 | 9 | 64,65,66,67 |
| 6 | 1 | 12 | 64 |
| 7 | 3 | 12 | 64,65,66 |
| 13 | 2 | 12 | 64,65 |

The complete dependency lists for t=64,65,66,67 are respectively

    (62,57,49,48), (63,58,50,49),
    (64,59,51,50), (65,60,52,51),

in the order G,d,F,d. For each row actually used, all original indices
in that list are outside the stated support. Induction provides equality
for any 64 or 65 in the later lists. None of the seven maps deletes an
active original index. Thus the new support is exactly S_s-r, not merely
a subset, and direct comparison gives the stated target. Every active
word is an unchanged actual word pair from W,W'.

## 5. Three right shifts with equal inverse prefixes

Starting with S_0, use V_i = W_(i-k) for k=1,2,3. The inverse dependency
lists at j=-1,-2,-3 are

    (15,13,8,0), (14,12,7,-1), (13,11,6,-2),

in the order d,G,d,F. Every nonnegative index in these three lists is
outside S_0. First d_-1=0, then d_-2=0, then d_-3=0 by (3).
No active word is cropped, because max S_0=58. The new supports are
S_0+1 = S_1, S_0+2 = S_2, S_0+3 = S_4. Therefore feasibility of S_0
implies feasibility of all three targets. Conversely, their left shifts
of size 1,2,3 give S_0 (also checked separately by the independent
exhaustive safe map enumeration). These four supports are equivalent
in feasibility. Their relation to S_9 remains one-way in this proof:
the left maps to S_9 are valid, but no unconditional inverse prefix for
S_9 is claimed. At j=-1 for S_9, (3) instead reads

    d_-1 = d_15 - d_8,

which this support substitution alone does not force to zero.

## 6. The special map S_3 to S_14

Use r=2. The original active index 1 is cropped, leaving twelve active
original pairs. At t=64, the predecessors (62,57,49,48) have exactly
one active pair: index 57 in the direct d term. Thus (2) gives

    d_64 = d_57 != 0.

At t=65 the predecessors (63,58,50,49) are all inactive, hence d_65=0.
The newly created d_64 does not occur in the recurrence at 65; the
smallest lag is two. Therefore the new support is exactly

    {j-2 : j in S_3, j>=2} union {62} = S_14.

The transformed first sixteen words are distinct (in particular new
indices 6,9,10,14,15 are active), and Section 1 proves that all 64 words
are a legitimate actual expansion. This implication does not depend on
the equality classification or an exclusion certificate. Using it to
exclude S_3 does depend on a separately valid exclusion of S_14.

## 7. Coverage and exact independent acceptance scope

Assume the inherited classification: every actual distance-13 pair has
one of the fifteen frozen exact supports. Assume also the independently
verified inherited exclusion of support 14. The seven left maps send
0,1,2,4 to 9 and 6,7,13 to 12. The special map sends 3 to excluded 14.
All other unexcluded indices are 5,8,9,10,11,12. Hence any actual
distance-13 pair yields an actual distance-13 pair on one of these six
representatives. Conversely, a real pair on any representative is
itself a distance-13 pair. Existence of distance 13 is therefore
equivalent, conditional on those inherited premises, to existence on
at least one of the six representatives.

The universal window theorem, distinctness lemma and eleven listed
support maps have complete proofs above. Their finite boundary
substitutions are independently checked by `check_independent.py`.
The checker uses only the standard library and the original frozen
support JSON; it does not execute or import `shift-reduction-v3/check.py`.
The original fifteen-support classification and impossibility of S_14
are explicit external premises, not re-proved by this review. No real
13-word pair, global lower bound 14, full SHA-256 hash result, Lean
compilation, external peer review or originality clearance is claimed.

The optional safe-shift enumeration retains every boundary having two
or more active terms as unknown. It uses independent rank-32 checks of
the original binary small-sigma maps to justify nonzero output for a
single active transformed term. This conservative enumeration proves
only the additional maps it accepts; its completeness is solely for
that specified oracle and offsets -63 through 63. It cannot exclude
more involved cancellations or prove that no stronger reduction exists.
