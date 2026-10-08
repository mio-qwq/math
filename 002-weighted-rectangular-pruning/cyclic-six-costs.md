# Independent pair costs on two induced six-cycles

Research note, 8 October 2026.

This note proves the sharp coefficient-one cover and pruning bounds for
simultaneously translation-invariant independent costs on a pair of induced
six-cycles. Neither coordinate relation is chordal bipartite. It also gives
the exact weighted augmented-cover optimum as the minimum of nine explicit
expressions, without any local-cost assumption. A positive one-parameter
family satisfies the local assumptions and has no common dominating
coordinate-product system. Translation-invariant partial original families
are included in the bound. General asymmetric costs remain unresolved here.

These are complete written arguments. No Lean formalization, executable
checker, numerical search or historical originality clearance is asserted.
The construction continues the proposed test [R002.3](../RESEARCH_QUESTIONS.md)
and uses the [actual conflict/coverage model](paper.md). The
[chordal theorem](chordal-bipartite-costs.md) does not cover these two relations.

## 1. Actual graph and assumptions

All indices below lie in the additive group T=Z/3Z. Set

    P=I=S=J=T,   E=F={(t,t),(t,t+1): t in T}.

Each coordinate graph is a connected six-cycle. Initially let R=P x J and
C=I x S. A member R(p,j) conflicts with C(i,s) when

    i=p+epsilon,   j=s+eta,   epsilon,eta in {0,1}.

The actual cross-corner families H=P x S and Z=I x J are full, since every
one of their coordinates has a conflict witness. The augmented graph has
left side R disjoint-union Z_L and right side C disjoint-union Z_R, with
exactly these edges:

* R(p,j)--C(i,s) at each conflict;
* R(p,j)--Z_R(i,j) for i=p or p+1;
* Z_L(i,j)--C(i,s) for j=s or s+1.

There is no Z_L--Z_R edge. The 36 vertices have 36 conflict edges and
18 edges of each coverage type, hence 72 edges in total. H is a budget
family, not an additional vertex family.

Take arbitrary nonnegative orbit costs X_d,Y_d,H_d,Z_d and assign

    x_pj=X_(j-p),   y_is=Y_(s-i),
    h_ps=H_(s-p),   z_ij=Z_(j-i).                         (1)

Both tagged copies of a Z corner cost z_ij. The same t is added to all four
coordinates in the symmetry action; independent coordinate translations
are not assumed. Put

    X=sum_d X_d, Y=sum_d Y_d, H=sum_d H_d, Z=sum_d Z_d.

The corresponding actual family totals are 3X,3Y,3H,3Z. For the cover
bound we assume x_pj y_is <= h_ps z_ij at every actual conflict. Equivalently,
putting d=s-p, the twelve orbit representatives are

    X_(d+eta) Y_(d-epsilon) <= H_d Z_(d+eta-epsilon).     (2)

Each represents three actual conflicts. The exact-optimum calculation in
Section 4 does not assume (2) and does not use H.

## 2. From twelve local inequalities to an aggregate inequality

Define, for each d,

    A_d=X_d Y_d, B_d=X_(d+1) Y_d,
    C_d=X_(d+1) Y_(d-1).

The two diagonal inequalities in (2) give

    H_d Z_d >= max(A_d,C_d).

The other two give

    H_d Z_(d+1) >= B_d,
    H_(d+1) Z_d >= B_d.

These account for all nine products H_d Z_k. Therefore

    H Z >= sum_d max(A_d,C_d) + 2 sum_d B_d.             (3)

Direct multiplication gives A_d C_d=B_d B_(d-1). Since all costs are
nonnegative,

    min(A_d,C_d) <= sqrt(B_d B_(d-1))
                 <= (B_d+B_(d-1))/2.

This includes every zero boundary and uses no division. Summing gives
sum min(A,C)<=sum B. Consequently (3) implies

    H Z >= sum_d(A_d+B_d+C_d) = X Y.                    (4)

The last equality holds because the three families exhaust all nine
ordered pairs of X and Y indices: their differences are 0,1,2. This
step is specific to T=Z/3Z and does not prove a longer-cycle statement.

## 3. Actual cover and pruning bounds, with sharp coefficient one

For nonnegative X,Y,H,Z satisfying XY<=HZ,

    min(X+Y,X+Z,Y+Z) <= H+Z.                            (5)

Here is a proof without a positivity assumption. If all three left sums
were strictly larger than H+Z, then X>H, Y>H and X+Y>H+Z. But

    XY-HZ=(X-H)(Y-H)+H(X+Y-H-Z)>0,

contrary to XY<=HZ. This also covers H=0 and Z=0.

