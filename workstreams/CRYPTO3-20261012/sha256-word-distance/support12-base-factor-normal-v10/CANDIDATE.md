# Candidate support-12 base/factor normal form

**Status: candidate algebraic reduction with seeded substitution checks.**
This package is not a complete written proof, an independent AI acceptance,
a Lean formalization, a SAT/UNSAT result, a message pair, or a support
exclusion.

All arithmetic below is in `R = Z/(2^32)`.  Put

```
D0(x,d) = sigma0(x+d) - sigma0(x),
D1(x,d) = sigma1(x+d) - sigma1(x).
```

The starting merged presentation has ten factor scalars, twelve first
endpoints (word 57 was already eliminated by the accepted sink lemma), and
five base-chart anchors: 27 free words.  The following substitution retains
one root scalar `A` and the twelve endpoints

```
X10,X11,X13,X15,X18,X20,X26,X28,X29,X34,X42,X43.
```

Define, in this order,

```
B = -D0(X10,A),
C = -D1(X43,-B),
K = -D1(X29,C),
P =  D0(X11,B),
Q =  D0(X13,C),
L =  D0(X15,K),
S =  D1(X26,P+A),
W =  D0(X29,C),
Z =  D0(X42,P+A).
```

These definitions are intended to eliminate respectively the original
coordinates `b,c,k,p,q,l,s,w,z`.  The exact-support inequalities become

```
A, B, C, K, P+A, Q+S, Z != 0.
```

## Thirteen retained factor equations

Direct substitution into the accepted v9 factor table leaves

```
15G: D1(X15,K)       = -A,
18F: D0(X18,B)       = -P-A,
18G: D1(X18,B)       = -B-C,
20F: D0(X20,-B)      = -Q-S,
20G: D1(X20,-B)      = -K,
26F: D0(X26,P+A)     = -B,
28F: D0(X28,Q+S)     = -B,
28G: D1(X28,Q+S)     = -L,
34F: D0(X34,B)       = -P-A,
34G: D1(X34,B)       =  B-C,
42G: D1(X42,P+A)     = -W-Q-S,
43F: D0(X43,-B)      = -P-A,
57G: D1(H,Z)         =  B.
```

The nine original equations `10F,11F,13F,15F,26G,29F,29G,42F,43G`
become identities by the displayed definitions.  Thus the 22 original
factor-derivative equations reduce to 13 equations.  This is definitional
elimination only; no division or unproved invertibility is used.

## Candidate base merge

Give the accepted support-12 base chart the active values `U_i=X_i` at the
twelve displayed indices, a temporary `U57=0`, and arbitrary anchors at
`9,12,14,19,22`.  Let its output be `C` and put

```
H = sigma1(C55) + C50 + sigma0(C42) + C41.
```

The independently accepted sink-coordinate lemma says that `H` and `R33`
do not depend on the temporary value of `U57`.  The proposed exact merged
model adds

```
R33 = 0,
D1(H,Z) = B,
```

and replaces the first endpoint at word 57 by `U57=H`.  Its offset is
`d57=Z`, where `Z` is the actual `F` derivative produced at factor 42.  This
is the candidate `42 -> 57` derivative cascade.

If the substitution argument is promoted to a complete proof, the model
will have 18 free words (one root scalar, twelve endpoints, five anchors),
14 word equalities including `R33`, and seven nonzero tests.  The intended
forward direction extracts these variables from two schedules.  The
intended reverse direction reconstructs word 57 at the forced base and then
uses the accepted difference-row and base-chart theorems.  Those universal
directions are stated here only as a proof candidate and have not received
independent acceptance.

## Reproduction and boundary

Run

```
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-base-factor-normal-v10/verify_candidate.py
```

The checker pins the accepted `base_completion.py` by SHA-256, uses seed
`0x0c012e57`, and performs 10,000 substitutions.  It checks the complete
22-to-13 equation map and, in 64 generated contexts, rechecks that changing
the temporary word 57 preserves `H` and `R33` while setting it to `H` zeros
`R57`.

Finite random substitution catches transcription and sign errors but cannot
establish a universally quantified identity.  This package contains no
solver feasibility result and makes no distance-13 or distance-14 claim.
