# Unit triples and the zero Fourier mode obstruction

The [Lean source](proof/UnitTripleZeroSum.lean) proves the phase geometry and
bounded-mode part of Section 2 of [the four-circulant written proof](direct-circulant-character.md).
It uses actual complex numbers and `Complex.normSq`; it does not use an
enumeration of phase samples or add a classification hypothesis.

If x,y,z have squared modulus one and x+y+z=0, then

    x²+xy+y²=0,    r=y/x,
    r²+r+1=0,     r³=1,    r≠1,
    y=xr,        z=xr²,    normSq(r)=1.

Thus the cyclic phase form follows from the unit and zero-sum equations.
Conjugating the sum and multiplying by xyz first gives xy+xz+yz=0;
the quadratic relation and ratio classification follow algebraically.
At any fixed primitive cube root omega, r is omega or omega². Accordingly
one of x+y omega+z omega² and x+y omega²+z omega equals 3x and has normSq 9.
If both squared mode bounds are at most 6, x+y+z cannot vanish.

The source also proves an arbitrary-root version that avoids choosing an
exponential or enumerating roots. For a unit triple (a0,a1,a2), suppose

    normSq(a0+a1 eta+a2 eta²) ≤ 6   for every eta³=1.

Then a0+a1 theta+a2 theta² is nonzero for every theta³=1, including theta=1.
Every complex cube root of one has normSq one; this is itself proved.
If a theta-mode vanished, the modulated triple
(a0,a1 theta,a2 theta²) would give a unit ratio r with r³=1.
Taking eta=theta/r makes a1 eta=a0 and a2 eta²=a0, contradicting
the bound with the exact amplitude 3a0 and normSq 9.
The modulated triple has the zero-sum classification; the original triple
need not itself be a permutation of the three distinct cube roots.

There are six audited declarations. The attached [audit](proof/UnitTripleZeroSum.audit.txt)
and [actual compiler record](proof/UnitTripleZeroSum.verification.json) document
the exact source, author compilation and separate reviewer replay.
The standard phase geometry is a supporting ingredient, with no historical
originality claim. It is not a solution of the general MUB conjecture.

The subsequent [actual Gram and block-inverse proof](gram-block-invertibility.md)
now derives these bounds from the six-by-six matrix equations and constructs
all four block inverses. This unit-triple file itself remains the conditional
scalar interface. Phase retrieval and the final Gram-to-product-cancellation
theorem remain written mathematics.

From the existing fixed `002-weighted-rectangular-pruning/proof/mathlib` package:

```powershell
lake env lean ../../../004-mub-triplets/proof/UnitTripleZeroSum.lean
```

Lean 4.34.1 and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`
are unchanged. The source imports no other project module.
