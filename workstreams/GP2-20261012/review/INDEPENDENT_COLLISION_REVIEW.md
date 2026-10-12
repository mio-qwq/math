# Independent collision-certificate review of the Kautz length-four upper bound

Date: 2026-10-12. Status: PASS, at the level of a complete written reduction
and an independently generated finite certificate checked from original
adjacency and BFS. No Lean compilation is claimed.

This refines the valid, coarser collision estimate in
`INDEPENDENT_WINDOW_REVIEW.md`. The seven-/nine-window identities and the
original-adjacency distance proof there remain unchanged.

## The verified finite bound

Write `(m)_k=m(m-1)...(m-k+1)` and

\[
 P_m=8(m)_2+12(m)_3+15(m)_4+3(m)_5.
\]

For every `m>=3`, and every GP set `S` in the original directed `Ka(m,4)`,
let `p=|S|/m^4`. The independently verified certificate proves

\[
 Q\leq\frac p2+\frac{P_m}{2m^7},              \tag{1}
\]

where `Q=q_1+q_2+q_3` is the sum of the joint inclusion probabilities for
two length-four windows shifted by one, two, or three coordinates in an
iid uniform letter string. Combining this with the exact nine-circle pair
identity gives

\[
 6p^2-9p+2+\frac{3P_m}{m^7}\geq0.             \tag{2}
\]

Consequently,

\[
 \operatorname{gp}(\operatorname{Ka}(m,4))
 \leq\left\lfloor
 \frac{m^4}{12}\left(9-\sqrt{33-\frac{72P_m}{m^7}}\right)
 \right\rfloor.                              \tag{3}
\]

The same formulas also hold for the same shift-adjacency definition over
two letters, although the source paper states its Kautz family for `m>=3`.
This small-alphabet extension is used internally in the finite certificate.

Here

\[
 P_m=3m^5-15m^4+27m^3-13m^2-2m,
\]

so the finite correction in the normalized bound is `O(m^-2)`. The limit
superior is bounded by `(9-sqrt(33))/12` as before.

## 1. Why seven-letter equality types suffice

For a seven-tuple of letters, relabel its distinct values by first appearance
to obtain a restricted-growth string `w` of length seven. If it has `k`
blocks, there are exactly `(m)_k` seven-tuples over `[m]` with this equality
type. There are 877 such types, generated recursively; the numbers by `k`
are `1,63,301,350,140,21,1`.

The seven cyclic four-windows of a type may include illegal words or
repeated occurrences of the same legal vertex. Discard illegal windows,
then give each distinct legal window a weight equal to its number of
occurrences. Selecting a vertex necessarily selects all its occurrences;
therefore the relevant optimization is weighted GP on these at most seven
distinct vertices, not arbitrary subsets of the seven positions.

Let `C(w)` be this maximum selected weight. Directed distances between legal
words using `k>=2` letters are unchanged on embedding their alphabet into a
larger alphabet: the distance formula proved from original adjacency in
Section 1 of `INDEPENDENT_WINDOW_REVIEW.md` depends only on suffix/prefix
overlaps. The proof also applies for `k=2`. For `k=1` there are no legal
four-letter windows. Consequently, restricting any original GP set `S` to
the windows of any actual seven-tuple gives a feasible weighted GP set in
the graph used by this local certificate. Thus `N_7<=C(w)`.

The function `N(N-2)` is at most `max(0,C(C-2))` for every integer
`0<=N<=C`. Hence

\[
 \mathbb E[N_7(N_7-2)]
 \leq\frac1{m^7}\sum_w
 (m)_{k(w)}\max\{0,C(w)(C(w)-2)\}.            \tag{4}
\]

This is a finite, exact reduction from an arbitrary GP set. It does not
assume that the original GP set is independent or contains only words
with distinct letters.

## 2. Independent finite certificate

`independent_collision_check.py` constructs all equality types from scratch.
It does not import or read another discovery program or discovery output.
For each `k>=2`, it builds `Ka(k,4)` from the shift-append adjacency and runs
BFS as needed. The actual run used 355 distinct BFS source rows.

For each type, `independent_collision_certificate.json` records:

- the canonical seven-letter pattern and its bound alphabet parameter;
- its distinct legal windows and their occurrence multiplicities;
- all directed distances between these windows, computed by BFS;
- the maximum selected weight and a GP subset attaining that weight;
- for every subset of greater weight, an ordered triple of its distinct
  vertices satisfying `d(u,w)+d(w,v)=d(u,v)`.

The verifier checks full coverage of the 877 types and of all required
higher-weight rejections. It reconstructs the original graph and BFS
distances again, validates every rejecting triple, and checks that the
attaining subset is actually GP. Thus every claimed local upper bound has
a complete finite refusal certificate, and every local equality has a
matching admissible witness.

The independently generated capacity distribution is:

