# Sharp universal replacement for the lower-GP product conjecture

## Scope

For all nonempty finite simple undirected graphs, gp^-(G square H)>=min(5,gp^-G,gp^-H), with no order, diameter or connectedness restriction. For every r>=6, the companion connected family has min(gp^-G_r,gp^-H_r)=r and product lower-GP exactly 5. Complete-graph examples for r=1,...,5 show that min(r,5) is the optimal universal lower bound depending only on the smaller factor parameter. The original-conjecture refutation and sharp replacement are one combined result. Source: [arXiv:2404.19451v1 Conjecture 2.10](https://arxiv.org/html/2404.19451v1), [final paper Conjecture 3](https://oro.open.ac.uk/98050/9/98050final.pdf), DOI 10.22049/cco.2024.29171.1879.

## Dependencies and prior theory

UNIVERSAL_FIVE_PROOF.md gives the universal reduction. verify_universal_five.py invokes verify_arbitrary_four.py, which imports verify_metric_rays.py. They derive the cone and face closure from inequalities without supplied ray/face-table input; metric_faces.json and metric_rays_verified.json are frozen exact comparison data. UNBOUNDED_GAP_PROOF.md additionally depends on [the existing fixed construction proof](../../../lower-gp-product319-counterexample/PROOF.md). No duplicate fixed319 or min4 package is included. verify_unbounded_gap.py is an optional semantic regression checker. Replay commands, if needed: `python verify_universal_five.py` and `python verify_unbounded_gap.py`.

Cartesian distances, true-twin saturation and polyhedral double-description theory are prior methods. The standard complete-graph Cartesian-product GP formula is credited to the original product literature.

## Verification boundary

The min5 theorem received independent mathematical and exact computational acceptance on 2026-10-10 using a different ray/face/profile implementation, checking all sizes 1..4 and the 25 rays / 9484 faces. The all-r family separately received independent written acceptance; its sharp-bound combination was checked against the min5 statement. The fixed319 Lean proof does not formalize these universal results.

The stated scope has complete independently reviewed written mathematics; finite certificates are identified above when required. There is no complete all-parameter Lean proof for these statements. No Lean compilation, mathematical enumeration or checker replay was performed during integration. Preparation checked exact source/output hashes, Python syntax, JSON encoding and required local dependencies. Historical novelty remains unconfirmed.

## Frozen sources

Original branch: `partner/dist-B`. Exact input/output hashes and all editorial transformations are recorded in `provenance.json`. Removed operational appendices remain accessible in the frozen sources.

| Integrated file | Frozen mathematical source | Original SHA256 |
|---|---|---|
| [UNIVERSAL_FIVE_PROOF.md](UNIVERSAL_FIVE_PROOF.md) | [workstreams/B/lower_gp_product/UNIVERSAL_FIVE_PROOF.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/lower_gp_product/UNIVERSAL_FIVE_PROOF.md) | `f9742af7532e5f2155048bc89e516747c659f42bd17b4bbf3133caffb1db4406` |
| [UNBOUNDED_GAP_PROOF.md](UNBOUNDED_GAP_PROOF.md) | [workstreams/B/lower_gp_product/UNBOUNDED_GAP_PROOF.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/lower_gp_product/UNBOUNDED_GAP_PROOF.md) | `4eb8215912faf05d7fae3f277b5d9ad3a74a437219058fb757ee0c9b377ef65b` |
| [verify_universal_five.py](verify_universal_five.py) | [workstreams/B/lower_gp_product/verify_universal_five.py](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/lower_gp_product/verify_universal_five.py) | `f354221432d3b0309b7b9b2345c1a5456221528dc028b2d29e5338d66e256fce` |
| [verify_arbitrary_four.py](verify_arbitrary_four.py) | [workstreams/B/lower_gp_product/verify_arbitrary_four.py](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/lower_gp_product/verify_arbitrary_four.py) | `69999ef184ce26c91ab5c2e53fb94a647e7d8b1f71a24b60d6596b41ad2e27b1` |
| [verify_unbounded_gap.py](verify_unbounded_gap.py) | [workstreams/B/lower_gp_product/verify_unbounded_gap.py](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/lower_gp_product/verify_unbounded_gap.py) | `5ecae32fccf89aebd374c4ef2f936c15ca9ab023195f25495694e74cf6b0408b` |
| [verify_metric_rays.py](verify_metric_rays.py) | [workstreams/B/lower_gp_product/verify_metric_rays.py](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/lower_gp_product/verify_metric_rays.py) | `59299a4e518d539dc9a527832eddfe8842f62c171cce1df0b46bf1634db9321c` |
| [metric_faces.json](metric_faces.json) | [workstreams/B/lower_gp_product/metric_faces.json](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/lower_gp_product/metric_faces.json) | `01001dc53737560f49749784eaef85fe4d8c9297afde51093923a34ef185a382` |
| [metric_rays_verified.json](metric_rays_verified.json) | [workstreams/B/lower_gp_product/metric_rays_verified.json](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/lower_gp_product/metric_rays_verified.json) | `0153b1d6ca7449b5c6f7a4af256b3bcf8c6513e48ac8b226554a1b384339a8ef` |

Existing required dependency: [workstreams/ROOT/lower-gp-product319-counterexample/PROOF.md](../../../lower-gp-product319-counterexample/PROOF.md), SHA256 `bfc815e52a7a918705b256fce12bf61a98a853fd49dcff5b2c4b9a47e865f658`; [frozen source](https://github.com/mio-qwq/math/blob/a8c3f22e26b08c2d294e2b0e6df2d9cfa430cda0/workstreams/ROOT/lower-gp-product319-counterexample/PROOF.md).
