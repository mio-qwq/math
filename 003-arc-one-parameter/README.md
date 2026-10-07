# Exact ARC core certificate and a conditional one-parameter note

This directory contains two verified components and one explicitly conditional
application:

1. An exact polynomial certificate for the finite algebra and 179-entry
   Hochschild cochain in OpenAI family 199. The checker verifies associativity,
   the symmetric form, every radical four-word, the twisted boundary identity,
   and the explicit nonzero cycle pairing. These are identities over
   `F_2[q]`, not numerical specializations.
2. A proved abstract extension-spectrum theorem. Under the stable-profile and
   twist-action hypotheses stated in [paper.md](paper.md), the converted
   module's positive self-Ext groups have an exact multiplicative-order
   classification, including a rational generating function.
3. A **conditional application** to the upstream ARC construction: replacing
   its independent parameters by `q=t, H_1=1, H_2=t` would give a construction
   over `F_2(t)`. This application still depends on the upstream infinite
   homological realization; the finite checker does **not** verify that
   realization or prove the complete ARC counterexample.

The note does not claim mathematical priority or a newly established
unconditional counterexample to Auslander--Reiten.

[Lean kernel certificates](proof/README.md) now cover the explicit algebra tables, trace pairing, cycle, boundary data and all 104976 radical four-word closure identities. The formalization scope and remaining semantic bridges are stated there separately from the Python certificate. The final universally quantified closure theorem depends only on standard `propext`; no certificate uses `sorry`, added axioms or `native_decide`.

The additional [Mathlib semantic layers](proof/mathlib/README.md) connect the scalar codes, byte packing and sparse products to genuine polynomial vectors. The actual twenty-coordinate multiplication is associative and has the two-sided unit e+f on **all** vectors, including every specialization in an arbitrary commutative characteristic-two ring. Its trace pairing has an exact dual-coordinate formula, is symmetric and left/right nondegenerate, and satisfies invariance and cyclic trace identities. The multiplication is now packaged as a genuine unital `Ring` and `Algebra R`, with an explicit 20-element basis and dimension 20 over every characteristic-two field. The homological realization remains separate; these results do not establish the complete ARC counterexample.

## Reproduce the exact certificate

Further formalized structure includes [perfect trace duality on the actual algebra](proof/mathlib/TwentyDimFrobenius.README.md), the actual [five-face cochain identity on arbitrary radical-span vectors](proof/mathlib/TwentyDimCochain.README.md) under every characteristic-two specialization, and a universal [full vector-valued boundary obstruction](proof/mathlib/CochainFullBoundary.README.md). The nonzero witness is q³, so the obstruction requires q³ to remain nonzero. These are precise intermediate results; the complete complex and Ext interpretation remain open.

Python 3.9 or later, standard library only:

```console
python checker/verify.py
python checker/verify.py --output results/verification.json
```

Expected coverage: `8000` basis triples, `104976` radical four-words,
`15250` composable four-words, `324` radical input pairs, `179` nonzero
cochain entries; cycle pairing `q^3 f`.

The [saved result](results/verification.json) states the verification scope and
records SHA-256 of the [fixed input](data/arc-core.json). Both flags concerning
verification of the complete ARC realization are deliberately `false`.

## Files and provenance

- [paper.md](paper.md): definitions, proof of the abstract spectrum formula,
  proof interpretation of the finite certificate, conditional specialization,
  and remaining verification gap.
- [checker/verify.py](checker/verify.py): new standalone exact checker.
- [data/arc-core.json](data/arc-core.json): finite data transcribed from
  OpenAI's algebra and cochain tables, with source hashes.
- [ATTRIBUTION.md](ATTRIBUTION.md): exact upstream version and license.

Upstream source is pinned to commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
