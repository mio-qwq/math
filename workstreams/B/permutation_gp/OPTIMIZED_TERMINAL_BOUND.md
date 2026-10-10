# Optimizing the already-accepted terminal-alphabet construction

This is a quantitative extension of B's frozen original counterexample, not a second conjecture refutation. The accepted PROOF.md and certificate remain byte-identical. Independent review of this extension and historical novelty are pending.

Let k>=3, d>=2k, N=d+k. For every integer 1<=t<=d+1, choose disjoint alphabets T,C of sizes t,N-t and take all injective words with the first k-1 symbols in C and the last symbol in T. The same lower-distance argument and the same k-1 fresh buffer symbols from outside the two endpoint words prove

    k <= dist(u,v) <= 2k-1

for distinct selected words, regardless of t. Thus this is an original-definition general-position set with

    F(t)=t (N-t)_(k-1).

The range t<=d+1 ensures at least k-1 available prefix symbols. Fresh buffers may belong to either alphabet; they are only required to avoid the two endpoint words. The buffer availability follows from N>=3k, exactly as in the frozen proof.

## Exact optimum within this construction

For 1<=t<d+1, all factors are positive and

    F(t+1)/F(t) = (t+1)(N-t-k+1) / [t(N-t)].

Subtracting the denominator from the numerator gives d+1-kt. Consequently F increases when kt<d+1, decreases when kt>d+1, and ties at successive t,t+1 precisely when kt=d+1.

Set t0=ceil((d+1)/k). This is a maximizing integer, and

    gp(Pe(d,k)) >= t0 (d+k-t0)_(k-1).

If k does not divide d+1, t0 is the UNIQUE maximizer in this family. If k divides d+1, the maximizers are exactly t0 and t0+1. This is family optimality, not the exact general-position number.

For fixed k and d tending to infinity, t0=d/k+O(1), giving

    F(t0) = [(k-1)^(k-1)/k^k] d^k + O_k(d^(k-1)).

Since the whole graph has (d+k)_k=d^k+O_k(d^(k-1)) vertices,

    liminf_{d -> infinity} gp(Pe(d,k)) / |V(Pe(d,k))|
       >= (k-1)^(k-1)/k^k.

The source's disproved proposed exact value 2(d+k-2)_(k-1) has order d^(k-1); this optimized construction has order d^k. The multiplicative discrepancy therefore grows at least linearly with d for fixed k, with asymptotic ratio at least

    [(k-1)^(k-1)/(2 k^k)] d.

For example k=3,d=9: t0=4 and F=4*8*7=224, against the source's180 and the previously frozen three-terminal construction's216. No maximum or minimum-counterexample claim follows.

## Provenance and limits

Original source: arXiv:2604.15909v1 Section3.3, Theorem3.6 and its following optimality conjecture. The source introduced the two-terminal disjoint-prefix construction; B's frozen packet extended it to three. This note optimizes that same credited family. The source and follow-up searches were rechecked 2026-10-10; no priority certification is asserted. This is not a new reservation on ROOT's orientation spectrum or trees, and not a claim to solve Problem5.2's exact permutation values.

The independent replay reconstructs every original injective word and arc for Pe(9,3), computes BFS from all224 selected vertices, and verifies the strict distance gap; it does not import the frozen proof's constructor or distance formula. A separate exact integer parameter check verifies the maximizing t set and the ratio sign over its declared finite range. Finite tests do not replace the all-parameter proof above.