Select the least expensive of the three actual covers

    R union C,   R union Z_L,   C union Z_R.             (6)

Every conflict or coverage edge meets the indicated selection. Their
costs are 3(X+Y),3(X+Z),3(Y+Z), so (4)--(5) prove

    cost(K) <= sum_actual H h + sum_actual Z z.          (7)

To transfer the result to pruning, let R',C' be unselected originals in
any augmented cover. They are conflict-free. A corner cannot be covered
by both a surviving R and a surviving C, since those originals would
conflict. In the cheapest tag completion, select Z_R precisely when a
surviving R covers it, and Z_L precisely when a surviving C covers it.
Let U be the actual corner set covered by neither. Nonnegative costs
allow removal of all other selected tags. The completed cover has cost

    deleted_original_cost + sum_actual Z z - sum_actual U z.  (8)

Conversely any conflict-free pair of survivor families has this actual
completion. Thus the augmented optimum equals sum_actual Z z plus the
minimum of deleted_original_cost-sum_actual U z. Equation (7) gives

    deleted_original_cost <= sum_actual H h + sum_actual U z. (9)

For full inputs, the three pruning choices associated to (6) are to
delete both original families, delete only R, or delete only C. In the
latter two cases U is empty because each actual corner has a surviving
neighbor. Their adjusted fees are 3(X+Y-Z),3X,3Y.

With all costs one, the nine edges R(p,j)--Z_R(p,j) and the nine edges
Z_L(i,j)--C(i,j) form a perfect matching. A cover must contain at least
one endpoint of each, so its cost is at least 18. Selecting R and C has
cost 18, equal to the H+Z budget. Equivalently the minimum adjusted fee
in (9) is 9, equal to the H budget. Coefficient one is therefore sharp
for both formulations even within this symmetry class.

For rational inputs, evaluating the three cover fees in (6) is an exact
finite construction. The proof needs no square-root computation in the
algorithm: square roots occurred only in the proof of feasibility.

## 4. Exact weighted optimum: nine expressions

For full inputs and arbitrary nonnegative X_d,Y_d,Z_d as in (1), without
the local inequalities, the augmented optimum is

    kappa = 3 min {
      X+Y, X+Z, Y+Z,
      X+Y+Z-Y_b-Z_(b-1)   (b in T),
      X+Y+Z-X_a-Z_(a+1)   (a in T)
    }.                                                   (10)

This is an exact value formula, not a list of all actual minimizing
vertex sets. Costs may be zero and expressions may coincide.

To prove it, first justify reduction to whole translation orbits.
Average any actual cover's vertex indicators over the three translations.
Its orbit values u on the left and v on the right lie in [0,1], obey
u+v>=1 on each quotient edge, and preserve total actual cost. At a
threshold theta in (0,1), select a left orbit if u>=theta and a right
orbit if v>1-theta. If neither endpoint were selected then u+v<1,
a contradiction. Threshold averaging gives each left orbit inclusion
probability u and each right orbit probability v. The average cover
cost is the original cost, so some threshold selects whole orbits at
no greater cost. Only finitely many threshold intervals occur. Every
quotient cover also lifts to an actual cover, at three times its orbit
cost. Hence the reduction is exact; it uses no solver assumption.

Index R orbits by a=j-p, C orbits by b=s-i, and Z orbits by c=j-i.
Every original pair of orbit indices conflicts: a-b=epsilon+eta can
be any element of T. Thus the quotient's original-conflict graph is
K_(3,3). Its other edges are

    R_a--Z_R,c for c=a or a-1;
    Z_L,c--C_b for c=b or b+1.                            (11)

Every quotient edge has an actual witness. Every cover of K_(3,3)
selects all R or all C: an omitted vertex on each side would leave
their edge uncovered.

If all R are selected, the remaining C--Z_L graph is a six-cycle.
Its inclusion-minimal covers are its two alternating sides and the
three complements of the opposite pairs (C_b,Z_L,b-1). Indeed, the
complements of inclusion-minimal covers are maximal independent sets.
A maximal independent set on a six-cycle either has three alternating
vertices or has two opposite vertices. Any other independent pair can
be extended, and no single vertex is maximal. These give respectively
fees Y,Z and Y+Z-Y_b-Z_(b-1).

If all C are selected, the remaining R--Z_R cycle gives fees X,Z and
X+Z-X_a-Z_(a+1). Nonnegative costs permit deletion of redundant selected
vertices, so an optimum has one of these inclusion-minimal forms.
Combining both cases proves exactly (10). The optimal adjusted pruning
fee is kappa-3Z by (8).

## 5. Positive examples outside common coordinate-product domination

