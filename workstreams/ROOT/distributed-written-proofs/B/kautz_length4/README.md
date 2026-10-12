# Partial universal bounds for Ka(m,4)

## Scope

The density lambda_4=lim gp(Ka(m,4))/m^4 exists and 26/125<=lambda_4<=377/1320. For every m>=11, gp<=floor(377(m)_4/1320)+m(m-1)(3m-5). The seven-window bound holds for m>=7. The three-block construction gives gp(Ka(5q,4))>=130q^4-74q^3+8q^2 for every q>=1. This is partial progress on [arXiv:2604.15909v1 Problem 5.2](https://arxiv.org/html/2604.15909v1#S5), not an exact formula.

## Dependencies and prior theory

The four notes depend on one another as indicated. LOWER_BOUND.md contains the complete 27-state integer table. three_block_certificate.json and verify_three_blocks.py provide the exact standard-library cross-check; no floating-point discovery optimizer is needed. From this directory: `python verify_three_blocks.py`.

The proof uses original directed suffix/prefix distances, window counting and subalphabet averaging. The auxiliary two-letter upper bound is proved self-contained. Standard averaging is prior theory.

## Verification boundary

Independent review on 2026-10-10 accepted lower, upper, density-limit and rounding arguments together.

The stated scope has complete independently reviewed written mathematics; finite certificates are identified above when required. There is no complete all-parameter Lean proof for these statements. No Lean compilation, mathematical enumeration or checker replay was performed during integration. Preparation checked exact source/output hashes, Python syntax, JSON encoding and required local dependencies. Historical novelty remains unconfirmed.

## Frozen sources

Original branch: `partner/dist-B`. Exact input/output hashes and all editorial transformations are recorded in `provenance.json`. Removed operational appendices remain accessible in the frozen sources.

| Integrated file | Frozen mathematical source | Original SHA256 |
|---|---|---|
| [DENSITY_LIMIT.md](DENSITY_LIMIT.md) | [workstreams/B/kautz_length4/DENSITY_LIMIT.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/kautz_length4/DENSITY_LIMIT.md) | `09447661ccbc4a77ad7df6b0f05db2074f26068a426bc4c530a31f94a1b7a6bf` |
| [LOWER_BOUND.md](LOWER_BOUND.md) | [workstreams/B/kautz_length4/LOWER_BOUND.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/kautz_length4/LOWER_BOUND.md) | `66b7948c36701f8440756977c96dd2720e77a8dcb4d8fd54890954b079f8bacc` |
| [UPPER_BOUND.md](UPPER_BOUND.md) | [workstreams/B/kautz_length4/UPPER_BOUND.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/kautz_length4/UPPER_BOUND.md) | `bf88314b7a277c56cccd942ad25151de17cfb223d2ed45e8dff221ec7ebf2acd` |
| [ROUNDING_REFINEMENT.md](ROUNDING_REFINEMENT.md) | [workstreams/B/kautz_length4/ROUNDING_REFINEMENT.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/kautz_length4/ROUNDING_REFINEMENT.md) | `564af17170330939088d518ae98372db185fe3295001d760c0b46ed8529e0023` |
| [three_block_certificate.json](three_block_certificate.json) | [workstreams/B/kautz_length4/three_block_certificate.json](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/kautz_length4/three_block_certificate.json) | `a03c89944757208aebcf39b87114b7bb4e5e4feeeb6041512e1a410837e80770` |
| [verify_three_blocks.py](verify_three_blocks.py) | [workstreams/B/kautz_length4/verify_three_blocks.py](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/kautz_length4/verify_three_blocks.py) | `c2830830e0c904b692dcdc3e84eccc85f7a99e87b2197e464b720277c250d085` |
