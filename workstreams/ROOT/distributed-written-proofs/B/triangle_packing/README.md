# El Zein–Mortada five-color Conjecture 2

## Scope

Every finite simple 1-saturated subcubic graph with every degree-three vertex in a triangle has a (1,2,3,4,5)-packing coloring. Here 1-saturated means at most one degree-three neighbour at each degree-three vertex. This is [arXiv:2603.25113v1 §5 Conjecture 2](https://arxiv.org/html/2603.25113v1#S5).

## Dependencies and prior theory

FIVE_PROOF.md uses STRUCTURAL_CLASSIFICATION.md, CHAIN_EMBEDDING.md, five_invariant.json, five_relations.json and verify_five.py. The verifier uses only the standard library and those two JSON inputs. Optional construction/discovery scripts are not dependencies of the invariant proof. From this directory the retained verifier can be invoked as `python verify_five.py`.

Boolean transfer relations and invariant induction are standard methods. The extracted structural/embedding lemmas do not include the other palette theorems of their source documents.

## Verification boundary

The universal reduction and finite invariant received genuinely independent review on 2026-10-10. An independent exact reconstruction actually checked 90 boundary states, 48 path states, 139 matrices, 225 seeds, 2085 closure transitions and T^14=T^13. These are historical checks, not integration-time replays.

The stated scope has complete independently reviewed written mathematics; finite certificates are identified above when required. There is no complete all-parameter Lean proof for these statements. No Lean compilation, mathematical enumeration or checker replay was performed during integration. Preparation checked exact source/output hashes, Python syntax, JSON encoding and required local dependencies. Historical novelty remains unconfirmed.

## Frozen sources

Original branch: `partner/dist-B`. Exact input/output hashes and all editorial transformations are recorded in `provenance.json`. Removed operational appendices remain accessible in the frozen sources.

| Integrated file | Frozen mathematical source | Original SHA256 |
|---|---|---|
| [STRUCTURAL_CLASSIFICATION.md](STRUCTURAL_CLASSIFICATION.md) | [workstreams/B/triangle_packing/PROOF.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/triangle_packing/PROOF.md) | `28901e98fd0c2eca8a89e7fe45da057ff334a49e15847fdbe795b51e9ea524bd` |
| [CHAIN_EMBEDDING.md](CHAIN_EMBEDDING.md) | [workstreams/B/triangle_packing/SECOND_PROOF.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/triangle_packing/SECOND_PROOF.md) | `2bc9a0494f2331ccc2accd33a195d4ba330dbf275a6d7bdea2e34b2e63a7411b` |
| [FIVE_PROOF.md](FIVE_PROOF.md) | [workstreams/B/triangle_packing/FIVE_PROOF.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/triangle_packing/FIVE_PROOF.md) | `808ff9c3c60a9b4a8663bb8a4f8c7af4d4aac6374decb3d7b6dd7377d33f1a20` |
| [verify_five.py](verify_five.py) | [workstreams/B/triangle_packing/verify_five.py](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/triangle_packing/verify_five.py) | `68266f6722b2dd9eb5c6d3c0d0c6f36c1727632c0071e59f31bba487c106a333` |
| [five_invariant.json](five_invariant.json) | [workstreams/B/triangle_packing/five_invariant.json](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/triangle_packing/five_invariant.json) | `27882d4e867f155012ecb847483bf0d3ddde9129744397946970718a4fcf8ca6` |
| [five_relations.json](five_relations.json) | [workstreams/B/triangle_packing/five_relations.json](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/triangle_packing/five_relations.json) | `f1dc06451e2dc451cbc7582af91652c27b8e351fed5bdbbaed2272b7381b2e14` |