Define common coordinate-product domination to mean positive families
r_p,b_j,a_i,c_s satisfying

    x_pj<=r_p b_j, y_is<=a_i c_s,
    r_p c_s<=h_ps, a_i b_j<=z_ij.                        (12)

For positive invariant tables in (1), such a system exists if and only if

    (max_d X_d)(max_d Y_d) <= (min_d H_d)(min_d Z_d).     (13)

For necessity, multiply each family of inequalities (12) around a
translation orbit and take cube roots. If r,b,a,c are the geometric
means of the corresponding coordinate families, then

    max X<=rb, max Y<=ac, rc<=min H, ab<=min Z.

Their product gives (13). For sufficiency, let x=max X, y=max Y,
z=min Z, and take the constant coordinate families

    r_p=1, b_j=x, a_i=z/x, c_s=xy/z.

They are positive, give rb=x, ac=y, ab=z, and give rc=xy/z<=min H.
Every inequality in (12) follows. No criterion for non-invariant
tables or zero-valued product domination is claimed by (13).

Now let M>1 and take

    X=(M,1,1), Y=(1,M,1), H=(M,M,M), Z=(1,1,M).          (14)

The three diagonal maxima max(A_d,C_d) are M,M,M^2, equal to H_d Z_d.
The B values are 1,M,M, each bounded by both designated off-diagonal
products in Section 2. Thus all twelve local constraints hold exactly.
But (max X)(max Y)=M^2>M=(min H)(min Z), so (12) is impossible.

For this family (10) gives

    kappa=6M+12,   sum_actual H h+sum_actual Z z=12M+6.  (15)

Indeed X=Y=Z=M+2. The first three scalar candidates in (10) equal
2M+4, and the six remaining candidates equal either 2M+5 or 3M+4,
so none is smaller. This is an exact positive-cost separation from
the explicitly defined domination model, on two nonchordal relations.
It is not a counterexample to the local-cost cover theorem.

## 6. Translation-invariant partial original families

The bound (7)--(9) also holds if R,C are unions of simultaneous
translation orbits and all actual original and corner costs are
invariant. Each original orbit has three coordinates. The actual H,Z
families are invariant: translate a conflict witness in either direction.

Pad missing original and corner orbits by zero. All padded tables
retain (1). A padded conflict between two actual originals has actual
H and Z witnesses and preserves its local inequality. Every other
original product is zero, so its local inequality holds. The padded
H+Z total equals the actual total.

Apply the full theorem, then restrict the selected cover to actual
originals and actual Z tags. The actual augmented graph is the induced
subgraph on these vertices; every actual edge remains covered and the
cost cannot increase. Remove selected isolated vertices. An initially
conflict-free actual original is isolated even in the augmented graph:
if it covered an actual corner, the opposite original witnessing that
corner would conflict with it. Hence every initially conflict-free
original is retained. Recomplete tags using actual surviving coverage,
as in (8), to obtain (9) with its actual U. Empty inputs and zeros are
included. Padded survivors are never used as actual corner witnesses.

Arbitrary partial patterns need not be invariant. Padding such a
pattern generally breaks (1), so this proof does not cover them.
The exact nine-expression formula (10) is asserted for full inputs;
it is not an unqualified formula for a partial actual graph.

## 7. A precise remaining gap

Neither relation has the nested-neighborhood removal step used in the
chordal theorem. A naive attempt to reuse its two-pivot suffix lift
already has a positive statewise deficit. With nonnegative B0,B1,w,
S=B0+B1>=w, the virtual suffix cost for a deleted second pivot is
(B1-w)_+. If the old survivor state keeps the first pivot and deletes
the second, retaining those decisions costs B1 at the new corner;
deleting both costs S-w. Their best adjusted fee exceeds the virtual
cost by exactly

    min(B1,S-w)-(B1-w)_+=min(B0,B1,w,S-w).                (16)

If w<=B1, the difference is min(w,B0); if w>B1, it is min(B1,S-w).
These give (16), including zero boundaries. At B0=B1=w=1 the gap is 1.
The two old neighborhoods are incomparable, so restoring the deleted
pivot can conflict with an old survivor.

This deficit concerns one attempted statewise lift. It is not a
counterexample to the general six-cycle theorem: old uncovered profit,
residual slack, another survivor state or the reverse pooling order
may compensate for it. The unresolved task is to control these coupled
choices for all asymmetric independent costs, or to give exact local
data together with a true augmented-cover lower bound above H+Z.
The symmetry theorem and formula above settle a specified portion of
that proposed research question; neither proves its general form nor
establishes that an equivalent question is globally open.
