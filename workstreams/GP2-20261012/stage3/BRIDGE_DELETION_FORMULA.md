# Exact weighted bridge deletion and its 10/6/3 interface bounds

GP2-20261012, 2026-10-13. Complete all-alphabet written theorem about
strict four-window codes. This is a positive structural refinement of
`../global_upper/ENDPOINT_SUPPORT_AND_INDEPENDENT_CODES.md`, not a new
lambda_4 endpoint, not a proof that independent codes are extremal, and
not a lower-order-cost repair of arbitrary GP sets. No complete Lean,
independent AI review or historical first-discovery claim is made.

## 1. Quantifiers and the exact formula

Let A be any finite nonempty alphabet, mu a probability distribution on A
(zero weights allowed), and C a strict subset of A^4: every word in A^8
has at most two selected occurrences among its five consecutive windows.
Put nu(w)=product of the four letter weights and p=sum_(w in C) nu(w).
Selected words are adjacent when the suffix of length three of the first
equals the prefix of length three of the second. Independence in this
note means absence of any such selected adjacency, including loops.

For each triple s=bcd define

    I_s={abcd in C:a in A}, O_s={bcde in C:e in A},
    i(s)=sum_a mu(a) 1{as in C},
    o(s)=sum_e mu(e) 1{se in C}.

Let B_C be the set of triples for which I_s and O_s are both nonempty,
and let mu_3(s)=mu(b)mu(c)mu(d). Define

    d(C)=sum_(s in B_C) mu_3(s) min{i(s),o(s)},
    b(C)=sum_(s in B_C) mu_3(s),
    a(C)=Pr[U_0U_1U_2U_3 in C and U_1U_2U_3U_4 in C],

where the letters are independent with common distribution mu.

**Theorem 1 (exact deletion).** The maximum product density of an
independent subset of this particular C is exactly

    p_ind(C)=p-d(C).                                  (1)

Every nonisolated weak component of the selected-word adjacency graph is
the complete bipartite graph from I_s to O_s for a unique s in B_C. These
components are vertex-disjoint. An optimal subset keeps the heavier of
I_s and O_s in each component and keeps all isolated words. Consequently
(1) is computable in O(|C|) arithmetic operations using prefix/suffix
tables, with no matching or integer-programming solver.

**Theorem 2 (weighted compatibility cost).** One has the exact identity
and inequality

    a(C)=sum_(s in B_C) mu_3(s)i(s)o(s),
    d(C)^2 <= b(C)a(C).                               (2)

In particular `p_ind(C)>=p-sqrt(b(C)a(C))`. If the active bridge set has
zero product weight, then d(C)=0, including cases with combinatorial
adjacency on zero-weight letters. These are statements about subsets
of a fixed code, not optimization over all pair or triple labels.

## 2. Proof of the complete-component structure and formula

No selected word w can have both a selected predecessor u and a selected
successor v. Indeed u,w,v spell three selected consecutive occurrences
at starts 0,1,2 in a six-letter word; append two arbitrary letters to
obtain an eight-letter contradiction. Words or letters may repeat, so
this argument also excludes selected loops and digons.

For s in B_C, each word in I_s is followed by every word in O_s because
the common overlap is exactly s. A word of I_s already has a successor,
so by the preceding paragraph it has no predecessor. All of its
successors have prefix s and are exactly O_s. Similarly each word of
O_s has no successor and all of its predecessors are exactly I_s.
Thus I_s and O_s are disjoint and their component is complete bipartite.

Different s cannot share a word on the incoming side (a word has only
one length-three suffix), nor on the outgoing side (only one prefix).
They cannot share a word on opposite sides either, because that word
would have both a predecessor and a successor. Every selected adjacency
has some overlap s, so this lists all nonisolated components.

An independent subset of a complete bipartite component must omit one
whole side: if it kept a word on each side there would be an adjacency.
With nonnegative weights its greatest retained weight is the larger
side weight. The two side weights are mu_3(s)i(s) and mu_3(s)o(s).
Since components are disjoint, their minimum deletion costs add. All
isolated words can be kept. This proves (1), including zero weights.

Condition on the shared triple in a random five-letter word. Its free
left and right letters are independent, so its two-window selection
probability is i(s)o(s). This proves the identity in (2). For every s,
`min{i(s),o(s)}^2<=i(s)o(s)`. The finite-sum Cauchy inequality with
weights mu_3(s) gives

    d(C)^2 <= b(C) sum_s mu_3(s) min{i(s),o(s)}^2
            <= b(C)a(C).

There was no division by b(C); all zero cases are included. QED.

## 3. A precise coupling to the accepted 10/6/3 hierarchy

