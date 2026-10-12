# Independent strict-window and original-GP audit of a 57-word dictionary

Date: 2026-10-12. **Verdict: PASS.** The review independently verifies the
exact finite dictionary below as a strict window code and proves its lift
to the original directed `Ka(m,4)` for arbitrary block sizes. It does not
use a theorem about maximum comma-free code size, repeat an optimum-code
search, or claim the historical dictionary as a new discovery. This is
independent AI-agent review, not external human peer review.

## 1. Frozen object and attribution boundary

The word list supplied for review is

`workstreams/GP2-20261012/literature_lifts/jiggs57_words.txt`

with SHA256

`26d405621e125016c26edf662bd1d18cb721bb6b09976c421fa5093e531a1f14`.

The exact list is reproduced here to fix the mathematical object:

```text
DBDD DDAD DDCD CCCB BCCB
DCCB ACCA DABD BABB DBCB
CACB DACB DCAD DACD DAAD
BCAD BAAD ACAB BAAA DCBD
BDAD BDCD CCCD BCCD DCCD
ACCD DABB BCAB ABCB DAAB
BBAD DCAB CACD DBAD ACAD
DBCD BAAB BCAA DCBB DBBD
DBBB CCCA BCCA DCCA ACCB
BABD BBCB BACB AACD BBCD
BACD DCAA ABAD DAAA AACB
ACAA ABCD
```

