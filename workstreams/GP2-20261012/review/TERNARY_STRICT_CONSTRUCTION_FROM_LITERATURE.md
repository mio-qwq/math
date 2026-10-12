# A classical ternary dictionary gives a strict Kautz construction

Date: 2026-10-12. Status: discovery note, with complete elementary proof below;
the discoverer is not the independent reviewer of this candidate. This file
records a literature-derived construction. It claims no novelty for the
classical comma-free dictionary or its ordinary comma-free density.

## 1. Exact source and relation

Golomb, Gordon and Welch, *Comma-Free Codes*, Canadian Journal of Mathematics
10 (1958), 202–209, give on page 206 a dictionary satisfying

\[
 a<c,\qquad b\ge d. \tag{1}
\]

For three letters they obtain 18 words. Page 208 uses this dictionary to give
the ordinary comma-free asymptotic lower bound \(2/9\).

Primary publisher PDF:
<https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B78C35132E2BCD4A14459BE6A142FF30/S0008414X00045296a.pdf/commafree_codes.pdf>.
DOI: <https://doi.org/10.4153/CJM-1958-023-9>.

The original printed page 206 was visually inspected after rendering the PDF
at twice its native dimensions on 2026-10-12. The weak inequality in (1) is
\(b\ge d\). Text extraction of this scan incorrectly renders it as a strict
inequality, so that extraction must not be used to transcribe the formula.

For convenience this note uses the reversal of (1):

\[
 C=\{abcd\in\{0,1,2\}^4:a\le c,\ b>d\}. \tag{2}
\]

Indeed, \(abcd\) satisfies (1) precisely when \(dcba\) satisfies (2).
The additional statement proved here is that this dictionary satisfies the
stronger five-window occurrence constraint needed for the GP construction.

## 2. The stronger occurrence constraint

For a word \(x_0\ldots x_7\in\{0,1,2\}^8\), let \(I_i\) indicate that its
four-letter window at position \(i\) belongs to \(C\), for \(0\le i\le4\).
We claim

\[
 \sum_{i=0}^4 I_i\le2. \tag{3}
\]

First, consecutive windows cannot both belong to \(C\). Membership at \(i\)
requires \(x_{i+1}>x_{i+3}\), while membership at \(i+1\) requires
\(x_{i+1}\le x_{i+3}\).

If three positions in \(\{0,1,2,3,4\}\) have no consecutive pair, they must
be exactly \(0,2,4\). Selection at these positions would require

\[
 x_1>x_3>x_5>x_7,
\]

a strictly decreasing chain of four elements in a three-element ordered set.
This is impossible, proving (3). The argument counts occurrences, and allows
equal selected words at different positions; it does not replace occurrence
counts by counts of distinct words.

Condition (3) is stronger than ordinary comma-freeness. In general, an
ordinary comma-free code with no two selected consecutive windows satisfies
(3), because its only possible triple of nonconsecutive selected starts is
\(0,2,4\), which ordinary comma-freeness excludes. Formula (2) provides both
properties by the direct argument above.

The restriction to three ordered symbols matters: on four symbols the word
\(03020100\) satisfies (2) at starts \(0,2,4\). Also, replacing \(b>d\) by
\(b\ge d\) fails even for the constant eight-letter word. These are explicit
negative controls for the alphabet and inequality parameters.

## 3. Original directed graph and GP bridge

Let \(B_0,B_1,B_2\) partition an actual alphabet of size \(m\), with block
map \(\pi\). Let \(S\) be all original Kautz vertices \(v_0v_1v_2v_3\), so
\(v_i\ne v_{i+1}\), for which
\(\pi(v_0)\pi(v_1)\pi(v_2)\pi(v_3)\in C\).

The original arc relation shifts a word left by one letter and appends a
letter different from its former last letter. Every shortest directed path
has at most four arcs: if the last letter of its first vertex differs from
the first letter of its last vertex, append the four letters of the last
vertex; otherwise append only its final three letters, using the common
letter as an overlap. In either case this constructs a legal walk of length
at most four.

Every directed walk of at most four arcs can be read as consecutive
four-letter windows of a word of length at most eight. Applying \(\pi\), and
extending the resulting block word to length eight if necessary, (3) allows
at most two selected occurrences. In particular, no shortest directed path
contains three distinct vertices of \(S\). Thus \(S\) is a general-position
set for the original directed definition. This proves the required universal
quantifier over shortest paths; no mutual-visibility interpretation is used.

Block words in \(C\) may have equal adjacent symbols. Actual selected
vertices still obey the original adjacent-letter inequality. This is why the
finite count below includes factors \(q-1\).

## 4. Exact counts and the asymptotic lower bound

There are six pairs \((a,c)\) with \(a\le c\), and three pairs \((b,d)\)
with \(b>d\). Hence \(|C|=18\). In lexicographic order the words are

```text
0100 0110 0120 0200 0201 0210 0211 0220 0221
1110 1120 1210 1211 1220 1221 2120 2220 2221
```

