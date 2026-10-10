# Internal independent mathematical audit

Date: 2026-10-10 UTC. Reviewer: a separately tasked internal assistant reviewer, not a human reviewer or external peer reviewer. No discovery scripts were read or reused. All audit writes are confined to this audit directory.

## Frozen artifact and verdict

Reviewed file: `workstreams/B/circulant/PROOF.md` at local Git commit `10c34c12b8ded555a953f75546f965cdf5a94151`.

Verified SHA-256: `8003f03393834d7ee763b6e182a05de06fcc85ff208f50caaae1c2d9a528e30b`.

Verdict: the revised written proof establishes the stated formula for every integer pair 1<=d<n. I found no remaining mathematical gap or counterexample. This is an internal mathematical review with executable consistency checks, not formal verification, human responsibility review, or a historical novelty determination.

The frozen artifact was read using `git show COMMIT:workstreams/B/circulant/PROOF.md`, saved as `frozen_PROOF_revised.md`, and checked with `sha256sum`. A `git diff` against the earlier reviewed version confirmed that the only change was the correction described below.

## Findings and correction history

1. An initial informal sketch overstated its anchor test as a full triple equivalence. The triple {0,1,3} at n=8,d=3 has strictly increasing compressed remainders but is not GP, since D(1,3)+D(3,0)=1+2=D(1,0). The correct statement concerns the particular ordered path 0→xi→xj. The first frozen manuscript already used the correct necessary ordered-path statement; this issue was not present in either frozen manuscript.

2. The first frozen manuscript, commit `746a7cfc4917496a3a9636e0a34f87de3f57524a`, SHA-256 `6112562685329989f44accf3078f818d9309ae0673581448f6f343d6efd80b7b`, had an incorrect inventory of endpoint-versus-two-edge comparisons in its final r=d+1 paragraph. The actual six comparisons are 1 versus 2; 1 versus q+2 twice; q+1 versus q+2 twice; and q+1 versus 2(q+1). The new frozen version contains exactly this correction. Each comparison is strict for q>=0, so the theorem and proof strategy were unchanged.

## Mathematical checks

- The directed-distance proof accounts for walks wrapping around the circle: a positive increment sum congruent to t modulo n is at least t. The construction attains ceil(t/d).
- Directed additivity is equivalent to a shortest path through a specified middle vertex. A concatenated minimum-length walk cannot repeat a vertex.
- The ceiling inequality is correct, including zero residues and equality at residue sum d.
- The anchor argument forces strictly increasing positive representatives t_i in 1,...,d. This proves k<=d+1, including k<=2.
- The optional compression identity holds for every ordered pair, including reverse-wrap pairs. It is not used circularly in the main upper bound.
- Section 5 legitimately applies the ceiling criterion to the three cyclic gap pairs, whose sums are less than n. For an interior anchor remainder t and endpoint remainder s, t<d and s-t<d, so the stated ordinary gap residues really are t and s-t, even when s=d.
- The cases s<r, s=r, and s>r cover all possibilities. At s=r the complement gap has residue zero; at s>r its residue is d+r-s. Both required inequalities give the claimed spacing bounds.
- Once the maximum remainder exceeds r, the first gap is at least r and every later adjacent gap is at least r. The counting bound follows without an omitted k=2 case.
- Both lower constructions satisfy all three cyclic gap-pair inequalities. The other orders have total displacement n plus the direct displacement; n>d guarantees strict inequality of lengths.
- The r=d boundary, zero ordinary remainder of n, is valid. The residue convention 2<=r<=d+1 is unique, including d=1.
- For r=d+1, the corrected six-order calculation proves the consecutive construction, including q=0 (the complete digraph). For d=1 the construction has two vertices and the universal bound is 2.

## Source match

I separately opened the versioned primary source at https://arxiv.org/html/2604.15909v1#S3.SS1 and inspected Theorem 3.3 and the paragraph immediately following it. The latter conjectures optimality of the larger of the consecutive and progression constructions for all n,d. The manuscript addresses that original optimality question. This source check does not establish absence of later work or global historical novelty.

## Independent executable checks

`check_independent.py` is an independently written Python standard-library checker. It builds every directed distance by BFS on the actual arc set; constructs forbidden unordered triples by checking all six permutations using those BFS distances; and exhaustively enumerates every GP subset containing 0 using only those forbidden triples. Translation symmetry suffices for the exact maximum. Neither the proposed formula nor the residue restriction is used to prune the search.

For every enumerated set it separately checks increasing compressed remainders, the potential distance identity, and GP preservation after compression. For every triple in [0,d], it checks the compressed span/gap criterion. It also checks the closed-form distance against every BFS distance.

Commands run successfully, exit status 0:

- `python workstreams/B/audit/check_independent.py > workstreams/B/audit/check_independent_results.json`
- `python workstreams/B/audit/check_independent_n22.py > workstreams/B/audit/check_independent_n22_results.json`
- `python workstreams/B/audit/check_boundary_negative.py > workstreams/B/audit/check_boundary_negative_results.json`

Main exact sweep: all 332 pairs with 3<=n<=30, 2<=d<n, and a=(n-1)%d+1>=2. All predicted maxima agreed. All 2,138,790 anchored GP sets passed projection checks. The smaller overlapping sweep through n=22 covered 161 pairs and 66,501 anchored GP sets; it is a subset, not additional independent coverage.

Boundary sweep: all 45 pairs with 2<=n<=16, 1<=d<n, and d=1 or n congruent to 1 modulo d. All predicted maxima agreed, and all 67,395 anchored GP sets passed the same checks. Together, the nonoverlapping main and boundary sweeps cover 377 graph instances and 2,206,185 anchored GP sets.

Negative controls: the boundary script replaces the predicted maximum by one larger and confirms the checker raises AssertionError; independently it corrupts the BFS-derived distance D(0,1) to 99 and confirms rejection. It also rejects the explicit non-GP triple {0,1,3} for n=8,d=3 while accepting {0,2}. Both injected-failure controls were detected.

These computations are finite consistency tests and regression checks. They do not replace the written proof, establish arbitrary-n correctness on their own, or certify the Python implementation formally.
