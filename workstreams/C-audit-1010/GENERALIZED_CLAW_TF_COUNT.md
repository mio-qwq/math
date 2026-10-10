# All generalized claw graphs: a parity-dependent exact TF-cousin count

Agent C-audit-1010, 2026-10-10. **Full written theorem candidate, pending ROOT's independent review.** No Lean compilation, human peer review, historical priority certificate, signed release or main-branch acceptance claimed.

## Original source, claim and boundaries

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3 (10 September 2026), Definition 6.1, Remark 6.2 and Section 7: https://arxiv.org/html/2603.27559v3 . The original cubic CG(n) is r=3. Remark 6.2 extends the source **construction** to K_(1,r), r>=2. It shows the particular **standard pair** CG_r(n), CG'_r(n) is TF-isomorphic only when rn is odd; it does **not** claim that every other cousin is absent for even r. Section 7 explicitly leaves the exact number of cousins of the cubic family for general odd n open. The guide/conjugacy correspondence is prior Theorem 4.6 (Pacco–Scapellato); it is not new here.

Write G_r(n) for the graph whose vertices are R_t (t mod 2rn), L_p (p mod rn), and C_i (i mod n), and whose **complete** edges are R_t R_(t+1), L_p R_p, L_p R_(p+rn), and C_i L_p when p=i mod n. It has (3r+1)n vertices, 5rn edges and is connected.

**Main theorem candidate (all n>=3, r>=2):** Among **connected** loopless undirected graphs H with CDC(H) isomorphic to CDC(G_r(n)), the exact number of isomorphism classes H **other than G_r(n)** equals:

- n even: **zero**, for every r>=2;
- n odd and r odd (r>=3): **two**;
- n odd and r even (r>=2): **one**.

For odd r,n, the cover group has order 8rn and strongly switching conjugacy class sizes 1,1,rn. For even r, odd n>=3, it has order **8nr²** and exactly **r(n+1)** strongly switching involutions in two conjugacy classes of sizes **r,rn**. These are universal mathematical claims, **not** deductions from the finite diagnostics.

This resolves the paper's all-odd-n counting question at r=3 if the earlier independently frozen proof passes ROOT review; the **new** portion treats the author's generalized claw family at even r. Do not extrapolate this n>=3 theorem to n=1: Petersen at (r,n)=(3,1) is an acknowledged exceptional case, and the even-r n=1 cover groups are larger.

## 1. All even n yield zero CONNECTED cousins

When n is even, rn is even. Colour R_t by t mod 2, L_p oppositely to p mod 2, and C_i by i mod2. This is a proper bipartition since p=i+jn has parity i. CDC(G)=G disjoint-union G for connected bipartite G. A **connected** base H with this CDC must itself be bipartite, giving CDC(H)=H disjoint-union H; comparing connected components yields H isomorphic to G. This does NOT exclude disconnected bases and makes no invalid assertion that even rn alone implies bipartiteness.

When n is odd, G is nonbipartite: the length-n ring path from R_i to R_(i+n), two leaves L_i,L_(i+n), and centre C_i form a simple odd cycle of length n+4. Thus CDC(G) is connected.

## 2. Odd r, odd n: previously frozen structural rigidity, with a new triangle invariant

For odd h=rn>=5, the cover ring vertices form two disjoint C_(2h). Each leaf connects antipodal ring vertices lying in **different** ring cycles, and every ring vertex has exactly one leaf neighbour. For r>=5, centres (degree r), leaves (degree3 with a centre neighbour) and rings (remaining degree3 vertices) are graph-intrinsic types. The r=3,n>=3 case instead uses the complete simple-6-cycle type certificate in C's existing frozen CG_ODD_COMPLETE_THEOREM.md.

Any cover automorphism is fixed by the image and orientation of **one** of the two ring cycles: at most 2·(4h)=8h choices. The 4h lifts of the original ring dihedral symmetries and their central deck flips realize all possibilities. Thus Aut(CDC(G)) = D_(2h) × C2, order 8h. The complete strongly switching set is deck, deck times halfturn rho_h, and deck times each of h even-axis reflections; the conjugacy class sizes are 1,1,h. By published Theorem 4.6 there are exactly three nonisomorphic bases, including the source: **two TF-cousins**.

