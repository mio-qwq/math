# Blind full factorization of the support-12 independent-pair problem

**Status: complete written algebraic proof, frozen before author-v8 contact.**
This is an independent-AI review object.  It is exact for the feasibility
problem in which the thirteen active word pairs are independent.  It is not
a SHA-256 base-message completion, a distance-13 message pair, a proof of
distance at least 14, or a Lean formalization.

## 1. Object and conventions

All quantities are in `R=Z/(2^32)`.  Let

```
f(x) = ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x) = ROTR17(x) xor ROTR19(x) xor SHR10(x).
```

For an actual oriented pair `(x,x')`, put

```
d = x'-x,   F = f(x')-f(x),   G = g(x')-g(x)                 (mod 2^32).
```

The exact support is

```
S={10,11,13,15,18,20,26,28,29,34,42,43,57}.
```

For every `16<=t<64`, substitution into the real SHA-256 message expansion
gives

```
E_t = d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16) = 0,           (1)
```

where a term whose index is outside `S` is zero.  The checker reconstructs
all 48 rows directly from (1): exactly 25 are nonzero, at

```
17,18,20,22,25,26,27,28,29,30,31,33,34,35,36,41,42,43,
44,45,49,50,57,58,59.
```

Thus no row was selected from a previously reduced author system.

## 2. Exact fourteen-coordinate linear parameterization

Use fourteen free scalar coordinates

```
a,b,c,e,p,q,r,s,u,v,z10,z11,z13,z57 in R.
```

The complete solution of the 25 additive rows is the following table.
Each row is the triple `(d_i,F_i,G_i)`.

| i | `(d_i,F_i,G_i)` |
|---:|---|
| 10 | `(-a,-b,z10)` |
| 11 | `(b,a-c,z11)` |
| 13 | `(-e,-p-q-r,z13)` |
| 15 | `(-u,-s,a)` |
| 18 | `(b,c,e-b)` |
| 20 | `(-b,q+r,u)` |
| 26 | `(-c,-b,p)` |
| 28 | `(-q-r,-b,s)` |
| 29 | `(-e,q,u)` |
| 34 | `(b,c,e+b)` |
| 42 | `(-c,v,r)` |
| 43 | `(-b,c,e)` |
| 57 | `(v,z57,b)` |

This table is valid over `R`, including wraparound.  It uses no division.

### Completeness proof

Order the 39 variables as `(d_i,F_i,G_i)` in increasing support order.
Starting with the 25 nonzero rows, the independent checker performs only:

1. row swaps;
2. multiplication of a row by `-1`;
3. addition of an integral multiple of one row to another.

It reaches rank 25 using 25 unit pivots and 86 such operations.  The largest
absolute entry in the resulting unimodular row transformation is 1.  Its
fourteen nonpivot coordinates are exactly

```
G10,G11,G13,G15,G26,G28,F29,G29,G42,F43,G43,d57,F57,G57.
```

The checker verifies the full integer identity `U*A=RREF`, not merely its
reduction modulo 2.  It then constructs the 39-by-14 matrix `B` represented
by the displayed table and verifies both

```
A*B=0 over the integers,
projection_of_B_to_the_14_free_coordinates = I_14.          (2)
```

The unit-pivot RREF says every vector in `ker(A)` is uniquely determined by
those fourteen coordinates and has the displayed pivot coordinates.  The
two identities in (2) give the converse.  Hence the table is the exact
kernel over every commutative ring, in particular over `R`; no field-only
rank inference has been used.

## 3. Necessary-and-sufficient ten-scalar actual-pair factor graph

Define the actual joint derivative relation

```
P(d,F,G) iff there exists x in R such that
  F=f(x+d)-f(x) and G=g(x+d)-g(x).
```

Also define its exact projections

```
PF(d,F) iff there exists G with P(d,F,G),
PG(d,G) iff there exists F with P(d,F,G).
```

The support-12 **independent-active-pair problem** is feasible if and only if
there exist ten scalars `a,b,c,e,p,q,r,s,u,v` satisfying

```
a != 0, b != 0, c != 0, e != 0, u != 0, q+r != 0, v != 0, (3)
```

and all thirteen factors

```
position 10: PF(-a,       -b)
position 11: PF( b,        a-c)
position 13: PF(-e,       -p-q-r)
position 15: P (-u,       -s,       a)
position 18: P ( b,        c,       e-b)
position 20: P (-b,        q+r,     u)
position 26: P (-c,       -b,       p)
position 28: P (-q-r,     -b,       s)
position 29: P (-e,        q,       u)
position 34: P ( b,        c,       e+b)
position 42: P (-c,        v,       r)
position 43: P (-b,        c,       e)
position 57: PG( v,        b).                              (4)
```

Conditions (3) are exactly the thirteen support nonzero conditions after
identical `d` forms are merged; no derivative `F` or `G` is required to be
nonzero.

### Why (4) is an equivalence

If thirteen actual pairs satisfy all original expansion rows, Section 2
extracts their unique fourteen coordinates.  Forgetting `G10,G11,G13,F57`
gives the ten scalars and the projected factors in (4), so (3)-(4) are
necessary.

Conversely, choose a witnessing actual pair for every factor in (4).  The
three `PF` witnesses supply `z10,z11,z13`; the `PG` witness supplies `z57`.
All thirteen triples then equal the table in Section 2, so (2) makes all 25
nonzero rows vanish, while the other 23 rows are identically zero.  Condition
(3) makes the support exact.  Thus (3)-(4) are sufficient for the
independent-pair problem.

The word “independent” is essential: this construction does not assert that
the thirteen unprimed words, or the thirteen primed words, extend from a
common pair of 16-word SHA-256 message blocks.  That cross-index completion
constraint is outside this theorem.

## 4. Reproducibility and controls

Run from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-review-v8/check_independent.py --negative
```

The checker is standard-library-only.  It independently implements both the
rotation formula and a direct output-bit formula for `f,g`, and compares them
on fixed edge and mixed words.  It also checks modular parameter samples
including wraparound.

Negative controls deliberately flip the `b` sign in `G34`, omit the `r`
term in `F13`, and remove active position 57.  Each must be rejected.

## 5. Scope boundary

This factor theorem is a complete written proof of an exact reduction.  It
does **not** decide whether the ten-scalar system (3)-(4) is feasible, and a
future SAT/SMT `unknown` or uncertified `unsat` will not change that status.
Likewise, even a satisfying assignment of (3)-(4) would be only thirteen
independent actual word pairs, not yet an actual SHA-256 message pair.

