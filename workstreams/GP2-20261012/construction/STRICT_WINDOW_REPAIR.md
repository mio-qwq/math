# An elementary repair theorem for length-four Kautz general position

Candidate written proof, GP2-20261012. Scope: the original directed general-position number of `Ka(m,4)`, where `m` is the alphabet size. This note does not determine the limiting density or claim historical priority. It supplies a structural reduction for the remaining problem. No external removal lemma is needed.

## 1. Statement

Write `A` for an alphabet of size `m >= 3`. A **strict window code** is a set `C subset A^4` such that every word `x_0 ... x_7 in A^8`, including words with repeated symbols, has at most two indices `t in {0,1,2,3,4}` satisfying

`(x_t,x_(t+1),x_(t+2),x_(t+3)) in C`.

Indices are counted with multiplicity: three selected occurrences violate this condition even if two occurrences are the same four-letter word. This is stronger than original general position at a fixed alphabet size.

**Theorem 1 (elementary repair).** If `S` is a general-position set in the original directed `Ka(m,4)`, there is a strict window code `C subset S`, consisting only of four-distinct-letter words, with

`|S minus C| <= 73 m^3`.

The construction of `C` below uses six prefix/suffix counting tables and is explicit. In particular, no compactness, regularity, hypergraph-removal theorem, numerical optimization or limit extrapolation supports Theorem 1.

The constant is deliberately not optimized. Its mathematical purpose is the order `O(m^3)`, one degree below the ambient `Theta(m^4)` size.

## 2. Original graph and distances

Vertices of `Ka(m,4)` are words `abcd` with `a != b`, `b != c`, `c != d`. There is an arc from `abcd` to `bcde` for each `e != d`. Digons are allowed.

For distinct vertices `u,v`, their directed distance is four minus the longest proper suffix/prefix overlap, allowing overlap zero. Indeed, a walk of length `s < 4` necessarily makes the last `4-s` letters of `u` equal the first `4-s` of `v`. Conversely the required target suffix can be appended when such an overlap exists. In the no-overlap case, the last letter of `u` differs from the first letter of `v`, so appending all four target letters gives a legal walk. Thus the diameter is at most four.

If all letters of `x_0 ... x_(j+3)` are distinct and `1 <= i < j <= 4`, its windows `W_0,W_i,W_j` have respective distances

`d(W_0,W_i)=i`, `d(W_i,W_j)=j-i`, `d(W_0,W_j)=j`.

The displayed overlaps give these distances, and any longer overlap would equate different letters of the injective word. The three windows are distinct. Consequently an original GP set cannot select all three of these windows.

## 3. Fiber deletion rule

For `l in {1,2,3}` and each `(4-l)`-letter word `z`, define original-`S` fibers

`L_l(z) = {u in S : suffix_(4-l)(u)=z}`,

`R_l(z) = {u in S : prefix_(4-l)(u)=z}`.

All these fibers are counted in the original set `S`, not in a successively shrinking set. Put

`T_1=7`, `T_2=13`, `T_3=15`.

Delete from `S` every word with a repeated letter. Also delete every word lying in any fiber `L_l(z)` or `R_l(z)` whose size is at most `T_l m^(l-1)`. Call the set remaining after this single simultaneous deletion `C`.

The number of valid Kautz words having a repeated letter is

`m(m-1)^3 - m(m-1)(m-2)(m-3) = m(m-1)(3m-5) <= 3m^3`.

For a fixed `l` and orientation, there are at most `m^(4-l)` fibers. Therefore the total number of words deleted in its small fibers is at most

`m^(4-l) T_l m^(l-1) = T_l m^3`.

Taking a union bound over both orientations and all three lengths gives

`|S minus C| <= (3+2(7+13+15))m^3 = 73m^3`.

Overlapping deletion sets can only reduce this count. The bound can exceed `|S|` for small `m`; no nonempty repaired set is asserted in that regime.

## 4. Distinct extension lemma

Suppose `b` distinct symbols are already fixed and we wish to choose `l` new ordered symbols. Among all `m^l` ordered choices, at most

`[b l + binom(l,2)]m^(l-1)`

