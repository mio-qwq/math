# The next missing mechanism: mixed reciprocal classes

This is a mechanism analysis, not a new extremal-value claim. The accepted
trace theorem counts a particular subset G of the empty-orbit event E: the
four cross pairs (a,b),(a,d),(c,b),(c,d) must have the same unordered
reciprocal class. Within that class all four eligible direction patterns
are included. In particular, G is exactly the quantity summed in (3) of
`RECIPROCAL_TRACE_BOUND.md`; it is not the full E.

## 1. Literal deterministic omission

On four equally weighted letters use the level matrix

    2 0 2 2
    2 2 1 2
    2 2 2 0
    1 2 2 2.

The tuple (0,1,2,3) has ell(01)=ell(23)=0 and ell(12)=ell(30)=1,
so it lies in E. Its cross-pair reciprocal classes alternate between
{0,2} and {1,2}, so it is absent from G. Direct exact counting of all
256 ordered tuples, including repetitions, gives

    E=96/256=3/8, G=40/256=5/32, E-G=56/256=7/32.

All 56 omitted tuples are listed in `mixed_class_witness.json` and are
reconstructed by `verify_mixed_class_obstacle.py`. This is an arbitrary
level relation, not a strict-code construction or a conjectured optimizer.
It establishes concretely that substituting G=E is invalid.

## 2. A rigorous dense family with most configurations omitted

For each n, independently assign one of three colors, uniformly, to every
ordered pair of n letters; opposite directed edges are independent. Draw
four letters uniformly with replacement. On the event that they are all
distinct, the eight directed cross-pair colors are independent.

Among their 3^8 color assignments, 3^6 satisfy E: two independent equalities
are imposed. Only 15 satisfy G: three diagonal-class assignments, plus
four direction patterns for each of three off-diagonal unordered classes.
Thus the corresponding probabilities are exactly

    E*=1/9, G*=15/6561=5/2187, G*/E*=5/243.

The probability of a repeated letter is at most 6/n, by the union bound.
Therefore each expectation over random colorings differs from its displayed
limit by at most 6/n.

These limits are realizable along deterministic finite level arrays, not
merely expectations. Changing one ordered-edge color changes the empirical
E_n by at most 4/n^2: at most four positions can use that edge, and each
fixes two of the four tuple coordinates. G_n depends on at most eight
ordered edges, so its corresponding change is at most 8/n^2. Reveal the
n^2 independent colors one at a time. The conditional-expectation increments
have mean zero, are pairwise orthogonal, and have magnitude at most the
respective change bounds. Summing their variances gives

    Var(E_n)<=16/n^2, Var(G_n)<=64/n^2.

The mean-square Markov bound and a union bound show that both deviations
from their expectations are at most n^(-1/4) with probability tending to
one. Choose a coloring satisfying both bounds for every sufficiently large
n. The resulting deterministic sequence has E_n->1/9 and G_n->5/2187.

This does not prove that extremal strict-code canonical levels behave like
these random relations. It identifies how much the current relaxation can
discard and why tuning only its scalar trace multiplier is unlikely to
close the main density gap.

## 3. Exact full functional and the next analytic target

Let H_i(x,y)=1{ell(xy)=i}, and let M_i have entries
sqrt(mu(x))H_i(x,y)sqrt(mu(y)). Direct four-index expansion gives

    E_ell=sum_(i,j) tr(M_i M_j M_i M_j),
    sum_i M_i=u u^t, u_x=sqrt(mu(x)).

This full alternating-color trace functional is already present in the
stage-one matrix counterexample; it is not presented here as a new prior-free
representation. Unlike centered perturbation traces, every displayed term
for the nonnegative color matrices is nonnegative. But separate mean bounds
for these alternating terms are not established, and the already verified
E>=1/9 counterexample prevents replacing the unresolved optimization by a
naive color-independence argument.

The next proof step is an inequality retaining a controlled collection of
mixed-class terms, coupled to the actual pair-level and triple interfaces,
or a uniform weighted cover cost for forced orbits. A fixed-array cover and
a large finite relation search do not themselves supply that all-alphabet
bridge. The current new trace theorem remains valid independently of this
unfinished step.
