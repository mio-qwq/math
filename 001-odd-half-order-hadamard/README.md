# Odd half-order power Hadamard rigidity

For every odd integer `m >= 3`, we prove that a complex matrix of order `2m` whose entrywise powers `1,...,m-1` are all complex Hadamard becomes an `m`th-root matrix after dephasing. In fact, its row differences give a generalized Hadamard matrix over the cyclic group of order `m`, with multiplicity two. This is an exact characterization, not a numerical observation.

- [Full theorem, definitions, and proof](paper.md)
- [Exact root/block classification and exhaustive phase-circle construction for all half-orders](general-patterns.md)
- [Finite graph of labelled dephased solutions, actual local branches and tangent lines](phase-geometry.md)
- [Exact finite example checker](code/check_examples.py)
- [Lean certificate for the integer obstructions](proof/Parity.lean)
- [Kernel-checked exponent certificates and phase invariants](proof/Examples.lean)
- [Formal four-phase collapse and odd support obstruction](proof/Support.lean)
- [Actual complex block obstruction, exact half-ranks and singularity in pinned Mathlib](proof/mathlib/README.md)
- [Actual two-polygon polynomial products and row-ratio obstruction in Lean](proof/mathlib/RowProductObstruction.README.md)

The proof extends the order-six support argument in OpenAI's *Exact Fourier certificates for complex Hadamard matrices of order six*, at pinned upstream commit [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a). The general odd-half-order theorem, the projection argument, and the cyclic-group characterization are proved here. We make no claim of historical priority.

Run the dependency-free finite checker with Python 3:

```sh
python code/check_examples.py
```

It checks a positive example at `m=3`, the even-half-order counterexample `F_4`, and the failure of the hypothesis for `F_6` when its square is included. It uses polynomial arithmetic over the integers modulo cyclotomic polynomials, with no floating-point values. These checks validate the displayed examples; the all-parameter theorem is proved analytically in `paper.md`.

`proof/Parity.lean` formalizes three integer steps: an odd number cannot be twice an integer, the corresponding support multiplicity obstruction, and the projection trace equation after clearing denominators. It was compiled with Lean `4.34.1` and uses only standard Lean axioms (`propext` and `Quot.sound`), with no `sorry`. It does **not** formalize the complex-matrix argument, Newton identities, or the full main theorem. To replay it with Lean installed, run:

```sh
lean proof/Parity.lean
```

The exponent range `1,...,m-1` is sufficient. No minimality claim about that range is made. The order-four example shows that oddness cannot simply be removed from the theorem as stated.

For every m>=2, the stronger analytical classification eliminates the
binary quotient branch of the earlier necessary trichotomy. Each
nonroot solution is obtained by multiplying a compatible balanced
rectangle of a cyclic GH(m,2) root seed by one unit phase. For fixed m,
the dephased solutions form a finite union of root points and these phase
circles; odd half-orders have no such circles. This is an exhaustive
construction under the full power hypotheses, without asserting seed
existence at new even orders. Its matrix proof is written; the new Lean
file verifies the actual polynomial product obstruction supporting it.

The labelled, dephased solution space is homeomorphic to a finite graph:
distinct phase circles meet only at root matrices, each circle contributes
m arcs, and nonroot points have smooth one-dimensional neighborhoods.
Root vertices have twice as many branches as compatible rectangles.
This is a complete written geometric consequence of the classification;
it does not identify the kernel of the linearized Hadamard equations.
