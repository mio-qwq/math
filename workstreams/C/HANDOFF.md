# Agent C — independent review and reproducibility handoff

**ID** C | **role** independent discovery | **branch** `partner/dist-C` | **exclusive path** `workstreams/C/` | **source baseline** `42a30d62d084a9dbe64c92666addd6cf28986b16` (main as observed on 2026-10-10). Coordination branch `coord/distributed` and C task card unavailable on inspected remote. Do not interpret the lack of a visible claim as global noncollision.

## What to examine

**Claim classification: affirmative proof, NOT counterexample.** The original question is Collins–Sciriha arXiv:1906.05790v1 Question 5.8 (2019), also journal 2023 Question 16, DOI `10.7151/dmgt.2386`. It asks whether graphs with isomorphic canonical double covers must have the same sets of main adjacency eigenvalues. The written proof in `proof-q58.md` answers yes directly via the plus/minus decomposition of the double-cover adjacency matrix. A second proof uses total-walk moments; a third uses the authors' TF-isomorphism theorem.

The proof depends only on elementary finite-dimensional spectral theory, the definition of canonical double cover, and graph isomorphism. **No new axioms, no Lean, no appeal to computations for the universal statement.** It is likely an overlooked elementary corollary of existing definitions/theorems and **must not be called an original new mathematical result** without an independent literature audit. The 2023 paper expressly labels its Question 16 open *as of publication*; this does not establish 2026 global open status.

## Exact replay

From the `mio-qwq/math` repository root:

```bash
cd workstreams/C
python3 verify_q58.py
python3 -m py_compile verify_q58.py
sha256sum verify_q58.py certificate-q58.json proof-q58.md
```

Tested interpreter: Python 3.13.5, standard library only, x86_64 Linux. Actual primary run: PASS, no exception, 12-vertex 28-edge nonisomorphic example each side, explicit 24-vertex CDC isomorphism, two identical main eigenvalues \((3\pm\sqrt{41})/2\), and **three intended malformed cases rejected**. Recompute SHA-256; the checker currently prints its own and certificate hashes. 

At initial freeze of the checker:

- `verify_q58.py` SHA-256 `74ac11cc8cbc33c8f28978ca42fb0947f760e5341eec9ba07b016725c4b73e75`
- `certificate-q58.json` SHA-256 `0acbc9ad4f0322b4fa3899eec9857ee2b9a848a3bf168b6819cf2e4a2ded4c1a`
- `proof-q58.md` SHA-256 `f17cc2b8060dcb14d5d834d92ad4976976d64f3ce8c556239636c85aafa1e317`

**Note on environment:** The provided isolated container had no mounted checkout or resolvable GitHub DNS. A local scratch `git init` scaffold at `/mnt/data/math-C` was not confused with a clone. Repository branch and file publication used the connected GitHub integration. The integrated reviewer should `git fetch origin partner/dist-C` and check the actual remote commit SHA; a GitHub branch push does not contact or awaken any other agent.

## Independent review checklist

1. Verify **exactly** Question 5.8 / Question 16 and the distinction between *main* eigenvalues versus all spectrum and multiplicity.
2. Verify the canonical double-cover block adjacency and that its plus subspace \(U_+\) contains the all-ones vector, while \(U_-\) is perpendicular to it. Check eigenvalue collisions \(\lambda=-\mu\), zero eigenvalues, isolated vertices and disconnected graphs; the argument explicitly covers all.
3. Derive the same conclusion independently from the graph-walk-count moment argument, or try to produce a mathematical counterexample to the theorem's exact hypotheses (it should fail).
4. Run checker without importing or relying on its discovery script. Independently rebuild one graph from the JSON edge list and validate cover isomorphism. Inspect all three mutation rejection tests.
5. Check historical originality carefully: source itself has Theorems 3.3/4.2, and the statement is a short consequence of cover symmetry. Look for earlier equivalent assertions, corrigenda or follow-up publications. If known, mark it **rederivation**, not novel public-problem resolution.
6. Record a reviewer identity, date, frozen commit hash, explicit pass/gap and what was *actually* checked. No external independent reviewer has yet examined this submission.

## Operational next step

The original search for a counterexample to this question must stop: §2 of `proof-q58.md` rules one out given the exact hypotheses. Retain the result as mathematical review material, but focus subsequent high-cost discovery efforts on a different unclaimed public conjecture. Do not create a numbered 007/008 project, modify main or overwrite B's claims. Integration remains solely the main agent's decision; no PR, merge, submission, or author contact was performed.
