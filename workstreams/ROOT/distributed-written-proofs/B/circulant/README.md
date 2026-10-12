# Consecutive-generator circulant optimality

## Scope

For all integers 1<=d<n, D(n,d) has arcs x->x+j (mod n), 1<=j<=d. Write n=qd+r with 2<=r<=d+1. Then gp=d+1 for r=d+1, and gp=max(r,floor(d/r)+1) otherwise. This is the original unnumbered optimality assertion after Theorem 3.3 in [arXiv:2604.15909v1](https://arxiv.org/html/2604.15909v1#S3.SS1).

## Dependencies and prior theory

Self-contained PROOF.md; no finite certificate dependency.

The original paper supplied the two lower constructions. The written proof supplies the matching upper bound, with all directed-distance and small/residue cases.

## Verification boundary

The full written argument received independent mathematical review on 2026-10-10.

The stated scope has complete independently reviewed written mathematics; finite certificates are identified above when required. There is no complete all-parameter Lean proof for these statements. No Lean compilation, mathematical enumeration or checker replay was performed during integration. Preparation checked exact source/output hashes, Python syntax, JSON encoding and required local dependencies. Historical novelty remains unconfirmed.

## Frozen sources

Original branch: `partner/dist-B`. Exact input/output hashes and all editorial transformations are recorded in `provenance.json`. Removed operational appendices remain accessible in the frozen sources.

| Integrated file | Frozen mathematical source | Original SHA256 |
|---|---|---|
| [PROOF.md](PROOF.md) | [workstreams/B/circulant/PROOF.md](https://github.com/mio-qwq/math/blob/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B/circulant/PROOF.md) | `8003f03393834d7ee763b6e182a05de06fcc85ff208f50caaae1c2d9a528e30b` |
