# Collaboration protocol and current handoff

This repository is shared by independently running research agents. The user authorizes ongoing research, formalization, review and GitHub publication. Prefer a concrete tractable proof gap, publish completed work promptly, and then continue improving it. Do not treat an unverified draft as a completed theorem.

## Check the live state

Read `README.md`, `FORMALIZATION.md`, recent commits, and each note before editing. Fetch `origin/main` and partner branches: this file can become stale. Milestone `5af6c3f` proves associativity of the actual twenty-coordinate multiplication over F₂ polynomials and after every specialization into a commutative characteristic-two ring. Earlier milestone `62e10d0` contains all 104,976 kernel-checked radical closure identities in note 003.

## Avoid overlapping edits

Use a separate checkout and a branch such as `partner/<topic>`. Maintain only your own `coordination/agents/<name>.md` status file, recording your base SHA, branch, exclusive file paths, completed statements, actual checks, precise remaining gaps and next step. Publish that record on your branch so other agents can discover it. Do not modify another agent's status file.

Completed proofs may be pushed to a partner branch immediately and proposed for integration by a PR. A branch publication is a public record; it does not mean the change has reached `main`. Fetch before integration, resolve conflicts without overwriting others' work, and recheck affected proofs. No force pushes or destructive cleanup of unknown work.

Git is the common coordination channel. If a direct messaging tool is available and authorized, identify the actual destination chat before messaging it. A push alone is not guaranteed to wake another chat. When no messaging tool exists, write concrete requests in your own status file and continue independent work.

## Current mathematical boundaries

- 001 has a complete written odd-half-order rigidity argument and Lean supporting proofs, including an actual complex Gram block obstruction. Newton identities and construction of these blocks from the original Hadamard matrix remain unformalized.
- 002 has a written product-weighted theorem, an independent rational checker, and Lean single-conflict classifications over natural and real costs. The actual positive two-product obstruction, rational witnesses and exact parameter ratios are formalized. The full rectangular theorem is not formally proved in Lean.
- 003 has eight compiled Std certificates, including all 104,976 closure identities, and semantic bridges from packed codes to actual polynomial vectors. Associativity now holds for the actual multiplication on all twenty-coordinate vectors and after every commutative characteristic-two specialization. Unit/trace laws are in progress; a library algebra instance and complete ARC homological realization remain open.

## In-flight work at handoff

Check `coordination/agents/primary.md` and recent commits for the latest ownership. The active files under `003-arc-one-parameter/proof/mathlib/` are `TwentyDimUnit.lean`, `TracePairSemantics.lean`, and `FiniteBilinearLaws.lean`. The primary agent handles integration, documentation and replay tooling. `FiniteBilinearUnit.lean` is compiled and published with this update.

A disjoint partner task is the Hadamard-to-block bridge in 001 or the general rectangular theorem in 002. Read each note's exact definitions before choosing a lemma. If working on 003, agree on a new file and dependency interface first. Avoid repeating the large finite closure computations unless relevant source or environment changes justify it.

## Verification and provenance

Lean is pinned to `leanprover/lean4:v4.34.1`, Mathlib to `d13f23b723b8a846827a245b89c10fc7d3f11612`, and the original source notes to OpenAI commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Record actual compilation, axiom audits and exact scope. Preserve attribution; do not make unchecked priority claims. Never commit credentials, private handoff prompts, local binary caches or tokens.
