# Exact conditional special-bit correlation for a fixed first word

Status: written research derivation with complete small-word self-checks. Independent verification and originality assessment are separate. This is an exact local correlation, not a cipher attack.

## 1. Function and assumptions

Use exactly the three-add local function and XOR-linearized output in `special_bit_signed_correlation.md`. Let `r,q>=1`, `i=r+q<n`, and `N=2^i`. The first input word `a` is now fixed; only `b,c,d` are independent and uniformly distributed. Write `A=a mod N`.

Define

\[
C_A=E_{b,c,d}[(-1)^{w[i]\oplus L[i]}].
\]

The upper bits of `a` do not affect this correlation. The claim about `b,c,d` being independent uniform remains an explicit assumption. Even substituting an RFC constant for `a` does not by itself turn this statement into a fixed-key attack or an analysis of the joint distribution of real counter and nonce inputs.

## 2. The formula

For an integer `x`, let `chi_l(x)=(-1)^bit_l(x)`, interpreted as a periodic function modulo `2^(l+1)` even when `x` is negative. Let

\[
H_p(x)=\sum_{z=0}^{x-1}\chi_p(z)
\]

for nonnegative `x`, continued periodically to all integers. For `p>ell` define

\[
T_{\ell,p}(A)=\sum_{x=0}^{A-1}\chi_\ell(x-A)H_p(x).
\]

Then

\[
\boxed{
C_A=\frac{N(1-2A)+2A(A-1)
       +4\sum_{\ell=0}^{r-1}2^\ell T_{\ell,\ell+q}(A)}
       {2^rN^2}.}
\]

Each `T` can be evaluated by a constant number of exact integer arithmetic operations, as given in section 4. Thus this is an `O(r)` arithmetic formula, without enumerating the possible values of `A` or any input word.

In particular,

\[
C_0=2^{-(2r+q)}.
\]

This is positive, whereas the average over uniform `a` is the negative quantity proved in the companion theorem. Conditional correlations must therefore retain their signs and their precise input distribution.

## 3. Proof of the formula

For fixed `a`, the map `(b,c,d) -> (b,u,t)` is a bijection, because

```
s = a + b
c = u - t
d = R_(-r)(t) XOR s.
```

Hence `b,u,t` are independent uniform. Set `S=s mod N` and `B=b mod N`. Then `S` is uniform, `B=(S-A) mod N`, and the first-add carry into bit `i` is exactly `[S<A]`.

As in the uniform-word proof, averaging the middle carry and changing to `V=R_q(b XOR u) mod N` gives independent uniform `S,V` and

\[
g=2^{-r}-\sum_{\ell=0}^{r-1}2^{\ell-r}
       \chi_\ell(B)\chi_{\ell+q}(V).
\]

Let `h_A(S)=(-1)^[S<A]`. Then

\[
C_A=2^{-r}M_0(A)-\sum_{\ell=0}^{r-1}2^{\ell-r}M_{\ell,\ell+q}(A),
\]

where

\[
M_0(A)=\frac1N\sum_{S=0}^{N-1}h_A(S)(1-2S/N)
      =\frac{N(1-2A)+2A(A-1)}{N^2}.
\]

For `ell<p<i`, first average over `V`, using

\[
E_V[(-1)^{[S+V\ge N]}\chi_p(V)]=\frac2N H_p(S).
\]

Consequently

\[
M_{\ell,p}(A)=\frac2{N^2}\sum_{S=0}^{N-1}
 h_A(S)\chi_\ell(S-A)H_p(S).
\]

The complete sum without `h_A` vanishes. To see this, set `P=2^p`; pair `S` with `S+P` in each `2P` period. Since `p>ell`, `chi_ell` has the same value at both positions, while `H_p(S)+H_p(S+P)=P`. Their paired sum is `P chi_ell(S-A)`, and `chi_ell` sums to zero over a half period of length `P`. Since `2P` divides `N`, the whole unweighted sum is zero. Replacing `h_A=1-2[S<A]` thus yields

\[
M_{\ell,p}(A)=-\frac4{N^2}T_{\ell,p}(A).
\]

Substitution proves the displayed formula. At `A=0` the prefix sums are empty, so `C_0=N/(2^rN^2)=2^{-(2r+q)}`.

## 4. Constant-size evaluation of the prefix sums

Fix `ell`, set `h=2^ell`, and write each integer `t=k(2h)+z` with `0<=z<2h` and Euclidean quotient `k` (possibly negative). Define

\[
F_0(t)=\begin{cases}z,&0\le z\le h,\\2h-z,&h<z<2h,\end{cases}
\]

\[
G_1(z)=\begin{cases}
z(z-1)/2,&0\le z\le h,\\
h(h-1)-z(z-1)/2,&h<z<2h,
\end{cases}
\]

\[
F_1(t)=-kh^2+k(2h)F_0(t)+G_1(z).
\]

Direct subtraction, including the transition between periods, proves

\[
F_0(t+1)-F_0(t)=\chi_\ell(t),\qquad
F_1(t+1)-F_1(t)=t\chi_\ell(t).
\]

For nonnegative `e` let

\[
Q_0(e)=F_0(e-A)-F_0(-A),
\]

\[
Q_1(e)=F_1(e-A)-F_1(-A)+A Q_0(e).
\]

Telescoping gives `Q_0(e)=sum_(x<e) chi_ell(x-A)` and `Q_1(e)=sum_(x<e) x chi_ell(x-A)`.

Now set `P=2^p`, `t=A mod (2P)`. Complete `2P` periods of the product `chi_ell(x-A) H_p(x)` vanish by the pairing argument above. The remaining triangular segment gives

\[
T_{\ell,p}(A)=
\begin{cases}
Q_1(t),&t\le P,\\
2Q_1(P)-Q_1(t)+2P\bigl(Q_0(t)-Q_0(P)\bigr),&t>P.
\end{cases}
\]

This uses a constant number of arithmetic operations on `O(n)`-bit integers for each `ell`. The overall formula uses `O(r)` such operations and `O(n)` auxiliary bits if the terms are accumulated in a stream. A unit-cost arithmetic bound is not a claim that multiplication of arbitrarily long integers costs constant bit time.

## 5. Exact standard-word predictions

For `(n,r,q,i)=(32,16,12,28)`, the formula gives the following predictions under the assumptions in section 1. The four nonzero words are the ChaCha constants documented in RFC 8439, section 2.3.

| Fixed `a` | Exact signed correlation | Approximate correlation |
|---|---|---:|
| `0x00000000` | `1/17592186044416` | `5.684341886080802e-14` |
| `0x61707865` | `-5014914159307157/295147905179352825856` | `-1.6991190082341052e-5` |
| `0x3320646e` | `-20742118815994171/590295810358705651712` | `-3.5138516066020844e-5` |
| `0x79622d32` | `-36166661545322725/590295810358705651712` | `-6.126870784216696e-5` |
| `0x6b206574` | `-14797957587093615/295147905179352825856` | `-5.013743051336016e-5` |

The exact fractions come from the integer prefix formula. No sampling or 32-bit exhaustive search is used. For every legal `(n,r,q)` with `n=3,4,5`, `experiments/exact_signed.py` compares this formula against complete enumeration of `(b,c,d)` for every `a`. It also checks that averaging `C_A` over all `a` returns the uniform-word theorem, and checks the auxiliary prefix formulas against direct summation, including negative prefix arguments.

Specification source: [RFC 8439, section 2.3](https://www.rfc-editor.org/rfc/rfc8439.html#section-2.3). Novelty blockers and the precise status of predecessor literature are maintained by the separate novelty review; correctness of this derivation is not a novelty certificate.