either use a fixed symbol or have a repeated new symbol. To prove this, sum over the `b l` events equating a new position to a fixed symbol and the `binom(l,2)` events equating two new positions. Each event has exactly `m^(l-1)` choices. This is a union bound; possible overlaps need no correction.

The same upper bound applies to the bad choices inside any particular fiber, since the fiber is a subset of the full space of choices. Therefore a fiber larger than the displayed bound contains a distinct extension avoiding all fixed symbols.

## 5. Proof that the repaired set is a strict window code

Suppose otherwise. After translating the earliest of three selected positions to zero, there are gaps `a,b >= 1`, `a+b <= 4`, and a word of length `a+b+4` whose windows at positions `0,a,a+b` all belong to `C`. Let its middle word be `v`. All four letters of `v` are distinct because of the first deletion rule.

The left window belongs to the original fiber

`L_a(prefix_(4-a)(v))`,

and the right window belongs to

`R_b(suffix_(4-b)(v))`.

As both endpoint windows survived deletion, these original fibers have sizes strictly greater than `T_a m^(a-1)` and `T_b m^(b-1)`, respectively.

We now choose new endpoint windows from these original fibers. They need not survive in `C`; membership in the original GP set `S` is enough. Their shared coordinates are exactly those fixed by the middle word. All overlap between the two endpoint intervals lies inside the middle interval. Thus the `a` free coordinates on the left and the `b` free coordinates on the right are disjoint and can be chosen independently after avoiding previously chosen symbols.

Choose the longer free side first; if the free lengths agree, choose either side first. The first extension must avoid the four middle symbols and its own internal repetitions. The second must additionally avoid the newly chosen symbols on the first side. The complete list of possible unordered gap pairs is:

| Free side lengths | First length | First bad-choice coefficient | Second length | Second bad-choice coefficient |
| --- | ---: | ---: | ---: | ---: |
| `1,1` | 1 | `4` | 1 | `5` |
| `1,2` | 2 | `4*2+1=9` | 1 | `6` |
| `1,3` | 3 | `4*3+3=15` | 1 | `7` |
| `2,2` | 2 | `4*2+1=9` | 2 | `6*2+1=13` |

Every coefficient is at most the threshold `T_l` for the corresponding free length `l`. Since each endpoint fiber is strictly larger than its threshold, the distinct extension lemma first provides the longer endpoint and then the shorter endpoint. The result is a word of length at most eight with all letters distinct. Its three windows at `0,a,a+b` belong to `S`: the middle window is the original `v`, and the new endpoint windows were chosen in original-`S` fibers.

Section 2 shows that these are three distinct selected vertices on a shortest directed path of length `a+b`. This contradicts original general position. Hence `C` is a strict window code and Theorem 1 follows.

Notice the two points that make the proof work: the middle word remains fixed, and original fibers are used for both extensions. The proof does not claim that an arbitrary original walk is geodesic or that an arbitrary GP set is independent.

## 6. Exact variational characterization of the limiting density

For each integer `r >= 1`, let `w(r)` be the maximum size of any strict window code in `[r]^4`. Repeated letters and equal adjacent letters are allowed in the template alphabet. Let

`Lambda = sup_(r>=1) w(r)/r^4`.

The density limit `lambda_4 = lim_(m->infinity) gp(Ka(m,4))/m^4` is already established in the inherited `DENSITY_LIMIT.md`.

**Theorem 2 (all finite window codes are asymptotically complete).**

`lambda_4 = Lambda`.

First, fix any strict code `D subset [r]^4`. Partition a large original alphabet into `r` equal blocks of size `q`, and select every valid Kautz word whose block word belongs to `D`. This is an original GP set: every geodesic has at most four edges, hence is represented by at most five consecutive windows; its block word can be extended to length eight, where `D` permits at most two selected occurrences. The size of this GP set is

`sum_(p in D) q product_(t=1..3) (q - 1_(p_t=p_(t-1))) = |D|q^4 + O_D(q^3)`.

This count uses only the restriction against the immediately preceding original letter, and therefore includes all permitted nonadjacent repetitions. Dividing by `(rq)^4` and taking `q -> infinity` gives `lambda_4 >= |D|/r^4`. Taking the supremum proves `lambda_4 >= Lambda`.

