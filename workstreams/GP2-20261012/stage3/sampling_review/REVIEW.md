# Independent review: endpoint loss and injective alphabet sampling

GP2-20261012, 2026-10-13. **Verdict: PASS within the stated scope.**
This is an independent AI mathematical and computational review of
`../ENDPOINT_ROTATION_LOSS.md` and `../INJECTIVE_SAMPLING_BRIDGE.md`.
The reviewed source hashes are recorded in `execution.json`.
No human peer review, Lean proof, first-discovery certification, new
lambda_4 endpoint, or solution of the six-index problem is claimed.

The review checker uses only the Python standard library. It imports no
workstream checker, model, solver, or certificate. Its five-letter witness
is copied explicitly from the theorem statement. The reviewer did not
repeat the primary checker's raw Kautz BFS or literal 5^8 enumeration;
its strictness algorithm instead checks prefix/suffix compatibility for
every possible pair of gaps between three selected occurrences.

## 1. Endpoint theorem: quantifiers and proof audit

The alphabet must be finite and nonempty, the letter weights nonnegative
and summing to one, and strictness must count selected **positions**, even
if several positions spell the same word. The statements allow individual
letter weights to be zero. Prefix and suffix supports are combinatorial
supports of the given code, without deleting zero-weight letters.

For independent cyclic coordinates, let E_i be the event that the i-th
edge runs from Q to P. Its probability is uv. Among unordered pairs of
edges there are four adjacent pairs of probability uvh and two opposite
pairs of probability u^2 v^2. Each three-edge intersection has probability
uvh^2, and the four-edge intersection has probability h^4. Inclusion-
exclusion gives exactly the displayed expression for F. Repeated values
of the independent coordinates do not change this calculation.

A selected rotation needs a Q-to-P edge between its last and first
positions. Thus F is an event of empty selected rotation orbit. Strictness
permits at most one selected position in the four-cycle: after a rotation,
two selected positions would give selected starts 0,j,4 in the periodic
eight-letter word. This includes periodic words, where repeated selected
occurrences are still forbidden. Consequently the empty probability is
exactly 1-4p.

The restriction to H^4 remains strict. For h>0 the previously accepted
uniform trace deficit delta applies after normalizing its weights, giving
an empty event of mass at least delta h^4. Every H^4 tuple has Q-to-P
edges, so this event is disjoint from F. For h=0 no normalization is
needed, and the contribution is zero. Hence

    1-4p >= F + delta h^4.

This review accepts the earlier trace bound as an explicit dependency;
it does not independently re-prove its value. The additional maximum with
delta follows by also applying that same bound to the whole alphabet.

The nonnegative type expansion in the source is correct. In particular
F>=l^4+r^4. If n=0, an avoiding cycle that reaches R remains in R; one
that reaches H must then enter R and cannot return to H. The only other
avoiding cycles are entirely in L. Thus F=l^4+r^4 when n=0.

For a selected adjacency abcd,bcde, a selected word ending in a would
create selected starts 0,3,4; a selected word beginning in e would create
selected starts 0,1,4. Hence a is in L and e is in R. An active bridge
bcd has b in P and d in Q. It follows that i<=l, o<=r and b(C)<=uv,
including bridges carried only by zero-weight words. The stated bounds
on a(C), d(C), and d(C)^2 then follow from the exact bridge identities
and weighted Cauchy inequality. These identities are the second explicit
accepted dependency of the endpoint note.

Finally put x=sqrt(lr). The constraint l+r<=1 gives x in [0,1/2], and

    a(C) <= lr(1-l)(1-r) <= x^2(1-x)^2.

The function x(1-x) is increasing on [0,1/2]. Its smaller inverse is
q(a), so x>=q(a(C)). The chain

    1-4p >= F >= l^4+r^4 >= 2l^2 r^2 >= 2q(a(C))^4

is therefore valid, including both closed endpoints. It does not supply
a positive bridge penalty when a(C)=0 and does not improve the uniform
lambda_4 interval on its own.

## 2. Sampling hierarchy and arbitrary Boolean motifs

The integer n must satisfy n>=4. M_n is the extremum over codes contained
in the injective four-tuples, but their strictness is still required on
all eight-letter index words. Testing only injective eight-letter words
would invalidate this model (and would be vacuous for n<8).

For an iid sampled alphabet map f:[n]->A, the complete inverse image
of a strict code is strict, because every violating index word maps to
a violating word with the same three selected positions. Taking its
injective-word subset preserves strictness. Each fixed injective four-
tuple has four independent mu-images, regardless of whether their
values happen to agree. Hence E|D_f|=(n)_4 p exactly, without a collision
correction, and p<=M_n/(n)_4.

