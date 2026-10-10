# Braun–Bruegge Conjecture 31 — exact scalar proof

Source: Benjamin Braun and Kaitlin Bruegge, *Facets of Symmetric Edge Polytopes for Graphs with Few Edges*, Journal of Integer Sequences 26 (2023), Article 23.7.2, Proposition 22 (p.12) and Conjecture 31 (p.24), https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf . Checked 2026-10-10. This proves the scalar conjecture, NOT the general polytope facet-maximization conjectures. Historical originality and external acceptance are not certified.

For positive same-parity integers a>=b>=c define

    F(a,b,c) = sum_{j=0}^c C(c,j) C(b,(b-c)/2+j) C(a,(a-c)/2+j).

Write B_m(t)=C(m,(m+t)/2) when |t|<=m and m+t even, and zero otherwise. For t=2j-c, the definition becomes the symmetric integer sum

    T(a,b,c) = sum_{t in Z} B_a(t) B_b(t) B_c(t) = F(a,b,c).

**Transfer lemma.** For positive same-parity p>=q>=3 and r>=1,

    T(p,q,r) <= T(p+2,q-2,r).

**Proof.** Set D(t)=B_{p+2}(t)B_{q-2}(t)-B_p(t)B_q(t). The unweighted total sum_t D(t) is zero by Vandermonde: sum_t B_p(t)B_q(t)=C(p+q,(p+q)/2), unchanged by (p,q)->(p+2,q-2). For parity-compatible |t|<=q-2,

    D(t)/(B_p(t) B_q(t))
      = (p-q+2)[q(p+2)-(p+q+1)t^2]
        / [q(q-1)((p+2)^2-t^2)].

The denominator is strictly positive, and the sole sign-dependent numerator factor decreases as |t| grows. At |t|=q the new q-2 row vanishes, giving D(t)<0, and beyond q both products vanish. Thus D is nonnegative in a central range, nonpositive outside, and changes sign at most once. Also B_r(t) is even and nonincreasing as |t| grows: B_r(t+2)/B_r(t)=(r-t)/(r+t+2) <=1 where nonzero. Choose any w_* between its values at the last nonnegative and first nonpositive D-shell. Termwise D(t)(B_r(t)-w_*)>=0. Consequently

    T(p+2,q-2,r)-T(p,q,r)
     = sum_t D(t)B_r(t)
     = sum_t D(t)(B_r(t)-w_*) >= 0.

This proves the lemma, even when r>q. The derivation uses only finite integer sums; no large-n induction or numerical approximation.

**Conjecture 31 transfer assertions.** In the original allowed domain a>=b>=c>=3, apply the lemma to (p,q,r)=(a,c,b), using symmetry, to obtain F(a,b,c)<=F(a+2,b,c-2). Apply to (a,b,c) to get F(a,b,c)<=F(a+2,b-2,c). In particular both hold when the author's final sorted-order condition is satisfied.

**Fixed-sum maximum.** Let a+b+c=n+1. If n is even (n>=4), all three entries are odd, since they have a common parity and their sum is odd. Repeated transfer from c into a until c=1, then from b into a until b=1, proves the maximum is attained at (n-1,1,1). If n is odd (n>=5), all three entries must be even, and the same argument terminates at (n-3,2,2). Each step decreases a positive entry by 2 only when it is at least 3. Symmetry handles any temporary reordering. Therefore the conclusion includes terminal rows of size 1 and 2.

**Erratum candidate, separate from the proof.** In the expanded illustrative inequality after Conjecture 31, the final lower binomial index on the right omits +2. It should be (a-c)/2+2+j upon changing (a,b,c) to (a+2,b,c-2). With (a,b,c)=(5,5,5), formal F gives 2252 <= 2310, whereas the printed expansion gives 1020. The formal conjecture itself remains correct.

**Validation and limits.** A standard-library checker under code/verify_braun_f31.py reconstructs both binomial definitions and tests all common-parity triples through sum 45, both transfers, the fixed-sum maxima, and the identified bad expansion. Its finite output only checks the stated general proof. No Lean compilation or independent ROOT acceptance is claimed. Bounded later-source screening including Mori–Mori–Ohsugi (2025) found no same-scope proof, but does not establish novelty. This is a reconstruction in a new runtime; prior signed local archive is presently inaccessible.
