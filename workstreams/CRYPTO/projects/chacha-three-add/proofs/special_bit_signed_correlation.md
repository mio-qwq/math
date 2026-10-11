# Exact signed correlation of a three-add ChaCha local component

Status: research derivation, with complete deterministic small-word self-checks. Independent verification and literature novelty review are separate gates. No new attack or originality is claimed here.

## 1. Precisely specified function and correlation

Let `n,r,q` be integers satisfying `r>=1`, `q>=1`, and `r+q<n`. All additions below are modulo `2^n`; `R_k` is left rotation by `k` bits in an `n`-bit word. Define

```
s = a + b
t = R_r(d XOR s)
u = c + t
v = R_q(b XOR u)
w = s + v
```

This is the first three modular additions of a ChaCha quarter round, stopping at the updated first word. The usual values are `(n,r,q)=(32,16,12)`.

Replace every modular addition by XOR to define the linear word

`L = a XOR b XOR R_q(b XOR c) XOR R_(r+q)(a XOR b XOR d)`.

Input words `a,b,c,d` are independent and uniformly distributed. Bit numbering starts at zero at the least significant bit. Set `i=r+q` and define the signed correlation

`C = E[(-1)^(w[i] XOR L[i])]`.

The probability of equality is `(1+C)/2`. The bias convention `Pr[equality]-1/2` would give `C/2`; it is not the correlation used below.

## 2. Theorem

For the parameters above,

\[
C=-\frac{1}{3\,2^r}-\frac{1}{7\,2^q}
  +\frac{4}{3\,2^{3r+2q}}+\frac{1}{7\,2^{3r+q}}.
\]

In particular, `C<0`. The answer is independent of `n` once `r+q<n`.

For standard `(32,16,12)` at bit 28,

\[
C=-\frac{47180567524833621}{1180591620717411303424}
  \approx -0.000039963495163690355.
\]

This is a local, uniform-state linear correlation. It is not a result for a fixed secret key, not a full-round distinguisher, and not a key-recovery attack. In particular, standard first column rounds fix `a` to a constant, so this unconditional average must not be substituted for that distribution; the fixed-word derivation is separate.

## 3. Carry identity and an invertible change of variables

Let `K1,K2,K3` be the carry vectors for `a+b`, `c+t`, `s+v`. Their bit zero is zero, and each modular sum equals the XOR of its operands and its carry vector. Direct substitution therefore gives

`w XOR L = K1 XOR R_(r+q)(K1) XOR R_q(K2) XOR K3`.

At bit `i=r+q<n`, this becomes exactly

`w[i] XOR L[i] = K1[i] XOR K2[r] XOR K3[i]`.

There is no independence assumption in this identity.

The map `(a,b,c,d) -> (s,b,u,t)` is bijective: its inverse is

```
a = s - b
c = u - t
d = R_(-r)(t) XOR s
```

Thus `s,b,u,t` are independent uniform words. For any addition `z=x+y`, the carry into bit `h` equals `[y mod 2^h > z mod 2^h]`. This follows by writing `z_low=x_low+y_low - carry*2^h`.

Write `N=2^i`, `S=s mod N`, `B=b mod N`, and `U=u mod 2^r`. Then

- `K1[i]=[B>S]`;
- averaging over the independent `t mod 2^r` gives
  \[
  g(U)=E_t[(-1)^{K2[r]}\mid U]
      =\frac{2(U+1)-2^r}{2^r};
  \]
- `K3[i]=[S+V>=N]`, where `V=v mod N`.

The lowest `q` bits of `V` come from input bits `n-q,...,n-1` of `b XOR u`. Because `n-q>r`, these `u` bits are disjoint from `U` and fresh uniform. Consequently

`V = Z + 2^q * ((B mod 2^r) XOR U)`

where `Z` is uniform in `[0,2^q)` and independent of `(S,B,U)`. Equivalently, `S,B,V` are independent uniform values in `[0,N)`, and

`U = (B mod 2^r) XOR (V >> q)`.

This step remains valid when the high source bits of `b` overlap its lower `i` bits: the independent high bits of `u` mask them. No additional condition such as `n>=r+2q` is needed.

