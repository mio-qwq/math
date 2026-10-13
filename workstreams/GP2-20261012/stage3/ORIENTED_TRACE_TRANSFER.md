# Quartic trace transfer and two exact oriented counterexamples

GP2-20261012, 2026-10-13. This note closes the proposed `2X<=T+L`
route negatively and also refutes the proposed scalar coefficient `1/5`.
Neither the accepted Ka4 bound nor its proof is changed. It gives a uniform
structural reason not to keep enlarging the same oriented-matrix search.
All counts below are integers, not solver optima. No independent AI review,
Lean formalization, sharp scalar constant or historical priority is claimed.

For an entrywise nonnegative real square matrix M retain

    T=tr((MM^t)^2), L=tr(M^4),
    X=tr(M^3 M^t), Y=tr(M^2(M^t)^2),
    R4=tr((M+M^t)^4)=2L+8X+4Y+2T.

## 1. A 46-vertex zero-one counterexample to the candidate

Let Q be the nonzero quadratic residues modulo 23, and let A be the
23-by-23 matrix `A_uv=1{v-u in Q}`. It has zero diagonal and no digons:
Q and -Q partition the nonzero residues, since -1 is not a square modulo
this prime. Let

    J = [[1,1],[0,1]],
    M = J tensor A = [[A,A],[0,A]].

Although J has diagonal ones, M is a **zero-one oriented matrix** of order
46. Even between matching indices of the two copies there is no arc,
because A has zero diagonal. There are no reverse cross-copy arcs.

Direct integer products and a separate expansion of all `46^4=4,477,456`
ordered quadruples give

    (T(A),L(A),X(A),Y(A))=(15433,15180,13915,15433),
    (T(M),L(M),X(M),Y(M))=(108031,30360,69575,92598).

These agree with trace multiplicativity under the tensor product:
the four factors for J are respectively 7,2,5,6. Consequently

    T(M)+L(M)-2X(M) = -759 < 0.                       (1)

This is an exact finite refutation of the all-order candidate in
`ORIENTED_FIFTH_REDUCTION.md`. The previously exhaustive order-at-most-five
checks remain true but cannot support the candidate beyond their stated
finite range. In particular, seeking a nonnegative flag decomposition of
that universal candidate is now an invalid target.

The candidate was only a sufficient route to a `1/5` reciprocal trace
coefficient. Failure of (1) alone would not refute that weaker coefficient;
the next construction does so separately.

## 2. A binary Cayley counterexample to the coefficient 1/5

Use the finite abelian group `G=Z_7 x Z_151`, in lexicographic order
`(i,j) -> 151i+j`. Let Q be the 75 nonzero quadratic residues modulo 151,
written increasingly as `q_0,...,q_74`, and set

    B={q_0,q_5,...,q_70}
     ={1,9,18,25,36,42,49,62,74,84,91,99,116,125,138},
    S=({0,4} x Q) union ({1} x B).

Select the arcs `v -> v+s` for s in S. This gives a zero-one matrix M
of order 1057 and outdegree 165. It has no loops because 0 is not in S.
It has no digons because the first coordinates 1 and 4 have no opposite
coordinates 6 and 3 in S, while Q intersect -Q is empty in coordinate 0.

Write `c(t)=#{(s_1,s_2) in S^2:s_1+s_2=t}`. Translation invariance and
commutativity give

    T=Y=|G| sum_t c(t)^2,
    L=|G| sum_t c(t)c(-t),
    X=|G| sum_(s,t in S) c(s-t).                       (2)

Here the equality T=Y is justified directly: the group-shift permutation
matrices commute with each other and their transposes, so M is normal.
For R4 use S union -S in place of S in the first formula. The checker
also verifies (2) by a **different** computation: it reconstructs all
1057 outgoing-neighbor sets, counts common outgoing neighbors, counts
rooted two- and three-step walks, and reconstructs underlying neighbors.
It does not rely on an FFT, approximate eigenvalue or presumed normality.

