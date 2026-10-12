# Independent review of elementary strict-window repair

Date: 2026-10-12. Decision: PASS as a complete written all-parameter proof,
with separate finite original-adjacency checks. No Lean or external human
peer review is claimed.

Reviewed source: `construction/STRICT_WINDOW_REPAIR.md`.

Frozen SHA256:
`56ed0af016042abcbca256b52f6fb7539edb908fe81d6ba585a21102f9c4c4f5`.

## Accepted scope

For any original directed-GP set `S` in `Ka(m,4)`, `m>=3`, the specified
simultaneous deletion gives `C subset S` consisting of four-distinct-letter
words and satisfying the strict condition: any eight-letter word has at
most two selected four-window occurrences, counted by position even if
the same selected vertex occurs more than once. The deletion bound is
`|S\C|<=73m^3`.

Combined with the inherited existence of the Kautz density limit, this
proves equality between that limit and the supremum of all finite strict
window-code densities, allowing the alphabet and code to vary. The weighted
finite-alphabet formulation is also valid. The theorem does not identify
an optimal finite alphabet or prove that a previously tested fixed block
family is complete.

## 1. Original adjacency and distance

The independent distance derivation is in Section 1 of
`INDEPENDENT_WINDOW_REVIEW.md`. It starts from the left-shift/append arcs
and proves that distinct legal four-words have distance four minus their
longest proper suffix/prefix overlap. Nonadjacent repeated letters and
digons are retained.

For an injective letter string of length `a+b+4<=8`, windows at starts
`0,a,a+b`, with `a,b>=1`, have distances `a,b,a+b`. Any longer overlap
would equate two distinct letters. Thus they are three different selected
vertices on a geodesic if all belong to `S`.

## 2. Fiber semantics and deletion count

The source defines `L_l(z)` by a fixed suffix of length `4-l`, and `R_l(z)`
by a fixed prefix of that length. All six tables are counted in the original
set `S` exactly once. Deletion is simultaneous; no later extension depends
on the sizes of the fibers of the repaired set.

A fixed fiber is parametrized injectively by the `l` free coordinates of
one four-letter word. There are at most `m^(4-l)` fibers for each orientation.
Deleting fibers of size at most `T_l m^(l-1)` therefore costs at most
`T_l m^3`. The union bound over both orientations is legitimate even if
their deleted sets overlap.

Legal Kautz words with some repeated letter number exactly

`m(m-1)^3-(m)_4=m(m-1)(3m-5)<=3m^3`.

With `(T_1,T_2,T_3)=(7,13,15)`, the stated total is indeed
`3+2(7+13+15)=73`, times `m^3`. An empty repaired set at small alphabets is
allowed, so thresholds larger than the possible fiber size create no gap.

## 3. Endpoint reconstruction covers every possible occurrence pattern

If strictness fails, select any three violating positions and translate the
earliest to zero. Their gaps satisfy

`(a,b) in {(1,1),(1,2),(2,1),(1,3),(3,1),(2,2)}`.

Fix the middle selected word `v`. It has four different letters. The left
selected word lies in `L_a(prefix_(4-a)(v))`; the right lies in
`R_b(suffix_(4-b)(v))`. Since both survived, those original fibers are
strictly larger than their deletion thresholds.

The free left coordinates occur strictly before the middle interval and
the free right coordinates strictly after it. They are disjoint. Any overlap
between the two endpoint windows lies inside the fixed middle interval,
so choosing their free parts separately gives compatible endpoint words.

Among `l` ordered free letters, avoiding `b` fixed symbols and internal
repetitions excludes at most
`(b*l + binom(l,2))*m^(l-1)` choices. Each equality event fixes one degree
of freedom; the union bound holds on the full space and therefore on any
fiber subset.

Choose the longer free part first. The necessary coefficients are:

| Gap lengths, ignoring orientation | First extension | Second extension |
| --- | --- | --- |
| 1,1 | 4 | 5 |
| 1,2 | 9 | 6 |
| 1,3 | 15 | 7 |
| 2,2 | 9 | 13 |

Each coefficient is bounded by the corresponding `T_l`. Strictly larger
fibers guarantee a good first extension, followed by a good second
extension avoiding the first as well. The resulting whole string has
distinct letters. Both new endpoints belong to original `S`; they need
not belong to `C`. The middle remains in `C subset S`. Section 1 then
contradicts original GP.

This also handles an initial violating word in which two selected occurrences
represent the same four-vertex. Reconstruction replaces its endpoints by
different original-S vertices, so no false inference from repeated copies
of a single vertex is used.

## 4. Asymptotic completeness and weighted form

For a fixed strict code `D subset [r]^4`, partition an original alphabet
of size `rq` into `r` equal blocks. Select all legal Kautz vertices whose
block word belongs to `D`. Any original geodesic has at most four edges;
its sequence of block letters is a segment of an eight-letter block word.
Strictness allows at most two selected occurrences on it, which proves GP
with the original universal-path quantifier.

For a block pattern `p`, the number of legal original words is exactly

`q * product_(t=1..3)(q - 1_(p_t=p_(t-1)))`.

Only equality with the immediately preceding original letter is forbidden.
Nonadjacent repeated letters are allowed and counted. Summing gives
`|D|q^4+O_D(q^3)` and therefore the lower comparison with its strict-code
density. The repair theorem gives the reverse comparison after dividing
by `m^4` and using `73/m -> 0`.

The inherited limit is needed only to pass between arbitrary alphabet
sizes and the equal-block subsequences in this formulation. It is
explicitly identified as a dependency in the source. Unequal block sizes
asymptotic to a probability vector give the weighted density polynomial;
zero-weight symbols can be omitted. The uniform finite codes already
give the same supremum.

The claimed finite consequence `gp(Ka(m,4))<=lambda_4*m^4+73m^3` follows
because the supremum bounds every strict code at its own finite alphabet.
The statement that strict-code densities themselves converge follows by
the same upper/lower squeeze. Neither assertion needs attainment of the
supremum.

## 5. Finite independent validation

`independent_repair_check.py` imports only the independent review-side
original-adjacency/BFS implementation. It does not read or import the
construction-side discovery checker. The proof source is bound by its
frozen SHA256.

The actual finite run checks:

- all six ordered gap cases against BFS in the original `Ka(8,4)`;
- the prefix/suffix roles for those cases;
- all thresholds and the required order of extension;
- that the twelve odd permutations form an original GP set in `Ka(4,4)`;
- their strict failure at starts `0,2,4` of `01320132`, including equality
  of the first and last selected four-word;
- the three different lifted windows of `0,2,6,4,1,3,7,5`, whose original
  BFS distances are `2,2,4`, so a naive blow-up is not GP;
- the simultaneous deletion rule on this small fixture;
- rejection of each understated threshold, incorrect alphabet binding,
  and a changed distance against original BFS.

The repaired small fixture is empty. This finite test checks semantics
and implementation, not existence of nonempty large repaired sets. The
universal proof is the fiber argument in Sections 2--3 above.

Reproduce from the repository root:

```sh
python workstreams/GP2-20261012/review/independent_repair_check.py
```

The actual output is saved as `independent_repair_check.log`; the review
hash manifest includes this document, the checker, and that log.

## Conclusion and remaining scope

The proof repairs the precise finite-alphabet obstruction to treating
strict-window templates as universal. Its conclusion is an asymptotically
complete variational formulation, with an explicit `O(m^3)` deletion bound.
It does not determine the variational supremum or resolve Kautz length four
exactly. Historical novelty remains a separate literature question; the
review certifies mathematical validity at the stated frozen source only.
