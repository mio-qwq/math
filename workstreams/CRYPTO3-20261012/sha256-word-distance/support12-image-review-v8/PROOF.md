# Independent acceptance: fixed-D joint-fibre obstruction

**ACCEPT**, bound to author manifest SHA-256
`f8166c958baead817204a262dbe0487ca5b856f05b5baa94433f5d69b0ef7c90`.
For the fixed numerical difference `D=0x00010000`, no two actual directed
word pairs in the selected twin core satisfy both

```text
F_D(x) = F_D(y)                              (mod 2^32),
G_D(y) - G_D(x) = 2D                         (mod 2^31).
```

Here `F_D` and `G_D` are the actual modular derivatives of the SHA-256
small sigmas on the same input word.  Thus the first two fibre memberships
in the accepted v7 selected joint-image criterion cannot hold for this D.

## Independent reconstruction

The reviewer checker imports no author code.  It constructs the sigma rows
by evaluating the standard rotations and shifts on all 32 basis words.  For
addition by `2^16`, it analytically constructs the 16 upper-half carry
classes and then directly assigns all `2^16` upper-half values to exactly
one class.  Their sizes are

```text
32768,16384,8192,4096,2048,1024,512,256,128,64,32,16,8,4,2,2.
```

No class equation contains a low-half coordinate, so every one of the
`2^16` lower halves remains free.  This proves that the 16 by 16 mask-pair
enumeration covers all ordered 32-bit pairs `(x,y)`.

For each output bit the checker exhausts the truth table of the at-most-two
toggled sigma bits, independently verifies its exact affine compression,
and inserts the resulting relations with a separately written highest-pivot
GF(2) eliminator.  The full sigma0 equation leaves 414 affine branches.  The
sigma1 gap through bits 0--29 leaves 20 branches.  Their complete bit-30
frontier has the five common masks

```text
07ff0000, 0fff0000, 1fff0000, 3fff0000, 7fff0000,
```

and, for every mask, two leaves at each incoming carry `-1,+1`.  Both sigma1
mask bits at bit 30 are one.  Hence both derivative contributions are odd,
their difference is even, the target bit is zero, and adding the odd incoming
carry cannot give an even digit equation.  All 20 branches die, giving
`414 -> 20 -> 0`.  This is a modulo-`2^31` obstruction; no unexamined bit 31
is needed.

The reviewer also reconstructs a different actual boundary witness:

```text
x=03ff4048, x+D=04004048,
y=abff151a, y+D=ac00151a,
F_D(x)=F_D(y)=402ff313,
G_D(y)-G_D(x)=c0020000.
```

The gap is `0x00020000` modulo `2^30` but `0x40020000` modulo `2^31`.
Therefore bit 30 is genuinely decisive.  Independent weakening controls
give 20 leaves after dropping that bit, 20 after dropping the top sigma0
bit, and 58 after replacing the target gap by zero.  Four damaged frontier
records are rejected.

## Negative orientation and exact scope

Reversing a pair is a bijection from difference `D` to difference `-D` and
negates both modular derivatives.  Reversing both twin pairs preserves their
sigma0 equality and negates their sigma1 gap.  Therefore a solution for
`D=0xffff0000` would reverse to a solution for `D=0x00010000`; the negative
orientation is excluded as well.

This acceptance excludes only fixed `D=+/-0x00010000` in the **selected
twin core**.  It is not an exclusion of every difference with `v2(D)=16`,
not the complete support-12 system, not a 16-word or 64-word message pair,
and proves neither distance-13 attainability nor distance at least 14.  It
is independent AI review, not Lean formalization or human peer review.

Read-only replay from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-image-review-v8/check_independent.py --negative
```