## 4. Walsh expansion of the middle-carry factor

Let `chi_h(x)=(-1)^bit_h(x)`. The exact affine bit expansion is

\[
g(U)=2^{-r}-\sum_{\ell=0}^{r-1}2^{\ell-r}\chi_\ell(U).
\]

Substitution of `U` gives

\[
C=2^{-r}M_0-\sum_{\ell=0}^{r-1}2^{\ell-r}M_{\ell,\ell+q},
\]

where independent uniform `S,B,V` define

\[
M_0=E[(-1)^{[B>S]+[S+V\ge N]}],
\]

\[
M_{\ell,p}=E[(-1)^{[B>S]+[S+V\ge N]}\chi_\ell(B)\chi_p(V)].
\]

The variables `B` and `V` separate after conditioning on `S`; this is justified by the bijection above, not by a heuristic.

## 5. Two elementary sums

Define the triangular prefix sum

\[
H_h(x)=\sum_{z=0}^{x-1}\chi_h(z),
\]

continued periodically with period `2^(h+1)`. On one period, if `J=2^h`, it is `x` for `0<=x<=J` and `2J-x` for `J<=x<2J`.

### 5.1 The unmasked term

For fixed `S`,

\[
E_B[(-1)^{[B>S]}]=2(S+1)/N-1,
\quad
E_V[(-1)^{[S+V\ge N]}]=1-2S/N.
\]

Averaging their product using the exact sums of `S` and `S^2` for `S=0,...,N-1` yields

\[
M_0=-\frac13+\frac{4}{3N^2}.
\]

### 5.2 The two masked terms

For `ell<p<i`,

\[
E_B[(-1)^{[B>S]}\chi_\ell(B)]=\frac2N H_\ell(S+1),
\]

\[
E_V[(-1)^{[S+V\ge N]}\chi_p(V)]=\frac2N H_p(N-S)
 =\frac2N H_p(S).
\]

The last equality follows from periodicity and symmetry of the triangle, since `2^(p+1)` divides `N`. Set `J=2^ell` and `P=2^p`. Because `p>ell`, the period `2J` divides `P`. Pair `x` with `x+P` in a full `2P` period. The small triangle has the same value at the two positions, whereas `H_p(x)+H_p(x+P)=P`. Therefore

\[
\sum_{x=0}^{2P-1}H_\ell(x+1)H_p(x)
=P\sum_{x=0}^{P-1}H_\ell(x+1)
=\frac{JP^2}{2}.
\]

Hence `E_S[H_ell(S+1)H_p(S)]=JP/4`, and

\[
M_{\ell,p}=\frac{2^{\ell+p}}{N^2}.
\]

## 6. Geometric sum and sign

Using `p=ell+q`,

\[
C=2^{-r}\left(-\frac13+\frac4{3N^2}\right)
 -\frac{2^{q-r}}{N^2}\sum_{\ell=0}^{r-1}2^{3\ell}.
\]

The geometric sum is `(2^(3r)-1)/7`, and `N=2^(r+q)`, which gives the theorem. Since `N>=4`, `M0<0`; each masked term is positive and subtracted with a positive coefficient. Thus `C<0` exactly.

For comparison only, treating the three distinct carry bits `K1[i],K2[r],K3[i]` as independent would give `2^(-2i-r)=2^(-3r-2q)>0`. This is a deliberately invalid negative control, not an existing paper's claimed formula. The theorem cannot, without checking an actual paper's masks and assumptions, be described as refuting a published attack.

## 7. Evidence and scope

The reproducible command and self-check results are in `../experiments/README.md` and `../experiments/results/exact_signed_max5.json`. The script directly enumerates original `(a,b,c,d)` inputs, not transformed variables, for all `n=3,4,5`, `r,q>=1`, `r+q<n`. It checks the signed count and all fixed first-word values.

The proof is the justification for 32-bit parameters; no 32-bit exhaustive test has been performed. No formal proof assistant was used. Novelty remains unassessed pending full-text review of near predecessors, especially INDOCRYPT 2025 and ICISC 2025 linear-approximation work, generic S-functions, and exact ARX linear models.