Now suppose C is **contained** in the marked code of an admissible
P10-valued triple labelling gamma with pair labels kappa and letter
labels eta as in `../stage2/TEN_STATE_REDUCTION.md`. Write the three
letter types as r0=(1,2), r1=(1,3), r2=(2,3), and put

    x=mu{eta=r0}, z=mu{eta=r2}.

The domains are

    gamma(abc) in [kappa(bc), kappa(ab)+(1,1)] coordinatewise,
    kappa(ab) in [eta(b), eta(a)+(1,1)] coordinatewise.

A marked triple arc p->q has p_second=5, q_first=1 and
q_second<=p_first+1. A triple that has both incoming and outgoing marked
incidence must therefore have profile (1,5). Two consecutive marked arcs
have the forced profile sequence

    (4,5) -> (1,5) -> (1,2).                           (3)

To see this directly, the shared profile is (1,5); an incoming marked
arc to it requires source first coordinate at least four, hence (4,5)
inside P10. An outgoing marked arc from it requires a terminal second
coordinate at most two, hence (1,2).

**Corollary 3 (interface-mass bounds).** Every active bridge s=bcd has

    gamma(s)=(1,5), eta(b) in {r1,r2}, eta(d) in {r0,r1},
    i(s)<=z, o(s)<=x.

Consequently

    b(C) <= (1-x)(1-z),
    a(C) <= b(C)xz,
    d(C) <= b(C) min{x,z}.                             (4)

**Proof.** For an incoming selected word abcd, (3) gives
gamma(abc)=(4,5), which forces kappa(ab)=(3,4) by the P10/Q6 domain
bounds. In turn eta(a) must be r2. Thus every predecessor's free letter
a has total available mass at most z. At the other end gamma(cde)=(1,2)
forces kappa(de)=(1,2), and eta(e) must be r0. Hence o(s)<=x.

The bridge profile (1,5) forces the second coordinate of kappa(bc) to
be four and the first coordinate of kappa(cd) to be one. The former
excludes eta(b)=r0, whose second coordinate plus one is only three.
The latter excludes eta(d)=r2, whose first coordinate is two. Summing
over independent letters b,c,d proves the b(C) bound; (2) and the pointwise
upper bounds prove the other two. QED.

Only containment of C in the marked code is needed: all arguments
use marked transitions of selected words, not the selection of every
marked word. The accepted ten-state completion supplies such labels for
every strict C. Its statistics i,o,d,a,b can therefore still be calculated
on the original C; one must not silently substitute the enlarged code's
statistics. The cost expressions provide a new interface functional to
couple to the pair-level empty-orbit loss. They do not license discarding
r0/r2 or the adjacency branch for free.

## 4. Checks, interpretation and remaining task

The checker constructs raw prefix/suffix adjacency independently of the
formula, finds weak components, verifies that each is exactly its predicted
complete bipartite component, and brute-forces all subsets **within** each
small component to check the weighted independent optimum. It compares
the strictness dynamic program with literal eight-letter words on small
inputs. It reconstructs the original Ka(4,4) adjacency (including digons),
uses BFS distances and tests every ordered triple of distinct selected
vertices, not mutual visibility. It also explicitly reconstructs the
10/6/3 labels for the compatible blow-ups and checks (3)--(4).

The classical two-pattern strict code {0001,0011} and its blow-ups are
inherited test fixtures, not new constructions. Their exact deletion
costs continue to show that the loss can have positive density. The new
content here is the general complete-component classification, exact
weighted formula, and its active-bridge mass coupling. Weighted complete
bipartite independent-set optimization and Cauchy are elementary standard
facts; historical novelty of this particular application is unconfirmed.

The coefficient one in `d(C)^2<=b(C)a(C)` is sharp: for the two-pattern
code with equal binary letter weights, p=1/8, d=1/16, b=1/8, a=1/32,
and both sides are 1/256. This sharpness concerns the compatibility-cost
inequality alone, not the maximal density of strict or independent codes.

```sh
python workstreams/GP2-20261012/stage3/verify_bridge_deletion.py
python -O workstreams/GP2-20261012/stage3/verify_bridge_deletion.py
```

The full all-alphabet statements are proved above. Exact finite inputs,
execution logs, hashes and damaged-input controls accompany the checker.
No fixed model output is promoted to a universal numerical optimum.
Original GP sets require the already accepted strict-window repair before
this theorem can be applied; it is not asserted directly for every GP set.

The trusted interval stays

    0.224808115216882691... <= lambda_4 <= 0.249578038101911868... .

Next: couple a provable mixed-class rotation loss with d(C), a(C) and
b(C) so that both the independent and positive-bridge regimes are covered.
The exact deletion formula is a bridge between those regimes, not the
missing uniform optimization itself.
