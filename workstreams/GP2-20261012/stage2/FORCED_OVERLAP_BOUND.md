# A compatibility loss beyond the pair-level rotation bound

GP2-20261012, stage 2. Candidate all-alphabet written theorem with exact finite certificates. The uniform numerical interval for lambda_4 is **unchanged** in this stage.

## 1. Definitions and theorem

Let A be any finite nonempty alphabet, mu any probability distribution on it, and ell:A^2->{0,1,2}. Use the candidate words V_ell, empty-orbit probability E_ell, and viable-orbit weight T_ell=(1-E_ell)/4 defined in `ROTATION_COMPLETION.md`.

Let F_ell consist of the words that are the **unique** V_ell candidate in their cyclic rotation orbit. For positive a,b with a+b<=4, let Theta_(a,b) be the probability that all three windows starting at 0,a,a+b of an independent-letter word of length 4+a+b belong to F_ell. Occurrences, not distinct words, are counted.

**Theorem.** For every strict code C contained in V_ell, its product-weight density p satisfies

    p <= (1-E_ell)/4 - (1/3) max_{a,b>=1, a+b<=4} Theta_(a,b).    (1)

Independence of C is not assumed. All repeated-letter configurations are included. No optimization over ell is asserted in (1).

## 2. Proof

Every selected word belongs to a primitive viable orbit; strictness permits at most one selected word per orbit. All four members of such an orbit have the same product weight. Therefore

    T_ell-p = sum of the one-representative weights of unoccupied viable orbits.

If a forced word w in F_ell is absent from C, then its orbit is unoccupied, because all other rotations violate ell. Different forced words belong to different orbits. Consequently

    q := Pr[random four-letter word belongs to F_ell minus C] <= T_ell-p.  (2)

On the event defining Theta_(a,b), strictness forces at least one of those three forced occurrences to be absent from C. This remains true when the same word occurs twice: otherwise all three occurrences would be selected, which strictness forbids. The union bound, with each window having the same product marginal, gives

    Theta_(a,b) <= 3q <= 3(T_ell-p).

Rearrange, then maximize over the six possible positive gap pairs. This proves (1) for arbitrary real probability distributions, including zero weights. There is no probabilistic independence assumption between the overlapping windows.

## 3. Exact computation without enumerating all eight-letter words

For h=1,2,3 and a (4-h)-letter string z, set

    L_h(z) = sum_{u in F_ell, suffix_(4-h)(u)=z} mu(u_1)...mu(u_h),
    R_h(z) = sum_{u in F_ell, prefix_(4-h)(u)=z} mu(u_(5-h))...mu(u_4).

Conditioning on the middle forced word v gives

    Theta_(a,b) = sum_{v in F_ell} mu(v) L_a(prefix_(4-a)(v))
                                             R_b(suffix_(4-b)(v)).       (3)

The a free letters of the left window and b free letters of the right window lie outside the middle word on opposite sides. They are independent conditional on v; no unexamined consistency condition is needed, even when the two endpoint windows overlap inside v. This proves (3).

The fiber tables require O(|A|^4) terms and all six moments can be evaluated in that order of arithmetic operations. For rational weights the calculation is exact. The verifier additionally uses direct concatenation of endpoint windows, independently of the fiber-sum implementation.

## 4. A fixed obstruction to rotation-only optimization

On six equally weighted letters, take rows indexed 0,...,5:

    1 2 0 1 2 0
    0 1 2 1 1 0
    2 0 1 2 2 1
    1 2 1 1 0 0
    1 0 2 1 0 0
    1 0 2 2 2 2.

Direct exact rotation enumeration gives

    E_ell = 7/162, T_ell = 155/648,
    |F_ell|=189.

The six moments are

| gaps (a,b) | Theta_(a,b) |
|---|---|
| (1,1) | 5/7776 |
| (1,2) | 2/2187 |
| (1,3) | 1951/839808 |
| (2,1) | 1/1152 |
| (2,2) | 0 |
| (3,1) | 715/279936 |

Thus every strict code compatible with **this fixed level array**, for the uniform distribution, obeys

    p <= 155/648 - 715/839808 = 200165/839808.

The positive moment also proves that no strict code saturates its rotation bound, whether independent or not. An explicit six-letter word with three consecutive forced windows is included in the certificate so that this nonattainment can be checked without trusting the rational moment computation.

This is a structural obstruction, not a new universal bound of 200165/839808 on lambda_4. A different ell need not have these values. An experiment minimizing E alone is therefore insufficient to find an extremal GP construction.

## 5. Connection to the original problem and remaining work

For an arbitrary actual GP set S in Ka(m,4), the inherited repair theorem gives a strict subset C losing at most 73m^3 vertices. Obtain ell from the ordered-pair graph of C and apply (1) with uniform weights. It yields

    |S| <= m^4[(1-E_ell)/4 - max Theta_(a,b)/3] + 73m^3.

The substantive remaining analytic question is a uniform optimization of this joint functional, or stronger global compatible constraints. No such optimization is proved here. In particular, this stage does not replace the inherited all-alphabet bound 182/729 or the inherited optimized Jiggs lower endpoint beta.

The penalty uses an elementary union bound; it is not asserted to have an optimal coefficient. Its role is to couple rotation losses with actual shared-prefix/suffix obstructions, something a smaller E by itself omits.

## 6. A minimal-size mechanism warning: canonical levels do not fix forced overlaps

This section does not claim minimal alphabet size or minimum counterexample size. It supplies a two-word example showing that recomputing **canonical** pair levels from a strict code does not make its forced set strict.

On A={0,1,2}, let

    C={2100,2110}.

There is no proper suffix/prefix overlap between any two of these words: suffixes of length one end in 0 instead of the initial 2; length-two suffixes are 00 or 10 instead of 21; length-three suffixes are 100 or 110 instead of 210 or 211. Thus C is nonoverlapping, hence strict.

Its selected pair graph has just 21->00 and 21->10. Canonical longest-incoming-walk levels are one at 00 and 10, zero everywhere else. Relative to these levels, both 2010 and 0100 are unique candidates in their respective rotation orbits. In the eight-letter word

    20100100,

the windows starting at 0,1,4 are respectively 2010,0100,0100. All are forced, so F_ell is not strict. This explicitly uses the occurrence quantifier; the repetition of 0100 cannot be omitted.

Therefore “replace ell by the canonical levels of a feasible code and then select all forced words” is not a valid completion procedure, even when the starting code is independent and has no proper overlaps. This is a strict-code obstruction, not a new counterexample to the original directed-GP problem or a new limiting-density endpoint.
