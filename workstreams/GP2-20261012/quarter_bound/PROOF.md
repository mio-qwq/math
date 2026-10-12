# A quarter-density upper bound for length-four Kautz general position

GP2-20261012. Complete written proof, with an independent internal review.
This is a partial answer for word length four in Chandran et al.,
[arXiv:2604.15909v1, Problem 5.2](https://arxiv.org/html/2604.15909v1#S5).
The alphabet size is `m`. The original directed graph, all shortest paths,
digons, and permitted nonadjacent repeated letters are retained.
This note does not determine the exact limit, solve other word lengths, or
claim historical priority or external human peer review.

## 1. Main result

Let `g(m)=gp(Ka(m,4))`, where `Ka(m,4)` has vertices `abcd` with
`a!=b`, `b!=c`, `c!=d`, and arcs `abcd -> bcde` for `e!=d`.
The inherited lower construction, together with the upper bound proved here,
gives

    26/125 <= lambda_4 = lim_(m -> infinity) g(m)/m^4 <= 1/4.

More explicitly, for every integer `m>=3`,

    g(m) <= (m)_4/4 + 73m^3,

where `(m)_4=m(m-1)(m-2)(m-3)`. The error coefficient is not optimized.
The four-factor numerator is divisible by four, so this expression is an
integer. For small alphabets it is a deliberately loose bound. The separate
seven/nine-window moment theorem in `../cyclic_moments/PROOF.md` gives a
useful bound with an `O(m^2)` correction and is independent of the repair
argument used here. The smaller of the available valid bounds may be taken.

The asymptotic upper endpoint improves the inherited `377/1320` to `1/4`.
The previous gap to `26/125` was `2561/33000`; the new gap is `21/500`.
Thus the gap decreases by `1175/2561`, approximately 45.88 percent.

## 2. Why strict window codes enter the original problem

A **strict window code** `C subset A^4` permits at most two selected
four-letter windows at starting positions `0,1,2,3,4` in every eight-letter
word in `A^8`. Equal adjacent letters are allowed in the template alphabet.
Occurrences are counted by position: the same word appearing twice counts
twice. This definition imposes a condition on every such word, not only
on geodesics.

The companion elementary repair theorem proves:

> Every original GP set `S subset Ka(m,4)` contains a strict window code
> `C`, all of whose words have four distinct letters, such that
> `|S minus C| <= 73m^3`.

The complete proof is in
`../construction/STRICT_WINDOW_REPAIR.md`, SHA256
`56ed0af016042abcbca256b52f6fb7539edb908fe81d6ba585a21102f9c4c4f5`.
For a self-contained account of the mechanism, its essential steps follow.

For distinct original vertices, directed distance is four minus the longest
proper suffix/prefix overlap, allowing overlap zero. Fewer than four shifts
must retain precisely that suffix. Conversely each overlap can be realized
by appending the target letters. With no overlap, the boundary letters differ,
so appending all four target letters is legal. In particular an injective
word of length at most eight gives geodesic windows at their natural offsets.

For `l=1,2,3`, count in the **original** set `S` each suffix and each prefix
fiber whose fixed word has length `4-l`. Delete words with any repeated
letter and words in any such fiber of size at most `T_l m^(l-1)`, where
`(T_1,T_2,T_3)=(7,13,15)`. Repeated-letter vertices number at most `3m^3`.
There are at most `m^(4-l)` fibers of either orientation, so the total
deletion is at most `[3+2(7+13+15)]m^3=73m^3`.

If three surviving windows had gaps `a,b>=1`, `a+b<=4`, fix the middle
word, whose four letters are distinct. Its left and right original-`S`
fibers are larger than the respective thresholds. Select a new endpoint
on the longer free side first, then the other endpoint, avoiding every
already fixed symbol and every repetition among newly chosen symbols.
For `l` free positions and `h` fixed symbols, at most
`[hl+binom(l,2)]m^(l-1)` choices are bad. For gap pairs `(1,1)`, `(1,2)`,
`(1,3)`, `(2,2)`, the two coefficients are respectively `(4,5)`, `(9,6)`,
`(15,7)`, `(9,13)`, covered by the thresholds. The rebuilt word has all
letters distinct and three distinct selected vertices on an original
geodesic. This contradicts the original GP condition.

The rebuilt endpoints need only be in the original `S`, which is why
simultaneous deletion using original fibers works. This proof neither
assumes independence nor treats every original walk as geodesic.

## 3. The rotation lemma

**Lemma.** A strict window code contains at most one word from each orbit
under cyclic rotation by one position. It contains no word of least period
one or two. Consequently

    |C| <= (m^4-m^2)/4

on an arbitrary `m`-letter alphabet. If every word of `C` has four distinct
letters, then

    |C| <= (m)_4/4.

**Proof.** Suppose a word `u=abcd` and a different rotation of it, by
`d` places with `1<=d<=3`, both belong to `C`. Read the eight-letter
periodic word `abcdabcd`, starting with `u`. Its windows at positions
`0,d,4` are selected. The windows at positions zero and four spell the
same word; they are nevertheless two selected **occurrences**. This
contradicts strictness.

If a selected word has least period two, its windows in that periodic
extension are selected at `0,2,4`. A period-one word also has these three
selected occurrences. Hence neither type may be selected. There are
exactly `m^2` words whose period divides two, namely `abab` with arbitrary
`a,b`. Every remaining word has a rotation orbit of size four. At most
one word can be selected from each of those `(m^4-m^2)/4` orbits.
On the four-distinct-letter domain there are exactly `(m)_4` words, and
each orbit again has size four, proving the last assertion. QED.

Apply the last assertion to the repaired code from Section 2, then add
back the at most `73m^3` deleted original vertices. This proves the finite
bound in Section 1, and division by `m^4` proves the asymptotic upper bound.

## 4. Limit existence and the lower endpoint

For completeness, limit existence needs no compactness theorem. Let `h(m)`
be the maximum size of an original GP set whose vertices have four distinct
letters, for `m>=4`. Restrict an optimal such set to a uniformly chosen
`r`-letter subalphabet, with `4<=r<=m`. The distance formula in Section 2
is unchanged by restricting the alphabet, so the restriction remains GP.
Each selected word survives with probability `(r)_4/(m)_4`. Therefore

    h(m)/(m)_4 <= h(r)/(r)_4.

This sequence is nonincreasing and bounded below by zero. Meanwhile

    h(m) <= g(m) <= h(m)+m(m-1)(3m-5),

since the final term is the exact number of valid repeated-letter vertices.
Consequently `g(m)/m^4` converges to the same limit.

The inherited three-block construction gives, for every integer `q>=1`,

    g(5q) >= 130q^4-74q^3+8q^2.

Its complete proof and fixed template are in
`workstreams/ROOT/distributed-written-proofs/B/kautz_length4/LOWER_BOUND.md`
at main `61488e05c9fe41984f483853f99e79f5715dc893`. This source is inherited
and unmodified. Dividing the displayed formula by `(5q)^4` proves the
lower endpoint `26/125`.

## 5. What the theorem does and does not settle

The repair theorem further proves the exact variational characterization

    lambda_4 = sup_(r>=1) w(r)/r^4,

where `w(r)` is the largest strict window code on `r` letters. Every such
template has a valid-word block lift to original Kautz GP sets, whose
leading term is its template density. Conversely the repair loses only
`O(m^3)` vertices. Thus the strengthened model is asymptotically complete
when **all finite alphabets** are allowed, although it is stronger at any
fixed alphabet size. No fixed number of blocks is proved sufficient.

The rotation lemma alone gives no strict code approaching density `1/4`.
Ordinary comma-free codes satisfy only some of the required exclusions;
they cannot be imported as constructions without checking the remaining
short-span triples. The exact value of `lambda_4`, the exact finite formula
for `g(m)`, and the original question at other word lengths remain open
within this work.

Independent review is recorded in
`../review/INDEPENDENT_REPAIR_REVIEW.md` and
`../review/INDEPENDENT_QUARTER_REVIEW.md`. Finite checks rebuild original
adjacency and distances and include deliberately corrupted inputs. The
universal rotation and repair arguments are written proofs; they do not
depend on a solver optimum. No successful Lean compilation or complete
Lean formalization is claimed for these new all-parameter statements.
