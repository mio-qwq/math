# A stronger universal empty-orbit bound from reciprocal trace configurations

GP2-20261012, 2026-10-13. Complete written candidate proof, pending independent
review when first drafted. The proof is for every finite alphabet and every
probability distribution. It does not optimize a fixed small alphabet or
assume independence of selected windows. No full Lean proof or historical
priority is claimed.

## 1. Statements and exact parameter scope

Let A be any finite nonempty alphabet, let mu be any probability distribution
on A, including zero weights, and let ell:A^2->{0,1,2} be arbitrary. For four
independent letters a,b,c,d with distribution mu, put

    E_ell = Pr[ell(ab)=ell(cd) and ell(bc)=ell(da)].

**Theorem 1.** With

    kappa = 3-2sqrt(2) = 1/(3+2sqrt(2)),
    delta = 1/[27(1+(3+2sqrt(2))^(1/3))^3],

one has

    E_ell >= delta >= 125/74088 > 1/729.                 (1)

The first constant is a somewhat stronger consequence of the proof than the
convenient rational certificate. It is not asserted optimal for arbitrary
three-valued relations or for canonical strict-code levels.

**Corollary 2.** Every strict four-window code C subset A^4 has product density

    mu^4(C) <= (1-delta)/4 <= 73963/296352 < 182/729.     (2)

Here strictness means at most two selected occurrences among the five windows
of every eight-letter word; repeated occurrences count separately.

**Corollary 3.** For the original directed Kautz graph Ka(m,4), with m the
number of letters and m>=3,

    gp(Ka(m,4)) <= floor(73963 m^4/296352) + 73m^3,
    beta <= lambda_4 <= (1-delta)/4 <= 73963/296352,

where beta is the independently checked weighted Jiggs lower endpoint in
the stage-one record. The sharper real coefficient can also be used in the
finite floor bound. Neither the exact finite formula nor the exact lambda_4
is established.

## 2. Six reciprocal classes and four eligible direction patterns

For i,j in {0,1,2}, define

    K_ij(x,y) = 1{ell(xy)=i and ell(yx)=j}.

Then K_ji(x,y)=K_ij(y,x). The nine kernels partition A^2.
For each diagonal class set r_ii=E K_ii(a,b). For i<j set
r_ij=E[K_ij(a,b)+K_ji(a,b)]. These are six nonnegative masses summing to one.
The diagonal kernels and the off-diagonal union kernels are symmetric.

For a diagonal class, require all four cross pairs (a,b),(a,d),(c,b),(c,d)
to lie in K_ii. This event implies E_ell. Its probability is the weighted
bipartite C4 count T(K_ii), at least r_ii^4 by Section 4.

Fix i<j and write K=K_ij, K^t=K_ji. Among tuples whose four cross pairs lie
in this unordered class, exactly four patterns imply the required two
equalities:

1. All four row-to-column pairs lie in K.
2. All four lie in K^t.
3. The diagonal row-to-column pairs lie in K and the other two in K^t.
4. The diagonal pairs lie in K^t and the other two in K.

The first two probabilities each equal T(K). The last two describe the
directed cycles a->b->c->d->a in K and K^t, so each equals L(K), the directed
C4 count. The four events are disjoint because K and K^t have disjoint
support. This statement remains true when letters repeat: impossible
direction patterns contribute zero, and all sums retain their multiplicities.

Events from different unordered classes, or a diagonal class, are disjoint
because the pair (a,b) alone determines its reciprocal class. They are only
a subset of E_ell, which can also use different unordered classes on different
cross pairs. Consequently

    E_ell >= sum_i T(K_ii) + sum_(i<j) 2[T(K_ij)+L(K_ij)].  (3)

The previous nine-kernel proof counted the first two patterns for each
off-diagonal class and omitted the two directed-cycle patterns. The gain
below uses their joint control; it does not assume L(K) itself is positive
by a fixed amount.

## 3. A matrix lemma with a self-contained Frobenius proof

For any entrywise nonnegative real square matrix M, put

    T=tr((MM^t)^2), L=tr(M^4),
    Y=tr(M^2(M^t)^2), X=tr(M^3 M^t), R=M+M^t.

All four scalars are nonnegative: T is a squared Frobenius norm, Y is
||M^2||_F^2, and L,X are sums of products of nonnegative entries.
For real matrices use <U,V>_F=tr(U^t V) and the elementary finite-sum
Cauchy inequality <U,V>_F^2<=||U||_F^2||V||_F^2.

The symmetric matrices U=MM^t and V=M^t M have squared norm T, and
<U,V>_F=Y by cyclic invariance of trace. Hence Y<=T.

Now set B=M^2+(M^t)^2 and D=MM^t+M^t M. They are symmetric and direct
expansion, cyclic trace and trace invariance under transpose give

    <B,D>_F=4X,
    ||B||_F^2=2(Y+L), ||D||_F^2=2(T+Y).

Therefore

    X^2 <= (Y+L)(T+Y)/4
         <= T(T+L)/2 <= (T+L)^2/2,
    X <= (T+L)/sqrt(2).                                 (4)

No division by T or T+L was used; zero matrices are included.
Expanding all sixteen terms of R^4 and grouping by cyclic order gives

    tr(R^4)=2L+8X+4Y+2T.

