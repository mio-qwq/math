# Residue upper bound for the original circulant conjecture

Source: Chandran et al., *The general position number of digraphs*, arXiv:2604.15909v1, §3.1, unnumbered conjecture after Theorem 3.3.

Let n=qd+a, q>=1 and 2<=a<=d-1. Put M=max(a,floor(d/a)+1). The source's two constructions give gp>=M. The following gives the matching upper bound.

For positive integers A,B, ceil(A/d)+ceil(B/d)>ceil((A+B)/d) holds exactly when A and B have nonzero residues modulo d whose sum is at most d. This follows by writing A=kd+r and B=ld+s with residues in 0,...,d-1.

Take any general-position set of size at least three and translate it to contain 0. Order its other vertices as 0<x1<...<xm<n. Distances are ceil(((v-u) mod n)/d). Set ri=xi mod d when nonzero, and ri=d otherwise.

For i<j, absence of a shortest 0-to-xj path through xi implies 0<ri<rj<=d: xi cannot have residue zero; if xj has nonzero residue, the ceiling criterion says that its residue must exceed that of xi; a final zero residue is represented by d. Thus the compressed residues are all distinct and strictly increasing.

Consider the three clockwise gaps xi, xj-xi, n-xj. Every pair of consecutive gaps corresponds to one of the three cyclic ordered triples on {0,xi,xj}. General position forces all three gaps to have nonzero residues modulo d and forces each pair of residues to have sum at most d. The first two gap residues are ri and rj-ri. If rj=a the third gap has zero residue, impossible. If rj>a its residue is d+a-rj (also valid for rj=d). Pairing it with each of the first two yields ri>=a and rj-ri>=a.

Now if rm<a, the set has at most a elements including 0. Otherwise rm>a, and each preceding residue is >=a. Applying the preceding argument to every successive pair of positive residues gives a minimum gap a between all successive elements of 0,r1,...,rm. Since rm<=d, the set has at most floor(d/a)+1 elements. A two-element set already satisfies the bound.

Hence gp<=M; the source's constructions prove equality. Only necessary cyclic-triple constraints are used, so no sufficiency claim about residue compression, nor any assumption excluding reverse orientations, is needed. The proof works for q=1 as well as q>=2.

Status: mathematical derivation independently matched the parent agent's derivation; direct BFS validation script tests the necessary residue constraints on all eligible anchored triples through n=90. Validation is evidence checking the argument, not a substitute for proof. No counterexample found.
