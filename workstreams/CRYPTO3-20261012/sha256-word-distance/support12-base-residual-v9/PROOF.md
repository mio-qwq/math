# Exact elimination of residual row 57

Status: complete author-written lemma, checked against the accepted v8 base
chart and the corrected v9 endpoint factorisation.  Independent review is
separate.  No existence claim is made.

All arithmetic is in `R=Z/(2^32)`.  Write `f=sigma0`, `g=sigma1`.  Let
`C(u,p)` be the accepted support-12 completion chart, where

```
S={10,11,13,15,18,20,26,28,29,34,42,43,57},
P={9,12,14,19,22}.
```

It satisfies 46 original recurrence rows and leaves precisely

```
R33 = C33 - g(C31) - C26 - f(C18) - C17,
R57 = C57 - g(C55) - C50 - f(C42) - C41.          (1)
```

## 1. Sink-coordinate lemma

Fix the twelve active coordinates `u_i`, `i in S\{57}`, and all five
anchors `p`.  The words `C0,...,C56`, and hence `R33`, are independent of
`u57`.  Put

```
H(u_without_57,p) = g(C55) + C50 + f(C42) + C41.   (2)
```

Then for every `u57`

```
R57 = u57 - H.                                    (3)
```

Consequently there is exactly one choice satisfying the second residual,
namely `u57=H`.

**Proof.**  Coordinate 57 belongs to the prescribed active set and is never
a target in the 46-step completion order.  Inspecting every selected row in
that order, a dependency on coordinate 57 occurs only in constructed
coordinates 59, 61, and 63 (and in prescribed coordinate 57 itself).  No
later backward-solving step for a coordinate at most 56 uses any of these
later coordinates.  Thus `C0,...,C56` are independent of `u57`.
Equation (1), with `C57=u57`, immediately gives (3).  The coefficient of
`u57` is the unit 1 in `R`, proving uniqueness.  The checker reconstructs
the dependency sets from the actual frozen order rather than trusting this
description.

## 2. Exact merge with the endpoint factorisation

In the corrected endpoint normal form, write

```
z=d57,    b=G57,
```

and recall that its local word-57 condition is only the projection
`PG(z,b)`: there exists *some* word `x` for which

```
g(x+z)-g(x)=b.                                     (4)
```

After base completion, however, the first endpoint at word 57 is not free:
Section 1 forces it to be `H`.  Therefore the exact merged condition is

```
u57 = H,
g(H+z)-g(H) = b.                                   (5)
```

The private `F57` coordinate remains irrelevant to the 16-to-64 schedule:
it first occurs in recurrence row 72, outside the window.  Hence, conditional
on the other twelve actual pair factors and all additive difference rows,
the combined base/endpoint obligations are exactly

```
R33=0,  u57=H,  g(H+z)-g(H)=b,                     (6)
```

together with the unchanged conditions at the other active words.  Row 57
of the second schedule then follows from row 57 of the first and the already
required difference identity `d57=F42`; row 59 is precisely what requires
the pointwise `G57=b` part of (5).

This is useful because it removes one 32-bit residual equation and one
existential local preimage, but it does **not** remove the word-57 constraint:
it strengthens the projected membership to evaluation at the forced base.

## 3. Why the projection cannot be retained

The implication `PG(z,b) => g(H+z)-g(H)=b` is false.  Take

```
z = 1,
b = g(1)-g(0) = 0x0000a000.
```

Then `PG(z,b)` is true, witnessed by base word `x=0`.  At the different
forced base `H=0x12345678`, direct FIPS evaluation gives

```
g(H+1)-g(H) = 0xffffa000 != b.
```

Thus parameter counting (five anchors versus two residual words), or an
unattached `PG` witness, cannot prove base completion.  Any solver that uses
the ten-scalar factor system must bind the word-57 pair to the `H` produced
by the same base chart.

## 4. Scope

The result neither solves `R33=0` nor proves that (5) can be met.  It gives
no distance-13 message pair, no exclusion of support 12, no distance-14
bound, no Lean formalisation, and no external human verification.

