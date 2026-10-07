# Formalization status

The Lean files are pinned to Lean `4.34.1`. Most use its bundled `Std` library; the isolated `proof/mathlib` packages pin Mathlib as well. All statements below have been compiled locally, and their axiom lists are printed by their source files. None uses `sorry`, an added axiom, or `native_decide`.

| File | Exact formal statement | Boundary |
| --- | --- | --- |
| [001/proof/Parity.lean](001-odd-half-order-hadamard/proof/Parity.lean) | Oddness, support multiplicity and cleared projection-trace equations are incompatible | Does not construct the complex projection or prove its trace formula |
| [001/proof/Examples.lean](001-odd-half-order-hadamard/proof/Examples.lean) | Cubic six-by-six row/column difference counts, their squares, Fourier-four opposite-root counts and fourth-root phase invariants | Exponent certificates; no formal bridge to complex matrices or the general rigidity theorem |
| [001/proof/Support.lean](001-odd-half-order-hadamard/proof/Support.lean) | Four-phase collapse and the odd support-count obstruction for every phase system satisfying the explicit cancellation laws | The complex-ratio and Newton-identity hypotheses are not yet connected to this abstract statement |
| [001/proof/mathlib/ProjectionTrace.lean](001-odd-half-order-hadamard/proof/mathlib/ProjectionTrace.lean) | Every finite-dimensional idempotent over a characteristic-zero field has integral trace, excluding the odd half-trace equation | Uses pinned Mathlib; construction from the Hadamard blocks is still separate |
| [001/proof/mathlib/BlockObstruction.lean](001-odd-half-order-hadamard/proof/mathlib/BlockObstruction.lean) | Actual complex Gram blocks with unit squared moduli and the stated orthogonality equations cannot have odd size; the projection and trace are constructed in Lean | Newton identities and the construction of the blocks from the original matrix remain to be formalized |
| [001/proof/mathlib/BlockRanks.lean](001-odd-half-order-hadamard/proof/mathlib/BlockRanks.lean) | The actual Gram equations force `2 * A.rank = m` and `2 * B.rank = m` for every positive size; both determinants vanish | Only A needs unit squared moduli; the original Hadamard-to-block construction remains separate |
| [001/proof/mathlib/ComplexSupport.lean](001-odd-half-order-hadamard/proof/mathlib/ComplexSupport.lean) | Actual nonzero complex four-phase and row-ratio collapse to `-1`; the resulting multiplicity of one is `2*t` and cannot equal odd m | Instantiates the abstract cancellation laws correctly on the nonzero subtype; Newton/Hadamard hypotheses and multiplicities still require a bridge |
| [002/proof/SingleConflict.lean](002-weighted-rectangular-pruning/proof/SingleConflict.lean) | For every four natural-number costs, cover and pruning feasibility have the stated exact criterion; the scaled nonproduct example fails both | The full arbitrary rectangular rank argument and arbitrary real weights are not formalized |
| [002/proof/mathlib/SingleConflictReal.lean](002-weighted-rectangular-pruning/proof/mathlib/SingleConflictReal.lean) | Exact real-cost cover/pruning thresholds and attained minimum; for every finite real K, two actual positive product systems defeat both bounds with coefficient K | Complete single-conflict obstruction; the general rectangular theorem remains unformalized. The rational-witness strengthening is supplied by the written proof |
| [002/proof/mathlib/RationalObstruction.lean](002-weighted-rectangular-pruning/proof/mathlib/RationalObstruction.lean) | For every real K ≥ 0, an actual positive rational coordinate witness produces two positive product systems defeating every cover and pruning bound | Formalizes the rational-witness strengthening; the general rectangular theorem remains separate |
| [002/proof/mathlib/ExactObstructionRatios.lean](002-weighted-rectangular-pruning/proof/mathlib/ExactObstructionRatios.lean) | Exact necessary-and-sufficient cover and pruning coefficients for every positive real parameter, including equality; their difference is a nonnegative square ratio | Full parameter family under the explicit two-product construction; no classification of general nonproduct systems |
| [003/proof/FiniteCore.lean](003-arc-one-parameter/proof/FiniteCore.lean) | All 1,000 basis triples of the explicit ten-dimensional table have equal encoded products, with output and coefficient bounds and two radical products | Fixed bit-polynomial table identities; the interpretation as a field algebra and the complete ARC realization are not formalized |
| [003/proof/FiniteCoreT.lean](003-arc-one-parameter/proof/FiniteCoreT.lean) | All 8,000 twenty-dimensional basis triples, both coefficient bounds, the dual recurrences, unit actions and all 400 trace pairings | Same fixed bit-polynomial scope; not the complete ARC realization |
| [003/proof/CochainData.lean](003-arc-one-parameter/proof/CochainData.lean) | The 179-entry cochain, coefficient bounds, the concrete internal bar differential and its nonzero encoded pairing | Does not yet turn the encoded data into formal Ext or cohomology objects |
| [003/proof/CochainBoundary.lean](003-arc-one-parameter/proof/CochainBoundary.lean) | Constant and linear boundary coefficients on all 324 radical input pairs | Fixed exact polynomial certificates; no arbitrary-field or full ARC realization |
| [003/proof/CochainClosure.lean](003-arc-one-parameter/proof/CochainClosure.lean) | All 104,976 radical four-word closure identities, assembled into a universally quantified theorem from 18 kernel-checked cases | Explicit packed bit-polynomial differential; the formal Hochschild complex and arbitrary-field interpretation remain separate |
| [003/proof/mathlib/BitPolynomial.lean](003-arc-one-parameter/proof/mathlib/BitPolynomial.lean) | An injective decoder into `Polynomial (ZMod 2)` sends XOR to addition and the frozen `pMul` to multiplication for every natural-number input; scalar associativity and commutativity follow | Scalar semantics only; packed vectors, the finite algebra instance and the complete homological realization still require bridges |
| [003/proof/mathlib/BytePacking.lean](003-arc-one-parameter/proof/mathlib/BytePacking.lean) | Eight-bit extraction commutes with XOR for all natural-number codes; packing a coefficient below 256 occupies exactly one coordinate, decoded as a genuine F₂ polynomial | Generic coordinate layer; full table sums, the algebra instance and Hochschild/Ext realization remain separate |
| [003/proof/mathlib/TermSemantics.lean](003-arc-one-parameter/proof/mathlib/TermSemantics.lean) | Arbitrary sparse encoded lists, scaled lists and left/right triple products decode as true polynomial-vector sums, under explicit bounds on every packed coefficient; duplicate labels are allowed | Generic list and nested-product semantics; table-specific associativity, algebra instance and Hochschild/Ext remain separate layers |