Additional exact algebra: the three explicit folds have simple-triangle counts **0,0,2** respectively, for every h odd>=5. In all three folds ring-induced components have lengths [2h], [h,h], [2h], so no ring-only triangles. Centres cannot lie in triangles. A leaf makes a triangle only if its two antipodal ring neighbours are adjacent. This never holds in the identity/halfturn folds; in the reflection fold the condition is 2t = ±1-h mod 2h, giving precisely **two distinct antipodal pairs** because h is odd.

## 3. Even r and odd n>=3: full cover group from two ring cycles and their leaf bundles

Let h=rn be EVEN. There are two ring components Q_c (c=0,1), parameterised by R_(c,t)=(R_t, layer epsilon=(t+c) mod2), with t mod2h. Both are cycles C_(2h). Each cover leaf can be uniquely written L_(c,p)=(L_p, layer epsilon=1-(p+c mod2)), p mod h; it is adjacent to the antipodal ring pair R_(c,p), R_(c,p+h) in **that same component**.

The intrinsic graph types are recognisable because r is even and r !=3: centres are the degree-r vertices (r=2 allowed), leaves the degree-three vertices adjacent to a centre, rings the other degree-three vertices.

For each centre (C_i, epsilon), let b mod2n be the unique solution of b=i mod n, b=epsilon mod2 (n is odd). The centre's neighbours are precisely all leaves L_(0,p) with p=b mod2n, and all leaves L_(1,p) with p=b+n mod2n. There are r/2 leaves in each bundle. In particular **each** of the 2n residue-bundles in Q_0 is matched by exactly one centre to the bundle differing by n in Q_1.

Every cover automorphism permutes the two ring cycles and restricts on each to a dihedral action. Thus it has parameters w in {0,1}, signs s_c in {+1,-1}, offsets a_c in Z/(2h), acting by

Q_c ring coordinate t -> (Q_(c XOR w), s_c t+a_c mod2h).

Each leaf is pinned by its unique antipodal ring-neighbour pair, so its action is forced to be L_(c,p) -> L_(c XOR w, s_c p+a_c modh). Centres are forced by their neighbour bundles. Preserving the matching of centre bundles is **equivalent** to

 (s_1-s_0)b+(s_1-1)n+a_1-a_0 = 0 (mod 2n) for every b mod2n.

Since n>=3, s_1-s_0 in {-2,0,2} vanishes for all b only if s_0=s_1=:s. The term (s-1)n then always vanishes modulo2n, leaving **a_1=a_0 (mod2n)**. Conversely, these conditions are sufficient to extend the ring/leaf maps uniquely over the centres; the explicit b correspondence preserves every edge and nonedge. Hence *all* cover automorphisms are exactly

 (w,s,a_0,a_1),  w∈{0,1}, s∈{±1}, a_0,a_1 mod2h, a_1=a_0 mod2n.

There are 2·2·(2h)·(2h/(2n)) = **8hr=8nr²** such automorphisms. No larger automorphism is possible because ring and leaf images already force every centre image.

## 4. Strong switches and their two conjugacy classes (even r, odd n>=3)

A ring R_(c,t) has original cover layer epsilon=t+c mod2; under the above automorphism the layer changes by a_0+w mod2. Thus it switches the bipartition exactly when a_0+w is odd.

For w=0, switching requires a_0 odd. The ring transformation can be involutive only if s=-1 (a rotation involution of C_(2h) has offset 0 or h, both even). Then each ring component has an odd-offset reflection t -> -t+a_c, which maps some ring vertex to an **adjacent** vertex because 2t=a_c±1 is solvable modulo2h. Therefore no w=0 guide is **strongly** switching.

For w=1, switching requires a_0 even. Squaring the action forces a_1=-s a_0 (mod2h), and compatibility then forces (s+1)a_0=0 (mod2n). If s=+1, a_0 must be a multiple of 2n: exactly **r** possibilities modulo2h. If s=-1, **every even** a_0 works: exactly **h=rn** possibilities. Each is strongly switching: ring vertices move to the other ring cycle, leaves map to leaves and centres to centres, so no vertex can be adjacent to its image.

The orientation sign s is conjugacy-invariant (it is a group homomorphism to {±1}). To see each sign class is transitive, conjugate by any component-preserving translation with b_1=b_0 mod2n. The guide's first offset becomes a'_0=a_0+b_1-s b_0. For s=+1 its possible changes b_1-b_0 traverse every multiple of2n (all r guides); for s=-1 taking b_1=b_0 gives a'_0=a_0+2b_0 (all h guides). Hence exactly **two conjugacy classes**, of sizes r and rn. The original deck involution is (w=1,s=+1,a_0=a_1=0), in the first class. Theorem 4.6 now yields two base isomorphism classes, original and **one TF-cousin**. The folded-base automorphism orders are 8nr²/(2r)=4nr and 8nr²/(2rn)=4r.

