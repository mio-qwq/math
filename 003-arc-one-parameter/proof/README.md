# Lean kernel certificates for the fixed finite tables

The files here use **Lean 4.34.1 and Std only**. The proofs use ordinary
`decide`, whose proof terms are checked by Lean's kernel. They do not use
`sorry`, added axioms, `native_decide`, or a compiler-trust axiom.
`#print axioms` reports the dependencies of each main theorem; standard
`propext` occurs in some reductions.

## Verified first stage: `FiniteCore.lean`

```console
lean 003-arc-one-parameter/proof/FiniteCore.lean
```

Run from the repository root with its pinned `lean-toolchain`.

The file defines the complete ten-letter table for `C`, with basis order
`e,x,y,z,u,v,t,j,f,n`. Coefficients are natural-number bit sets: bit `i`
represents the coefficient of `q^i` over `F_2`. Its recursively defined
`pMul` is carryless polynomial convolution. Eight bits per output basis
coordinate are used to pack a finite vector.

The kernel proves the equality of the packed left and right products on
**every one of the 1000 basis triples**, verifies all output basis labels,
checks the left-path composed coefficient bound `<256`, and checks
`utu=(1+q)v` and `utut=(q+q^2)z` in this representation. The additional
right-path bound is included in the subsequent certificate when available.

**Formalization boundary:** these are equalities about the explicit Lean
definitions of bit-polynomial computations and packed vectors. This first
file does not construct the abstract ring `F_2[q]`, a scalar-extension
interpretation into arbitrary fields, a Lean algebra instance, or the
homological ARC construction. Its theorem is not a formal proof of the
complete Auslander--Reiten counterexample. The finite mathematical meaning
and upstream provenance are discussed in `../paper.md` and
`../ATTRIBUTION.md`.

The data source is OpenAI family 199 at commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The Lean table was transcribed
from the fixed `../data/arc-core.json`; its corresponding source hashes
are recorded there.