The opposite bound M_n/n^4<=lambda_4 uses the previously accepted strict-
template bridge to Kautz GP sets. Restricting an optimal N-index code to
a uniformly random n-subalphabet retains each word with probability
(n)_4/(N)_4, proving monotonicity of rho_n. Every injective rotation
orbit has four elements and at most one selected word, so rho_n<=1/4.
This proves the stated convergent bounds and error. The estimate 6/n
for the collision probability is the six-pair union bound. The resulting
finite-GP inequality for an independently certified M_n<=U_n follows
from the accepted deletion bound of at most 73m^3 vertices.

Theorem 2 is valid for any **finite Boolean formula** in the queried
indicators, including negation and overlapping queries. For a fixed
injection of its k labelled indices, each queried tuple is still
injective, and its membership in D_f is exactly its image's membership
in C. Thus the entire Boolean formula, not merely each positive query,
has the required distribution. Summing its truth value over injections
proves E N_Phi(D_f)=(n)_k Phi(C,mu). Taking the expectation of a pointwise
inequality proves transfer for any finite family of motifs with arbitrary
real coefficients; no positivity assumption on those coefficients or
independence between the indicator queries is needed.

The restriction that **each query** uses four distinct indices is
essential. The actual sampled letters may coincide. Recomputed canonical
labels, support-existence predicates and the nonlinear deletion cost do
not become finite Boolean query motifs merely by naming them. The source
correctly states these limitations.

## 3. Five-index witness and the precise certificate obstruction

The independent checker accepts all 30 listed words as injective words
on five letters. For gaps 1,2,3, respectively, it finds 4,15,60 compatible
ordered pairs. For each of the six positive gap pairs whose sum is at
most four, there is no selected middle word having both the required
predecessor and successor. This is an exact strictness proof: compatible
neighboring overlaps are sufficient to concatenate three words, and any
three selected occurrences in an eight-letter word yield one of those
six gap pairs. The criterion includes repeated indices and repeated
selected words.

The 30 words occupy all 30 injective rotation orbits exactly once. Each
four-letter restriction has six words and remains strict. This verifies
M_5=30 and M_4=6 using the general orbit upper bound.

The injective five-letter adjacent occurrences are exactly

    01234, 01324, 02134, 03124.

Thus N_adj(D)=4 and the proposed order-five inequality has left side
1/4+c/30 for every c>0. It cannot be a pointwise certificate on all
strict five-index codes. This does **not** refute an all-alphabet product
inequality p+c a<=1/4 from a different argument or a richer finite
certificate. For clarity, the same witness's actual uniform product
density is 30/5^4, whereas its injective normalized density is 30/120;
these are different quantities. No six-index search or extremal claim
was made in this review.

## 4. Actual independent checks

The accompanying checker performed:

- Complete enumeration of 256 L/R/H/N cyclic type strings, of which
  81 have no Q-to-P edge; output of the full monomial coefficient table.
- Direct rational comparisons of that probability, inclusion-exclusion
  and the nonnegative expansion on all 255 nonzero weight vectors in
  {0,1,2,3}^4 after normalization. Among them, 174 contain zero weights.
- The prefix/suffix strictness proof, orbit occupancy, four-letter
  restrictions, and four injective adjacent occurrences described above.
- An exact weighted sampling calculation for five Boolean motifs over
  all 32 maps from five indices to the binary strict template
  {0001,0011}, with weights (2/5,3/5). It includes adjacent conjunction,
  XOR, empty rotation, and shared-index queries involving negation.
  Every sampled index code is independently checked for strictness.
- Eight damaged-input controls: incorrect endpoint coefficient, negative
  and zero-total weights, a selected constant loop, a second selected
  rotation, a noninjective selected index word, a repeated-index motif
  query, and an incorrect adjacent-occurrence count. All are rejected
  through explicit exceptions, so the checks survive Python -O.

Commands, actual timestamps, exit codes, source hashes, and output hashes
are in `execution.json`; the deterministic output is `run.log`. The
ordinary and optimized runs agree byte for byte. These finite checks
support semantic accuracy; the all-alphabet validity rests on the written
proofs above and the explicitly identified inherited dependencies.

One stray `+` between “distinct indices” and “among” in the initial source
snapshot was reported to the primary agent and corrected there. No
mathematical error was found. Only this review subdirectory was edited;
the primary agent owns publication and integration.
