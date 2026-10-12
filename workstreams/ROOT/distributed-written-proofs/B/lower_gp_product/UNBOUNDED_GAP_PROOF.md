# Arbitrarily large failure and the optimal replacement bound

This proof extends the fixed lower-GP counterexample to all integer parameters r>=6.

## Elementary unbounded-gap family

For each integer r>=6, construct G_r as two K_r graphs identified at one vertex c. Write the two remaining (r-1)-cliques as A,B and choose a in A,b in B. Construct H_r from landmarks z,u_0,u_1,v_0,v_1 and FOUR r-vertex cliques Q_ij exactly as in [the fixed construction proof](../../../lower-gp-product319-counterexample/PROOF.md): each Q_ij is adjacent precisely to z,u_i,v_j outside itself, and the landmarks induce K5minus the two edges u_0u_1,v_0v_1. Thus

    |G_r|=2r-1, |H_r|=4r+5,
    gp^-(G_r)=r, gp^-(H_r)>=r.

The G_r classification from the fixed proof works verbatim: its maximal GP sets are the two K_r blocks and A union B, whose sizes are r,r,2r-2. True-twin saturation in H_r forces any maximal GP set meeting Q_ij to contain all r vertices. The same six maximal GP subsets within the five landmarks have outside extensions, so every maximal GP set meets a Q-clique. These are complete all-parameter arguments, not extrapolations from finite tests.

The FIVE product points

    (a,u_0),(a,u_1),(c,z),(b,v_0),(b,v_1)

remain GP and maximal. Their selected distances and every case in the fixed proof depend only on landmark roles and membership in A,B,Q_ij, never on the number of clones. All required classes are nonempty for r>=6. Therefore

    gp^-(G_r square H_r)<=5,       min{gp^-(G_r),gp^-(H_r)}=r.

The deficit from the ORIGINAL conjectured bound is at least r-5 and is UNBOUNDED. The ratio of product lowerGP to the smaller factor lowerGP is at most5/r, tending to0. No increasing unbounded function of the smaller factor parameter can serve as a universal lower bound. This conclusion is elementary and independent of the metric-cone theorem. It concerns lower GP, not the previously known lower-TERMINAL gap in the original Proposition1.

The r=6instance is exactly the frozen11by29counterexample. No smaller construction is needed for acceptance.

## Sharp universal replacement, with explicit dependency

UNIVERSAL_FIVE_PROOF.md proves

    gp^-(G square H)>=min{5,gp^-(G),gp^-(H)}

for every nonempty finite simple undirected G,H. Combining it with the elementary family above gives gp^-(G_r square H_r)=5 for EVERY r>=6.

In fact the optimal lower bound that depends ONLY on r=min{gp^-G,gp^-H} is exactly min{r,5}. For r=1,...,5 take G=H=K_r. Each factor has lowerGP r. In K_r square K_r any GP set of size<r leaves an unused row and unused column; their intersection is distance2from every selected point and can be added (old pair distances are at most2). A full row is maximal: any outside point shares a column with one row point and has distance2to every other row point, giving a forbidden triple. For r=1 the singleton product is immediate. Thus the product lowerGP is exactly r. Together these examples attain the bound for EVERY positive integer r.

This supplies a sharp replacement for the false conjecture. The elementary counterexamples/unbounded failure do NOT depend on accepting the universal theorem; the optimality/lower-equality conclusion DOES. The two dependencies are separate written results; no universal Lean or historical-priority claim is made.
