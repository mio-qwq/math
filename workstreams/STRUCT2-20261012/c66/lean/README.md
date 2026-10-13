# Formal component transport for the C66 boundary proof

`ComponentSupport.lean` imports only Std. It defines the original unordered
edge variable (all diagonals map to the same ground), then generates the
reflexive, symmetric, transitive closure of **every** ordered TF equation.
The component indicator is proved to be invariant under the prescribed
two-fold permutation pair. No component invariance premise is supplied.

The file constructs the actual finite component edge list by filtering all
unordered pairs, proves its adjacency equals the closure-defined relation
for an ungrounded component, and proves both coordinate permutations
preserve its endpoint set. A distinct orbit prefix of length `m` then has
`m <= 2 * componentEdges.length`. The `Nodup` orbit-prefix premise is the
ordinary distinctness property of a genuine cycle; no numeric cycle bound
is assumed. The generic finite-list theorem is also exposed separately.

The actual official Lean 4.34.1 run passes 12 named axiom audits without
errors, warnings or `sorryAx`. The axiom union is only `propext`,
`Classical.choice` and `Quot.sound`. Four elementary transport results
depend on no axioms. Records are under
`verification/20261013-c66-critical-boundary/`.

Reproduction:

```sh
python3 verify_component_support.py --lean /absolute/path/to/lean \
  --build-dir /chosen/build --output-dir /chosen/receipt
```

The compiler must be official Lean 4.34.1, release commit
`5045d0056413266e57c625dcd7c365b10e377c52`. On the application-path-limited
execution host, add `--adapter /chosen/runtime_path.so`; its source and
explanation are reused from `../../cg/lean/runtime_path.c` and the CG README.
The adapter changes only executable-path discovery, not the proof kernel.

The probability bound, component-excess sum, short-cycle count and the full
expectation limit in `../CRITICAL_BOUNDARY.md` remain written theorems. This
module supplies their central structural interface, not a Lean proof of the
entire asymptotic theorem or new independent written acceptance.

The initial proof iteration unfolded `List.flatMap` past the induction
hypothesis and produced an unsolved length goal. Explicit constructor and
length rewrites preserve the hypothesis and resolve it. Only the final clean
compilation is included in the successful audit receipt.

## Actual singleton classification for the exact window

`SingletonComponent.lean` imports `ComponentSupport` and defines
`FreeSingleton` directly through the complete equality closure: its edge
variable is not the ground and every variable connected to it equals it.
It proves this is equivalent to both permutations fixing the two endpoints
pointwise, or both sharing the same transposition. The invariance of the
one-edge adjacency is derived from the actual closure, and the converse
is proved by induction over all equality paths.

The two-module chain passes 21 named audits (12 existing and 9 new) with
official Lean 4.34.1 and only `propext`, `Classical.choice`, `Quot.sound`.
The generic one-edge classification itself uses no axioms. Reproduce with:

```sh
python3 verify_singleton_component.py --lean /absolute/path/to/lean \
  --build-dir /chosen/build --output-dir /chosen/receipt
```

The same optional `--adapter` is supported. Actual logs and hashes are in
`verification/20261013-c66-exact-window/`. The first source iteration left
conditional terms unsimplified in the edge-variable fiber proof; explicit
equality/order cases fixed this. Failed draft compilations are not counted
as passed audits. Finite cardinalities, probability products, factorial
tails and the expectation limit in `../EXACT_WINDOW.md` remain written.
