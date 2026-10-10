# Independent mathematical and statement review

Date: 2026-10-10 UTC. A separate AI reviewer, uninvolved in the discovery or Lean implementation, read the original 2019 definitions and Question 5.8, the frozen C mathematical note, and the complete Lean source. This is independent AI review, not human peer review.

**Verdict: PASS for the mathematical proof and its formal statement.** The reviewed source SHA256 is `2cb2850b7a7556806cec97e6fdb6a600d944d8106131e46e1ee1da0ee3ae0095`.

The reviewer checked the following correspondences directly:

- The finite neighbor sum is the actual 0–1 adjacency action. A vector with nonzero coordinate sum is necessarily nonzero and is nonorthogonal to the all-ones vector, matching the source definition of a main eigenvalue.
- The `Sum` vertex type is two disjoint copies. Its cross-layer edges and absence of same-layer edges are precisely the canonical double cover. No extra vertical edge is inserted at an isolated vertex.
- A cover eigenvector `(x,y)` descends via `x+y`, which has the same nonzero coordinate sum; a base eigenvector lifts via `(x,x)`. This covers zero, negative and repeated eigenvalues without a spectral-decomposition assumption.
- `RelIso` is an arbitrary adjacency-preserving bijection. It does not require a layer-preserving map or a fixed labeling. Transporting a vector by its inverse preserves both the eigen-equation and total coordinate sum.
- Empty, disconnected, bipartite and non-bipartite graphs, including isolated vertices, create no omitted case. The final pointwise equivalence for every real number is equality of sets of main eigenvalues, not equality of full spectra or multiplicities.

The reviewer also read the actual successful compiler JSON and original axiom log. Source hashes before and after the run agree; exit code, warnings, errors and panics are zero; all seven declarations use only `propext`, `Classical.choice` and `Quot.sound`. The reviewer did not rerun the compiler. The evidence is one actual successful compilation plus independent mathematical, source and log review.

The original [arXiv Question 5.8](https://arxiv.org/pdf/1906.05790) and definitions were read directly. The corresponding journal Question 16 is supported by the C handoff and publisher-indexed text; neither this reviewer nor the integrator successfully retrieved the full journal PDF in this cycle. The [2026 successor's Section 7](https://arxiv.org/html/2603.27559v3#S7) was read and still calls the question open. This establishes the reviewed target, not global historical originality.

No remaining mathematical or graph-to-formal-definition gap was identified. Historical originality remains unestablished: the short argument could already be a known or implicit consequence of earlier theory. The finite 12-vertex demonstration, weighted spectral-mass refinement and alternative TF-matrix proof are not part of these seven formal declarations and were not independently replayed by this reviewer.