Conversely, apply Theorem 1 to an optimal original GP set on an alphabet of size `m`. Its repaired set is an admissible strict code, so

`gp(Ka(m,4)) - 73m^3 <= w(m) <= Lambda m^4`.

Division by `m^4` and passage to the limit give `lambda_4 <= Lambda`.

In particular `w(m)/m^4` also tends to `lambda_4`. A finite consequence, useful when a universal upper bound on strict code density is proved, is

`gp(Ka(m,4)) <= lambda_4 m^4 + 73m^3`.

An equivalent weighted formulation allows a finite code `D subset [r]^4` and a probability vector `(p_1,...,p_r)`, with density

`sum_((a,b,c,d) in D) p_a p_b p_c p_d`.

Every such density is at most `lambda_4`, by block sizes asymptotic to `m p_i`; the uniform case already attains the same supremum. This proves completeness only when the number of blocks and the code are both allowed to vary. It does not identify a fixed optimal number of blocks, certify the old three-block class as complete, or guarantee that the supremum is attained.

## 7. A precise probabilistic interface

Given any finite strict code `D` and independent identically distributed letters `U_i`, define

`X_i = 1_D(U_i,U_(i+1),U_(i+2),U_(i+3))`.

The process is stationary, and groups of variables whose underlying four-letter windows are disjoint are independent. In particular it is 3-dependent, and every five consecutive `X_i` sum to at most two. Theorem 2 identifies `lambda_4` with the supremum of the density of these **finite four-letter factors** with the strict constraint. A universal bound for the larger class of all stationary 3-dependent binary processes satisfying the constraint is therefore valid for `lambda_4`. No converse representation of every 3-dependent process by a four-letter factor is claimed.

## 8. Finite warning and validation boundary

The twelve odd permutations of four fixed letters are an original GP set, as established in the inherited `SUPPORT_ROUTE_OBSTACLE.md`. They are not a strict window code: for example `01320132` selects the windows at positions `0,2,4`, with the first and last occurrence equal. A naive two-clone blow-up of this GP set is not GP: the eight pairwise distinct original symbols

`0,2,6,4,1,3,7,5`

have odd-permutation block patterns at positions `0,2,4` when the blocks are `{0,1}`, `{2,3}`, `{4,5}`, `{6,7}`. Their directed distances are `2,2,4`. The distinction repaired by Theorem 1 is thus necessary at finite alphabets.

The accompanying checker rebuilds the original adjacency and runs BFS, checks the stated distance identities and this blow-up failure, validates the threshold table and deletion implementation, and checks a small genuine strict-code construction. It includes damaged distance, threshold and alphabet-binding controls. The checker is a finite semantic validation, not a computational proof of the all-parameter repair theorem. The universal argument is Sections 2–5. No Lean compilation or complete Lean formalization is claimed.

## 9. Literature and attribution

- Original question: Chandran et al., [arXiv:2604.15909v1, Problem 5.2](https://arxiv.org/html/2604.15909v1#S5), fixed word length four. The current general problem and historical relationship are recorded by the main GP2 source check.
- Inherited Kautz distance and density proofs: `workstreams/ROOT/distributed-written-proofs/B/kautz_length4/LOWER_BOUND.md` and `DENSITY_LIMIT.md`, baseline `61488e05c9fe41984f483853f99e79f5715dc893`.
- The initial route considered the partite hypergraph removal lemma: Terence Tao, [A variant of the hypergraph removal lemma, arXiv:math/0503572v2, Corollary 1.14](https://arxiv.org/pdf/math/0503572), published in *Journal of Combinatorial Theory, Series A* 113 (2006), 1257–1280. That theorem would give only an `o(m^4)` repair here. The complete elementary proof above instead uses the interval overlap of the three windows and proves `O(m^3)`. The external removal theorem is not a dependency of either displayed theorem.

Historical novelty of this specific application has not been certified. This note should be described as a candidate structural theorem pending independent review, not a solution of Problem 5.2 or an external peer-reviewed result.