Replay from the repository root:

```sh
lean 001-odd-half-order-hadamard/proof/Parity.lean
lean 001-odd-half-order-hadamard/proof/Examples.lean
lean 001-odd-half-order-hadamard/proof/Support.lean
lean 002-weighted-rectangular-pruning/proof/SingleConflict.lean
lean 003-arc-one-parameter/proof/FiniteCore.lean
```

To compile `FiniteCoreT.lean`, first build its imported module. In PowerShell:

```powershell
$env:LEAN_PATH = (Resolve-Path '003-arc-one-parameter/proof').Path
lean -o 003-arc-one-parameter/proof/FiniteCore.olean 003-arc-one-parameter/proof/FiniteCore.lean
lean 003-arc-one-parameter/proof/FiniteCoreT.lean
```

To replay all eight files of the 003 certificate, including every closure case, use its dependency-ordered script:

```powershell
& '003-arc-one-parameter/proof/verify.ps1'
```

The largest closure blocks take longer than the small table checks. See the [003 proof README](003-arc-one-parameter/proof/README.md) for coverage, provenance cross-checks and exact limits, and the [001 Mathlib README](001-odd-half-order-hadamard/proof/mathlib/README.md) for the separately pinned matrix package.

The proofs certify the propositions stated in these files. A formal proof of a supporting certificate is a formalization contribution, but it is not a formal proof of every theorem in the surrounding papers. Mathematical provenance and the specific formalization work are identified separately in the notes. No claim of first formalization or historical priority is made.
