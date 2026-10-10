# Comparing the two parity-class maximizers for even numbers of rows

**Conditional on no unverified assumptions.** This is an exact combinatorial theorem about the multi-row centered binomial function H from GENERALIZATION.md. It is not a solution to unrelated geometric facet conjectures, and its historical originality is not certified.

Fix an even number t=2h>=4 of rows and a total S>=2t that is even. Positive vectors of equal parity may be all odd or all even. The strict transfer theorem proves unique maximizers **within each** parity class:

    odd:  (S-t+1,1,...,1)
    even: (S-2t+2,2,...,2).

Write S=2t-2+2k, where k>=1 (so the even class is feasible), and define

    O_h(k)=2*C(2k+2h-1,k+h)
    E_h(k)=2^(2h-1)*C(2k,k)+2*C(2k,k+1).

These are the two exact values. Let R_h(k)=O_h(k)/C(2k,k) and Q_h(k)=E_h(k)/C(2k,k)=2^(2h-1)+2k/(k+1).

## Theorem (single parity crossover)

For each fixed h>=2, the ratio O_h(k)/E_h(k) is **strictly increasing** over integers k>=1. It converges to

    2^(2h) / (2^(2h-1)+2) > 1.

At k=1:

- If h=2 or h=3 (t=4,6), the odd class dominates, and therefore dominates for every larger k.
- If h>=4 (t>=8), the even class strictly dominates at k=1, but eventually the odd class strictly dominates. Consequently there is a unique single crossover in dominance as k increases, with at most one equality at an intermediate k. The threshold can be found exactly by comparing the displayed integer formulas; no real-valued approximation is needed.

**Proof.** The factorial quotient in R_h gives

    R_h(k+1)/R_h(k)
      = [(2k+2h+1)(k+1)] / [(k+h+1)(2k+1)]
      = 1 + h/[(k+h+1)(2k+1)].

Likewise,

    Q_h(k+1)/Q_h(k)
      = 1 + 2/[(k+1)(k+2) Q_h(k)].

The former multiplicative increase is larger if

    h (k+1)(k+2) Q_h(k) > 2(k+h+1)(2k+1).

Now Q_h(k)>=2^(2h-1)>=8, while for k>=1,

    2(k+h+1)(2k+1)/[(k+1)(k+2)] < 2(h+2).

Since h*8>2(h+2) for h>=2, the required strict inequality follows. Hence O_h/E_h strictly increases.

The fixed-h central-binomial factorial quotient yields R_h(k)->2^(2h), while Q_h(k)->2^(2h-1)+2; the displayed limit is greater than one for h>=2. Finally, k=1 gives O_h(1)=2*C(2h+1,h+1) and E_h(1)=2^(2h)+2. For h=2,3 these are respectively 20>18 and 70>66. For h=4, 252<258. Moreover O_{h+1}(1)/O_h(1)=4-2/(h+2)<4, so O_h(1)<4^h<E_h(1) for every h>=4. QED.

## A sharp warning against over-generalizing the three-row conjecture

At t=8 and S=16, the all-odd class maximizer (9,1,1,1,1,1,1,1) has H=252, while the all-even class maximizer (2,2,2,2,2,2,2,2) has H=258. At t=8 and S=18, the all-odd class max (11,1,1,1,1,1,1,1) has 924, whereas the all-even class max (4,2,2,2,2,2,2,2) is 776. Thus neither parity class wins uniformly at all totals for t>=8.

Independent exact finite arithmetic checker: code/verify_cross_parity.py. This is a mathematical extension of the centered-binomial theorem, not a counterexample to the original three-row Conjecture 31. It does not claim a novel publication or an independent external review.
