# Attribution and scope

The ten-dimensional algebra `C`, its trivial extension `T`, the 179 nonzero
cochain entries, the bar cycle, and the twisted boundary formula are due to
OpenAI, *An explicit counterexample to the Auslander--Reiten conjecture*,
September 23, 2026, family 199.

Pinned source:

- Repository: <https://github.com/openai/math>
- Commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`
- Source directory:
  `preprints/An-explicit-counterexample-to-the-Auslander-Reiten-conjecture-September-23-2026/build/`
- Finite source files: `03-algebra.tex` and `09-cochain.tex`.
- Relevant homological source files: `02-conversion.tex`, `04-resolution.tex`,
  `05-cones.tex`, `06-lift.tex`, `07-branches.tex`, `08-consequences.tex`.

The upstream repository is licensed under Apache License 2.0. The data file
explicitly transcribes the finite mathematical tables and records source
hashes. The checker implementation and exposition in this directory were
written for this certificate. They do not replace or verify the entire
upstream manuscript.

The abstract spectrum theorem extends the upstream short exact sequence
labelled `conv:end-cohomology` by computing its kernels and cokernels when
the twist ratio has finite order. The one-variable application remains
conditional on the upstream realization and all-degree profile assertions.
No first-proof, novelty, or priority claim is made.

## Lower-algebra formalization and prior mathematical results

The compiled OpenAI manuscript places the lower-algebra calculation in
Section 5, Lemma 5.1 (`res:base` in `04-resolution.tex`). The source
filename's number is not the compiled section number. The following
mathematical statements already occur there:

| Prior mathematical statement | Actual Lean implementation here |
| --- | --- |
| The resolution with Cf in degree zero, Ce in every positive degree, and the specified u/ell maps | `LowerAlgebraResolution`, `LowerAlgebraProjective`, `LowerAlgebraCategoricalResolution` |
| All positive Ext_C(s,s) vanish | `LowerAlgebraCategoricalResolution` |
| Evaluation identifies Hom_C(Ce,C) with eC and Hom_C(Cf,C) with fC | `LowerAlgebraRegularHom` |
| Ext_C(s,C) is concentrated in degree two and is a one-dimensional right f-simple | `LowerAlgebraRegularExt` proves the actual Ext profile and scalar equivalence; `LowerAlgebraRegularRightAction` proves the actual right-character action |

These implementations construct the actual corners, complete maps,
specified projective resolution and Mathlib Ext classes, and prove the
required comparison and boundary statements. They are formalization
contributions; the table does not present its underlying mathematical
statements as new discoveries. A separate bundled right-module
equivalence, the trivial-extension derived triangle and the full
twenty-dimensional Ext algebra are still absent from the formalization.
The source files retain explicit assumptions for each result; in
particular the complete regular-target profile requires q nonzero,
whereas the resolution and its positive self-Ext vanishing do not.

Qiyue Tang, [*A note on counterexamples to homological conjectures*,
Hexagon 2610.00143v1](https://hexagonmath.org/pdf/2610.00143v1),
7 October 2026, Proposition 3.2 (p. 5), also gives the lower resolution
and both Hom cohomology calculations. Its signed algebra uses
`1-q^m` in arbitrary characteristic; in characteristic two its displayed
lower multiplication specializes to the one used here. Theorem 1.1
and Corollary 1.2 state a much broader counterexample construction over
fields containing an element of infinite multiplicative order, using a
twisted dual construction. Our current characteristic-two Lean work
does not verify that full theorem or claim priority for its base-field
extension. The original PDF labels the manuscript a public discussion
draft. Neither public availability nor the comparisons above substitute
for an independent audit of its surrounding counterexample proof.
