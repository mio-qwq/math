# Closed form and short recurrence in the overlapping-carry region

Date: 2026-10-11. Status: complete written research derivation with passed bounded self-checks. Independent verification and originality review remain separate gates. This document does not claim a new cipher attack or a new published-best complexity.

This is an appended research cycle. The preceding special-bit, conditional-word, and positive-range files remain frozen.

## 1. Exact scope and result

Use the same three-addition local function and its all-XOR linearization as in `special_bit_signed_correlation.md`:

```
s = a+b
t = R_r(d XOR s)
u = c+t
v = R_q(b XOR u)
w = s+v
L = a XOR b XOR R_q(b XOR c) XOR R_(r+q)(a XOR b XOR d).
```

All additions are modulo `2^n`, all rotations are left rotations in an `n`-bit word, and all four input words are independent uniform. Assume

\[
r,q\ge1,\qquad 0\le k\le q,\qquad i=r+q+k<n.
\]

Let `C_k=E[(-1)^(w_i XOR L_i)]`, where the subscript now denotes the offset `k` from bit `r+q`, not the absolute bit position. Define

\[
\alpha=-\frac1{3\,2^r}+\frac4{3\,2^{3r+2q}},
\]

\[
\beta=-\frac1{7\,2^q}-\frac1{7\,2^{3r+q}},
\qquad
\delta=\frac2{7\,2^{3r+q}}.
\]

Then

\[
\boxed{C_k=\alpha\,4^{-k}+\beta\,2^{-k}+\delta\,16^{-k}.}
\]

This is independent of `n` subject to the stated condition. At `k=0` it equals the previously derived special-bit formula. The condition `k<=q` is weaker than the initially proposed `k<min(r,q)`; no condition `k<r` is needed.

For every four consecutive offsets that remain in the allowed domain,

\[
\boxed{C_{k+3}=\frac{13}{16}C_{k+2}
              -\frac{11}{64}C_{k+1}
              +\frac1{128}C_k.}
\]

Precisely, the recurrence requires `k+3<=min(q,n-r-q-1)`. The formula also implies `C_k<0`; section 6 proves the sign without comparing rounded numerical values.

## 2. Removing the middle addition

The carry identity gives, at `i=r+q+k<n`,

\[
w_i\oplus L_i=K1_i\oplus K1_k\oplus K2_j\oplus K3_i,
\quad j=r+k.
\]

The invertible change `(a,b,c,d) -> (s,b,u,t)` makes its four output words independent uniform. Average the independent middle-addend word `t`. Then change from `u` to `Y=R_q(b XOR u)`. The independent variables are now `s,b,Y`, and the middle-carry factor is

\[
2^{-j}\left(1-\sum_{\ell=0}^{j-1}2^\ell
  \chi_\ell(b)\chi_{\ell+q}(Y)\right).
\]

There is no rotation wraparound in this expression: `ell+q<i<n` for every retained term. Truncate all three independent words to `i` bits, writing them as `S,B,Y` in `[0,N)`, where `N=2^i`.

Define

\[
A(S,B)=(-1)^{[B>S]+[B\bmod2^k>S\bmod2^k]},
\qquad
D(S,Y)=(-1)^{[S+Y\ge N]}.
\]

Thus

\[
C_k=2^{-j}\left(M_0-
  \sum_{\ell=0}^{j-1}2^\ell M_{\ell,\ell+q}\right),
\]

where

\[
M_0=E[A(S,B)D(S,Y)],
\quad
M_{\ell,p}=E[A(S,B)D(S,Y)\chi_\ell(B)\chi_p(Y)].
\]

The two carry factors can be averaged separately over `B` and `Y` **after conditioning on S**. This exact conditional factorization is not an independence assumption about their carries.

## 3. Splitting at the lower carry

Set

\[
K=2^k,\quad H=2^{r+q},\quad N=KH,
\quad S=KX+s,
\]

where `0<=X<H`, `0<=s<K`. Write `B=KZ+b` similarly. Define

\[
a_s=E_b[(-1)^{[b>s]}]=\frac{2s+2-K}{K},
\qquad U_X=2X-H+1.
\]

