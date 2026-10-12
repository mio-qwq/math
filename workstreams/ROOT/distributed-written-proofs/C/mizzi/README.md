# Mizzi v3: both cycle conjecture clauses

## Scope

The first clause holds for all nonisomorphic finite simple undirected graph pairs with isomorphic canonical double covers: one has two vertex-disjoint C_k and the other C_(2k), for odd k>=3, including disconnected/bipartite cases. The second clause holds for connected asymmetric unstable graphs in the source scope. More generally, any finite asymmetric graph with an explicit nontrivial TF automorphism has vertex-disjoint C_k and C_(2k). The conditional bundle lemma assumes an odd-order inverse TF pair and a chosen odd moving-orbit quotient cycle, giving C_k plus (M-1)/2 disjoint C_(2k) cycles. Source: [Mizzi arXiv:2603.27559v3 §7](https://arxiv.org/html/2603.27559v3#S7).

## Dependencies and prior theory

The four mathematical notes contain the first-clause proof, long/short presentations of the same second-clause proof, and the bundle lemma. Theorem C retains its explicit TF hypothesis. Disconnected raw CDC-instability alone does not imply that hypothesis and is not asserted to satisfy the second-clause conclusion. Finite example JSON/checkers are not dependencies of these universal written proofs.

Inverse TF pairs and odd-order restrictions are prior: [Lauri–Mizzi–Scapellato (2011), Propositions 3.1/3.3](https://ajc.maths.uq.edu.au/pdf/49/ajc_v49_p165.pdf), [Bychawski (2024), Theorem 6.2](https://arxiv.org/html/2406.06267v1#S6). Generalized CRT is standard.

## Verification boundary

The first clause and the full/short/bundle second-clause packet received genuine independent mathematical reviews on 2026-10-10. The transcripts correct the second-clause introductory/corollary scope to the reviewed connected/explicit-TF range.

The stated scope has complete independently reviewed written mathematics; finite certificates are identified above when required. There is no complete all-parameter Lean proof for these statements. No Lean compilation, mathematical enumeration or checker replay was performed during integration. Preparation checked exact source/output hashes, Python syntax, JSON encoding and required local dependencies. Historical novelty remains unconfirmed.

## Frozen sources

Original branch: `partner/dist-C`. Exact input/output hashes and all editorial transformations are recorded in `provenance.json`. Removed operational appendices remain accessible in the frozen sources.

| Integrated file | Frozen mathematical source | Original SHA256 |
|---|---|---|
| [mizzi_first_clause_full_proof_20261010.md](mizzi_first_clause_full_proof_20261010.md) | [workstreams/C/mizzi_first_clause_full_proof_20261010.md](https://github.com/mio-qwq/math/blob/979598c300580b18b603b51ded9ccdf59f470faa/workstreams/C/mizzi_first_clause_full_proof_20261010.md) | `d80d92b21977b47ffcd03e3020e200f774099fa02dfd9dd051bf8b8f7e6de266` |
| [mizzi_v3_asymmetric_full_proof.md](mizzi_v3_asymmetric_full_proof.md) | [workstreams/C/mizzi_v3_asymmetric_full_proof.md](https://github.com/mio-qwq/math/blob/979598c300580b18b603b51ded9ccdf59f470faa/workstreams/C/mizzi_v3_asymmetric_full_proof.md) | `3b5ffdf2e287e775377e8dabf9ce33ec2450c4c56667074453c6520b655827e8` |
| [mizzi_v3_short_proof.md](mizzi_v3_short_proof.md) | [workstreams/C/mizzi_v3_short_proof.md](https://github.com/mio-qwq/math/blob/979598c300580b18b603b51ded9ccdf59f470faa/workstreams/C/mizzi_v3_short_proof.md) | `430ea6b6f279ee9896c761b4b6cebba999cbe8e62d2c1218b534d2a0ab8328d7` |
| [mizzi_cycle_bundle_extension.md](mizzi_cycle_bundle_extension.md) | [workstreams/C/mizzi_cycle_bundle_extension.md](https://github.com/mio-qwq/math/blob/979598c300580b18b603b51ded9ccdf59f470faa/workstreams/C/mizzi_cycle_bundle_extension.md) | `80f97a8814efd262bd9ee07be5c504118db12f05c258602070b0e61a84226cff` |
