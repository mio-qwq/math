# Independent review of the classical ternary strict-window construction

Date: 2026-10-12. Scope: the original directed general-position problem for
`Ka(m,4)`, where `m` is the total number of actual letters. This review was
performed by an AI research agent that did not discover the candidate. It is
independent mathematical and computational review, not human peer review.

**Verdict: PASS for the ternary strict-window property, its all-parameter
original-GP lift, and the equal-block lower bound with leading density
`2/9`.** Sections 4–6 also give an independently derived exact count for
arbitrary block sizes and a finite balancing theorem for this fixed template.
These are not upper bounds for arbitrary GP sets.

## 1. Exact object and reviewed source

The discovery note reviewed was

`workstreams/GP2-20261012/review/TERNARY_STRICT_CONSTRUCTION_FROM_LITERATURE.md`

with SHA256

`c505466f843428df45d6d3f115536c3298f3b5b1d6db5fb319350cfafd1e8f0c`.

The candidate was reconstructed directly from the predicate

\[
D=\{(a,b,c,d)\in\{0,1,2\}^4:a\le c,\ b>d\}. \tag{1}
\]

There are six choices for the ordered coordinate pair `(a,c)` and three
choices for `(b,d)`, so `|D|=18`. No old template optimizer or saved set of
eighteen words was imported by the independent checker.

