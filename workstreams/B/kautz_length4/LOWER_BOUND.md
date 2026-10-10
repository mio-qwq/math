# A universal length-four Kautz lower bound

For every integer m>=3,

    gp(Ka(m,4)) >= C(m,2)+3 C(m,3)+4 C(m,4)
                 = m(m-1)(m^2-2m+3)/6.

This is a constructive partial result on arXiv:2604.15909v1 Problem5.2, NOT an exact formula or a refuted conjecture. In fact it gives6 and22 at m=3,4, below the source's known optima7 and27. No novelty or independent-review claim. The length-three equality remains frozen separately.

## Construction

Order the m-letter alphabet. Select the disjoint union of:

- A: alternating words abab with a<b;
- V: words abcd with a>b, a>c, d>=b, d>c, and b!=c.

These conditions guarantee all adjacent letters differ. In V the only possible equality involving d and an interior letter is d=b>c. Equality a=d is permitted. A has C(m,2) words. The seven order patterns in V are

    2012, 2013, 2101, 2102, 2103, 3012, 3102.

Exactly three use three distinct letters and four use four letters. Each r-letter pattern has C(m,r) realizations. This proves the size formula.

## Original distances

For distinct length-four Kautz words u,v, the directed distance is the smallest s in{1,2,3} with suffix_(4-s)(u)=prefix_(4-s)(v), if such s exists, and4 otherwise. Shift and append the target suffix realizes every such overlap; in the absence of an overlap the last letter of u differs from the first of v, so appending all four target letters is legal. Shorter walks necessarily create the corresponding overlap. In particular diameter<=4.

## Independence

Suppose abcd is selected and bcde is selected.

- V to V would require d>=b from the first word and b>d from the second.
- A to V would require b>b, since the first word is abab.
- V to A would require b=d<c=e from the second word, contrary to d>c in the first.
- A to A would require simultaneously a<b and b<a.

Thus the set is independent, so selected-to-selected distances are at least2.

## Exclusion of the remaining geodesic triples

A three-selected-vertex geodesic could only have distance decomposition2+2=4. Write its middle word as v=abcd. Its first word must end in ab and its last word must begin with cd.

If v is in V, then a>b. No selected word can end in ab: a V-word ending in ab has b>a by its final-letter-versus-second-middle inequality, whereas an A-word ending in ab has a<b by its defining order. Both contradict a>b. Therefore v cannot have a selected predecessor at distance2.

If v is in A, then ab=cd. The first and last selected words consequently have a two-letter overlap, so their distance is at most2, rather than4. They cannot be endpoints of the supposed geodesic.

This excludes every original directed geodesic triple and proves the lower bound for all m. No numerical optimization is used in this proof.

## Discovery, limits and next decision

An exploratory rank-pattern model has44 binary pattern choices and12296 forbidden pattern combinations obtained from all short geodesic word patterns. SciPy/HiGHS reported optimality inside that RESTRICTED class for five objectives, producing this construction. That floating-point optimization is discovery only and supplies no original GP upper bound. The elementary inequalities above replace its validity judgment entirely.

The uniform order-pattern class already misses both source optima. A next viable exact-value route must allow letter-dependent choices or nonuniform alphabet blocks; repeating the same44-pattern optimization does not address the gap. The positive asymptotic density1/6 is a lower bound, not the maximum density. Preserve this partial result without relabeling it an exact solution.

## A second construction with better asymptotic density

Partition the alphabet into nonempty blocks of sizes a,b, a+b=m. Select all valid Kautz words with block patterns0010,0110,0111. Their counts are respectively a^2(a-1)b, a^2b(b-1), ab(b-1)^2. The total is

    ab[(m-1)^2-ab].

Every selected word starts in block0 and has its third letter in block1. Thus a two-letter suffix cannot equal a selected two-letter prefix. The three-letter suffix block patterns are010,110,111, whereas prefixes are001 or011; these lists are disjoint. Thus no selected ordered pair has distance1 or2. Its distance is3 or4, and any sum of two positive selected distances exceeds the diameter4. The construction is universally GP, independently of any solver.

