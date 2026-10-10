# Exact Lean / Mathlib interface for the Hall proof

**Status:** implementation specification only. The active worker container (2026-10-10) has NO \`lean\`, \`lake\`, or \`elan\` executable, and cannot access GitHub from its shell. No file in this directory is represented as compiled, axiom-audited, or a complete Lean proof.

## Frozen mathematical objects

The original complete Conjecture 10 proof (independent written mathematical PASS) is frozen at \`7168f6df66ba5518cd3420c4668eab5352e4be8c\`. The new Hall-based strengthening is \`../proof/HALL_TRANSVERSAL.md\`. It is **an alternative proof of Lemma 1**, not an amendment of the frozen original.

## Pinned Mathlib source verified on GitHub

The mathematical repository uses Lean 4.34.1 and the coordination note specifies Mathlib commit \`d13f23b723b8a846827a245b89c10fc7d3f11612\`. We read the ACTUAL file \`Mathlib/Combinatorics/Hall/Finite.lean\` at that commit (Git blob \`9e013ce0f999e3135ec53e1abda4d178af3fa044\`) and confirmed that it exports the exact theorem

    Finset.all_card_le_biUnion_card_iff_existsInjective'

with type, omitting universe variables:

    {ι α : Type*} → [Finite ι] → [DecidableEq α] →
    (t : ι → Finset α) →
    (∀ s : Finset ι, s.card ≤ (s.biUnion t).card) ↔
      ∃ f : ι → α, Function.Injective f ∧ ∀ x, f x ∈ t x

Link: https://github.com/leanprover-community/mathlib4/blob/d13f23b723b8a846827a245b89c10fc7d3f11612/Mathlib/Combinatorics/Hall/Finite.lean

**A small uncompiled import/application sketch** (but NO new finite-partition theorem) is shipped separately as \`HallBridge.lean\` and labelled uncompiled. The Hall theorem itself is already fully formalized in Mathlib and must be attributed as an imported result, not an A achievement.

## Finite-partition formalization strategy

Take a finite decidable element type X, part indices \`Fin k\`, second-part indices \`Fin m\`, and block families \`P : Fin k → Finset X\`, \`S : Fin m → Finset X\`.

Dependencies needed before matching:

1. Both \`P\` and \`S\` partition \`Finset.univ\`, with pairwise disjoint nonempty blocks. Prove \`2 ≤ (P i).card\` and \`2 ≤ (S j).card\`.
2. Select distinct \`a i, b i : X\` with \`a i ∈ P i\`, \`b i ∈ P i\`, \`a i ≠ b i\`. Define candidate pair \`C i := {a i,b i}\`. Distinct P blocks imply all candidate pairs are disjoint.
3. Define \`dangerous j : Prop := S j ⊆ (Finset.univ.biUnion C) ∧ ∀ i, ((S j) ∩ C i).card ≤ 1\`. Let \`ι = {j : Fin m // dangerous j}\`.
4. Define \`N : ι → Finset (Fin k)\` as the P-indices whose candidate pair intersects \`S j\` nontrivially. For any \`J : Finset ι\` define \`U := J.biUnion fun j => S j.val\`. Using S disjointness and cardinal minima, \`2*J.card ≤ U.card\`. Using only two candidates per P and \`S j ⊆ ⋃ C i\`, prove \`U.card ≤ 2*(J.biUnion N).card\`. \`omega\` then yields exactly the Hall hypothesis \`J.card ≤ (J.biUnion N).card\`.
5. Apply the confirmed existing theorem directly:
   \`(Finset.all_card_le_biUnion_card_iff_existsInjective' N).mp hallBound\`
   to obtain an injection \`f : ι → Fin k\` with \`f j ∈ N j\`.
6. For matched P index f j, choose the **other** candidate outside S j; the dangerous predicate guarantees such a candidate. Distinctness of f ensures compatibility. For unmatched P indices choose an arbitrary candidate. Prove exactly one element chosen per P and every dangerous S misses its matched candidate. Safe S either contains a noncandidate or contains both candidates of one P, hence also cannot be fully chosen.

This proves the **partition theorem**. Derive the old Q-graph lemma by taking second parts S as connected-component vertex sets, with min S-cardinality from no isolated Q vertices. The latter is the only graph-specific step.

## Scope, negative controls and mathematical obligations

- Do not accidentally formalize a *common transversal of the two partitions*, which is a DIFFERENT stronger property; here the chosen set avoids fully containing any S block.
- Do not replace the dangerous predicate by merely \`S j ⊆ candidates\`: if both candidates of the same P lie in S, that block is automatically safe.
- Do not drop the minimum-two condition on EITHER partition. Both are genuinely necessary in general (counterexamples in HALL_TRANSVERSAL.md).
- Distinct matching representatives are P-indexes; they are NOT vertices chosen in R. A matched P index chooses the **other candidate** outside its corresponding dangerous S block.
- Matchings can be implemented via the standalone Python augmenting-path algorithm for numerical regressions, but the infinite theorem is proven by the Hall cardinal argument, NOT by running that program.

## Future actual compiler acceptance

In an authorized system with Lean 4.34.1 and pinned Mathlib available: run \`lake env lean workstreams/A/formal/HallBridge.lean\`, then compile the full finite-partition proof with no \`sorry\` or added axioms; record \`#print axioms\` for every final declaration. Do not submit/merge or claim Mathlib formalization before the proof really compiles. No scheduled job or paid compute resource was used.