If `Z<X`, the product of the two first-add carry signs is `(-1)^[b>s]`. If `Z>X`, it is its negative. If `Z=X`, the two carry bits coincide and their product is exactly `+1` for every `b`. This equal-block case is the source of the correction relative to a product approximation.

It follows that

\[
E_B[A\mid S]=\frac{1+U_Xa_s}{H}.
\]

For a mask below the split, `ell<k`, the equal block has zero masked average and

\[
E_B[A\chi_\ell(B)\mid S]
=\frac{2}{N}U_XH_\ell(s+1).
\]

For a mask at or above the split, set `e=ell-k>=0`. Since `chi_ell(B)=chi_e(Z)`, summing over `Z` gives

\[
E_B[A\chi_\ell(B)\mid S]
=\frac1H\left(2a_sH_e(X)+(a_s+1)\chi_e(X)\right).
\]

Here `H_h(x)=sum_(z=0)^(x-1) chi_h(z)` is the periodic triangular prefix sum used in the previous proofs.

For the final carry,

\[
E_Y[D\mid S]=1-\frac{2S}{N}
 =\frac{1-U_X-2s/K}{H},
\]

\[
E_Y[D\chi_p(Y)\mid S]=\frac2N H_p(S).
\]

The domain condition `k<=q` ensures `p=ell+q>=k`. Consequently, with `f=p-k`,

\[
H_p(KX+s)=K H_f(X)+s\chi_f(X).
\]

This within-block affine identity is the only place where the upper bound on `k` is required. If `p<k`, the larger block can contain complete oscillations of `H_p`, so this identity cannot be applied.

## 4. Elementary triangular-wave averages

Let `X` be uniform in `[0,H)`, with `H` a power of two, and let `0<=e<f<log2(H)`. Finite period sums give

\[
E[H_e(X)H_f(X)]=\frac{2^{e+f}}4,
\]

\[
E[\chi_e(X)H_f(X)]
=E[H_e(X)\chi_f(X)]
=E[\chi_e(X)\chi_f(X)]=0.
\]

The first identity follows by pairing `X` with `X+2^f`: the smaller triangle is unchanged while the two larger-triangle values sum to `2^f`. The first vanishing identity follows by the same pairing and summing the smaller square wave. The other two follow because the smaller-period factor is unchanged while the larger square wave changes sign.

For any `0<=f<log2(H)`, setting `P=2^f` also gives

\[
E[U_XH_f(X)]=P/2,
\qquad E[U_X\chi_f(X)]=-P.
\]

For completeness, over a single period of length `2P`,

\[
\sum H_f(X)=P^2,\quad
\sum XH_f(X)=P^3,\quad
\sum X\chi_f(X)=-P^2.
\]

Summing translated periods gives the displayed expectations for every allowed `H`.

Similarly, when `ell<k`, `J=2^ell` and `s` is uniform in `[0,K)`,

\[
E[H_\ell(s+1)]=J/2,
\qquad
E[sH_\ell(s+1)]=J(K-2)/4.
\]

These follow from the same period sums after shifting the argument by one. We will also use `E[a_s]=1/K`, `E[s]=(K-1)/2`, `E[U_X]=0`, and `E[U_X^2]=(H^2-1)/3`.

## 5. The exact moments

### 5.1 Unmasked moment

Using the conditional expressions from section 3,

\[
M_0=\frac1{H^2}E[(1+U_Xa_s)(1-U_X-2s/K)].
\]

Terms containing a single `U_X` vanish. The remaining terms give

\[
\boxed{M_0=\frac1K\left(-\frac13+\frac4{3H^2}\right).}
\]

### 5.2 Mask below the lower carry: `ell<k`

Set `p=ell+q`, `f=p-k>=0`, `J=2^ell`, and `P=2^f`. Then

\[
M_{\ell,p}=\frac4{N^2}
\left(K E[U_XH_f(X)]E[H_\ell(s+1)]
 +E[U_X\chi_f(X)]E[sH_\ell(s+1)]\right).
\]

The averages in section 4 yield

\[
M_{\ell,p}=\frac4{N^2}
 \left(\frac{KPJ}{4}-\frac{PJ(K-2)}4\right)
=\boxed{\frac{2^{\ell+p-k+1}}{N^2}.}
\]

### 5.3 Mask at or above the lower carry: `ell>=k`

