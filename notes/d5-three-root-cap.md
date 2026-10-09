# A continuous obstruction after deleting three specified D5 roots

**Scope.** Delete the three scaled roots `e1+e2`, `e1+e3`, `e2+e3` from the
40 roots of D5 and fix the other 37. At most three mutually compatible
points of squared norm 2 can be added. If three are added, they must be the
three removed roots. The added points may have arbitrary real coordinates.
This is a restricted replacement theorem, not a proof that the unrestricted
five-dimensional kissing number is 40. Historical novelty is undetermined.

The [Lean source](proof/K5ThreeRootCap.lean) proves the real-coordinate
obstruction and the classification of three compatible completion members.
The [receipt](results/d5-three-root-cap.json) gives the exact source hash,
actual primary and independent elaborations, and declaration axiom audits.
There is no finite-grid assumption or computational vertex-completeness
assumption in the proof.

## Exact geometric problem

Use scaled coordinates: every point has squared norm 2 and distinct points
have inner product at most 1. Dividing all vectors by sqrt(2) gives the usual
unit-sphere formulation with inner product at most 1/2. The D5 roots are
`±ei±ej`, for `1<=i<j<=5`.

For a prospective point `a=(p,q,r,d,e)`, the retained-root inequalities are
precisely the following 37 signed inequalities, compressed using absolute
values:

- `|p-q|, |p-r|, |q-r| <= 1`, and `-p-q, -p-r, -q-r <= 1`;
- each of `|p|,|q|,|r|` plus either `|d|` or `|e|` is at most 1;
- `|d|+|e| <= 1`.

The first line represents nine signed constraints, the second 24, and the
last four. Only `p+q<=1`, `p+r<=1`, `q+r<=1` are omitted. Lean's
`rootVector` builds the actual signed coordinate vectors;
`dot_rootVector` and `geometric_iff_root` identify their inner products with
these signed inequalities.

## Analytic proof

First use a two-coordinate rigidity lemma. Suppose nonnegative
`P,Q,t1,t2,t3` satisfy `P+ti<=1`, `Q+ti<=1`, and `ti+tj<=1` for distinct
tail indices. There is no hypothesis on `P+Q`. If their squared norm is 2,
all three tails vanish. Indeed, let `h=max(t1,t2,t3)`. For `0<h<=1/2`, the
squared norm is at most

`2(1-h)^2+3h^2 = 2-4h+5h^2 < 2`.

For `1/2<=h<=1`, the two other tails and both distinguished coordinates
are at most `1-h`, so the squared norm is at most

`h^2+4(1-h)^2 <= 5/4 < 2`.

At `h=0`, squared norm 2 forces `P=Q=1`. This is an elementary continuous
inequality, with a kernel-checked proof by a finite case split on the
largest of the three real tail coordinates.

If one of `p,q,r` were negative, its absolute-value sum constraint with
each of the other coordinates would follow from the retained difference
or negative-sum constraints. Taking that coordinate as a tail and the two
other first coordinates as distinguished coordinates applies the lemma
and forces the negative coordinate to vanish. Thus `p,q,r>=0`.

Set `b=max(|d|,|e|)` and `c=min(|d|,|e|)`. Then `0<=c<=b`, `b+c<=1`, and
each of `p,q,r` is at most `1-b`. Write `s=p+q+r`. Nonnegativity yields

`2 = p^2+q^2+r^2+b^2+c^2 <= (1-b)s+b(b+c) <= (1-b)s+b`.

If `s<=2`, this is at most `2-b`, so `b=0` and `s=2`. Therefore every
compatible sphere point has `s>=2`. At equality the tails vanish and each
first coordinate is 0 or 1; precisely two are 1. The cap boundary thus
consists of the three removed roots.

In unit normalization this is the common cap with projection at least
sqrt(2/3) onto `(1,1,1,0,0)/sqrt(3)`. The proof uses one fixed axis and
does not apply different coordinate permutations to points before summing.

For four scaled compatible points, their sum `z` has first-three-coordinate
sum at least 8. Cauchy--Schwarz gives `||z||^2>=64/3`, whereas their four
norms and six pairwise inner products give `||z||^2<=8+12=20`.
This contradiction proves the replacement bound. For three points the
corresponding lower and upper bounds both equal 12. Each point must be on
the cap boundary, hence is a removed root. Distinctness follows because a
repeated vector has self-inner-product 2, violating the pair bound 1.

Interior compatible single points do exist: `(4/5,4/5,4/5,1/5,1/5)` is an
exact example. The conclusion does not restrict every single point to the
three removed roots; it restricts families attaining size three.

## Literature and precise formalization boundary

[Cohn and Rajagopal (2026), Section 2](https://arxiv.org/html/2412.00937v3)
reports the unrestricted range `40<=tau5<=44` and studies several
40-point configurations. [Cohn, Jiao, Kumar and Torquato (2011), Section 3](https://msp.org/gt/2011/15-4/gt-v15-n4-p11-p.pdf)
already proves infinitesimal jamming of Dn for n>=4. Those known results
are attributed here. The present theorem has the particular finite
replacement quantifiers above. The bounded literature review has not
established historical originality of this restricted result or its
elementary ingredients; no priority claim is made.

Lean endpoints `geometric_four_points_impossible` and
`geometric_three_completion_members` quantify arbitrary vectors in
`Fin 5 -> Real`, assume only norm and actual retained-root/pair inner-product
conditions, and prove respectively impossibility and membership in the
three explicitly removed coordinate vectors. The final identification of
the three-member point set uses the distinctness observation just given;
there is no separate Lean theorem packaging that observation as a Finset
equality. Arbitrary other deletions, motion of the retained roots, other
40-point starting configurations and the unrestricted kissing number are
outside these endpoints.

Reproduce using the repository's pinned Lean/Mathlib environment:

~~~sh
cd 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../notes/proof/K5ThreeRootCap.lean
~~~
