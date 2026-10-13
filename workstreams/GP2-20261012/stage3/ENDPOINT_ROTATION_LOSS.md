# Endpoint-supported rotation loss, with a bridge constraint

GP2-20261012, 2026-10-13. All-alphabet written theorem. The statements
below add a support-dependent constraint; they do not improve the current
uniform endpoint for lambda_4. They apply to strict window codes, and to
original Kautz GP sets only after the accepted strict-window repair.

## 1. Exact endpoint obstruction

Let A be a finite nonempty alphabet, mu any probability distribution on A
(zero weights allowed), and C a strict subset of A^4. Thus every word of
length eight has at most two selected occurrences in its five windows.
Put p=mu^4(C). Let P and Q be respectively the first- and last-letter
supports of C, and partition A into

    L=P\Q, R=Q\P, H=P intersection Q, N=A\(P union Q).

Write their masses as l,r,h,n, respectively, so l+r+h+n=1, and put
u=l+h=mu(P), v=r+h=mu(Q).

For four independent letters placed in a directed cycle, let F be the
probability that none of the four cyclic edges has its first letter in Q
and its second in P. Then

    F = 1-4uv+4uvh+2u^2 v^2-4uvh^2+h^4.                 (1)

Let delta denote the accepted constant

    delta=1/[27(1+(3+2sqrt(2))^(1/3))^3].

**Theorem 1.** For all the alphabets, distributions and strict codes above,

    1-4p >= F+delta h^4.                                (2)

In particular one may replace delta by the rational 125/74088. Together
with the previously proved global trace inequality this gives

    1-4p >= max{delta, F+delta h^4}.                     (3)

There is no claim that the right side has a uniformly larger minimum than
delta. In fact l=r=n=0 leaves h=1 and exactly the old constant.

**Proof of (1).** Label the four cyclic edge events Q->P. Each has
probability uv. Four adjacent pairs of edge events have probability uvh;
the two opposite pairs have probability u^2 v^2. Each of the four
three-edge intersections has probability uvh^2, and the four-edge
intersection has probability h^4. Inclusion-exclusion for avoiding their
union gives (1). Coordinates are independent draws, not required to have
different values. Thus repeated letters cause no exceptional cases.

**Proof of (2).** If a rotation of abcd belongs to C, its last letter is
in Q and the next cyclic letter (its first letter) is in P. Thus every
tuple counted by F has an empty selected rotation orbit.

Every strict code has at most one selected rotation position, counting
positions even for periodic words: two selected positions would produce
three selected windows at starts 0,j,4 in a periodic eight-letter word.
The empty-orbit probability is consequently exactly 1-4p.

When h>0, restrict C to H^4 and use the conditional letter distribution
mu/h on H. This is again a strict code. The accepted reciprocal trace
theorem gives an empty-orbit probability at least delta in that restricted
alphabet, contributing at least delta h^4 in the original probability
space. An H^4 tuple has all four cyclic edges in Q->P, so this contribution
is disjoint from F. If h=0 its contribution is zero, with no conditional
distribution needed. Adding proves (2); (3) also uses the global trace
theorem. QED.

## 2. A nonnegative form and the bridge coupling

The exact obstruction also has the following nonnegative expansion:

    F = l^4+r^4
        +4n[l^3+r^3+l^2 r+lr^2+h(l^2+r^2+lr)]
        +n^2[6(l^2+r^2)+8lr+8h(l+r)+2h^2]
        +4n^3(l+r+h)+n^4.                              (4)

This follows either by substituting 1=l+r+h+n in (1), or by grouping the
256 cyclic four-letter type strings in {L,R,H,N}^4 by their type counts.
The exact coefficient table is in the certificate and is independently
reconstructed by the checker. Hence F>=l^4+r^4, with equality when n=0.
For n=0 there is also a direct explanation: from R a cycle avoiding Q->P
can only move to R; from H it must move to R. Any other avoiding cycle
must therefore consist entirely of L.