Set `e=ell-k` and `f=p-k=e+q`, so `f>e`. Multiplying the conditional expressions gives

\[
M_{\ell,p}=\frac2{NH}
E[(2a_sH_e(X)+(a_s+1)\chi_e(X))
  (KH_f(X)+s\chi_f(X))].
\]

All mixed triangle/square and square/square terms vanish by section 4. Since `E[a_s]=1/K`, only one term remains:

\[
M_{\ell,p}=\frac4{NH}E[H_e(X)H_f(X)]
=\boxed{\frac{2^{\ell+p-k}}{N^2}.}
\]

The two formulas combine as

\[
\boxed{
M_{\ell,\ell+q}=\frac{2^{2\ell+q-k}}{N^2}
 \begin{cases}2,&\ell<k,\\1,&\ell\ge k.\end{cases}}
\]

The factor of two in the lower-mask range is an exact correction, not an empirical fit.

## 6. Geometric summation and recurrence

Substituting the moments yields

\[
C_k=2^{-(r+k)}\left[
\frac1K\left(-\frac13+\frac4{3H^2}\right)
-\frac{2^{q-k}}{N^2}
 \frac{2^{3(r+k)}+2^{3k}-2}{7}\right].
\]

Use `K=2^k`, `H=2^(r+q)`, and `N=KH`. Collecting coefficients of `4^-k`, `2^-k`, and `16^-k` gives exactly the formula in section 1.

Moreover `H>=4`, so `M0<0`; every masked moment is positive. Hence `C_k<0` directly from its moment expression.

The three geometric sequences satisfy the common characteristic polynomial

\[
(z-1/4)(z-1/2)(z-1/16)
=z^3-\frac{13}{16}z^2+\frac{11}{64}z-\frac1{128}.
\]

This proves the recurrence wherever all four offsets lie in the allowed range. It is derived from the exact finite-sum formula, not fitted to four standard-word values.

## 7. Standard-word values and an actual boundary failure

For `(n,r,q)=(32,16,12)`, all available offsets are `k=0,1,2,3`; the formula gives

| Absolute bit | Exact signed correlation |
|---:|---|
| 28 | `-47180567524833621/2^70` |
| 29 | `-88356335546507093/2^72` |
| 30 | `-170707871589853653/2^74` |
| 31 | `-335410943676546677/2^76` |

Together with the frozen positive-range proof, this provides exact closed expressions for every output bit of this particular uniform-input, three-add, all-XOR-mask model at standard parameters. This does not establish optimal masks or an attack on a complete quarter round or full cipher.

Blind extrapolation beyond `k<=q` fails. For `r=q=1`, `k=2`, `i=4`, and any `n>=5`, exact threshold counting gives `-7/256`, while extrapolating the displayed formula gives `-57/2048`. Their difference is `1/2048`. Here the masked term with `ell=0` has `p=1<k=2`, outside the within-block affine condition. The counterexample is the smallest failing absolute-bit position in the bounded scan, not a claim that every possible larger-domain extension must fail.

## 8. Evidence, audit boundary, and stopping decision

`experiments/overlap_moments.py` computes the borrow and final-carry threshold sums directly for each `S`, then multiplies their conditional sums. It does not use the root agent's four-state code or enumerate new four-word inputs. For `i<=8` it checked 62 in-domain parameter triples, 214 masked moments, and 14 already-frozen original-input correlations; all passed. It also tested the 22 out-of-domain triples in that bounded domain and found a mismatch in each. Complete results and the command receipt are in `experiments/OVERLAP_RUN.md` and `experiments/results/overlap_moments_max8.json`.

The four standard-word fractions from the root agent were known before this derivation, as was the suggestion to investigate a combination of the three geometric sequences. They were used only for the final numerical cross-check. The moment formulas, geometric summation, and recurrence above were derived from the carry thresholds. The root implementation and independent verifier's code were not read during this subcycle. This is not claimed as a blind discovery of the initial hypothesis or as independent human review.

The bounded cycle's stopping target was an exact formula or an informative failure within `0<=k<min(r,q)`. The stronger range `0<=k<=q` has a complete proof and a documented boundary failure; no larger computation is warranted for this target. The next gate is independent mathematical review and detailed comparison with earlier exact ARX correlation methods. Originality and publication value remain unresolved.
