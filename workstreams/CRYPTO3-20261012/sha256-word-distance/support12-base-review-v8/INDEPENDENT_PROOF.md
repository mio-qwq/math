# Blind independent support-12 base-coordinate elimination

**PRE-AUTHOR result.** This derivation and its checker were frozen before
reading any file from `support12-base-lift-v8`.  It starts only from the
original SHA-256 message-schedule recurrence and the frozen support-12 index
set.  It is a base interpolation theorem, not a construction of the active
pairs and not a distance-13 message-pair result.

All words lie in `Z/(2^32)`.  Put

```
f(x) = ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x) = ROTR17(x) xor ROTR19(x) xor SHR10(x).
```

For `16 <= t < 64` write the original row as

```
R_t(W) = W_t - g(W_(t-2)) - W_(t-7)
               - f(W_(t-15)) - W_(t-16).
```

The frozen support-12 coordinates are

```
S = {10,11,13,15,18,20,26,28,29,34,42,43,57}.
```

Here the thirteen values `W_i`, `i in S`, are arbitrary specified first
endpoints of candidate active pairs.  Nothing below asserts that the second
endpoints exist or that these thirteen values obey the support difference
equations.

## Exact elimination

Choose five free inactive anchors

```
A = {21,22,23,24,32}.
```

Starting with the values on `S union A`, apply the 46 ordered `(row,target)`
pairs in `COORDINATE-CERTIFICATE.json`.  At every step the target is the
only coordinate in that row not already known.  If it occurs as `W_t`,
`W_(t-7)`, or `W_(t-16)`, ordinary modular addition uniquely isolates it.
If it occurs inside `f(W_(t-15))` or `g(W_(t-2))`, invert `f` or `g`.

The checker reconstructs both 32 by 32 binary matrices from the displayed
bit definitions.  Gaussian elimination gives rank 32 for each, and all 64
basis compositions in both directions are checked.  Hence `f` and `g` are
permutations of 32-bit words and every one of the 46 steps is a genuine
unique reverse operation.  The step types are:

| reversible occurrence | count |
|---|---:|
| output identity `W_t` | 21 |
| additive `W_(t-7)` | 3 |
| additive `W_(t-16)` | 11 |
| `f` inverse | 3 |
| `g` inverse | 8 |

After these steps all 64 coordinates are known.  Exactly rows 33 and 57
were not used for reconstruction.

## Equivalence

For every assignment of the thirteen specified values on `S` and the five
anchor values on `A`, the ordered elimination returns one and only one word
vector `W`.  By construction it obeys the 46 used recurrence rows.  It is an
actual SHA-256 expanded schedule exactly when

```
R_33(W) = 0  and  R_57(W) = 0.                 (1)
```

Necessity follows because every actual schedule obeys all 48 rows.
Sufficiency follows because the construction already imposed the other 46.
Uniqueness is stepwise uniqueness in reverse order.  Thus existence of a
base schedule with the specified `S` values is equivalent to existence of
five anchors satisfying the two exact residual equations (1).

This theorem does **not** show that the two residuals have a simultaneous
solution for any candidate active data.

## Minimality inside the explicit propagation class

The checker exhausts all inactive anchor subsets of cardinality 0 through 4:

```
1 + 51 + 1275 + 20825 + 249900 = 272052.
```

For each subset it repeatedly asks whether an unused original five-coordinate
row has exactly one unknown.  None determines all 64 coordinates.  The
five-anchor set above does.  Since a completed elimination using `a` anchors
uses `51-a` rows and leaves `48-(51-a)=a-3` residual rows, this proves that
five anchors and two residuals are minimal in this precise one-row reversible
propagation class.

This is not a claim of minimality among arbitrary combinations of nonlinear
rows, auxiliary variables, or other coordinate systems.

## Roundtrip and controls

The checker expands deterministic genuine 16-word SHA-256 inputs, retains
only the 13 fixed coordinates and five anchors, reconstructs the other 46
coordinates, and obtains the exact original 64-word schedule with both
residuals zero.  These are ordinary single schedules used to test the
coordinate chart; they are not two messages at distance 13.

Negative controls damage a solve target, omit a residual, alter an inverse
column, and alter a fixed roundtrip coordinate.  Each is rejected.  The
checker uses only the Python standard library and does not import author code
or a solver.

Run from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-base-review-v8/check_independent.py
```

Scope exclusions: no residual solution, no full message pair, no proof that
distance 13 is attainable, no lower bound 14, no Lean formalization, and no
human peer review.