| Number of blocks `k` | Capacity 0 | Capacity 1 | Capacity 2 | Capacity 3 | Capacity 4 | Sum of positive `C(C-2)` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 35 | 14 | 7 | 0 | 7 | 56 |
| 3 | 56 | 70 | 147 | 28 | 0 | 84 |
| 4 | 14 | 49 | 252 | 35 | 0 | 105 |
| 5 | 0 | 7 | 126 | 7 | 0 | 21 |
| 6 | 0 | 0 | 21 | 0 | 0 | 0 |
| 7 | 0 | 0 | 1 | 0 | 0 | 0 |

The final column gives the coefficients

\[
 56(m)_2+84(m)_3+105(m)_4+21(m)_5=7P_m.
\]

Using the exact identity
`E[N_7(N_7-2)]=14Q-7p` in (4) proves (1).

The classification above is a certificate-assisted finite theorem, not
a claim of a handwritten classification of all 877 cases. The verifier's
generation of all masks involves at most 128 subsets per equality type.

## 3. Independent proof that one collision cannot contribute error

The vanishing `k=6,7` coefficients also have a direct proof.

Assume the seven cyclic letters have at least six different values. They
have at most one repeated pair. Distinct start positions cannot give equal
four-letter words: equality of the first letters and of the second letters
would already impose two distinct coordinate equalities. On a seven-cycle,
the unordered pair of coordinates cannot be invariant under a shift by one.

Suppose three selected start positions are present. As in the distinct-letter
argument, choose the complement of a largest cyclic gap and rotate it so
the starts are `0<s<t<=4`. Each gap between consecutive selected starts is
at most three. The three legal selected four-windows therefore cover every
adjacent-letter comparison in the entire `t+4`-letter segment. All those
adjacent pairs are unequal, and the corresponding shift walk is legal.

To be a geodesic it suffices to exclude a suffix/prefix overlap longer than
the automatic `4-t`. With indices `a_0,...,a_6` modulo seven, the endpoint
words are `a_0a_1a_2a_3` and `a_ta_{t+1}a_{t+2}a_{t+3}`.

- For `t=2`, overlap three forces adjacent letters equal.
- For `t=3`, overlap two forces adjacent letters equal; overlap three forces
  `a_1=a_3=a_5` and `a_2=a_4`.
- For `t=4`, overlap one forces `a_3=a_4`; overlap two forces `a_2=a_4`
  and `a_3=a_5`; overlap three forces `a_1=a_4`, `a_2=a_5`, and `a_3=a_6`.

Every possibility contradicts segment legality or requires at least two
independent coordinate identifications. Hence the walk is geodesic, contrary
to the selected middle vertex. Thus `N_7<=2` whenever there are at least
six distinct letters.

For a bound not using the full finite classification, the bad event has
probability

\[
 \delta'_m=1-\frac{(m)_7+21(m)_6}{m^7}\leq\frac{140}{m^2}.
\]

The union bound uses 35 possible equal-valued triples and 105 partitions
of four positions into two equal-valued pairs. Every tuple with at most
five distinct values has at least one such configuration, each of probability
`1/m^2`. Replacing `delta_m` by `delta'_m` in the coarser review supplies
an independently handwritten `O(m^-2)` error route as well.

## 4. Quadratic and branch control

The nine-circle identity gives
`E[binom(N_9,2)]=9Q+9p^2`. The pointwise integer inequality
`binom(N,2)>=2N-3` therefore gives

\[
 18p-3\leq9Q+9p^2
 \leq\frac92p+\frac{9P_m}{2m^7}+9p^2,
\]

which rearranges to (2).

Because all falling-factorial terms are nonnegative for integer `m>=2`,
`P_m>=0`. Moreover

\[
 3m^5-P_m=m^2(15m^2-27m+13)+2m>0 \quad(m\geq2).
\]

The bracket is positive for `m>=2`, for example because
`15m^2-27m=m(15m-27)>0`. For `m>=3` this yields
`3P_m/m^7<9/m^2<=1`. For `m=2` the ratio is exactly `3/8`.
Thus `33-72P_m/m^7>9` and the larger quadratic root is greater than one.
Since `p<=1`, the larger-root branch is impossible. This proves (3) for
all claimed parameters, without an asymptotic branch assumption.

## 5. Reproduction and negative controls

Generate the certificate and run the complete independent audit:

```sh
python workstreams/GP2-20261012/review/independent_collision_check.py --write-certificate
```

Verify the saved certificate against fresh original-adjacency BFS:

```sh
python workstreams/GP2-20261012/review/independent_collision_check.py --verify-certificate workstreams/GP2-20261012/review/independent_collision_certificate.json
```

The audit includes deliberately understated capacity, a wrong distance,
a wrong alphabet parameter, a reduced final polynomial coefficient, and a
missing higher-weight refusal. Every modified object was rejected in the
actual execution. The independent first-/second-moment checks and finite
GP fixtures are in the companion window-check file.

The log files record the actual commands' output. Hashes in
`review_sha256.json` bind the review documents, independent checkers, finite
certificates, and logs.
