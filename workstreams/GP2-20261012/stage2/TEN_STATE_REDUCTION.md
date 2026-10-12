# A ten-state model for the entire strict-code optimization problem

GP2-20261012, stage 2. Candidate complete written theorem; independent review and full Lean formalization remain pending. This is a further reduction beyond the 14 -> 9 -> 5 hierarchy in `HIERARCHICAL_MODEL.md`.

## 1. Statement

Retain the allowed and marked transitions of the inherited fourteen-state target, but restrict to

    P10 = {(a,b): 1<=a<b<=5}.

**Theorem.** Every strict four-window code over a finite alphabet is contained in a marked code admitting a P10-valued admissible triple assignment. Conversely every such marked code is strict. Thus the maximum product-weight density for **each** finite alphabet and nonnegative letter distribution is unchanged by restricting to P10. The supremum over all finite weighted alphabets is the original Kautz limiting density lambda_4 via the stage-one repair bridge.

The proof has two genuinely different cases. Restricting the canonical fourteen-state assignment to P10 without this case distinction would be unjustified: an independent code can have a canonical second-hit time six.

## 2. Nonindependent codes: two consecutive selected arcs force the second hit

Suppose C contains adjacent words abcd and bcde. They form two consecutive selected arcs in the full triple shift graph. For **any** target triple xyz, append x,y,z after those two arcs. This gives a five-arc walk ending at xyz that includes two selected arcs. Hence the canonical maximum count satisfies F_5(xyz)>=2. Strictness gives the reverse inequality, so

    F_5(s)=2 for every triple s.

The canonical hit-time pair therefore has its second coordinate at most five, and is in P10. The inherited completion argument gives an admissible marked code containing C. This reasoning concerns literal full-shift walks, not an assumption that these walks are Kautz geodesics.

## 3. Independent codes: an explicit five-profile embedding

Assume no two selected words are adjacent. The selected ordered-pair graph has no three-edge walk; let ell:A^2->{0,1,2} be maximum incoming walk length. Its selected edges strictly increase ell.

Choose tau:A^3->{0,1} equal to one on the triple-prefix support of C and zero on its triple-suffix support. These supports are disjoint by independence. Assign all remaining triples zero. Then

    C subset C_(ell,tau),
    C_(ell,tau)={abcd: ell(ab)<ell(cd), tau(abc)=1, tau(bcd)=0}.

This completed code is independent. If three of its windows had gaps a,b with a+b<=4, independence forces a=b=2, contradicting three strict increases in a three-valued level function. Hence it is strict.

For a triple s=abc, put x=ell(ab), y=ell(bc), t=tau(s), and define

    gamma(s) = (3-x,5), if t=1 and x<2;
             = (1,5-y), if t=0 and y>0;
             = (2,4), otherwise.                          (3.1)

Only the five profiles

    (3,5), (2,5), (1,4), (1,3), (2,4)

are used. They are all in P10.

Here is a structural verification of all allowed transitions. Attach to a level x the pair type

    q_0=(2,4), q_1=(1,4), q_2=(1,3).

Every ordered pair among these three types satisfies the pair-threshold inequalities. Each profile (3.1) lies in the rectangle domain

    I_(q_y) intersect O_(q_x),

where I_(alpha,beta) means first coordinate >=alpha and second >=beta, while O_(alpha,beta) means first <=alpha+1 and second <=beta+1. The inert profile (2,4) lies in all nine domains; the source extreme and terminal minimum give the other two cases. Consecutive profiles share their intermediate pair type q_y, so the target arc is allowed.

To identify marked arcs, the only used sources with marked outgoing incidence are (3,5) and (2,5), and the only used marked destinations are (1,4),(1,3). Between consecutive triple profiles with pair levels x,y,z, a marked arc occurs exactly when t=1, the following tau is zero, and

    5-z <= (3-x)+1, equivalently x<z.

Thus the marked code is **exactly** C_(ell,tau). All 108 combinations of x,y,z in {0,1,2} and the two tau bits are independently checked in the verifier.

This handles the empty code as well, using the constant inert profile. It proves the independent case, and with Section 2 proves the theorem.

## 4. The complete reduced hierarchy is 10 -> 6 -> 3

The P10 target has 76 allowed arcs and 10 marked arcs. Its maximal nonempty complete rectangles are exactly

    Q6 = {(alpha,beta): 1<=alpha<beta<=4},
    I_q={(a,b) in P10: a>=alpha,b>=beta},
    O_q={(a,b) in P10: a<=alpha+1,b<=beta+1}.

The same envelope argument as in `HIERARCHICAL_MODEL.md` now uses clamps **3 and 4**, rather than 3 and 5. A minimum source second-hit time of either four or five puts no nontrivial extra upper bound on destination second-hit times (all are <=5), so the clamp to four is exact.

The six pair types have 31 allowed transitions, again

    q->q' iff alpha'<=alpha+1 and beta'<=beta+1.

Their three maximal nonempty rectangles are indexed by

    R3={(1,2),(1,3),(2,3)}.

Use clamps **2 and 3** for this second envelope. The derived graph on R3 is complete, including its loops. Accordingly every choice of letter types eta:A->R3 is permissible; pair choices are in the associated rectangle intersections, and triple choices are in the associated P10 intersections.

There is no fixed bound on the number of letters or blocks: pair/triple assignments still distinguish letters having the same eta type. In particular, the independent construction in Section 3 uses the **single** letter type (1,3) at all letters, while its ordered-pair labels remain arbitrary functions of both letters. “One type” does not mean “one alphabet letter.”

## 5. Three choices per triple and the remaining adjacency branch

For q=(alpha,beta), q'=(alpha',beta') with nonempty domain, retain

    (alpha+1,5), if beta=4;                source extreme
    (1,beta'), if alpha'=1;                terminal minimum
    (1,5), if beta=4 and alpha'=1.         bridge

If none applies, retain any one domain element. There are at most three choices. Exactly the marked row/column domination proof in `HIERARCHICAL_MODEL.md` applies, now relative to all ten profiles, and therefore retains all previously selected words under simultaneous replacement.

The result is an exact nonnegative weighted optimization model with three letter types, six pair types, and at most three choices at each triple. It covers both independent and nonindependent codes.

Two consecutive marked arcs still necessarily have profile sequence

    (4,5) -> (1,5) -> (1,2).

The first letter of their five-letter concatenation has type (2,3), and the last has type (1,2). The all-(1,3) representation of independent codes contains no such adjacency. We do **not** prove that the remaining two letter types can be discarded in optimizing the full problem, nor that the independent optimum equals the unrestricted optimum.

## 6. Why this is not already the exact lambda_4

The reduction is exact in feasibility and weighted objective, not only a list of necessary conditions. But the number of ordered-pair and triple variables still grows with the alphabet, and choosing them to maximize all marked overlaps is a global optimization problem. The numerical interval remains the stage-one interval; this theorem is a smaller exact structural target for the next analytic/optimization step.

The generic rectangle/right-adjoint principle is classical and is attributed in `HIERARCHICAL_MODEL.md`. This note's specific content is the case-dependent exclusion of the four second-hit-time-six profiles, the explicit five-profile independent embedding, and the resulting marked-objective-preserving 10/6/3 hierarchy. Neither minimality of these state counts nor historical priority is claimed.
