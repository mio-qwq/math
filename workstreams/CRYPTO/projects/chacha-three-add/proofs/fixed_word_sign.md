# A complete conditional-sign classification at the special bit

Status: written research derivation with passed bounded self-checks. This is a corollary of the exact fixed-first-word formula and an elementary finite-sum identity; it is not assigned an originality level. Independent review remains required.

## 1. Statement

Use the assumptions of `fixed_first_word.md`: `r,q>=1`, `i=r+q<n`, `N=2^i`, fixed `a`, and independent uniform `b,c,d`. Put `A=a mod N`. The signed correlation at output bit `i` obeys

\[
C_A=\begin{cases}
2^{-(2r+q)},&A=0,\\
-2^{-(2r+q)},&A=1,\\
\text{strictly less than }-2^{-(2r+q)},&2\le A<N.
\end{cases}
\]

Thus its sign is positive exactly when the lower `r+q` bits of `a` are all zero. It is never zero. Among the `2^n` possible fixed words, the fraction with positive correlation is exactly `2^-(r+q)`. This is a classification under the explicit local uniformity assumptions, not a probability claim about keys in an attack.

## 2. A triangular-area identity

Recall

\[
T_{\ell,p}(A)=\sum_{x=0}^{A-1}\chi_\ell(x-A)H_p(x),
\quad p>\ell,
\]

where `chi_ell` is the periodic square wave and `H_p` is its triangular prefix sum. Set `h=2^ell`, `P=2^p`, and

\[
F_\ell(t)=\sum_{z=1}^t H_\ell(z)\qquad(t\ge0).
\]

For `t=(A-1) mod (2P)`,

\[
\boxed{
T_{\ell,p}(A)=
\begin{cases}
-F_\ell(t),&0\le t\le P,\\
F_\ell(t-P)-hP/2,&P<t<2P.
\end{cases}}
\]

In particular,

\[
-hP/2\le T_{\ell,p}(A)\le0.
\]

### Proof

First assume `A>=1`. Since `chi_ell(-d-1)=-chi_ell(d)`, reversing the sum gives

\[
T_{\ell,p}(A)=-\sum_{d=0}^{A-1}\chi_\ell(d)H_p(A-1-d).
\]

Discrete summation by parts, with `H_ell(0)=H_p(0)=0`, yields

\[
T_{\ell,p}(A)=-\sum_{z=1}^{A-1}H_\ell(z)\chi_p(A-1-z)
            =-\sum_{y=0}^{A-2}H_\ell(A-1-y)\chi_p(y).
\]

The first factor has period `2h`, which divides `P` because `p>ell`. The square wave `chi_p` is positive for the first `P` positions of its `2P` period and negative for the next `P`. Therefore complete `2P` blocks cancel. In the remaining block of length `t`, if `t<=P`, reversing the order gives the positive sum `F_ell(t)` inside the minus sign. If `t>P`, the first `P` terms contribute `hP/2`, because a complete period of `H_ell` has sum `h^2` and there are `P/(2h)` periods. The remaining negative terms contribute `-F_ell(t-P)`. This proves the identity for `A>=1`.

For `A=0`, the defining sum is empty. The displayed expression gives the same result: then `t=2P-1` and `F_ell(P-1)=F_ell(P)=hP/2`, since `H_ell(P)=0`.

Finally `H_ell(z)>=0`, so `F_ell` is nondecreasing, and `F_ell(P)=hP/2`. This proves both bounds on `T`.

## 3. Correlation sign

The exact fixed-word formula has numerator

\[
N-2A(N+1-A)+4\sum_{\ell=0}^{r-1}2^\ell T_{\ell,\ell+q}(A).
\]

All terms in the sum are nonpositive. At `A=0` each sum is empty and the numerator is `N`. At `A=1`, every `T` is zero because it only contains `H_p(0)`, and the numerator is `-N`.

For `2<=A<N`,

\[
A(N+1-A)-N=(A-1)(N-A)>0.
\]

Therefore the first two terms already give a quantity strictly below `-N`, and adding the nonpositive sum preserves strictness. Division by the positive denominator `2^r N^2` proves the classification.

## 4. Alternative constant-size evaluation

The triangular area itself has a simple closed form. Write `t=k(2h)+z`, `0<=z<2h`. Then

\[
F_\ell(t)=kh^2+
\begin{cases}
z(z+1)/2,&z\le h,\\
h^2-(2h-z)(2h-z-1)/2,&z>h.
\end{cases}
\]

This gives an alternative `O(r)` evaluation of `C_A`, using only nonnegative prefix arguments and eliminating the signed-prefix primitives in the earlier implementation. Both algorithms derive from the same mathematical formula; agreement between them is a research self-check, not an independent verification by another researcher.

The accompanying bounded experiment checks the new triangle-area identity directly, compares the two arithmetic algorithms, and verifies the sign classification across all parameter sums `2<=r+q<=12` and all `A` at each parameter. Those finite checks do not replace the general proof above.
