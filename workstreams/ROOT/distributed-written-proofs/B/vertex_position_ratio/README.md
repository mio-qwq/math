# Unbounded vertex-position ratio

## Scope

For every r>=2 the connected family has p_v=2r and p_u>=r(r+1), giving vp/vp^->=(r+1)/2. For k=2^h, h>=2, the connected bipartite subcubic family has p_v=2k and p_u>=(k-1)(k-2)/2+k, giving vp/vp^->=(k^2-k+2)/(4k). This refutes the boundedness question [Problem 4, DOI 10.7151/dmgt.2491](https://doi.org/10.7151/dmgt.2491), [author version](https://oro.open.ac.uk/87516/8/87516_EA.pdf), preprint arXiv:2209.00359v2 Problem 2.4.

## Dependencies and prior theory

Both proofs are self-contained; SUBCUBIC_PROOF.md uses definitions in PROOF.md. No exact global parameter, regular-cubic, planar or minimum-order result is asserted.

Generic root-geodesic, poset and strict-boundary facts are prior theory, including the source boundary lemma. The roots need not be global extremizers; vp^- is not the lower general-position number. The subcubic result strengthens the same original answer.

## Verification boundary

Both all-parameter family proofs separately received independent mathematical review on 2026-10-10.

The stated scope has complete independently reviewed written mathematics; finite certificates are identified above when required. There is no complete all-parameter Lean proof for these statements. No Lean compilation, mathematical enumeration or checker replay was performed during integration. Preparation checked exact source/output hashes, Python syntax, JSON encoding and required local dependencies. Historical novelty remains unconfirmed.

## Frozen sources

Original branch: `partner/dist-B`. Exact input/output hashes and all editorial transformations are recorded in `provenance.json`. Removed operational appendices remain accessible in the frozen sources.

| Integrated file | Frozen mathematical source | Original SHA256 |
|---|---|---|
| [PROOF.md](PROOF.md) | [workstreams/B/vertex_position_ratio/PROOF.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/vertex_position_ratio/PROOF.md) | `4acc0615adf48f35b98f2973527b61b8d4de550a2c6e3feab6b7fc91635d5bba` |
| [SUBCUBIC_PROOF.md](SUBCUBIC_PROOF.md) | [workstreams/B/vertex_position_ratio/SUBCUBIC_PROOF.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/vertex_position_ratio/SUBCUBIC_PROOF.md) | `662b373c535973b83c9676e850fc134410d1c14e767f970d7dded8cce671918e` |