Let b(C), a(C), d(C), i(s), o(s) have the meanings in
`BRIDGE_DELETION_FORMULA.md`: active-triple mass, selected-adjacency
probability, exact optimal deletion cost, and the two free-letter masses.

**Theorem 2.** Every active triple s satisfies

    i(s)<=l, o(s)<=r,       b(C)<=uv,
    a(C)<=lr b(C)<=lr uv<=1/16,
    d(C)<=b(C)min{l,r},     d(C)^2<=b(C)a(C).             (5)

Define, for 0<=a<=1/16,

    q(a)=[1-sqrt(1-4sqrt(a))]/2.

Then another uniform, support-free form of the bridge penalty is

    1-4p >= 2 q(a(C))^4.                               (6)

Its coefficient is not claimed sharp for actual strict codes.

**Proof.** In a selected adjacency abcd,bcde, the letter a cannot be the
last letter of any selected word: such a word would give selected starts
0,3,4. Since a is the first letter of abcd, a lies in L. In the same way
e lies in R, using starts 0,1,4 if a selected word began with e. This
reasoning counts occurrences and does not assume distinct words.

For an active triple bcd, its first letter b is in P because bcde is
selected, and its last letter d is in Q because abcd is selected.
Therefore the active triples lie in P x A x Q and have mass at most uv.
The pointwise free-letter bounds and the exact bridge identities give (5),
except its last numerical bound. For that bound, uv<=(1-l)(1-r) and
l(1-l)r(1-r)<=1/16. The exact deletion and Cauchy assertions are the
previously proved bridge theorem, applied without enlarging C.

For (6), put t=lr and x=sqrt(t). The mass constraint l+r<=1 implies
0<=x<=1/2. By (5) and l+r>=2sqrt(lr),

    a(C) <= t(1-l)(1-r) <= x^2(1-x)^2.

The function x(1-x) is increasing on [0,1/2], so x>=q(a(C)). Finally

    1-4p >= F >= l^4+r^4 >= 2l^2 r^2 = 2x^4
           >= 2q(a(C))^4.

All divisions and square roots are justified on the displayed closed
intervals. Zero-weight supports are combinatorial supports; no positivity
of the weights of their individual letters has been assumed. QED.

These intrinsic support bounds supplement the 10/6/3 letter-type bounds;
they require no choice of completion labels. They cover the adjacency
branch but vanish when a(C)=0. Closing the global problem still requires
a stronger inequality in the independent or small-bridge regime.

## 3. Verification and provenance

`verify_sampling_endpoint.py` checks (1) and (4) by a complete type-polynomial
coefficient comparison, evaluates (2) with the rational constant on exact
strict fixtures, reconstructs a,b,d from literal words, and checks the
bridge inequalities without floating arithmetic. The inverse in (6) is
tested through its equivalent monotone squared-polynomial steps; decimal
root evaluation is not used as proof. The companion sampling theorem,
raw original Kautz BFS and damaged-input controls share the same checker.

The universal proof is above; finite fixtures are semantic checks. An
independent AI mathematical review is recorded separately. No Lean proof,
human peer review or historical-priority certification is asserted.
Inclusion-exclusion, Cauchy and conditioning are standard tools. The
endpoint lemma comes from the inherited workstream note
`../global_upper/ENDPOINT_SUPPORT_AND_INDEPENDENT_CODES.md`.

The original source remains [arXiv:2604.15909](https://arxiv.org/abs/2604.15909),
Problem 5.2, and the broader prior-source limits are recorded in
`../recovery_review/literature/LATEST_PRIMARY_SOURCE_CHECK.md`. On
2026-10-13 the directly retrieved official records still displayed v1
(2026-04-17) and the survey [2501.19385v5](https://arxiv.org/abs/2501.19385)
(2026-08-16). This is version verification, not a complete novelty search.

The accepted numerical interval is unchanged:

    0.224808115216882691... <= lambda_4 <= 0.249578038101911868... .
