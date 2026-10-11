# An exact positive-correlation range before the special bit

Status: written research derivation with complete small-word self-checks. Originality and independent verification remain separate gates. This statement concerns the same XOR-linearized three-add local function as `special_bit_signed_correlation.md`.

## 1. Statement

Assume `r>=q>=1`, `r+q<n`, and independent uniform input words `a,b,c,d`. Put `delta=n-r-q>0`. For every bit `0<=i<r+q`, let `k=(i-q) mod n`. Then

\[
\boxed{E[(-1)^{w[i]\oplus L[i]}]=2^{-(\delta+i+k)}.}
\]

In particular, standard parameters `(32,16,12)` give

\[
C_i=\begin{cases}
2^{-(24+2i)},&0\le i\le 11,\\
2^{-(2i-8)},&12\le i\le 27.
\end{cases}
\]

This theorem stops before bit `r+q`. It makes no statement about bits above that position or about fixed `a`. The condition `r>=q` is sufficient for the proof below, and is not asserted to be necessary.

## 2. Expressing the correlation in independent variables

The bijective change `(a,b,c,d) -> (s,b,u,t)` from the companion proof makes those four full words independent uniform. For a nonnegative bit index `h`, write

\[
A_h=(-1)^{[b\bmod 2^h>s\bmod 2^h]},
\]

\[
B_k=(-1)^{[t\bmod 2^k>u\bmod 2^k]},\qquad
D_i=(-1)^{[(s\bmod2^i)+(v\bmod2^i)\ge2^i]}.
\]

Here `A_0=B_0=D_0=1`. With `j=i+delta<n`, the carry identity at bit `i` becomes

\[
C_i=E[A_i A_j B_k D_i].
\]

Averaging over the independent `t` gives

\[
g_k(u)=E_t[B_k\mid u]
       =\frac{2(u\bmod2^k+1)-2^k}{2^k},
\]

with the same formula equal to one when `k=0`.

## 3. Averaging the intervening `s` bits

Condition on the lower `i` bits of `s,b` and on the `delta` bits `b_i,...,b_(j-1)`. Set `rho=[b_low_i>s_low_i]` and `X=floor((b mod2^j)/2^i)`. The higher `s` segment is uniform in `[0,2^delta)`. The borrow into bit `j` occurs for exactly `X+rho` segment values, so

\[
E_{s_i,\ldots,s_{j-1}}[A_iA_j]
=2^{-\delta}+A_i\sum_{m=i}^{j-1}2^{m-i-\delta}\chi_m(b).
\]

Neither `g_k(u)` nor `D_i` uses these `s` bits, so the conditional expectation can be substituted directly into `C_i`.

The constant term contributes

\[
2^{-\delta}E[g_k(u)D_i]=2^{-\delta}2^{-k}2^{-i}.
\]

Indeed, since `b` is uniform and independent of `u`, the word `v=R_q(b XOR u)` is uniform and independent of `u,s`. Hence the two expectations factor: the average carry sign at bit `k` is `2^-k`, and that at bit `i` is `2^-i`.

## 4. Every correction term vanishes

For each `m` with `i<=m<j`, consider

\[
E[A_i\chi_m(b)g_k(u)D_i].
\]

Only input bit positions

\[
J_i=\{(p-q)\bmod n:0\le p<i\}
\]

of `b XOR u` occur in `v mod2^i`.

If `m` is not in `J_i`, flipping `b_m` changes `chi_m(b)` but leaves `A_i,g_k,D_i` unchanged; therefore the expectation is zero.

If `m` is in `J_i` and `m>=k`, simultaneously flip `b_m` and `u_m`. This preserves `b XOR u`, preserves the lower `i` bits of `b`, and preserves the lower `k` bits of `u`. Again only `chi_m(b)` changes sign, so the expectation is zero.

Thus a nonzero term would require

\[
m\in[i,j)\cap J_i\cap[0,k).
\]

This intersection is empty under the stated assumptions. If `i>=q`, then `k=i-q<i`. If `i<q`, then `J_i=[n-q,n-q+i)` (empty at `i=0`), whereas

\[
j=i+n-r-q<n-q
\]

because `i<q<=r`. Every correction term therefore vanishes, proving the claimed correlation.

## 5. Verification and model limits

The deterministic experiment `experiments/exact_signed.py` checks every output bit in this range for every eligible parameter triple with `n=3,4,5`. The small-word checks do not prove the general theorem; the conditional-expectation and sign-reversing arguments above supply that proof.

The mask `L` is fixed by replacing additions by XOR. No search for optimal masks is included. A nonzero local correlation does not imply that composing these masks across rounds is valid; exact signed hull aggregation and input-distribution constraints are separate problems. No new reduced-round attack is claimed.
