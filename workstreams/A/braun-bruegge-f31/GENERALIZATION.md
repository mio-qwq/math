# Strict pairwise majorization for any number of centered binomial rows

**Source context:** Braun–Bruegge, *Journal of Integer Sequences* 26 (2023), Proposition 22 gives a product-of-binomial-rows count for multi-path graphs. Their Conjecture 31 concerns three same-parity rows. This note proves a stronger **scalar t-row statement** for every t>=3; the t=3 case recovers Conjecture 31. Historical novelty is NOT certified. This is not a proof of the mixed-parity or global facet-maximization conjectures.

For a vector m=(m_1,...,m_t) of positive integers sharing parity, define

    H(m)= sum_{s in Z} product_{i=1}^t B_{m_i}(s),

where B_m(s)=C(m,(m+s)/2) if m+s is even and |s|<=m, and zero otherwise. This is exactly the scalar function F of Proposition 22 for a sorted vector, since substituting s=2j-min(m_i) gives its formula.

## Theorem (strict outward two-unit transfer)

If t>=3, p>=q>=3, and the other t-2 row sizes r_1,...,r_{t-2} are positive integers of the same parity as p,q, then

    H(p+2,q-2,r_1,...,r_{t-2}) > H(p,q,r_1,...,r_{t-2}).

If t=2, the corresponding transfer is always an equality (Vandermonde).

**Proof.** Let D(s)=B_{p+2}(s)B_{q-2}(s)-B_p(s)B_q(s) and W(s)=product_i B_{r_i}(s). By Vandermonde, sum_s D(s)=0. For |s|<=q-2 in the common parity class, the sign of D(s) is the sign of

    q(p+2)-(p+q+1)s^2.

At |s|=q, D(s)<0; outside this finite range D(s)=0. Thus D(s) is nonnegative near the center and nonpositive past a single threshold in |s|. Every factor B_{r_i}(s) is even and nonincreasing in |s|, hence W(s) is also even and nonincreasing. Subtracting an intermediate threshold value W_* from W, the summands D(s)(W(s)-W_*) are all nonnegative, so sum_s D(s)W(s)>=0.

For *strictness*, take s_0=0 when q is even and s_0=1 when q is odd. At this central index, D(s_0)>0 (for odd q the relevant numerator equals (q-1)(p+1)>0), while D(q)<0. Every r_i has B_{r_i}(s_0)>0 and B_{r_i}(s_0)>B_{r_i}(q) because s_0<q, including the case r_i<q where the latter value is zero. As t>=3 there is at least one unchanged row, hence W(s_0)>W(q). The single-sign-change argument is therefore strict; sum_s D(s)W(s)>0. For t=2, W=1 and sum D=0. QED.

## Corollary (unique fixed-parity maximizer)

Fix t>=3, the sum S, and one of the two common parities epsilon. Let d=1 if all entries are odd, and d=2 if all entries are even. Assume S>=td and S has the required parity. Among all positive same-parity t-vectors with sum S, the unique maximizer of H up to permutation is

    (S-(t-1)d, d, ..., d).

Indeed, sort the vector, and whenever a nonlargest entry q>d transfer two units from it to the largest entry p. The row sizes remain positive and parity-compatible, and the theorem strictly increases H at every step. Iteration terminates at the displayed vector. The all-odd and all-even parity classes are *separate*: when t and S are even both classes can be feasible, and this theorem deliberately does not compare their two maxima. The odd maximum equals 2*C(S-t+1,(S-t+2)/2); the even maximum is 2^(t-1)*C(S-2t+2,(S-2t+2)/2)+2*C(S-2t+2,(S-2t+4)/2), when the respective class is feasible.

The scalar theorem should not be reinterpreted naively as a simple-graph extremal result when multiple path lengths are one, since their graph construction then has repeated direct edges (a multigraph issue). All statements above are solely about the binomial sum from the original definition.

Exact bounded regression: code/verify_generalization.py, with direct binary-word counts and all common-parity vectors of bounded small total size; it is NOT a formal proof of the infinite theorem.