Both computations yield

    T=Y=1592337733, L=229808712, X=1036917000,
    R4=18308979822,
    10(T+L)-R4=-87515372<0.

Thus

    2(T+L)/R4=1723885/8660823 < 1/5.                  (3)

All four indices include repetitions; no injective-count approximation is
used in (1)--(3). This is a counterexample even for a uniformly weighted
binary oriented kernel, not merely an arbitrary weighted matrix. It can
be made an off-diagonal reciprocal class of a three-level relation by
assigning levels 0 to its arcs, 1 to the reverse arcs, and 2 to all other
ordered pairs. This is not asserted to be the canonical level relation
of an extremal strict code, nor is it a Kautz GP set.

## 3. Uniform transfer theorem: orientation alone adds no quartic inequality

**Theorem.** For every four real coefficients alpha,beta,gamma,eta, the
following statements are equivalent:

1. `alpha T(M)+beta L(M)+gamma X(M)+eta Y(M)>=0` for every finite
   zero-one square matrix M with zero diagonal and no digons.
2. The same inequality holds for every finite entrywise nonnegative real
   square matrix B, with no restriction on its diagonal or digons.

The matrix order is unrestricted in both statements. Thus this theorem
does not identify a finite-order optimum. It concerns homogeneous linear
inequalities in these four **quartic** traces, not arbitrary inequalities
that retain labelled-edge support information.

**Proof.** The second statement immediately implies the first. For the
converse fix a nonnegative r-by-r matrix B. The zero matrix is trivial.
Otherwise choose a positive sigma such that

    p_ij=sigma B_ij,  p_ij+p_ji<=1,  2p_ii<=1;

for example `sigma=1/(2 max_ij B_ij)` works. For each N form r equal
blocks of N vertices. Independently for every unordered pair of distinct
vertices in blocks i,j, put an i-to-j arc with probability p_ij, put the
opposite arc with probability p_ji, or put neither with the remaining
probability. Within a single block use probability p_ii for each of the
two directions. The resulting n-by-n adjacency matrix A_N, n=rN, is
binary, zero-diagonal and has no digons in every realization.

Each of T,L,X,Y expands into a sum over four vertices of a product of
four distinct unordered-edge indicators whenever those four vertices are
distinct. For these tuples independence gives exactly the product of
the four appropriate p entries. The unrestricted block-index sum is
`sigma^4 F(B)/r^4`, for F any of T,L,X,Y. At most a fraction 6/n of tuples
have a repeated vertex, and each summand and its probability product is
in [0,1]. Therefore

    |E[F(A_N)/n^4]-sigma^4 F(B)/r^4| <= 6/n.          (4)

Changing one unordered-edge variable can change a normalized F by at
most 8/n^2: there are four edge positions and two possible assignments
of its endpoints, with at most n^2 choices of the other two vertices.
Expose the n(n-1)/2 independent variables. Conditional-expectation
increments have mean zero, are pairwise orthogonal, and have magnitude
at most 8/n^2. Hence

    Var(F(A_N)/n^4) <= 32/n^2.                        (5)

The mean-square Markov bound with tolerance n^(-1/4), followed by a union
bound for the four F's, gives failure probability at most 128/n^(3/2).
For every sufficiently large N there is therefore a deterministic
realization such that all four normalized counts differ from their
expectations by at most n^(-1/4). Choose one such realization for each
N. By (4), all four counts converge to `sigma^4 F(B)/r^4`.

Apply statement 1 to every chosen A_N, divide by n^4, take the limit and
divide by the positive scalar sigma^4/r^4. This proves statement 2. No
independence between the four trace counts was assumed. QED.

**Corollary (a ceiling, not a proved lower coefficient).** If a constant c
satisfies `2(T+L)>=c R4` for every finite binary oriented matrix, then

    c <= 2548/12899 = 0.19753469261183038... < 1/5.    (6)