Among these words, five have zero equal adjacent block pairs, ten have one,
and three have two. If all three blocks have size \(q\ge1\), a pattern with
\(e\) equal adjacent pairs contributes exactly \(q^{4-e}(q-1)^e\) actual
legal vertices. Therefore

\[
 \boxed{\operatorname{gp}(\operatorname{Ka}(3q,4))
 \ge18q^4-16q^3+3q^2.} \tag{4}
\]

For arbitrary block sizes \(n_0,n_1,n_2\), the exact size of this construction
is the finite polynomial

\[
 \sum_{c\in C}n_{c_0}
 \prod_{i=1}^{3}\bigl(n_{c_i}-{\bf1}_{c_i=c_{i-1}}\bigr). \tag{5}
\]

For arbitrary \(m\ge3\), write \(q=\lfloor m/3\rfloor\), place \(q\) actual
letters in each block, and place the leftover letters anywhere. Taking the
subset of the resulting GP set whose letters all lie in the first \(3q\)
letters gives

\[
 \operatorname{gp}(\operatorname{Ka}(m,4))
 \ge18\lfloor m/3\rfloor^4-16\lfloor m/3\rfloor^3
      +3\lfloor m/3\rfloor^2. \tag{6}
\]

Consequently the construction proves directly

\[
 \liminf_{m\to\infty}
 \frac{\operatorname{gp}(\operatorname{Ka}(m,4))}{m^4}
 \ge\frac{18}{3^4}=\frac29. \tag{7}
\]

No finite optimum is asserted in (4)–(6).

The weights of the three blocks can be optimized exactly for this template.
Let their limiting probabilities be \(x_0,x_1,x_2\), and put
\(s=x_0^2+x_1^2+x_2^2\). For independent block labels,

\[
 \Pr(a\le c)=\frac{1+s}{2},\qquad
 \Pr(b>d)=\frac{1-s}{2}.
\]

The two coordinate pairs are independent, so the template density is
\((1-s^2)/4\). Since \(s\ge1/3\), its maximum is \(2/9\), attained exactly
at equal block weights. This is optimality within this fixed template,
not an upper bound for all strict codes or GP sets.

## 5. Actual direct checks

On 2026-10-12 a fresh direct enumeration of the \(3^8=6561\) block words
found maximum selected occurrence count two. The eighteen patterns and the
adjacent-equality histogram were also generated directly from (2). The
following command reproduces these checks and the two explicit negative
controls; it uses no previous template search or solver certificate.

```sh
python - <<'PY'
from collections import Counter
from itertools import product
C = {w for w in product(range(3), repeat=4)
     if w[0] <= w[2] and w[1] > w[3]}
assert len(C) == 18
hist = Counter(sum(w[i] == w[i+1] for i in range(3)) for w in C)
assert hist == {0: 5, 1: 10, 2: 3}
counts = [sum(w[i:i+4] in C for i in range(5))
          for w in product(range(3), repeat=8)]
assert len(counts) == 6561 and max(counts) == 2
wrong_alphabet = tuple(map(int, '03020100'))
hits = [i for i in range(5)
        if wrong_alphabet[i] <= wrong_alphabet[i+2]
        and wrong_alphabet[i+1] > wrong_alphabet[i+3]]
assert hits == [0, 2, 4]
wrong_weak = (0,) * 8
assert sum(wrong_weak[i] <= wrong_weak[i+2]
           and wrong_weak[i+1] >= wrong_weak[i+3]
           for i in range(5)) == 5
print('PASS: 18 patterns, 6561 words, histogram 5/10/3; both negatives detected')
PY
```

These computations audit the small block code. The proofs in Sections 2–4
establish strictness and the GP construction for all block sizes. The
independent reviewer is responsible for a separate reconstruction from
original adjacency and BFS; this discovery note does not claim to be that
review. No Lean compilation has been run for this note.

## 6. What the literature does and does not settle here

Fimmel, Michel, Pirot, Sereni and Strüngmann, *Diletter and triletter
comma-free codes over finite alphabets*, Australasian Journal of Combinatorics
86(2) (2023), 233–270, page 236, explicitly describe the even-length
comma-free leading coefficient as still undetermined. Definition 2.1
distinguishes ordinary comma-free codes from strong comma-free codes.
Primary PDF: <https://ajc.maths.uq.edu.au/pdf/86/ajc_v86_p233.pdf>.

Tang, Golomb and Graham, *A New Result on Comma-Free Codes of Even
Word-Length*, Canadian Journal of Mathematics 39(3) (1987), 513–526, page 514,
report the earlier computer determination \(W_4(4)=57<60\) and study
nonattainment of the primitive-orbit bound. Those ordinary comma-free facts
do not prove a GP bound or certify that a larger dictionary is strict.
Primary PDF:
<https://www.cambridge.org/core/services/aop-cambridge-core/content/view/71A7831337DAC1E7D03DF9AE4C096F08/S0008414X0000448Xa.pdf/a-new-result-on-comma-free-codes-of-even-word-length.pdf>.

The reviewed sources establish the classical origin of the dictionary and
the need for an additional strict-window argument. They do not certify that
the Kautz implication (7) has never appeared elsewhere. No exhaustive novelty
or open-status claim is made from search non-detection.
