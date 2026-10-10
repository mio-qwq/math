# Circulant research result

No counterexample found. A residue upper-bound derivation instead proves the conjectured value; see DERIVATION.md and the parent-reviewed PROOF.md.

## Witness search

{
  "cases": 319,
  "statuses": {
    "exhausted": 231,
    "timeout": 88
  },
  "n_range": [
    18,
    311
  ],
  "d_range": [
    16,
    60
  ],
  "q_values": [
    1,
    2,
    3,
    5
  ],
  "nodes": 11702039
}

The search fixed vertex 0 by translation and used bitset elimination of all forbidden triples. Each case had a 0.2-second search budget after preparation. Exhausted cases searched for a set of size one above the conjectured bound; timeout cases are inconclusive and give no upper bound. Search stopped by interrupt when the mathematical derivation made further witness hunting unnecessary. The interrupted in-progress case is not included in the JSONL log. No candidate JSON was created because no witness was found.

## Independent BFS boundary validation

Direct BFS validated the distance formula and the necessary residue inequalities for all 3,346 eligible graphs with 5<=n<=90, all 6,884,676 anchored triples, and 2,536,059 general-position triples. All assertions passed. This includes q=1, residue-zero endpoints, and a near both boundaries 2 and d-1. Full machine-readable results and actual Python/platform versions are in lemma_validation.json.

## Reproduction

Run python search.py for the randomized deterministic-order witness search (seed 15909; original run intentionally stopped after 319 completed cases). Run python verify_lemma.py for the independent BFS check. No commits, pushes, or external peer communications were performed. Scripts, derivation, and logs are hashed in WORKER_SHA256SUMS.
