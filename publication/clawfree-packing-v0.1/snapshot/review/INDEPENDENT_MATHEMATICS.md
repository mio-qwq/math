# Independent mathematics review: claw-free (1,1,3,3,4) obstruction

Status: **written mathematics, independent small-case runtime and complete mathematical/semantic manuscript review PASS**.
This is an independent AI review, not external human peer review.
The reviewer did not participate in discovery, Lean implementation, or manuscript writing.
Only this review directory is writable by the reviewer. No Lean compilation, Git mutation,
old 531441-case enumeration, or publication has been performed by the reviewer.

## Exact inputs and current coverage

- Original source: [Mortada, El Zein and Al Hajjar, arXiv:2608.02566v1](https://arxiv.org/html/2608.02566v1), definition, Figure 1/Proposition 1, Section 6 Problem 1.
- Frozen mathematical Lean input, fully read: `research/workstreams/ROOT/clawfree-11334-counterexample/ClawFree11334.lean`, SHA-256 `afad6d3313c93fd5681be0ba0e25d302c73d019448681cb4c6552f8a0e0765b2`.
- Frozen JSON graph input, hash checked: `counterexample.json`, SHA-256 `7d1cdd61f032185728ffac6a6b0b6a79c611e0a36341a78eb35610df55b95ccd`.
- Source PDF downloaded into this review directory: `source-arxiv-2608.02566v1.pdf`, SHA-256 `35981c55c509304c36ac6079ae0d60fa5c70bc7d57fd3537f6e8a8dd684f8dbc`.
- `PROOF.md` was read **after** the core necessary conditions and odd-ring contradiction were independently reconstructed. It agrees with that reconstruction. SHA-256 `9ff9ef34895a71fc0d2c3c66960fde9d30de4405c09815af21936d9e91f2ea04`.
- Historical `INDEPENDENT_REVIEW.md` was not used to derive or accept the mathematics.
- `lean-audit.json` was inspected as historical metadata only. This reviewer has not rerun Lean and does not convert historical metadata into a new compilation claim.
- Source PDF Figure 1 was actually visually inspected in `source-figure1-page3.png`. Its 12 vertex circles form four disjoint triangles, with the six reciprocal inter-triangle edges giving a K4 quotient. This directly confirms the order/structure boundary used to exclude H.
- `paper/main.tex` and `paper/references.bib` were fully reviewed; `FINAL_MANUSCRIPT_REVIEW.md` binds accepted final TeX `dc1b75ef1aa6d01dd4a766b65e33e4a13b96418ad8dbae44d8a4f14e8e82aed9` and Bib `a2cf6d36e99843b73016dafe370d28c58ecaec941d77675535c4e86c9dbe482f`. Both reviewer precision suggestions were resolved; no mathematical must-fix item remains.

## Original scope and semantic alignment

The source question concerns every connected claw-free subcubic graph other than its exceptional graph H. Its five labels are distinct, with radii 1,1,3,3,4, and equality of a label requires distance **strictly greater** than its radius. There is no three-connectivity assumption or diamond-free-core assumption. The fixed witness is cubic, so it satisfies subcubicity.

The original Figure 1 and Proposition 1 identify H with the triangle replacement of K4, hence with 12 vertices. The proposed witnesses have 12k vertices for odd k>=3, so cardinality excludes H. The Lean endpoint separately excludes isomorphism to **every** simple graph on `Fin 12`; it does not need a special labelling of H.

This is a negative answer to this precise Problem 1. It is not a solution of the Gastineau--Togni (1,1,2,3) problem, a refutation of a (1,1,3,3,3) positive theorem, a minimum-order result, or a determination of the ordinary packing chromatic number.

## Independent reconstruction

Let D_k have vertices a_i,b_i,p_i,q_i, with i in Z/kZ, diamond edges
a_i b_i, a_i p_i, a_i q_i, b_i p_i, b_i q_i, and joining edges q_i p_(i+1).
For k>=3 the vertices and all listed edges are distinct, and every vertex has degree three.
The diamonds are connected and their joining edges make a cyclic connected graph.
It has 4k vertices and 6k edges.

Let G_k have one vertex (v,w) for each oriented incidence vw of D_k. For each v,
join the three (v,w) vertices into T_v. For every core edge vw, also join
(v,w) to (w,v). This defines a simple connected graph with 12k vertices,
12k internal edges and 6k reciprocal edges, hence 18k edges. Every vertex has
two adjacent neighbours in its own triangle and one reciprocal neighbour:
it is cubic and cannot be the centre of an induced claw.

### Arbitrary high representatives

Suppose a packing colouring c exists. A triangle T_v cannot be coloured with
only its two radius-one labels, since those classes are independent. Choose
**any existing** vertex r_v=(v,s_v) in T_v whose label is one of A,B,C, with
radii 3,3,4, and set f(v)=c(r_v). No vertex is recoloured or discarded from
the assumed colouring, and no uniqueness of a high vertex is asserted.
Representatives from different T_v are distinct.

For a core edge uv the following original-graph walk connects arbitrary
selected representatives:

    (u,s_u), (u,v), (v,u), (v,s_v).

Consecutive equal endpoints are omitted. The other steps are real edges,
so length is at most three. Thus any shared high label would violate its
radius, and f is a proper three-colouring of D_k. This is true for every
allowed choice of high representatives, including a triangle with several
high labels.

### Private-neighbour condition for radius four

Let I=f^(-1)(C), v in I, and r_v=(v,w). For any u in I with u!=v and wu a
core edge, the real original-graph walk

    (v,w), (w,v), (w,u), (u,w), (u,s_u)

has at most four edges, again omitting a final repeated point if needed.
Its endpoints are distinct, so it contradicts the two selected vertices'
common radius-four label. Therefore

    N_D(w) intersect I = {v}.

The equality, rather than just an inclusion, follows because vw is itself
an edge. Also f(w)!=C by properness. Hence w is an **external** private
neighbour. Only a necessary condition has been derived. The proof does not
assume that properness/private neighbours are sufficient for a lift.

The four-edge bound is essential: a four-edge same-label separation is
allowed by radius three but forbidden by radius four. There is no off-by-one
conversion from packing distance >4 to distance >=4.

### Complete diamond-tip obstruction

In a properly three-coloured diamond, the adjacent a_i,b_i use different
labels. Both tips must use the remaining label, so f(p_i)=f(q_i)=t_i.
Suppose t_i=C. The **entire** neighbour set of p_i is

    {a_i,b_i,q_(i-1)}.

The first two neighbours are adjacent to both C-tips p_i and q_i, so neither
is private to p_i. The joining edge p_i q_(i-1) gives f(q_(i-1))!=C. The
proper triangle a_(i-1)b_(i-1)q_(i-1) then has one centre of label C.
That centre is a C-neighbour of q_(i-1) distinct from p_i. Thus the third
candidate is not private either. All three candidates have been excluded;
there is no hidden fourth external neighbour.

This contradiction excludes C from every tip pair. The joining edges now
give t_i!=t_(i+1) with t_i in {A,B}. Alternation around an odd cycle forces
t_0 to equal its opposite, impossible. This proves the written theorem
for every odd integer k>=3. For k=3 there are three distinct diamonds and
the three joining inequalities make the three t_i pairwise different,
which is already impossible with two labels. No argument degenerates at k=3.

### Diamond-free property of G_k

The reciprocal edges are a matching. A triangle containing two or more
reciprocal edges would have two such edges meeting at a vertex, impossible.
A triangle containing exactly one reciprocal edge would have a two-step
path between its endpoints consisting of internal edges. Internal edges
stay within a single T_v, whereas the reciprocal endpoints lie in two
different T_v. That is also impossible. Consequently every triangle of
G_k is exactly one T_v. These triangles are pairwise disjoint. A diamond
has two triangles sharing an edge, so G_k contains no diamond, even as a
non-induced subgraph. This is a direct written structural conclusion;
the old Lean endpoint does not formalize it.

## Lean semantic review, without a new execution claim

The fully read frozen source uses actual `SimpleGraph (Fin 36)`, its degree,
explicit `graph.Walk` objects, and `graph.edist`. The graph is defined by
same-block distinct vertices plus an involutive reciprocal `partner`.
Fixed data decisions include equality with the embedded 54-edge list,
cubicity and port/core facts. They do not enumerate all colourings.
The distance lemmas construct walks and use `Walk.edist_le`; they do not
postulate a distance matrix or claim a walk is shortest.

`Packing11334` quantifies every pair of distinct vertices and retains the
strict inequality in the original graph's `edist`, with radius labels
1,1,3,3,4. The contradiction quantifies unrestricted `Fin 36 -> Fin 5`
colour functions. Extraction chooses an existing high slot via Classical
choice, converts its label to `Fin 3`, and proves properness and private
neighbours from those actual walks. `core_obstruction` then excludes the
fixed three-diamond core. No graph-colouring normal form is inserted.

Formal coverage is the fixed k=3 witness. The entire odd-k theorem,
diamond-freeness, new small-case BFS runs and any historical-priority claim
are outside that Lean endpoint. A current source-bound serial replay is
ROOT's task; this review does not assert it has already happened.

## Literature and wording risks

[Brešar--Kuenzel--Rall, arXiv:2409.15455v1, Section 2](https://arxiv.org/html/2409.15455v1#S2) already defines rings of diamonds and uses triangle replacement of cubic multigraphs. The paper should cite this construction history and avoid saying these graph operations or graph families are themselves newly invented.

[Anderson--Kuenzel--Marcano Cuellar, arXiv:2607.25198v1, Theorem 4](https://arxiv.org/html/2607.25198v1#S2) states the diamond-free claw-free cubic (1,1,2,3) positive result. Since G_k itself is diamond-free, this is relevant context, but its palette is different; the present obstruction does not contradict that theorem. The diamonds of D_k must not be confused with diamonds in G_k.

This review checks the precise cited v1 problem and these two construction/palette boundaries. It is not an exhaustive novelty or priority certificate. The manuscript must not call the AI review human peer review or describe the fixed Lean witness as a universal odd-k formalization.

## Remaining work at this durable checkpoint

The reviewer has completed its assigned mathematical/manuscript scope. ROOT's final package replay, PDF visual QA, execution/manifest binding and human/priority questions are separate from this independent AI mathematical PASS; see `FINAL_MANUSCRIPT_REVIEW.md`.

## Actual independent runtime: 2026-10-12

`independent_bfs_checks.py` was newly written in this review directory and actually
run with Python 3.12. It imports only standard-library modules, never the original
verifier. Its run began at 2026-10-12T10:50:36.693918+00:00 and ended at
2026-10-12T10:50:36.752517+00:00 with process exit code 0 and status PASS.

- Program SHA-256: `41fcbebed9e58f15c29867f490e9e08ffe416337102e973713b5b7b1cb688e17`.
- Saved output: `independent-bfs-results.json`, SHA-256 `0e5ed3714ad79d522e0a7f8f6f40f6a7fcfb79760f4cef26c45eda24321be84a`.
- The output binds all exact input hashes. The original verifier was hashed only, not executed or imported; its SHA-256 is `e9e7cb20a1b6989905563193bd92c388231e6e3a049caa27f6db1b33fdb7f573`.
- Historical audit JSON SHA-256 is `c017e9c568d6c75ca0ceff19b898680a31debdb9ab282c552f9b046e0b01b03a`; hashing it is not a Lean rerun.
- HISTORY SHA-256 is `933174d6a36d9424fff4331024f62515e3234fd3485fbfd03decd4541f5a40c6`; it was not used to justify the proof.

| k | Core order/size | Expanded order/size | Triangles | Adjacent endpoint checks | Private endpoint checks | Local tip cases |
|---|---|---|---|---|---|---|
| 2 | 8/12 | 24/36 | 8 | 108 | 144 | 32 |
| 3 | 12/18 | 36/54 | 12 | 162 | 216 | 48 |
| 4 | 16/24 | 48/72 | 16 | 216 | 288 | 64 |
| 5 | 20/30 | 60/90 | 20 | 270 | 360 | 80 |
| 7 | 28/42 | 84/126 | 28 | 378 | 504 | 112 |

Every constructed graph passed simplicity, connectivity, degree-three,
claw-free, exact-triangle and no-shared-triangle-edge checks. The small-case
constructor independently recovered the certificate's sorted incidence labels,
all 18 core edges, all 54 expanded edges, all reciprocal partner slots and the
five radii. All 36x36=1296 vertex pairs were compared against both the JSON
graph and the frozen Lean definition/embedded edge list.

The 1134 adjacent-endpoint checks and 1512 private-endpoint checks validated
both explicit edge-by-edge walks and independently computed BFS distances;
all were within the required bounds. The 336 local tip cases use only the
six colour permutations of one diamond and locally compatible pairs of
diamonds, not global core colourings or original colourings. They verified
the complete candidate-neighbour obstruction for both tip directions.

The exact negative-control path for k=3 was

    (2,11), (11,2), (11,8), (8,11), (8,9).

Its BFS distance is exactly 4. The same-label pair is allowed at radius 3
and forbidden at radius 4, confirming the radius threshold used in the
private-neighbour proof. For even k=2,4 the program exhibited proper core
three-colourings with C at every a_i and private neighbour b_i; this checks
that the oddness obstruction is not silently applied to even rings. No
packing-colouring existence claim is inferred from these necessary-condition
controls. Local triangles with distinct labels (0,2,3) or (2,3,4) also
illustrate why high-point uniqueness cannot be assumed from a triangle alone;
these are expressly local examples, not colourings of G_k.

The written infinite-family proof is accepted independently. The finite
runtime checks guard construction/metric/semantic errors; they are not the
proof of all odd k. No mathematical gap was found within the stated theorem.
