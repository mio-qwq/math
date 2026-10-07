# 002: Product-weighted rectangular pruning

For two arbitrary finite relations, this note proves a product-weighted bound for a vertex cover of the associated conflict/coverage graph. It yields a conflict-free pruning whose deletion cost is charged to cross-corners and points still uncovered. Nonnegative real weights are allowed; rational inputs have a deterministic exact algorithm. The universal coefficient one is sharp.

Read [paper.md](paper.md) for the complete proof, definitions, zero-weight cases, sharpness examples, and provenance. The rank method comes from the [upstream pruning argument](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/02-pruning.tex), independently proved in this note. The product-weighted lifting and exact certificate workflow are the extensions documented here. Literature priority has not been established.

The proof does not assume the upstream second-neighborhood theorem. [Lean proofs](proof/README.md) certify the complete single-conflict criteria, including a [Mathlib real-cost version and unbounded obstruction](proof/mathlib/README.md); the general rectangular theorem remains unformalized.

[boundary.md](boundary.md) proves that the product assumption cannot be convexified: a sum of two strictly positive product systems already violates both conclusions on one conflict, and no uniform finite coefficient can repair either extension. The obstruction has exact cover and pruning ratios, and its rational family has a complete written proof. The separate exact checker enumerates all covers and feasible prunings of the displayed numerical instance and checks a matching flow certificate. The finite stress results actually run for the main theorem are recorded in [validation.json](validation.json).

## Reproduce

Python 3.10 or later; standard library only. From this directory:

```text
python code/solve.py examples/sharp.json examples/sharp.certificate.json
python code/check_certificate.py examples/sharp.certificate.json
python code/solve.py examples/rational.json examples/rational.certificate.json
python code/check_certificate.py examples/rational.certificate.json
python code/solve.py examples/zero.json examples/zero.certificate.json
python code/check_certificate.py examples/zero.certificate.json
python code/stress.py
python code/check_nonproduct.py examples/nonproduct.json
```

The checker independently rebuilds all conflicts, cross-corners, and network arcs. It verifies exact capacity/conservation constraints, equality of flow value and cover cost, the cover bound, and the pruning bound. A supplied flow and equal-cost cover certify the minimum cover, with no need to trust the search program. These finite checks support reproducibility; the mathematical theorem is proved in `paper.md`.

## Input

Coordinates are integers starting at zero, with sizes specified separately for `P`, `I`, `S`, `J`. Arrays `E`, `F`, `R`, `C` contain relation/family pairs in the order defined in the paper. The four weight arrays `a`, `b`, `c`, `d` contain nonnegative rational strings, such as `"3/7"` or `"0"`. Duplicate pairs are rejected. Example and certificate files are JSON.