For m>=4, putting q=ab gives q((m-1)^2-q), which increases for 0<=q<=floor(m^2/4), since 2floor(m^2/4)<=(m-1)^2. A balanced partition therefore maximizes this construction and yields

    gp(Ka(m,4)) >= floor(m^2/4)*[(m-1)^2-floor(m^2/4)].

Together with the preceding ordered construction, take the maximum of the two bounds. The balanced-block bound gives20,60,144 at m=4,5,6 and asymptotic density3/16 among the m(m-1)^3 vertices. This is still not an exact value; it remains below the known source value27 at m=4. The discovery program exhausts a small sufficient binary-window-code class, but no original upper bound is inferred from it.


## A stronger three-block construction and complete finite certificate

Partition the alphabet into three nonempty ordered blocks of sizes a,b,c. Select ALL valid Kautz words with one of these block patterns:

    0011 0012 0020 0211 0212 0220 0221 1011
    1012 1020 1120 1121 1220 1221 2220 2221

Every block word of length8 has at most TWO selected consecutive length4 windows. Here is an exact finite proof. A state is its last three block symbols. Give a transition weight1 precisely when its length4 window is listed above, and0 otherwise. Let F_t(s) be the maximum weight of a t-transition walk ending in state s, allowing any initial state. Then F_0(s)=0 and

    F_(t+1)(xyz) = max_{a in {0,1,2}} [F_t(axy) + 1_{axyz selected}].

The complete table below gives F_0 through F_5 for all27 states. Each entry is the maximum of exactly three listed predecessor entries plus a literal0/1, so the table is an exhaustive exact arithmetic certificate, not a numerical optimization result.

    state  F0 F1 F2 F3 F4 F5
    000    0  0  0  1  1  2
    001    0  0  0  1  1  2
    002    0  0  0  1  1  2
    010    0  0  0  1  1  2
    011    0  1  1  1  2  2
    012    0  1  1  1  2  2
    020    0  1  1  1  2  2
    021    0  0  0  1  1  2
    022    0  0  0  1  1  2
    100    0  0  0  1  1  2
    101    0  0  0  1  1  2
    102    0  0  0  1  1  2
    110    0  0  1  1  1  2
    111    0  0  1  1  1  2
    112    0  0  1  1  1  2
    120    0  1  1  2  2  2
    121    0  1  1  2  2  2
    122    0  0  1  1  1  2
    200    0  0  1  1  2  2
    201    0  0  1  1  2  2
    202    0  0  1  1  2  2
    210    0  0  1  1  2  2
    211    0  1  1  1  2  2
    212    0  1  1  1  2  2
    220    0  1  1  2  2  2
    221    0  1  1  2  2  2
    222    0  0  0  1  1  1

In particular max F_5=2. A directed geodesic in Ka(m,4) has at most4 edges and hence at most5 consecutive windows in a letter word of length at most8. Its block word can be extended to length8 arbitrarily. Thus three selected vertices on that geodesic would contradict the certified bound. This proves the construction universally, including repeated letters and selected adjacent vertices. No assumption about independence or distinct original letters is needed.

Its size is the sum over the16 displayed patterns p of

    n_(p0) product_{i=1..3} (n_(pi) - 1_{pi=p_(i-1)}),

because only the immediately preceding letter is forbidden. When b=c this simplifies to

    b[a^3+4a^2 b-3a^2+8ab^2-9ab+2a+3b^3-4b^2+b].

In particular, for EVERY integer q>=1, choosing (a,b,c)=(q,2q,2q) gives

    gp(Ka(5q,4)) >= 130q^4 - 74q^3 + 8q^2.

For arbitrary growing m, choose block sizes differing from(m/5,2m/5,2m/5) by bounded rounding errors. The lower asymptotic density is26/125, improving the previous3/16. These are constructive lower bounds, not exact maxima or a new counterexample count.

Verification: verify_three_blocks.py checks every entry of the forward certificate, separately uses the reversed-direction dynamic program, and enumerates all6561 length8 block words. It also independently rebuilds original graphs by ordered-pair adjacency, BFS and every selected ordered triple for four small block-size choices. Two deliberately damaged certificates must fail. Discovery's floating-point optimizer is not imported or required.
