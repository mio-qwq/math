# Claw-free subcubic (1,2,2,2,2) coloring

## Scope

Every finite simple claw-free graph of maximum degree at most three has the stated packing coloring, including disconnected graphs, leaves and isolated vertices. This is [arXiv:2608.02566v1 §6 Conjecture 1](https://arxiv.org/html/2608.02566v1#S6).

## Dependencies and prior theory

FULL_PROOF.md states the imported theorem and supplies the simple line-graph root construction, six explicit local cap rows and exhaustive diamond induction.

This is explicitly a corollary of the published Yang–Wu (2022) edge-coloring theorem plus elementary diamond reductions. Triangle-expansion existence subclasses are already consequences of that prior theorem. The imported theorem is a dependency, not a new theorem proved here.

## Verification boundary

Independent written review on 2026-10-10 accepted the full corollary and checked the six local P/D rows by original-distance BFS. It did not reprove the published 2022 theorem or replay all original graph fixtures.

The stated scope has complete independently reviewed written mathematics; finite certificates are identified above when required. There is no complete all-parameter Lean proof for these statements. No Lean compilation, mathematical enumeration or checker replay was performed during integration. Preparation checked exact source/output hashes, Python syntax, JSON encoding and required local dependencies. Historical novelty remains unconfirmed.

## Frozen sources

Original branch: `partner/dist-B`. Exact input/output hashes and all editorial transformations are recorded in `provenance.json`. Removed operational appendices remain accessible in the frozen sources.

| Integrated file | Frozen mathematical source | Original SHA256 |
|---|---|---|
| [FULL_PROOF.md](FULL_PROOF.md) | [workstreams/B/clawfree_12222/FULL_PROOF.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/clawfree_12222/FULL_PROOF.md) | `3a8e3787fa4b6aeb9f428ee573b92166df09fa652947e8b5f921337ab1c17117` |
