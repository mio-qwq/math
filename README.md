# Mathematical research notes and verification artifacts

This repository records explicit mathematical statements, complete proofs where available, and reproducible exact checks. The status of each result is stated separately from its computational or formal verification status. No claim of historical priority is made.

## Results

| Note | Mathematical scope | Verification scope |
| --- | --- | --- |
| [001 — Odd half-order Hadamard rigidity](001-odd-half-order-hadamard/README.md) | General theorem for every odd half-order; complete written proof | Exact examples and Lean proofs of support and actual complex block obstructions; the full rigidity theorem is not yet formalized |
| [002 — Product-weighted rectangular pruning](002-weighted-rectangular-pruning/README.md) | Product-weighted cover/pruning theorems with sharp constant; no finite uniform coefficient works for sums of two positive product systems | Independent rational checker, 67,132 exact instances, and Lean proofs of real-cost single-conflict criteria and the unbounded obstruction |
| [003 — ARC core certificate and extension spectra](003-arc-one-parameter/README.md) | Finite polynomial identities and an abstract spectrum theorem under explicit hypotheses; the one-variable ARC application remains conditional | Lean constructs the actual algebra, perfect trace, specified all-degree projective resolution and nonzero actual f-character Ext³ when q³ is nonzero, with full inverse-twist chain comparison and canonical Ext transport in every degree. Over characteristic-two fields the algebra is self-injective and every positive Ext(M,A) vanishes. The fixed-class canonical twist calculation, full self-Ext profile and complete ARC remain open |

## Reproduction

See [FORMALIZATION.md](FORMALIZATION.md) for the exact Lean statements, commands, and remaining boundaries.

Each note has its own README and fixed inputs. Python checkers use exact arithmetic and the standard library. Lean is pinned by `lean-toolchain` to `leanprover/lean4:v4.34.1`. Most certificates use its bundled `Std` library; each additional `proof/mathlib` package pins Mathlib and its dependencies.

For example, from the repository root:

```sh
lean 001-odd-half-order-hadamard/proof/Parity.lean
```

## Provenance and limitations

The starting point is [OpenAI's public mathematical collection](https://github.com/openai/math), snapshot `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Each note identifies the exact source and distinguishes the prior statement from the extension or checking work recorded here. Reading a source, running finite examples, and checking a portion in Lean do not amount to verification of all its surrounding claims.

Literature review and external mathematical review remain open. Correctness and precise disclosure of verification scope take precedence over claims of novelty.

Licensed under Apache-2.0; see [LICENSE](LICENSE) and the attribution in each note.