The source note attributes the classical dictionary to Golomb, Gordon and
Welch, *Comma-Free Codes*, Canadian Journal of Mathematics 10 (1958), 202–209,
page 206. Its reported original formula is `a<c, b>=d`. This review checks the
algebraic relationship: reversing a word `abcd` to `dcba` transforms that
formula precisely into (1). Thus the template itself is not a new
construction. The printed-source transcription and historical coverage were
handled by the separate source audit; this review does not claim to have
repeated its visual examination. The [publisher PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B78C35132E2BCD4A14459BE6A142FF30/S0008414X00045296a.pdf/commafree_codes.pdf)
and [DOI record](https://doi.org/10.4153/CJM-1958-023-9) identify the original
source. The additional mathematical issue checked here is the stronger
window-occurrence property and its implication for the Kautz problem.

## 2. Independent proof of the strict-window property

A strict window code permits at most two selected occurrences among the five
length-four windows of **every** length-eight word. Occurrences are counted
by their starting positions, including repeated occurrences of the same
four-letter word. Adjacent equal block labels are allowed.

Let `x_0,...,x_7` be arbitrary elements of `{0,1,2}`. Consecutive selected
windows at positions `i` and `i+1` would respectively require

\[
x_{i+1}>x_{i+3},\qquad x_{i+1}\le x_{i+3},
\]

which is impossible. Any three nonconsecutive positions among `0,1,2,3,4`
must be `0,2,4`. Selection at those positions would require

\[
x_1>x_3>x_5>x_7,
\]

a strict descending chain of length four in a set of size three. This too is
impossible. Hence (1) is a strict window code. No distinctness assumption on
the eight symbols or on the selected words occurs in this argument.

Both restrictions are essential. Replacing `b>d` by `b>=d` selects all five
occurrences in the constant word. Applying (1) to four block labels selects
positions `0,2,4` in `03020100`. These are actual violations of the strict
constraint, not failures inferred from an optimization timeout.

## 3. Bridge to the original directed graph

Partition an actual alphabet `A` into three ordered blocks `B_0,B_1,B_2` and
write `pi:A->{0,1,2}` for the block map. Select exactly

\[
S=\{v_0v_1v_2v_3\in A^4:
v_i\ne v_{i+1}\ (0\le i<3),\quad
\pi(v_0)\le\pi(v_2),\quad \pi(v_1)>\pi(v_3)\}. \tag{2}
\]

In the original graph, an arc maps `abcd` to `bcde` for every `e!=d`. Thus
every directed walk is a sequence of consecutive length-four windows. Digons
are retained. No edge is removed to produce an oriented graph.

Every pair of vertices has directed distance at most four. If the last
letter of the first vertex differs from the first letter of the target,
append all four target letters. If those letters coincide, append only the
last three target letters. Both walks are legal because the target itself
has unequal adjacent letters.

Every shortest directed path therefore has at most four arcs and is read in
a word of length at most eight. Its block word can be extended arbitrarily
to length eight. Section 2 allows at most two selected window occurrences
in that word. In particular no such shortest path has three distinct
vertices of `S`. This proves that (2) is original directed general position
for every choice of the three block sizes. It addresses every shortest path,
not the existence of one path avoiding a third selected vertex.

Actual letters with equal adjacent block labels must still be unequal.
Nonadjacent actual letters may coincide. The count below enforces exactly
these original restrictions.

## 4. Exact count for arbitrary block sizes

Put

\[
x=|B_0|,\quad y=|B_1|,\quad z=|B_2|,\quad
m=x+y+z,\quad t=xy+xz+yz.
\]

**Proposition 1.** For any nonnegative integer block sizes, the size of (2) is

\[
\boxed{N(x,y,z)=t\bigl((m-1)^2-t\bigr)+2xyz.} \tag{3}
\]

**Proof.** First ignore the adjacent-letter restrictions. The number of
ordered actual-letter pairs satisfying the weak block inequality is
`m^2-t`, and the number satisfying the strict block inequality is `t`.
The coordinate pairs are disjoint, so the initial number is `t(m^2-t)`.

Let `E_1,E_2,E_3` be the events that the first and second, second and third,
or third and fourth actual letters coincide, respectively, restricted to
the words counted so far. The relevant single-event counts are

\[
\begin{aligned}
|E_1|&=xy^2+xyz+xz^2+yz^2,\\
|E_2|&=x^2y+xy^2+x^2z+2xyz+y^2z+xz^2+yz^2,\\
|E_3|&=x^2y+x^2z+xyz+y^2z.
\end{aligned}
\]

For example, `E_1` uses a single actual letter in a block `i`, the third
letter in a block at least `i`, and the fourth in a block strictly below
`i`. Summing over `i=0,1,2` gives the first displayed polynomial. The other
two follow in the same way. Their sum is

\[
|E_1|+|E_2|+|E_3|=2mt-2xyz.
\]

The only nonempty pairwise intersection is `E_1 cap E_2`: its first three
actual letters agree and the last lies in a strictly lower block. Its count
is `t`. The intersection `E_1 cap E_3` would impose both a weakly increasing
and a strictly decreasing comparison on the same two block labels, while
`E_2 cap E_3` violates the strict comparison immediately. The triple
intersection is empty as well. Inclusion-exclusion gives

\[
|S|=t(m^2-t)-(2mt-2xyz)+t
=t\bigl((m-1)^2-t\bigr)+2xyz,
\]

as claimed. In particular the answer is symmetric in the three block sizes,
despite the ordered description of the template. This proof includes
nonadjacent repetitions; it does not impose all-four-distinct letters. ∎

The checker separately generates the count polynomial from the eighteen
individual patterns: a pattern `c_0c_1c_2c_3` contributes

\[
n_{c_0}\prod_{i=1}^{3}
\bigl(n_{c_i}-{\bf1}_{c_i=c_{i-1}}\bigr).
\]

It compares coefficients in `Z[x,y,z]` with (3). This is an exact finite
polynomial-identity audit, not a test at sample block sizes.

## 5. Balanced sizes optimize this fixed template for every m

**Proposition 2.** For every integer `m>=3`, among all nonnegative integer
triples `x+y+z=m`, the count (3) is maximized exactly when the three sizes
differ by at most one.

**Proof.** Since (3) is symmetric, take any largest and smallest sizes to be
`x` and `z`. If `x>=z+2`, replace them by `x-1,z+1` while fixing `y`. Direct
expansion of (3) gives

\[
\begin{aligned}
&N(x-1,y,z+1)-N(x,y,z)\\
&\qquad=(x-z-1)
\bigl(x^2+y^2+z^2-3x-z+2\bigr). \tag{4}
\end{aligned}
\]

The first factor is positive. If `z=0`, the second is
`(x-1)(x-2)+y^2`, which is positive for `x>=2` and `x+y=m>=3`. If `z>=1`,
then `x>=3`, and it is
`x(x-3)+z(z-1)+y^2+2>0`. Thus every unbalanced triple admits a strictly
improving integer balancing step. Iterating reaches a balanced triple,
and all balanced triples have the same count by symmetry. This proves both
maximality and its equality case. ∎

This proposition concerns only the full lift of the fixed ternary template
(1). It does not show that optimal original GP sets have three blocks or that
the repaired strict-code problem is optimized by this template.

## 6. Explicit lower bound for every alphabet size

For `m>=3`, write `m=3q+r`, where `q>=1` and `r in {0,1,2}`. Use balanced
block sizes `(q,q,q)`, `(q,q,q+1)`, or `(q,q+1,q+1)`. Propositions 1–2 give

\[
\boxed{
\operatorname{gp}(\operatorname{Ka}(3q+r,4))\ge
\begin{cases}
18q^4-16q^3+3q^2,&r=0,\\
18q^4+8q^3-2q^2,&r=1,\\
18q^4+32q^3+18q^2+4q,&r=2.
\end{cases}} \tag{5}
\]

Consequently `liminf gp(Ka(m,4))/m^4 >= 2/9`. Together with the inherited
existence of the density limit, this is `lambda_4>=2/9`. The amount by which
the leading coefficient exceeds the inherited `26/125` is exactly
`16/1125`.

The optimal leading coefficient within this template also follows directly
from weighted block probabilities `p_0,p_1,p_2`. Set
`s=p_0^2+p_1^2+p_2^2`. The two coordinate-pair events have probabilities
`(1+s)/2` and `(1-s)/2`, so their product is `(1-s^2)/4`. Since `s>=1/3`,
this is at most `2/9`, attained exactly at equal block probabilities.

No exact value of `gp(Ka(m,4))`, no assertion that `lambda_4=2/9`, and no
solution for all word lengths is inferred from (5).

## 7. Actual independent checker and evidence

The standard-library checker is `verify_lower18.py`. The following command
was actually executed from the repository root on 2026-10-12 with Python
3.12.14 and exited zero:

```sh
python workstreams/GP2-20261012/construction/verify_lower18.py > workstreams/GP2-20261012/construction/lower18_check.log
```

It reconstructs the dictionary from (1), independently of the discovery
note's word list, and checks all `3^8=6561` block words. The counts with zero,
one, and two selected occurrences are `729,4374,1458`; no larger count occurs.
It also regenerates the adjacent-equal-block histogram, obtaining five,
ten, and three patterns with zero, one, and two equal adjacent pairs.

The finite graph audits rebuild **every original arc** by shift and append,
then compute all ambient ordered-pair distances by BFS. The overlap formula
is checked against these BFS distances, but does not supply them. For all
distinct selected `u,w,v`, the checker tests
`d(u,v) != d(u,w)+d(w,v)`. Equality is exactly the existence of a shortest
directed path between two selected endpoints passing through a third; its
absence is the original all-geodesics GP condition.

| Block sizes | Actual letters | Ambient vertices | Selected vertices | All ambient ordered-pair distances | Distinct ordered triples checked |
| --- | ---: | ---: | ---: | ---: | ---: |
| `1,1,1` | 3 | 24 | 5 | 576 | 60 |
| `1,1,2` | 4 | 108 | 24 | 11,664 | 12,144 |
| `1,2,2` | 5 | 320 | 72 | 102,400 | 357,840 |
| `2,2,2` | 6 | 750 | 172 | 562,500 | 5,000,040 |

No violating triple was found, and these are verification examples of the
construction rather than new finite optimal values.

The deterministic `lower18_certificate.json` stores the template, exact
polynomial coefficients, every ambient vertex and original adjacency list,
the exact selected set, and all selected-pair BFS distances. Each distance
row is a string of digits in the recorded selected-vertex order. The
certificate was written, reloaded, and replayed against a fresh original
adjacency/BFS reconstruction during the same successful execution. Its
SHA256 is

`b9b8da78a2e17220a8cc278f4e6bc5b680254471b717aa50fb4cf8e65f154973`.

Eight deliberate negative controls were all detected: adding the constant
template word; weakening the strict inequality; applying the rule to four
block labels; binding a certificate to a wrong alphabet size; corrupting a
selected-pair distance; damaging the target set; removing an original arc;
and changing the claimed count. The first three give explicit violating
block words; the other five are rejected by exact reconstruction. The full
actual output is in `lower18_check.log`.

The polynomial audit verifies (3), each residue case in (5), and the
balancing identity (4) coefficient by coefficient over the integers. The
positivity argument and the universal GP theorem remain the written proofs
above. No Lean compilation, formal theorem, floating-point certificate, or
external human review is claimed.
