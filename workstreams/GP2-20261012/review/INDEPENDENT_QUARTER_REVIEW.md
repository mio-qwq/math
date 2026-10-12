# Independent review: the rotation bound for strict four-window codes

Date: 2026-10-12. Status: independent written verification passed. This is an
elementary proof, not a Lean formalization. The reviewer did not participate in
the discovery of the strict-window repair theorem or its application below.

## 1. The exact occurrence condition

Let \(A\) be an alphabet of cardinality \(m\), and let \(C\subseteq A^4\).
Call \(C\) **strict** if, for every word \(x_0x_1\ldots x_7\in A^8\),

\[
 \sum_{i=0}^{4}{\bf1}_{C}(x_ix_{i+1}x_{i+2}x_{i+3})\le2. \tag{1}
\]

The sum counts positions. Equal four-letter words at different positions
contribute separately. No adjacent-inequality restriction is imposed in (1).
Let \(w(m)\) denote the maximum size of a strict code on \(m\) letters.

## 2. Aperiodic rotation orbits

Write \(\rho(a_0a_1a_2a_3)=a_1a_2a_3a_0\). Suppose that both \(u\) and
\(\rho^d(u)\), for some \(1\le d\le3\), belong to \(C\). The eight-letter
word \(uu\) then has selected windows at positions \(0,d,4\). These are three
different positions, even if two or all three windows are the same word.
This contradicts (1).

It follows simultaneously that:

* no two different words in the same four-rotation orbit can be selected;
* if \(\rho^d(u)=u\) for some \(1\le d\le3\), then \(u\) cannot be selected.

Every rotation orbit has cardinality \(1\), \(2\), or \(4\). A word has orbit
cardinality less than \(4\) exactly when it has the form \(abab\), including
\(a=b\). There are \(m^2\) such words. The remaining \(m^4-m^2\) words form
disjoint orbits of cardinality \(4\). Consequently, for every integer \(m\ge1\),

\[
 \boxed{w(m)\le\frac{m^4-m^2}{4}.} \tag{2}
\]

The right side is an integer because it counts these orbits. This proof gives
an upper bound only; selecting one representative per orbit need not produce a
strict code.

## 3. Consequence for the original directed general-position problem

Here \(\operatorname{Ka}(m,4)\) has all four-letter words with adjacent letters
different as vertices; an arc shifts left by one letter and appends a letter
different from the previous last letter. A general-position set contains no
three distinct vertices lying in order on any shortest directed path.

The independently reviewed repair theorem states that every such GP set \(S\)
has a subset \(C\subseteq S\), with

\[
 |S\setminus C|\le73m^3,
\]

which satisfies (1). Its proof actually produces a set \(C\) whose words have
four distinct letters. The exact reviewed source is
`construction/STRICT_WINDOW_REPAIR.md`, SHA256
`56ed0af016042abcbca256b52f6fb7539edb908fe81d6ba585a21102f9c4c4f5`;
the independent reconstruction is `review/INDEPENDENT_REPAIR_REVIEW.md`.

Applying (2) therefore gives

\[
 \operatorname{gp}(\operatorname{Ka}(m,4))
 \le\frac{m^4-m^2}{4}+73m^3. \tag{3}
\]

Using the additional distinct-letter property, the \((m)_4\) possible words
split into rotation orbits of cardinality \(4\), so the same argument gives
the slightly sharper finite version

\[
 \operatorname{gp}(\operatorname{Ka}(m,4))
 \le\frac{(m)_4}{4}+73m^3. \tag{4}
\]

For \(m<4\), \((m)_4=0\), and (4) still follows because the repaired set is
empty. For the graph question one may restrict to \(m\ge2\), or to the
original problem's domain \(m\ge3\).

Either (3) or (4) proves directly

\[
 \limsup_{m\to\infty}
 \frac{\operatorname{gp}(\operatorname{Ka}(m,4))}{m^4}\le\frac14. \tag{5}
\]

With the inherited, separately established existence of the density limit,
this is \(\lambda_4\le1/4\). Together with the inherited lower bound it gives
\(26/125\le\lambda_4\le1/4\). It does not determine the limit, give the exact
finite GP numbers, or solve all Kautz word lengths.

## 4. Relation to ordinary comma-free codes

An ordinary comma-free code has the property that for every \(u,v\in C\),
the three four-letter windows of \(uv\) starting at \(1,2,3\) are outside
\(C\). Condition (1) implies this property, because the windows at \(0\) and
\(4\) are already selected. The converse is false, even for codes consisting
only of words with distinct letters.

For example, on the alphabet \(\{0,1,2,3,4,5\}\), let

\[
 C_0=\{0123,1234,2345\}.
\]

All cross-boundary windows are displayed below. None is in \(C_0\).

| First word | Second word | Window at 1 | Window at 2 | Window at 3 |
|---|---|---|---|---|
| 0123 | 0123 | 1230 | 2301 | 3012 |
| 0123 | 1234 | 1231 | 2312 | 3123 |
| 0123 | 2345 | 1232 | 2323 | 3234 |
| 1234 | 0123 | 2340 | 3401 | 4012 |
| 1234 | 1234 | 2341 | 3412 | 4123 |
| 1234 | 2345 | 2342 | 3423 | 4234 |
| 2345 | 0123 | 3450 | 4501 | 5012 |
| 2345 | 1234 | 3451 | 4512 | 5123 |
| 2345 | 2345 | 3452 | 4523 | 5234 |

Thus \(C_0\) is comma-free. The word \(01234500\) has its windows at
\(0,1,2\) in \(C_0\), so it violates (1). This example is a comparison of
code conditions, not a claimed GP set in the original graph.

This distinction prevents importing a comma-free-code lower bound without
checking the additional triples whose first and last selected starts are
separated by two or three positions. More precisely, after translating the
first selected start to zero, a strict violation has starts \(0,a,a+b\) with
\(a,b\ge1\) and \(a+b\le4\). Ordinary comma-freeness rules out the three cases
with \(a+b=4\); strictness additionally rules out gaps \((1,1),(1,2),(2,1)\).

The rotation argument itself is classical for comma-free codes. A primary
modern source is Fimmel, Michel, Pirot, Sereni and Strüngmann, *Diletter and
triletter comma-free codes over finite alphabets*, Australasian Journal of
Combinatorics 86(2) (2023), 233–270, Definition 2.1 and Section 3:
<https://ajc.maths.uq.edu.au/pdf/86/ajc_v86_p233.pdf>.
The new project implication depends on the repair theorem connecting the
original GP condition to strict codes; no novelty is claimed for the necklace
count (2).

## 5. Reproducible direct check of the comparison example

The following command was actually run on 2026-10-12 and passed all 27
comma-free comparisons. Its purpose is only to audit the displayed finite
example; statements (2)–(5) follow from the proofs above.

```sh
python - <<'PY'
from itertools import product
C = {tuple(map(int, w)) for w in ('0123', '1234', '2345')}
checks = [(u + v)[j:j + 4] not in C
          for u, v in product(C, repeat=2) for j in range(1, 4)]
assert len(checks) == 27 and all(checks)
w = tuple(map(int, '01234500'))
assert [j for j in range(5) if w[j:j + 4] in C] == [0, 1, 2]
print('PASS: 27 comma-free comparisons; strict violation at starts 0,1,2')
PY
```

No computation is used to certify a universal GP optimum or an unproved
equivalence of code classes. No Lean compilation was performed for this file.
