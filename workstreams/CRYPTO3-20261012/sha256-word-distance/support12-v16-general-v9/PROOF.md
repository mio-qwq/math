# A strict valuation-16 residue extension and the failure of uniformity

All arithmetic is modulo `2^32`.  Let

```text
f = ROTR7 xor ROTR18 xor SHR3,
g = ROTR17 xor ROTR19 xor SHR10,
F_D(x)=f(x+D)-f(x),  G_D(x)=g(x+D)-g(x).
```

This is a complete author finite proof for the bounded residue set below.
It has not yet received independent review or Lean formalization.

## Theorem

For

```text
q in {1,3,7,9,11,17,19,29,31},  D=q*2^16,
```

there are no words `x,y` satisfying

```text
F_D(x)=F_D(y),
G_D(y)-G_D(x)=2D.
```

The same holds for `-D`: reverse both directed pairs.  Equality of the
sigma0 derivatives is preserved after both are negated, while negating
and swapping the two sigma1 derivatives restores the `2D` orientation.
Thus the selected twin requirement, and hence the selected three-pair
joint-image core, is excluded for these eighteen signed residues.

This strictly extends the independently accepted `q=1` result, but does
not cover the whole exact-valuation-16 layer.

## Exact finite cover

For each of all sixteen odd `q` in `1..31`, addition by `D=q*2^16`
leaves the low half unchanged.  The checker exhausts every upper word
`u=0..65535`, grouping it by

```text
alpha=(u xor (u+q mod 2^16))<<16.
```

For each group it records every fixed upper input coordinate.  It checks
that all members satisfy these coordinate equations and that the group
size is exactly the size of the resulting affine cube.  Distinct groups
partition all `2^16` upper words; the two low halves remain free.  The
Cartesian square of these exact cubes therefore covers every ordered
word pair `(x,y)`, not a sampled family.

The checker constructs the 64 small-sigma rows from their rotation and
shift definitions and compares every basis image with a separate direct
implementation.  For a fixed XOR class, a toggled output bit contributes
`1-2b`; an untoggled bit contributes zero.  At each bit the exact truth
table of the at-most-two toggled row values and the incoming integer carry
is enumerated.  Any affine compression is checked by reconstructing its
whole truth table.  GF(2) insertion either retains the exact affine leaf
or stores an XOR of original equations equal to `0=1`; every stored
contradiction is checked directly.

The complete positive-q classification is:

| q | input classes | F leaves | twin leaves | result |
|---:|---:|---:|---:|---|
| 1 | 16 | 414 | 0 | excluded |
| 3 | 29 | 3,123 | 0 | excluded |
| 5 | 41 | 3,495 | 3 | survives |
| 7 | 40 | 2,310 | 0 | excluded |
| 9 | 51 | 3,277 | 0 | excluded |
| 11 | 63 | 10,057 | 0 | excluded |
| 13 | 62 | 10,054 | 2 | survives |
| 15 | 49 | 2,345 | 4 | survives |
| 17 | 59 | 3,983 | 0 | excluded |
| 19 | 82 | 31,014 | 0 | excluded |
| 21 | 93 | 33,495 | 4 | survives |
| 23 | 81 | 28,467 | 2 | survives |
| 25 | 80 | 28,634 | 2 | survives |
| 27 | 91 | 47,541 | 4 | survives |
| 29 | 79 | 45,225 | 0 | excluded |
| 31 | 56 | 9,874 | 0 | excluded |

All 21 surviving affine leaves yield 21 distinct actual fixtures.  Each
fixture is directly evaluated, and four one-bit damages to every fixture
are rejected.  `CERTIFICATE.json` freezes all class sizes, counts,
contradiction totals and fixtures.

## Why the q=1 bit-30 obstruction is not uniform

For `q=1`, the accepted v8 frontier reaches bit 30 with odd incoming
carry while both toggled g-mask bits are one.  The two derivative
contributions have even difference, so the bit equation cannot close.

For `q=5`, a full counterexample to that attempted generalization is

```text
D=00050000
x=0ffb000a, x+D=1000000a
y=0ffb0002, y+D=10000002
F_D(x)=F_D(y)=40406e02
G_D(x)=1ff8913e, G_D(y)=2002913e
G_D(y)-G_D(x)=000a0000=2D.
```

Both input XOR masks equal `1ffb0000`, whose g-image is `e007f2c2`.
At bits 29, 30 and 31 the two toggled base bits agree and the incoming
carry is zero.  Hence the parity contradiction used at `q=1` is absent;
the fixture survives all 32 bits.  This is an actual pair-level witness,
not merely an affine leaf, but it is not a message pair.

## Stronger-core screening is only an observation

The 21 frozen twin fixtures were used in 42 preregistered Z3 4.15.3
queries: one query for the required third joint-image member and one for
the reciprocal sigma0 edge per fixture.  All returned `unsat` in under
0.006 seconds each.  No checkable UNSAT certificate was produced, so none
of those observations is used in the theorem.  In particular this stage
does not exclude the full three-pair or four-pair system for the seven
surviving q values.

## Replay and exact scope

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-general-v9/check.py --negative
```

Only Python's standard library is used by the proof replay.  The proof
does not assert all valuation-16 residues, all 48 support rows, base
completion, a distance-13 message pair, or distance at least 14.

