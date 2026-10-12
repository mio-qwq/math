# Blind derivation of an exact 18-word support-12 message normal form

**PRE-AUTHOR freeze.**  This document was derived before reading any future
author proof in `support12-base-factor-normal-v11/`.  Its only inputs are the
accepted/frozen full-factor v9 theorem, base interpolation v8 theorem and
row-57 residual merge v9 theorem.  It is not a satisfiability result, a
distance-13 witness, a distance-14 lower bound, or a Lean formalisation.

All arithmetic below is in `R=Z/(2^32)`.  Put

```
f(x)=ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x),
D0(x,d)=f(x+d)-f(x),   D1(x,d)=g(x+d)-g(x).
```

## 1. Base chart and its independence boundary

Use the accepted v8 anchors

```
P={9,12,14,19,22}
```

and prescribe first endpoints at the twelve active positions

```
T={10,11,13,15,18,20,26,28,29,34,42,43}.
```

The rewritten 47-row chart from the accepted v9 residual merge takes these
17 words as inputs, solves row 57 for coordinate 57, and leaves only row 33
unused.  Denote its output by `C`, put `U_i=C_i` for `i in T`, and put

```
H=C57=g(C55)+C50+f(C42)+C41,
R33=C33-g(C31)-C26-f(C18)-C17.
```

The dependency calculation has no `u57` input at all: `H` and `R33` depend
only on the twelve `U_i` and five anchors.  In particular both are
independent of the additional factor word `z` introduced below.  The first
sequence is a genuine SHA-256 expanded schedule exactly when `R33=0`.

## 2. Starting 27-word system and the 22 local equalities

Before elimination, combine those 17 base inputs with the ten shared factor
coordinates

```
a,b,c,k,p,q,l,s,w,z.
```

The accepted full-factor table prescribes the following differences and
small-sigma images at the thirteen active positions:

| i | d_i | F_i | G_i |
|---:|---|---|---|
|10|a|-b|private|
|11|b|p|private|
|13|c|q|private|
|15|k|l|-a|
|18|b|-p-a|-b-c|
|20|-b|-q-s|-k|
|26|p+a|-b|s|
|28|q+s|-b|-l|
|29|c|w|-k|
|34|b|-p-a|b-c|
|42|p+a|z|-w-q-s|
|43|-b|-p-a|-c|
|57|z|private|b|

Binding this table to the common first endpoints gives exactly 22 local
coordinate equalities: one `F` equality at each of 10, 11 and 13; two
equalities at each of 15, 18, 20, 26, 28, 29, 34, 42 and 43; and the
pointwise `G` equality at 57.  The last is specifically

```
D1(H,z)=b,
```

not the existential projection `PG(z,b)`.

## 3. Nine triangular definitions

Five of the 22 equations define private/shared image coordinates:

```
p=D0(U11,b),  q=D0(U13,c),  l=D0(U15,k),
s=D1(U26,p+a),  w=D0(U29,c).                       (A)
```

Four more equations have unit coefficients in a triangular order:

```
b= D1(H,z),
k=-D1(U20,-b),
a=-D1(U15,k),
c=-D1(U43,-b).                                    (B)
```

No inversion of `f`, `g`, or a modular coefficient occurs in (A)--(B).
Thus (A) removes five words and five equations, and (B) removes four more
words and four more equations.  Starting from 27 words and 23 equations
(the 22 local equations plus `R33=0`), this leaves 18 words and 14 equations.
Equivalently, the 22 local factor equations on thirteen positions reduce
exactly to the following thirteen equations.

## 4. Exact reduced system

The free words are the twelve `U_i`, the five anchors, and `z`.  Construct
`C,H,R33` with the rewritten base chart, then define `b,k,a,c,p,q,l,s,w` by
(B) and (A).  Require

```
R33 = 0,                                                   (R)

D0(U10,a)              = -b,                              (10F)
D0(U18,b)              = -p-a,                            (18F)
D1(U18,b)              = -b-c,                            (18G)
D0(U20,-b)             = -q-s,                            (20F)
D0(U26,p+a)            = -b,                              (26F)
D0(U28,q+s)            = -b,                              (28F)
D1(U28,q+s)            = -l,                              (28G)
D1(U29,c)              = -k,                              (29G)
D0(U34,b)              = -p-a,                            (34F)
D1(U34,b)              =  b-c,                            (34G)
D0(U42,p+a)            =  z,                              (42F)
D1(U42,p+a)            = -w-q-s,                          (42G)
D0(U43,-b)             = -p-a.                            (43F)
```

Exact support additionally requires precisely the seven distinct difference
classes

```
a, b, c, k, p+a, q+s, z
```

to be nonzero.  Every `d_i` in the table is one of these values or its
negative, and every class occurs, so these seven conditions are necessary
and sufficient for the active set to be exactly the frozen support.

## 5. Forward and reverse implications

**Original to reduced.**  Given two genuine schedules with exactly this
support, project the first schedule to the twelve active inputs and five
anchors and put `z=d57`.  Base-chart uniqueness reconstructs the first
schedule and gives `R33=0` and `C57=H`.  The actual pairs define the ten
factor coordinates.  The nine selected local equalities force (A)--(B), in
the displayed order; the remaining local equalities are exactly the thirteen
reduced factor equations.  Exact support gives the seven nonzero classes.

**Reduced to original.**  Given the eighteen free words satisfying (R), the
thirteen factor equations, and the seven nonzero conditions, the rewritten
chart gives a genuine first schedule.  Definitions (A)--(B) restore all
nine eliminated local equalities, including the pointwise position-57
condition at the same forced endpoint `H`.  Together with the remaining
thirteen equations, every displayed `(d,F,G)` is realised by the actual pair
`(U_i,U_i+d_i)` (and `(H,H+z)` at 57).  The accepted full-factor theorem
then zeros all 48 schedule-difference rows.  Keeping inactive words equal
therefore produces a genuine second schedule.  The seven nonzero classes
make its expanded-word support exactly the thirteen frozen positions.

The first sixteen words of the two schedules are consequently a pair of
message blocks.  This is an equivalence only: it does not show that the
fourteen equations and seven inequations possess a solution.

## 6. Certification boundary

`check_pre_author.py` reconstructs the rewritten chart without importing
author-v11 code, verifies its dependency boundary, checks the 22-to-13
identity after all nine substitutions on deterministic random inputs,
checks the exact seven-class support criterion, reconstructs all additive
difference rows, and runs sign/index damage controls.  These finite checks
support the displayed algebra; the universal claim is the written
triangular proof above.

Status at this freeze: independent AI derivation, pre-author.  No author
comparison has yet occurred; no Lean or human certification is claimed.
