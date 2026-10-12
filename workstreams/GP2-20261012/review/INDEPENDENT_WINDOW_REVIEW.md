# Independent review: seven- and nine-window upper bound for Kautz length four

Date: 2026-10-12. Status: independent written proof and original-adjacency
computational checks. This document makes no claim of Lean formalization or
external human peer review.

## Result and scope

Let `Ka(m,4)` have alphabet `[m]`, all four-letter words with unequal adjacent
letters as vertices, and arcs `abcd -> bcde` whenever `d != e`. A general-position
set means that no shortest directed path between two selected vertices contains
a third selected vertex. Reverse arcs and repeated nonadjacent letters are
allowed. These are the conventions of Definition 2.1 and Section 3.2 of
[Chandran et al., arXiv:2604.15909v1](https://arxiv.org/html/2604.15909v1).

For every `m >= 7`, put

\[
  \delta_m=1-\frac{(m)_7}{m^7}
  =1-\prod_{j=0}^{6}\left(1-\frac jm\right).
\]

For every general-position set `S` in `Ka(m,4)`, put `p=|S|/m^4`. Then

\[
  p\leq\frac{2+5\delta_m}{7},\qquad
  6p^2-9p+2+15\delta_m\geq0.                     \tag{1}
\]

Consequently, for every `m >= 221`,

\[
 \operatorname{gp}(\operatorname{Ka}(m,4))
 \leq \left\lfloor \frac{m^4}{12}
       \left(9-\sqrt{33-360\delta_m}\right)\right\rfloor. \tag{2}
\]

In particular, without needing to assume the existence of a density limit,

\[
 \limsup_{m\to\infty}
 \frac{\operatorname{gp}(\operatorname{Ka}(m,4))}{m^4}
 \leq \frac{9-\sqrt{33}}{12}
 =0.27128644612183095\ldots.                    \tag{3}
\]

These statements concern the full GP set, including vertices whose
nonadjacent letters repeat. There is no additional repeated-word correction
term in (1) or (2).

## 1. Distance from the original adjacency

For distinct legal words `u,v`, let `r` be the largest proper suffix/prefix
overlap length, allowing `r=0`. Then

\[
 d(u,v)=4-r.                                   \tag{4}
\]

Indeed, after `t<4` shifts, the first `4-t` letters of the new state are
exactly the last `4-t` letters of `u`. Thus reaching `v` in `t<4` steps requires
an overlap of length `4-t`, and no path shorter than `4-r` can exist.

For the other direction, append the last `4-r` letters of `v` to `u`.
When `r>0`, the concatenation is legal because the overlap agrees and every
adjacent pair inside `v` is unequal. When `r=0`, the last letter of `u` differs
from the first of `v`, since equality would itself give a one-letter overlap.
Therefore this is a legal walk of length `4-r`. The lower bound shows it is
shortest, hence a path. Equal vertices have distance zero and are treated
separately.

This proof uses the original shift adjacency. It does not replace the graph
by an orientation or impose an independent-set assumption on `S`.

## 2. Seven distinct cyclic letters

Take pairwise distinct letters `a_0,...,a_6`, with subscripts read modulo seven,
and let

\[
 W_i=a_i a_{i+1}a_{i+2}a_{i+3}\quad(0\leq i<7).
\]

All seven words are legal and distinct. For `1 <= t <= 4`, the directed walk
`W_i,W_{i+1},...,W_{i+t}` is a geodesic of length `t`: if an overlap of length
`s>0` exists between the endpoints, distinctness forces `4-s=t` modulo seven.
With `1 <= s <= 3` and `1 <= t <= 4`, this means exactly `s=4-t`; if `t=4`
there is no positive overlap. Equation (4) applies.

Any three distinct start positions split the circle into three positive
integer gaps summing to seven. A largest gap has length at least three.
The complementary clockwise segment has length at most four and contains
all three chosen start positions, with the middle one strictly interior.
The corresponding window path is a geodesic. Hence any GP set contains at
most two of the seven windows.

This is an existence-of-a-forbidden-geodesic argument and therefore respects
the universal shortest-path quantifier in the GP definition. It makes no
claim that arbitrary long walks are geodesics.

## 3. Iid cyclic windows and exact pair counts

Define `f` on all words in `[m]^4` as the indicator of `S`; it is zero on
illegal words. Let `a_i` be independent uniform letters. A single window has
mean `p`. For `d=1,2,3`, define

\[
 q_d=\mathbb E\big[
 f(a_0a_1a_2a_3)f(a_da_{d+1}a_{d+2}a_{d+3})\big],
 \qquad Q=q_1+q_2+q_3.
\]

For `n=7` or `9`, take `n` iid letters, form the cyclic windows, and let `N_n`
count selected windows, with multiplicity by starting position. Repeated
letters and repeated windows on these random circles cause no definitional
problem.

For an odd circle, every unordered pair of start positions has a unique
short circular separation `d <= (n-1)/2`, with exactly `n` pairs of each
separation. The shorter oriented segment is a convenient way to represent
the pair; the product of its two indicators is symmetric in the endpoints.

| Circle length | Short separation | Number of pairs | Pair expectation |
| --- | --- | --- | --- |
| 7 | each of 1, 2, 3 | 7 per separation | respectively `q_1,q_2,q_3` |
| 9 | each of 1, 2, 3 | 9 per separation | respectively `q_1,q_2,q_3` |
| 9 | 4 | 9 | `p^2` |

For separation `d<=3`, the union of the two windows contains exactly `4+d`
distinct *coordinate positions*, which is at most seven. Its joint law is
the same iid law used to define `q_d`, even when the segment wraps across
the chosen coordinate origin. Equal sampled letter values do not change
that law. For separation four on the nine-circle the two coordinate sets
are disjoint, so their indicators are independent.

Thus, exactly,

\[
 \mathbb E N_7=7p,\quad
 \mathbb E\binom{N_7}{2}=7Q,\quad
 \mathbb E N_9=9p,\quad
 \mathbb E\binom{N_9}{2}=9Q+9p^2.              \tag{5}
\]

No independence between three windows is assumed.

## 4. Collision error on the seven-circle

The event that the seven sampled letters fail to be pairwise distinct has
probability exactly `delta_m`. Off this event, Section 2 gives `N_7<=2`.
Everywhere, `0<=N_7<=7`. Therefore

\[
 \mathbb E N_7\leq2(1-\delta_m)+7\delta_m
 =2+5\delta_m.                                \tag{6}
\]

For every integer `0<=N<=2`, `binom(N,2)-N/2<=0`, while for every integer
`0<=N<=7` its maximum is `35/2`, attained at `N=7`. Hence

\[
 7Q-\frac{7p}{2}
 =\mathbb E\left[\binom{N_7}{2}-\frac{N_7}{2}\right]
 \leq\frac{35}{2}\delta_m,
 \qquad Q\leq\frac p2+\frac52\delta_m.        \tag{7}
\]

The union bound over the 21 unordered pairs of positions gives
`delta_m<=21/m`; thus the alternative coarse error `105/(2m)` in (7) is
also valid. Keeping `delta_m` exact is sharper.

## 5. The nine-circle inequality and root selection

For every integer `N`,

\[
 \binom N2-2N+3=\frac{(N-2)(N-3)}2\geq0.     \tag{8}
\]

Apply this to `N_9`, then use (5) and (7):

\[
 18p-3\leq 9Q+9p^2
 \leq\frac92p+\frac{45}{2}\delta_m+9p^2.
\]

Rearrangement gives the second inequality of (1). Equation (6) gives the
first.

If `delta_m<=11/120`, the quadratic has roots

\[
 r_\pm=\frac{9\pm\sqrt{33-360\delta_m}}{12}.
\]

The first inequality of (1) gives
`p <= (2+5*(11/120))/7 = 59/168 < 3/4`, whereas `r_+ >= 3/4`.
The quadratic is nonnegative only outside the interval between its roots;
the large-root branch is impossible. Thus `p<=r_-`.

Each factor `1-j/m` increases with `m` for `m>=7`, so `delta_m` decreases.
The accompanying checker verifies `delta_221<=11/120` using exact integer
arithmetic, proving the stated threshold in (2). A simpler sufficient
threshold is `m>=230`, using the union bound `delta_m<=21/m`.

Finally `delta_m` tends to zero, and the right side of (2), divided by `m^4`,
tends to `(9-sqrt(33))/12`. This proves (3). If the separately established
density limit exists, the same number bounds that limit.

## 6. Independent computational checks and their limits

Run from the repository root:

```sh
python workstreams/GP2-20261012/review/independent_window_check.py
```

To regenerate the explicit finite certificates:

```sh
python workstreams/GP2-20261012/review/independent_window_check.py --write-certificates
```

The checker uses only Python's standard library. It reconstructs vertices
and arcs from the original adjacency, computes BFS distances, and checks
every ordered triple of each supplied selected set. Distance certificates
are compared against freshly reconstructed BFS matrices. The overlap
formula is checked against BFS on every ordered vertex pair for `m=3,4`.

It verifies a seven-point GP set for `m=3` and an independently specified
twelve-point GP set for `m=4`. These are validation fixtures, not new finite
optimality claims. It also verifies all 35 triples of canonical distinct
seven-cycle windows using original-adjacency BFS in `Ka(7,4)`. Alphabet
relabeling and the argument in Section 2, rather than finite computation,
extend this to all distinct seven-tuples.

For each finite GP fixture it enumerates the iid seven- and nine-letter
spaces and checks the exact first and second moment identities in (5)
with rational arithmetic. Negative tests reject a non-GP enlargement of
the selected set, a modified distance, a modified adjacency, and an
incorrect alphabet-size binding.

These finite checks are error detectors for the definitions and identities.
The all-parameter result follows from Sections 1--5, not from numerical
sampling, LP output, or enumerated small optima.

## Literature boundary

The original Kautz problem is Problem 5.2 in the cited April 2026 preprint.
The August 16, 2026 v5 of
[Chandran--Klavzar--Tuite, The General Position Problem: A Survey](https://arxiv.org/html/2501.19385v5)
still lists the Kautz `k>=3` determination in its open-problem section and
cites that preprint as reference [25]. This identifies the source problem
and the latest directly read author statement; it is not an exhaustive
originality certificate.

The general pair-moment technique is elementary. The claimed new scope
here is the specific valid combination of seven- and nine-window identities
for directed Kautz GP and the resulting density bound. No assertion that
the exact Kautz length-four value, the density, or all `k>=3` cases is solved
is made.