To prove this, use the circulant nonnegative matrix on Z_7 with first row
`(5,1,0,0,5,0,0)`. Direct matrix products and four-index expansion give

    (T,L,X,Y,R4)=(31157,4515,20650,31157,361172),
    2(T+L)/R4=2548/12899.

The theorem transfers any proposed scalar inequality from binary oriented
matrices to this matrix. Its diagonal entries do not invalidate the
argument: the transfer proof simulates them by arcs between distinct
vertices of a block. The construction in Section 2 is a deterministic
binary finite witness to (3); the transfer theorem supplies the stronger
universal ceiling (6). Neither says that the ceiling is attainable or
that it is the sharp universal constant. The accepted coefficient
`3-2sqrt(2)` is below this ceiling and is unaffected.

## 4. Correction of the previous local-minimality inference

The previous note correctly exhausts **zero-one** orientations through
five vertices: its pair-interface bracket first becomes negative at order
five. However that does not imply a five-vertex minimum for weighted
matrices or for all useful flag certificates. Already the oriented matrix

    0 0 1 1
    0 0 2 0
    0 0 0 0
    0 1 0 0

has `(x,y,z,w)=(0,2,0,1)` at the interface (2,3) and bracket -1.
Adding either direct endpoint arc again leaves these two-step counts
unchanged. There cannot be a weighted counterexample on at most three
vertices: for distinct endpoints there is at most one intermediate vertex,
and the orientation hypothesis lets it contribute to at most one of
x,y,z,w. The bracket is then zero (x or y) or a nonnegative square (z or w).
For equal endpoints x=y=0 and the bracket is z^2+w^2.

Even product-weighted indicator kernels exhibit this four-vertex issue:
replace the entry 2 by 1, give letter weights (1,2,1,1)/5, and the actual
weighted matrix interface bracket is -1/625. Hence the old assertion that
any useful local-to-global certificate "must see at least five vertices"
was too broad and is withdrawn. The zero-one finite minimality statement
is retained at its correct scope.

## 5. Reproduction, literature and next mechanism

Run from the repository root:

```sh
python workstreams/GP2-20261012/stage3/verify_oriented_trace_transfer.py
python -O workstreams/GP2-20261012/stage3/verify_oriented_trace_transfer.py
```

The certificate binds construction parameters, exact integer counts,
reduced fractions and full regenerated matrix SHA256 values (ASCII rows
of 0/1 followed by LF). Six full-entry altered-input controls are rejected.
The actual logs, command metadata and hashes are recorded alongside it.
The universal transfer theorem is the written proof above, not a finite
simulation or a solver claim.

The Paley construction and random blow-up/concentration tools are classical;
no priority for those mechanisms or for the trace-counterexample application
is asserted. The bounded fresh source check on 2026-10-13 found that the
original public arXiv page still has only v1 (2026-04-17), whose Problem 5.2
asks for Kautz word lengths at least three. The survey is still v5
(2026-08-16), and its open-problem list still includes that question:

- https://arxiv.org/html/2604.15909v1 (Definition 2.1; Problem 5.2)
- https://arxiv.org/html/2501.19385v5 (Theorem 5.61; Section 6)

This is not an exhaustive search or proof that no later solution exists.
A Paley lecture-note URL was located but its body could not be fetched in
this run; it is not used as a proof source. The finite Paley witnesses are
reconstructed directly from modular squaring by the checker.

The accepted interval stays

    0.224808115216882691... <= lambda_4 <= 0.249578038101911868... .

The next core task is **mixed reciprocal classes coupled to the exact
10/6/3 hierarchy**, not a square/flag proof of the refuted candidate.
Because the universal quartic inequality cone is unchanged by orientation,
an improvement exploiting orientation must retain more labelled-support
structure or canonical strict-code compatibility than these four scalars.
