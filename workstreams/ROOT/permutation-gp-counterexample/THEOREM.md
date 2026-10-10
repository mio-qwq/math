# A counterexample to permutation-digraph general-position optimality

For the original permutation digraph `Pe(6,3)`, there is a general-position set
of 90 vertices. The proposed exact value is 84. Thus the unnumbered optimality
conjecture immediately following Theorem 3.6 in Chandran et al.,
[*The general position number of digraphs*, arXiv:2604.15909v1,
Section 3.3](https://arxiv.org/html/2604.15909v1#S3.SS3), is false.
Theorem 3.6 supplies a lower bound; that theorem remains valid.

## The original object and a complete finite counterexample

The alphabet is `A={0,...,8}`. Vertices are ordered triples of pairwise distinct
letters. The arc rule is

`(a,b,c) -> (b,c,z)` if and only if `z` is absent from **all three** old letters.

In particular, appending the dropped first letter is forbidden. The graph has
`9*8*7=504` vertices and `504*6=3024` arcs. Distances are directed distances in
this full graph. General position means that no shortest directed path between
selected vertices contains a third selected vertex, as in the original
Definition 2.1.

Partition the alphabet into `T={0,1,2}` and `C={3,...,8}`. Let

`S={(a,b,t): a,b in C, a!=b, t in T}`.

All selected triples are valid vertices and `|S|=6*5*3=90`. Fix two different
selected vertices `u=(a,b,t)` and `v=(c,e,s)`. After one shift the old terminal
letter `t` is in position two, and after two shifts it is in position one.
Those positions must contain letters of `C` in a selected vertex. Therefore
there is no walk of length one or two from `u` to `v`, and their distance is
at least three.

At most four letters of the six-element set `C` occur in `a,b,c,e`. Choose two
different letters `p,q` from the remaining letters. Then

`(a,b,t) -> (b,t,p) -> (t,p,q) -> (p,q,c) -> (q,c,e) -> (c,e,s)`

is a legal five-step walk. Each appended letter is absent from the entire old
word: the buffer letters avoid both prefixes and each other, the target prefix
letters are distinct, and `T` and `C` are disjoint. Hence every directed
distance between different selected vertices lies between three and five.
For three different selected vertices `u,w,v`,

`dist(u,w)+dist(w,v) >= 6 > 5 >= dist(u,v)`.

If a shortest `u,v` path passed through `w`, its two subpaths would be shortest
and the distance equality would hold. The strict inequality excludes that
possibility for every ordered triple. Thus `S` is in general position. The
original parameter hypotheses are satisfied: `k=3` and `d=6>=2k`. The proposed
value is `2(7)_2=2*7*6=84<90`. No exact maximum or minimality computation is
needed to refute this conjecture.

## Written extension to every original parameter pair

For `k>=3` and `d>=2k`, put `N=d+k`, reserve three terminal letters `T`, and use
all injective `(k-1)`-letter prefixes from `C=A\T`. This gives

`|S|=3(N-3)_(k-1)`.

Here `(x)_r` is the falling factorial. A terminal letter retained from the
initial word excludes any positive walk shorter than `k` between different
selected vertices. The union of two endpoint words uses at most `2k` letters,
whereas `N>=3k`. Choose `k-1` different unused buffer letters. Append these
buffers, then all `k` target letters. Immediately before the first target
letter, the old word consists of the original terminal and the buffers; that
target letter is in `C`, the old terminal is in `T`, and the buffers avoid the
target. This step and all subsequent steps satisfy the original arc rule.
The resulting walk has length `2k-1`.

All selected directed distances therefore lie in `[k,2k-1]`; the same strict
distance argument proves general position. Moreover, with the positive factor
`F=(N-3)_(k-2)`,

`3(N-3)_(k-1)-2(N-2)_(k-1) = (d-2k+1) F > 0`.

Thus the three-terminal construction strictly improves the conjectured value
for every original parameter pair. This is a written universal proof; the
fixed counterexample and the universal extension have separate formalization
scopes recorded in `verification.json`.

## Lean proof of the original fixed counterexample

`PermutationGP90.lean` uses all injective `Fin 9` triples and the complete original
arc relation. Its `SimplePath` binds the vertex list, ordered endpoints, actual
arcs and length; repeated vertices are excluded by construction. Kernel proofs
convert any walk to a no-longer simple path and split a path at a support vertex
with exact total length. `OriginalGeneralPosition` quantifies every shortest
simple path and every selected point on it. The final declarations
`permutation_original_counterexample` and `not_original_conjectured_upper_bound`
therefore use the original path property, rather than an assumed distance table.

The actual ROOT3 execution compiled the exact published source with zero errors,
warnings or panics. Eighteen axiom audits use only subsets of `propext`,
`Classical.choice`, and `Quot.sound`, including declarations with empty axiom
sets. There is no `sorry`, `native_decide`, or added axiom. `axioms.txt` and
`verification.json` retain the actual successful audit and timestamps. The
all-parameter extension above has a separate independently checked written
proof; it is not claimed to be universally Lean formalized.

Replay from the repository's pinned project directory
`002-weighted-rectangular-pruning/proof/mathlib` with Lean 4.34.1 and the exact
Mathlib revision recorded in `verification.json`:

```text
lake env lean ../../../workstreams/ROOT/permutation-gp-counterexample/PermutationGP90.lean
```

## Evidence, provenance and limitations

The source's Theorem 3.6 uses a two-terminal construction. The present
three-terminal extension explicitly builds on that credited construction.
The frozen discovery packet is [distributed stream B, e6ff181](https://github.com/mio-qwq/math/commit/e6ff18129aadad59150473c2e5faca16c5435d42).
ROOT independently reconstructed the finite argument; a separate agent checked
the original definitions, ran an independently written integer verifier before
reading B's program, and reviewed the full-parameter argument.

The independent verifier reconstructs all 504 vertices and 3024 arcs, certifies
504 integer BFS rows, checks 8010 selected ordered pairs and all 704880 ordered
distinct triples, and rejects two corrupted controls. Its results and exact
selected set are in `verify_independent.json`. Run with Python 3, standard
library only:

```text
python verify_independent.py
```

The checker writes its sibling JSON report, including current time and source
hash. Preserve the published receipt when replaying if exact original bytes
are needed. Historical firstness is not established; bounded primary-source
and duplicate searches are recorded in `SOURCES.md`. This mathematical result
is distinct from a priority claim, a journal referee decision, and a paper
submission.

AI systems assisted the mathematical derivation, exact checking, independent
review, formalization and preparation of these technical materials. No AI
system is designated as a paper author. Human author identity and responsibility
remain to be confirmed separately before any formal submission.