## 5. Explicit nonisomorphic cousin even when rn is even

The ordinary reflection mu_0 sends R_t->R_(-t), L_p->L_(-p), C_i->C_(-i). It is an involutory graph automorphism sending no vertex to an adjacent vertex (even-axis reflection of an even ring). Define the **reflection-twist** F by B(u,v)=A(u,mu_0(v)). It is symmetric, has no loops, and has the same CDC, with explicit layer map (v,0)->(v,0), (v,1)->(mu_0(v),1).

For even r and odd n>=3, F is directly nonisomorphic to G, independently of the group count. Its ring-induced graph has edges R_s--R_(-s±1) and forms one C_(2h), with a canonical ring-cycle coordinate f(s)=-s if s even and f(s)=s if s odd. A leaf L_p of F joins an antipodal pair whose index in this ring coordinate is q(p)=p (even p) or -p (odd p), modulo h. Centre C_i of F meets leaves with p=-i modn. As j runs through r consecutive petals p=-i+jn, parity alternates because n is odd and r is even; their pair-indices q(p) modulo n have both distinct residues +i and -i for every i !=0 (n odd). Every centre of **G** instead has all its pair-indices congruent to one residue modn.

An isomorphism must preserve centres, leaves and rings by intrinsic degrees/neighbour-types; its restriction to the unique ring cycle is a dihedral transformation, which sends every antipodal-pair coordinate x to ±x+t mod h and preserves the number of distinct residues mod n among a centre's attached leaves. G has n centres with signature size1; F has one of size1 and n-1 of size2. Thus F is **not isomorphic** to G. The original Remark 6.2 only excluded the author's different standard twist CG'_r(n); this construction does not contradict that specific claim.

## 6. Actual verification and limitations

All computations listed were **actually executed** on CPython 3.13.5 Linux on 2026-10-10, with exact graph edges and no numerical spectra:

- Cubic/odd fold triangle replay: 15 odd n=3,...,31 PASS; three negative controls rejected; source SHA256 709402ab00f57fee490219d36c460fdafe715a39124b733397f7f342f44b5ffc.
- General source construction over 36 r,n cases PASS. Importantly the first (incorrect) attempted assertion that even rn implies bipartiteness was **rejected** by actual graphs; corrected statement is only **even n** implies bipartiteness. General source SHA256 b7015f2f33e92d8e532764578de581dabf033f5ee92ba4ffdd526ab4213d51d8.
- Original-definition **reflection-twist certificate** over 24 even-r/odd-n pairs (r=2,4,6,8,10,12 and n=3,5,7,9) PASS, including both CDC adjacency and invariant centre signatures; three damaged-input controls rejected; source SHA256 975a50dc26b6601c94e0ede39a4979b571f2b73ac5f49d3fce74fef0713c9f3c.
- Independently generated **all predicted group actions** over 12 even-r/odd-n pairs (r=2,4,6,8; n=3,5,7), every graph automorphism checked on raw CDC adjacency, class parameters PASS, three damaged cases rejected; source SHA256 fce2a2071a93e13286ca16cc0c2fd25447d3a1b880345b77c8f23583c3156311.
- A different NetworkX 3.6.1 VF2 enumeration COMPLETED for (r,n)=(2,3),(2,5),(2,7),(4,3), confirming group orders 96,160,224,384 and strongly switching class size pairs [2,6],[2,10],[2,14],[4,12]. At (5,1),(7,1) with odd rn, complete automorphism counts 40,56. A (5,3) VF2 run **timed out**, and no exact full enumeration is claimed there.

The original portable source/checker/results have been retained in C-audit local research files for independent replay. Finite tests do NOT prove the universal theorem. No n=1 classification, no arbitrary disconnected-bases classification and no general TF-cycle conjecture resolution is claimed by this note.

**Reviewer requirements:** Recheck r-generalized definitions in source Remark6.2; validate centre bundle CRT and the exceptional necessity n>=3; audit the strong-switch count and conjugacy; audit the direct reflection-twist nonisomorphism invariant; and apply source Theorem4.6 only under its connected CDC hypotheses. Search for older equivalent results. Until then, this is a correct-looking **written theorem candidate** rather than an independently accepted new result. No modification of main/coordination/other workers, no force push, PR, author contact, paper submission, or announcement of historical firstness.
