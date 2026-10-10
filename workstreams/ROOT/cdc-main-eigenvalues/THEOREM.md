# Canonical double covers preserve main eigenvalues

This note gives an affirmative answer, with Lean verification, to Collins–Sciriha's arXiv Question 5.8 (journal Question 16). It is a positive theorem, not a counterexample. Historical originality is not established; the argument is elementary and may already be implicit in earlier spectral theory. Independent acceptance of this integration is recorded in `verification.json`.

## Exact statement and proof

For a finite simple graph G with adjacency matrix A, a real number λ is **main** when there is a vector x such that Ax=λx and the sum of x's coordinates is nonzero. The latter condition also implies x≠0. Write M(G) for the set of such numbers.

The canonical double cover CDC(G) has two copies of V(G), with edges between copies exactly where G has an edge. Its adjacency action on a pair of vectors is D(x,y)=(Ay,Ax).

**Theorem.** M(CDC(G))=M(G). Consequently, CDC(G)≅CDC(H) implies M(G)=M(H).

If D(x,y)=λ(x,y) and the sum of all coordinates is nonzero, then A(x+y)=λ(x+y), and x+y has that same nonzero coordinate sum. Conversely, a main eigenvector x of A gives the cover eigenvector (x,x), whose coordinate sum is twice that of x. This proves the first equality. Any graph isomorphism transports eigenvectors by a permutation, preserving their coordinate sums, proving the consequence.

No assumption of connectivity, absence of isolated vertices, nonzero λ, or preservation of the two layers is needed. The assertion concerns sets of main eigenvalues, not the entire adjacency spectrum.

## Lean statement correspondence

`CDCMainEigenvalues.lean` uses Mathlib's `SimpleGraph`, arbitrary finite vertex types and real vectors.

- `adjAction` is the coordinate formula for multiplication by the actual 0–1 adjacency matrix.
- `MainEigen` is exactly the eigenvector condition above.
- `cover` is the two-copy graph on `V ⊕ V`, with cross-layer adjacency inherited from G and no same-layer edges.
- `cover_main_iff` proves preservation for every real λ.
- `iso_main_iff` proves invariance under an arbitrary adjacency-preserving bijection.
- `same_main_of_cover_iso` proves the original question. Its `RelIso` hypothesis is the relation-isomorphism type underlying Mathlib graph isomorphisms; it imposes no layer condition.

The proof is universal. It has no finite search, unproved spectral lemma, new axiom, `sorry`, or external-computation oracle. The successful actual run produced seven audited declarations, zero warnings and zero errors; dependencies are only `propext`, `Classical.choice` and `Quot.sound`. See `axioms.txt` and `verification.json`.

Using the repository's pinned project and installed dependency cache:

```console
cd 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../workstreams/ROOT/cdc-main-eigenvalues/CDCMainEigenvalues.lean
```

Toolchain: Lean 4.34.1; Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`. The source SHA256 is `2cb2850b7a7556806cec97e6fdb6a600d944d8106131e46e1ee1da0ee3ae0095`.

## Source, provenance and historical limit

The exact question is in Collins–Sciriha, [arXiv:1906.05790v1, Question 5.8](https://arxiv.org/pdf/1906.05790), p.15. The [published article](https://doi.org/10.7151/dmgt.2386), *Discussiones Mathematicae Graph Theory* 43(2) (2023), 507–532, uses Question 16. A later [2026 paper, Section 7](https://arxiv.org/html/2603.27559v3#S7), still describes the question as open. These historical statements do not establish novelty of this note.

The distributed C stream supplied the frozen [written argument and exact demonstrator](https://github.com/mio-qwq/math/tree/9d8f6264eb4c1f4f912e166e16df1e70cc4f97f7/workstreams/C). This integration gives a shorter eigenvector-sum proof and implements the universal statement in Lean. The 12-vertex demonstrator was separately replayed with exact integer arithmetic and three rejected corruptions; it is an illustration and is not used to justify the universal theorem.

Literature checks on 2026-10-10 included the original version, the later paper, title/wording/erratum searches and the [original author's research page](https://luke.collins.mt/walks/). The author's UCL publication endpoint returned no readable content; a search-indexed 2023 talk PDF returned 404. Those were not counted as completed reviews. No prior explicit resolution was located in the sources actually read, but earlier implicit consequences and unindexed results remain possible.

AI assistants contributed the mathematical derivation, independent checks and Lean development. This technical repository note does not assign paper authorship or claim human independent discovery, peer review, journal acceptance or historical priority.
