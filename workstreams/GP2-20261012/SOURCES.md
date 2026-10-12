# Kautz length-four source and provenance check

Date: 2026-10-12. This note records actual source coverage, not an assertion
that every publication has been searched or that historical priority is proved.

## Original question

Chandran S.V., Di Stefano, Erskine, Haritha S, Thomas and Tuite,
[*The general position number of digraphs*](https://arxiv.org/abs/2604.15909).
The live arXiv version list displayed only v1, submitted
2026-04-17 10:10:49 UTC. The [v1 HTML](https://arxiv.org/html/2604.15909v1)
was read at Definition 2.1, Section 3.2 and Problem 5.2.

- General position quantifies every shortest directed path.
- Digons are permitted; an oriented graph is a different restricted class.
- In `Ka(m,k)`, m is the number of letters and k is the word length.
- Vertices have unequal adjacent letters; arcs shift and append.
- Problem 5.2 asks for general formulas including Kautz k>=3.
- Table 1 includes the finite Ka(3,4) and Ka(4,4) values 7 and 27.
  These observations are prior work and are not new computations here.

## Later direct author statement

Chandran S.V., Klavzar and Tuite,
[*The General Position Problem: A Survey*](https://arxiv.org/abs/2501.19385),
live v5 dated 2026-08-16 16:08:22 UTC. The
[v5 text](https://arxiv.org/html/2501.19385v5) was read at Section 5.6,
Section 6 and reference [25]. It gives the general k=2 Kautz value and again
lists determining k>=3 as a research problem. Reference [25] is the above
digraph preprint.

These are the latest directly read source statements found in this check.
No public source determining lambda_4 or all finite Ka(m,4) values was located.
This is evidence supporting continued work, not a certification of current
openness across all indexed and unindexed literature.

## Additional coverage and limits

Two search systems were used for the arXiv identifier, full paper title,
Kautz/general-position terms and length-four/solution/bound variants.
The source-checking reviewer also inspected accessible recent publication
lists for James Tuite, Grahame Erskine and Ullas Chandran, and the first page
of Gabriele Di Stefano's institutional research listing. These lists are
incomplete coverage. Some official author sites and Scholar/Semantic Scholar
outlinks could not be read; no negative evidence is inferred from that failure.
A MathDB item encountered in the search merely extracted a question from
the original preprint and was not counted as a subsequent solution paper.

Two related methods were inspected but are not dependencies of the new
theorems:

- Stanovnik, Moskon and Mraz,
  [*In search of maximum non-overlapping codes*](https://link.springer.com/article/10.1007/s10623-023-01344-z),
  DCC 92 (2024), 1299-1326. The recursive prefix/suffix partition method is
  relevant background. Its non-overlap requirement is stronger than GP, and
  its exact length-four code bound is not a GP upper bound.
- Shen, Shangguan, Lin and Ge,
  [*Constrained coding upper bounds via Goulden-Jackson cluster theorem*](https://arxiv.org/abs/2407.16449).
  The finite forbidden-substring counting method is related background;
  it does not optimize the present GP problem by itself.

The repair proof initially considered a hypergraph-removal route and records
that source in its own note. Its final elementary argument does not import
the removal lemma.

## Inherited evidence

The verified current main was `61488e05c9fe41984f483853f99e79f5715dc893`.
The B freeze was `802e030aa8ac47a2018c9441a6b19f59b2db2535`; the visible
coordination reference was `abd8e85628b1348f250c5d5c46a5450caae2876d`.
The integrated entry is
[`workstreams/ROOT/distributed-written-proofs/B/kautz_length4/`](https://github.com/mio-qwq/math/tree/61488e05c9fe41984f483853f99e79f5715dc893/workstreams/ROOT/distributed-written-proofs/B/kautz_length4).
Its four proofs, certificate, checker and provenance file were read. The B
support-route obstruction and five-letter stop note were read by exact Git
reference. No old optimization or old large enumeration was rerun.

The inherited lower coefficient 26/125, limit existence, and old upper
377/1320 retain their existing written-review status and attribution.
The new seven/nine moment combination, exact collision correction and
elementary repair are separate mathematical claims. Their review is by
independent AI research agents, not external human peer review. They are
partial progress on the k=4 subproblem, not a solution of all Problem 5.2.

## Classical comma-free sources used in the later phase

- S. W. Golomb, B. Gordon and L. R. Welch,
  [*Comma-Free Codes*](https://doi.org/10.4153/CJM-1958-023-9),
  Canadian Journal of Mathematics 10 (1958), 202–209. The primitive-orbit
  argument is classical. The printed page 206 gives the ternary dictionary
  `a<c, b>=d`; the current eighteen-word template is its reversal. Page 208
  already states the ordinary comma-free lower coefficient `2/9`. The
  scanned weak inequality was checked visually because text extraction is
  inaccurate. No novelty is claimed for this dictionary or its code density.
- B. H. Jiggs,
  [*Recent Results in Comma-Free Codes*](https://doi.org/10.4153/CJM-1963-021-1),
  Canadian Journal of Mathematics 15 (1963), 178–187. Page 184, Section 3,
  prints the 57-word dictionary used here. That printed page was downloaded,
  rendered and visually transcribed. Its 57 literal words are independently
  checked; the source's exhaustive-maximality claim is not a dependency.
  Theorem 5 explains why a size greater than 56 has no selected adjacency,
  but the new checker also verifies this property directly.
- Fimmel, Michel, Pirot, Sereni and Struengmann,
  [*Diletter and triletter comma-free codes over finite alphabets*](https://ajc.maths.uq.edu.au/pdf/86/ajc_v86_p233.pdf),
  Australasian Journal of Combinatorics 86(2) (2023), 233–270. Page 236
  describes even-length leading coefficients as undetermined. This does
  not certify today's best bounds or exclude an already known improvement.

The code conditions are different: ordinary comma-freeness forbids selected
starts `0,j,4`; the strict window condition also forbids triples spanning
only two or three shifts. The explicit separating dictionary
`{0123,1234,2345}` is documented in the quarter review. Therefore ordinary
comma-free lower bounds are transferred only after the extra strictness
check. Conversely, the reciprocal-pair upper proof uses only comma-freeness
and has that broader code-theoretic scope.

Further primary-source checks and actual access gaps are recorded in
`review/COMMA_FREE_LITERATURE_GATE.md`. The new package does not claim first
discovery of a coding-theoretic density bound merely because no prior
instance was located. All source URLs, template identities and new Kautz
implications are kept distinct from historical-priority questions.
