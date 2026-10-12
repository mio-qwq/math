# Centered-binomial transfers: the Braun–Bruegge scalar conjecture

This package gives a complete written proof of the **scalar** Conjecture 31 in Braun and Bruegge, *Facets of Symmetric Edge Polytopes for Graphs with Few Edges*, Journal of Integer Sequences 26 (2023), Article 23.7.2, and two direct extensions. [Original paper](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf).

For positive integers a≥b≥c of common parity, the original binomial sum F is nondecreasing under each legal transfer of two units from a smaller row to the largest row. At fixed a+b+c=n+1, its maxima occur at (n−1,1,1) for even n≥4 and (n−3,2,2) for odd n≥5. `PROOF.md` gives the definitions, both transfers, maxima and a separate correction to the original illustrative expansion.

`GENERALIZATION.md` proves strict transfer for any t≥3 positive same-parity rows, and the unique fixed-parity maximizer up to permutation. With t=2 the transfer is an equality. `CROSS_PARITY.md` compares the two feasible parity-class maxima for even t≥4: their odd/even ratio strictly increases with total size, with one crossover at most; at t≥8 neither parity class dominates for all totals.

These are scalar binomial-sum results. Multiple length-one paths cannot be treated as different edges of a simple graph; this package does not settle the more general fixed-edge-count graph/polytope facet-maximization conjectures. Vandermonde, binomial unimodality and single-crossing comparison are classical tools; their use does not certify novelty.

An AI reviewer independently reconstructed the original scalar and same-parity proofs from their definitions on 10 October 2026. The identical frozen originals were checked on 12 October; the crossover proof was then independently checked algebraically, together with 152 small exact adjacent-ratio comparisons. No complete Lean formalization, kernel compilation or axiom audit is provided. Neither mathematical priority nor peer review is certified, and this package has not been submitted as a separate paper.

The three standard-library scripts in `code/` preserve the frozen program bytes. They provide bounded exact regressions, whose historical worker execution must not be confused with independent reruns. `VERIFICATION.json` records the actual review scope; `provenance.json` records all original and integrated hashes and fixed GitHub source links.