Call this set `D`. It contains exactly 57 distinct words over the four
labels `A,B,C,D`. The supplying source audit identifies B. H. Jiggs,
*Recent Results in Comma-Free Codes*, Canadian Journal of Mathematics 15
(1963), 178–187,
[DOI 10.4153/CJM-1963-021-1](https://doi.org/10.4153/CJM-1963-021-1),
page 184, Section 3. The original
[publisher PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3F80EAEA1B86983AF9CCBB3410B93FF9/S0008414X00029382a.pdf/div-class-title-regent-results-in-comma-free-codes-div.pdf)
is linked by that audit. The independent mathematical review
starts from the frozen words above, and does not assume either that the
published code is optimal or that its claimed structural properties are
correct. The primary-source transcription and bibliography are handled by
the separate literature source record. No historical priority claim for
the Kautz application follows from source non-detection.

After the independent calculations, Sections 1–2 of
`../literature_lifts/JIGGS57_WEIGHTED_LIFT.md` were read and compared with
this audit. The reviewed complete-file SHA256 was
`069a2aad0a9bf45796ad97f549c0bfa282dce0d0a4a3b1114f74f47b5dfdde23`.
The PASS verdict covers the strictness/GP bridge and count formulas in
those sections. The four-weight maximization in its Sections 3–5 is assigned
to a separate reviewer and is outside this review's acceptance claim.

The checker translates `A,B,C,D` to `0,1,2,3`, respectively. Both the exact
source hash and that alphabet binding are recorded in the certificate.

## 2. Finite strictness certificate

For a dictionary of four-letter words, strictness means that every
eight-letter word has at most two selected four-letter window occurrences
at starts `0,1,2,3,4`. All eight labels may repeat, and identical selected
words at different starts count as different occurrences.

The independent checker reconstructs `D` from the frozen source and loops
over all `4^8=65,536` possible eight-letter words. Its exact selected-window
count distribution is

| Number of selected occurrences | Number of eight-letter words |
| --- | ---: |
| 0 | 7,289 |
| 1 | 43,534 |
| 2 | 14,713 |

These counts sum to 65,536. There is no word with three or more selected
occurrences. This is a complete finite check of the precise strict-code
condition, rather than a sample of walks or a count of distinct codewords.

An independently organized audit checks two useful sufficient properties:

- None of the `57^2=3,249` ordered pairs `(u,v)`, including `u=v`, satisfies
  `suffix_3(u)=prefix_3(v)`. Hence two selected windows cannot be adjacent.
- For each of those ordered pairs, none of the three interior four-windows
  at offsets `1,2,3` in the concatenation `uv` belongs to `D`. This checks
  `3*57^2=9,747` possibilities and establishes ordinary comma-freeness.

These properties imply strictness without any further enumeration: three
nonadjacent starts in `0,...,4` must be `0,2,4`; the endpoint windows then
form a concatenation of two codewords, and its middle word at offset two
contradicts ordinary comma-freeness. Equality of the endpoint codewords is
allowed in that check. This implication does not assert that arbitrary
comma-free codes are strict, since adjacent selected windows can occur in
other comma-free codes.

Thus strictness is checked both directly from its complete finite
definition and by a separate exact pair/overlap calculation. The finite
dictionary and the standard-library checker are the certificate; no
floating-point optimization or unverified claim from the original paper
is a premise.

## 3. Arbitrary-block construction in the original directed Kautz graph

Let `B_A,B_B,B_C,B_D` partition an actual alphabet of size `m>=3`; empty
blocks are permitted. Let `pi` be the map from actual letters to their
block labels. Define

\[
S=\{v_0v_1v_2v_3:\ v_i\ne v_{i+1}\ (0\le i<3),\quad
\pi(v_0)\pi(v_1)\pi(v_2)\pi(v_3)\in D\}. \tag{1}
\]

**Theorem 1.** The set (1) is general position in the original directed
`Ka(m,4)` for every choice of the four block sizes.

**Proof.** Original vertices have unequal adjacent actual letters. An arc
maps `abcd` to `bcde` for every `e!=d`; any digons are retained. Every
directed walk is read in consecutive four-letter windows of a word.

Any pair of vertices is joined by a directed walk of length at most four:
append all four target letters if the last initial letter differs from
the first target letter, and append only the last three target letters
if those letters agree. These appends are legal by the target's adjacent
inequalities. Hence every shortest directed path has at most four arcs.

The block labels along such a path form a word of length at most eight,
which may be extended arbitrarily to length eight. Section 2 permits at
most two selected window occurrences. Therefore no shortest directed path
between selected endpoints passes through a third selected vertex. This
is the original all-shortest-paths general-position definition. It is not
the existence of one avoiding path. ∎

The proof explicitly permits equal adjacent block labels and nonadjacent
repetitions of actual letters. Only the original adjacent actual-letter
inequalities enter (1).

## 4. Exact counts and the asymptotic consequence

Write `n_A,n_B,n_C,n_D` for the four block sizes. The exact size of (1) is

\[
\boxed{
F(n_A,n_B,n_C,n_D)=
\sum_{c\in D} n_{c_0}
\prod_{i=1}^{3}\bigl(n_{c_i}-{\bf1}_{c_i=c_{i-1}}\bigr).
} \tag{2}
\]

Indeed, the first actual letter has `n_(c_0)` choices. Each later letter
has all letters in its prescribed block available, except the immediately
preceding actual letter when both blocks coincide. This counts every
original legal vertex exactly once and imposes no condition on
nonadjacent actual letters. Formula (2), together with the 57-word list,
is an explicit integer polynomial valid for all nonnegative block sizes.

Regenerating the patterns from the word list gives 23 with no equal
adjacent block pair, 28 with one, and 6 with two. Equal block size `q>=1`
therefore gives

\[
\begin{aligned}
F(q,q,q,q)
&=23q^4+28q^3(q-1)+6q^2(q-1)^2\\
&=57q^4-40q^3+6q^2.
\end{aligned}
\]

Consequently

\[
\boxed{\operatorname{gp}(\operatorname{Ka}(4q,4))
\ge57q^4-40q^3+6q^2\qquad(q\ge1).} \tag{3}
\]

For arbitrary `m>=4`, let `q=floor(m/4)`, distribute all actual letters
among four blocks each of size at least `q`, and use (1). Restricting to
the first `q` actual letters of every block gives at least the count in
(3). Theorem 1 proves GP in the entire `m`-letter graph, so this argument
does not assume that arbitrary induced embeddings preserve geodesics.

It follows that

\[
\liminf_{m\to\infty}
\frac{\operatorname{gp}(\operatorname{Ka}(m,4))}{m^4}
\ge\frac{57}{256}.
\]

The inherited density-limit existence turns this into
`lambda_4>=57/256`. Since `57/256-2/9=1/2304>0`, the ternary lower bound
`2/9` is not the limiting optimum. No exact value of `lambda_4` is inferred.

For the convenient unequal block sizes `(5q,5q,3q,3q)`, independent
per-word multiplication in `Z[q]` gives

\[
\boxed{\operatorname{gp}(\operatorname{Ka}(16q,4))
\ge14733q^4-2528q^3+94q^2\qquad(q\ge1).} \tag{3a}
\]

For all `m>=16`, take `q=floor(m/16)` and assign the remaining actual
letters arbitrarily to the four blocks. The full construction is GP by
Theorem 1 and contains the subset counted in (3a). This proves the same
lower count for every such `m`, and in particular

\[
\lambda_4\ge14733/65536=0.2248077392578125.
\]

This is an exact evaluation at fixed integer block proportions. It does
not use a numerical optimum or assert that these rational proportions
maximize the four-weight polynomial.

More generally, for any probability vector `(p_A,p_B,p_C,p_D)`, take block
sizes asymptotic to `m p_i`. Formula (2) gives the leading density

\[
P(p_A,p_B,p_C,p_D)=\sum_{c\in D}\prod_{i=0}^{3}p_{c_i}, \tag{4}
\]

and Theorem 1 proves `lambda_4>=P(p)` for every such vector. Formula (4)
justifies subsequent exact rational weighted lower bounds, without
assuming that equal block weights optimize this particular dictionary.
Numerical optimization of (4), if performed elsewhere, must still be
distinguished from an exact evaluation at a specified rational vector.

## 5. Independent original-adjacency and BFS audits

The actual command, executed with Python 3.12.14 on 2026-10-12 and returning
exit code zero, was

```sh
python workstreams/GP2-20261012/construction/verify_jiggs57.py > workstreams/GP2-20261012/construction/jiggs57_check.log
```

The checker uses the original shift-and-append/BFS engine already written
by this independent reviewer in `verify_lower18.py`, frozen at SHA256
`f46274fb83baf013131258cc3e62b62e6f535f5aea81d0fc3e15212ea19d76db`.
It does not import a discoverer's checker or distance certificate. Every
ambient vertex and every original arc is reconstructed before distances
are computed by BFS. The suffix/prefix distance formula is compared to
all those distances, and is not used to generate them.

| Ordered block sizes | Actual letters | Ambient vertices | Selected vertices | All ambient ordered-pair BFS distances |
| --- | ---: | ---: | ---: | ---: |
| `1,1,1,1` | 4 | 108 | 23 | 11,664 |
| `2,1,1,1` | 5 | 320 | 72 | 102,400 |
| `2,2,2,2` | 8 | 2,744 | 616 | 7,529,536 |

These are construction audits, not assertions of finite optimality.
Each selected-pair distance is stored in the certificate. To check the
original GP property efficiently, the verifier represents, for each
selected `u` and distance `a`, the set of selected vertices at distance
`a` from `u` as a bitset. For every ordered selected endpoint pair `(u,v)`
at distance `d`, and every positive split `a+(d-a)=d`, it checks that

\[
\{w:d(u,w)=a\}\cap\{w:d(w,v)=d-a\}=\varnothing.
\]

This excludes exactly all distinct selected triples on a shortest path.
The positivity of both distances guarantees that the middle vertex is
distinct from the endpoints. This is an exact reorganization of the
triple test; it does not sample middle vertices.

For the three cases the checker examines respectively 506, 5,112, and
378,840 distinct ordered endpoint pairs, with 1,305, 13,704, and 1,065,272
positive distance splits. These tests cover all 10,626, 357,840, and
232,607,760 distinct ordered triples, respectively. There is no violation.

The deterministic `jiggs57_certificate.json` contains the exact word list,
its source hash, all ambient vertices, original adjacency lists, complete
selected sets, every selected-pair distance, and the finite audit totals.
It was reloaded and replayed against another adjacency/BFS reconstruction
during the successful execution. Its SHA256 is

`7477898ad8cefffe37bcb9a62d5cc7b48640364993393b712c203893de8b12e1`.

## 6. Negative controls and acceptance scope

Seven deliberate failures were checked and rejected:

- Adding `AAAA` to the dictionary selects all five windows of `AAAAAAAA`.
- The original Kautz vertices `0101,1012,0120` have successive distances
  `1,1` and endpoint distance `2`; the GP bitset test rejects them as a
  geodesic triple. Their complete directed distance matrix is recorded.
- A wrong actual-alphabet size is rejected against the block-size binding.
- A corrupted selected-pair distance is rejected against fresh BFS.
- A damaged selected set is rejected against the defined full lift.
- A removed original arc is rejected against original adjacency.
- A changed claimed count is rejected against both enumeration and (2).

The actual outputs and explicit witnesses are in `jiggs57_check.log`.

The complete finite strict-code certificate and the universal written lift
argument justify (3) and (4). They do not establish optimality of the
historical dictionary, exact maximum GP values, attainment of the limiting
density, or a general formula for all word lengths. No Lean formalization
or successful Lean compilation is claimed for this result. All source
attribution and open-status claims remain limited to the separately
documented literature coverage.