Using Y<=T, (4), and L>=0,

    tr(R^4) <= 2L+6T+4sqrt(2)(T+L)
              <= (6+4sqrt(2))(T+L).

It follows that

    2(T+L) >= (3-2sqrt(2)) tr(R^4).                     (5)

A completely rational weakening follows from 177/250>1/sqrt(2), verified
by (177/250)^2-1/2=79/62500>0. Replacing (4) by
X<=(177/250)(T+L) gives

    tr(R^4) <= (1458/125)(T+L),
    2(T+L) >= (125/729) tr(R^4).                        (6)

The entrywise nonnegativity hypothesis is material; arbitrary real matrices
can have L<0. The transpose and trace factors must not be replaced by
entrywise squares or by an unweighted adjacency transpose in the weighted
implementation.

## 4. Weighted C4 counts and the six-mass inequality

For a kernel K on A, use the real matrix

    M_xy=sqrt(mu(x)) K(x,y) sqrt(mu(y)).

Then T and L above are precisely the product-weight bipartite and directed
C4 counts. For off-diagonal reciprocal kernels, M^t represents K^t, and
R represents the symmetric union kernel S=K+K^t. Because S is symmetric,
tr(R^4)=T(S).

For every nonnegative kernel S of mean r, two finite-sum Cauchy inequalities
give

    T(S)=E_(a,c)[E_b S(a,b)S(c,b)]^2
        >= [E_b(E_a S(a,b))^2]^2 >= r^4.

Zero letter weights cause no difficulty. Thus (3),(5) imply

    E_ell >= sum_i r_ii^4 + kappa sum_(i<j) r_ij^4.     (7)

For any positive coefficients c_s and six nonnegative masses r_s summing to
one, weighted convexity of the fourth power gives

    sum_s c_s r_s^4 >= 1/(sum_s c_s^(-1/3))^3.

For completeness this follows by choosing
q_s=c_s^(-1/3)/Z, Z=sum c_s^(-1/3): Jensen applied to
sum q_s(r_s/q_s)^4 gives Z^3 sum c_s r_s^4>=1.
There are three coefficients one and three kappa, yielding delta in (1).

The rational version admits an exact polynomial certificate without roots.
Set c=(1,1,1,125/729,125/729,125/729) and
t=(5/42,5/42,5/42,3/14,3/14,3/14). Then sum t_s=1 and
c_s t_s^3=125/74088 for every s. The identity

    x^4-t^4-4t^3(x-t)=(x-t)^2(x^2+2xt+3t^2)

is nonnegative for x,t>=0. Multiply by c_s and sum, using sum r_s=sum t_s.
This proves sum c_s r_s^4>=125/74088 exactly. Since kappa>=125/729,
the sharper delta is at least that rational value as well.

## 5. From strict windows back to the original Kautz definition

For a strict code C, its ordered-pair digraph ab->cd has no three-edge walk:
one would concatenate four pairs and select windows at starts 0,2,4.
The greatest incoming walk length is therefore ell:A^2->{0,1,2}, and
every selected abcd satisfies ell(ab)<ell(cd).

Strictness also permits at most one selected rotation position among abcd,
bcda,cdab,dabc. Two such positions would give three selected occurrences
at 0,j,4 in the periodic eight-letter word, counting repeated words too.
On E_ell none of the four positions can be selected, since each relevant
strict comparison has equal levels. Rotation preserves the product
distribution, so 4 mu^4(C)<=1-E_ell. This and Theorem 1 prove (2).

Finally `../construction/STRICT_WINDOW_REPAIR.md` places a strict code
inside any original directed Ka(m,4) GP set by deleting at most 73m^3
vertices. Under uniform weights, |C| is an integer and is bounded by
floor(73963m^4/296352). Add the deleted vertices and pass to the previously
proved density limit. The original any-shortest-directed-path definition,
digons and valid adjacent-letter inequalities are handled by that inherited
repair theorem, not silently replaced by mutual visibility or full-shift
strictness at fixed m.

## 6. Provenance, validation and remaining mechanism

The original public source is Chandran et al., arXiv:2604.15909v1,
Problem 5.2. The August 16, 2026 survey arXiv:2501.19385v5 still lists the
general k>=3 Kautz question; this does not certify absence of all later work.
Rotation counting and comma-free split graphs have classical sources,
recorded in `../recovery_review/literature/LATEST_PRIMARY_SOURCE_CHECK.md`.
The generic matrix tools are ordinary finite-sum trace identities and
Cauchy inequalities. Their specific reciprocal-class application requires
a separate novelty search; no priority or global best-known claim is made.

The proof above, rather than finite matrix sampling, establishes all-parameter
scope. A standard-library exact checker reconstructs the four pattern events,
weighted matrix identities, Cauchy steps and rational polynomial certificate.
Negative controls reject altered constants, trace coefficients and matrix
bindings. Actual commands and logs are recorded beside it when executed.
This improvement is numerically modest; it does not make the upper endpoint
close to the lower construction or solve Ka4.

The next structural goal is a larger empty-orbit/forced-loss inequality
coupling these reciprocal classes with actual overlapping triple choices.
Improving a relaxed relation bound alone cannot be advertised as an exact
strict-code optimum. The full 10/6/3 hierarchy and all split interfaces
remain available for that coupling.
