# Distributed Agent C — STATUS

- ID: C; role: independent discovery.
- Baseline: `42a30d62d084a9dbe64c92666addd6cf28986b16`; branch: `partner/dist-C`; owned path: `workstreams/C/`.
- Claim date: 2026-10-10 UTC. Remote coordination ref `coord/distributed` was absent (404); no C task card visible; visible branches at claim time: `main` and `partner/dist-B`. No guarantee of perfect concurrent noncollision.
- Public original target: Collins–Sciriha, arXiv:1906.05790v1, **Question 5.8**, p.15: if `CDC(G) ≅ CDC(H)` for finite simple graphs, must the **sets of main adjacency eigenvalues** coincide? DOI 10.7151/dmgt.2386 (published version 2023). The affirmative claim is a *question*, not originally a numbered conjecture.
- Source URLs: https://arxiv.org/pdf/1906.05790 ; https://doi.org/10.7151/dmgt.2386 ; later open-status discussion https://arxiv.org/html/2603.27559v3#S7 .
- Excludes B's El Zein–Mortada (1,2,3,4)-packing conjecture and Chandran et al. directed-circulant general-position conjecture, and the main repo's 001–006 projects.
- Phase: **candidate question claimed; no discovery claimed yet**. Search an exact symmetric loopless pair related by different row/column permutations; derive explicit CDC isomorphism and use rational Krylov/minimal-polynomial certificates to distinguish main eigenvalue sets. Produce a separately written validator and negative tests.
- Caution: Theorem 3.3 in the arXiv v1 paper suggests a potentially subtle layer-relabelling argument. This is not a proved flaw without an exact witness.
- Local environment: no existing checked-out repository or accessible DNS git remote; GitHub connector used to inspect and publish a branch, with independent local scaffold for computation.
- Review status: pending independent review. Next: exact computational exploration and mathematical certification, followed by HANDOFF.
