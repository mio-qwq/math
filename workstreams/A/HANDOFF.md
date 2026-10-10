# Agent A — handoff to ROOT (2026-10-10)

Read STATUS.md for the task acknowledgement, exact scope and old-archive recovery gap. This branch contains a **new unsigned transport reconstruction**, not the earlier signed frozen handoff. The user explicitly requested that available results be pushed first; the GitHub connector cannot transmit an old signed commit object and the original local archive is inaccessible in this session. Do not silently attribute this new commit to the old signed SHA.

## New self-contained result

Braun–Bruegge, *Facets of Symmetric Edge Polytopes for Graphs with Few Edges*, JIS 26 (2023), Article 23.7.2, Conjecture 31, PDF p.24. Full written argument: workstreams/A/braun-bruegge-f31/PROOF.md. Exact standard-library checker: workstreams/A/code/verify_braun_f31.py. The proof addresses the original scalar binomial-sum assertion only, not the broad geometric conjectures 13/32/33/36.

Reproduce from repository root:

    python3 workstreams/A/code/verify_braun_f31.py

Actually run with Python 3.13.5 in the recovered container:
    
    PASS original=720 brute=23 transfer=1029 maxima=720 Vandermonde=209 negative-tests=PASS

Two canonical Git blob SHAs verified by refetching the worker branch through GitHub:

    eef18bb24d0ab4d6d882039e74cc72ce85f67dc2  workstreams/A/braun-bruegge-f31/PROOF.md
    c3eaaa71c9e5b9e934cd1f85a85b814089ec3a20  workstreams/A/code/verify_braun_f31.py

ROOT acceptance checklist: (1) Read the exact published definition in Proposition 22 (p.12), and the two inequalities and parity cases in Conjecture 31 (p.24); (2) independently establish the Vandermonde row-product identity, sign change including endpoints |t|=q, and the arbitrary monotone B_r weighting; (3) check that both order-sensitive substitutions are legal, or follow from symmetric T; (4) verify the final parameter 1 and 2 endpoints; (5) run code against immutable blob SHAs, inspect the negative tests. The printed explanatory inequality in the source seems to omit the +2 offset; keep this erratum observation separate from the genuine statement.

The written proof and finite regression were freshly reconstructed and executed this session. **No ROOT review, Lean formalization or novelty certificate is claimed.** A previous session reported distinct frozen signed commits, but their exact source files and cryptographic signatures cannot be recovered from this runtime. Treat this packet as a new review object.

## Next research / independent handoff

No active high-cost new claim yet. Existing reservation covers Ficarra–Moradi Question 4.2; proposed alternative Braun–Bruegge scalar result is flagged for ROOT scope acceptance. Agent A should source-gate a new disjoint conjecture and publish a separate claim/STATUS update before expensive work. Do not create project numbers, alter shared docs, or re-run large negative enumerations solely to inflate progress.


## Two new theorem packets after the initial scalar proof

1. GENERALIZATION.md — strict transfer for any t>=3 same-parity rows, uniqueness of each fixed-parity extremizer. Exact checker command: python3 workstreams/A/code/verify_generalization.py. Git blobs 6ce46c7fe426a8c62b508cc17ca308ce4591e94b and 3dc16deef1bb333e61394035a7e743b0d1e7a1a8; actually passed 2924 transfers, 499 maxima and 51 independent binary-word cases.
2. CROSS_PARITY.md — even t=2h>=4 parity-class comparison; odd/even extremum ratio increases strictly in k and tends above one; t>=8 has a single crossover starting from even dominance at S=2t. Checker command: python3 workstreams/A/code/verify_cross_parity.py. Git blobs e6695ed03c2459f5a22106f43352c6c7900f4edb and d63eb3fd2b3b836c0983b389f794b9054a8066a5; actually passed 1798 monotone-ratio comparisons, plus exact t=8 boundary examples.

Both are derived from the *scalar original Proposition 22 definition*, not claims on arbitrary multigraph facets. In particular, multiple path lengths 1 violate simple-graph distinct-path conditions. ROOT must audit that semantic scope before declaring a combinatorial polytope theorem. These additions were constructed/tested in the resumed session, without external independent review. The previous-session signed archive is still unavailable; all GitHub API transport commits remain unsigned. No automatic scheduled task has been created.
