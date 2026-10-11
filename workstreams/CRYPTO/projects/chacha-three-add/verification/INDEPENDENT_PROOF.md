# Independent proof of the endpoint signed correlation

Author role: independent verification agent. Date: 2026-10-11.

This derivation was completed using only the supplied word-operation specification and candidate formula. No discovery implementation or discovery proof was read. It is a written mathematical proof, not a proof-assistant formalization and not human peer review. Novelty is not assessed here.

## Statement

Let `a,b,c,d` be independent uniform n-bit words. All additions below are modulo 2^n. Bits are numbered from zero at the least significant bit, and `rotl` moves a bit at position j to position j+r modulo n. Put

```
s = a + b
t = rotl(d xor s, r)
u = c + t
v = rotl(b xor u, q)
w = s + v.
```

Let L be w computed from the same inputs with all three additions replaced by XOR. For integers r,q>=1 satisfying r+q<n, put i=r+q. Then

\[
\operatorname{Cor}_i=\mathbb E[(-1)^{(w\oplus L)_i}]
=-\frac1{3\,2^r}-\frac1{7\,2^q}
+\frac4{3\,2^{3r+2q}}+\frac1{7\,2^{3r+q}}.
\]

The expectation is over the complete independent uniform four-word input distribution.

## 1. Exact carry identity

For an n-bit sum z=x+y, define its carry word as `x xor y xor z`. Its j-th bit is the carry into bit j; in particular the zeroth bit is zero. Let alpha, beta, gamma be the carry words of `a+b`, `c+t`, and `s+v` respectively.

If `s0,t0,u0,v0,L` denote the XOR-only computation, direct XOR cancellation gives

\[
s\oplus s_0=\alpha,\qquad
t\oplus t_0=\operatorname{rotl}(\alpha,r),
\]

\[
u\oplus u_0=\operatorname{rotl}(\alpha,r)\oplus\beta,
\]

\[
w\oplus L
=\alpha\oplus\operatorname{rotl}(\beta,q)
\oplus\operatorname{rotl}(\alpha,r+q)\oplus\gamma.
\]

Consequently, at i=r+q<n,

\[
(w\oplus L)_i=\alpha_i\oplus\beta_r\oplus\alpha_0\oplus\gamma_i
=\alpha_i\oplus\beta_r\oplus\gamma_i. \tag{1}
\]

This identity does not assert that the three carries are independent.

## 2. A bijection gives independent words

Change variables from `(a,b,c,d)` to `(s,b,u,t)`. The inverse is

\[
a=s-b\pmod{2^n},\qquad c=u-t\pmod{2^n},\qquad
d=\operatorname{rotr}(t,r)\oplus s.
\]

This is a bijection on the complete 2^(4n)-element input set. Thus s,b,u,t are independent uniform n-bit words. Define

\[
R=2^r,\quad Q=2^q,\quad M=2^i=RQ,
\quad S=s\bmod M,\ B=b\bmod M,\ U=u\bmod R,\ T=t\bmod R,
\quad V=v\bmod M.
\]

From the inverse subtraction and the definition of a carry,

\[
\alpha_i=\boldsymbol 1_{B>S},\qquad
\beta_r=\boldsymbol 1_{T>U},\qquad
\gamma_i=\boldsymbol 1_{S+V\ge M}. \tag{2}
\]

For example, if B>S then `(a mod M)=M+S-B`, and adding B produces carry one; equality B=S produces carry zero. These exact endpoints matter.

The low i bits of `rotl(b xor u,q)` have the form

\[
V=Q((B\bmod R)\oplus U)+H,
\]

where H is the q-bit block of `b xor u` at positions n-q,...,n-1. Since n-q>r, the corresponding u bits are disjoint from the low r bits U. Conditional on b,U,S,T, these high u bits are still uniform. Hence H is uniform on [0,Q) and independent of B,U,S,T. This remains valid even if the corresponding b positions overlap B: XOR with a fresh uniform u block makes H uniform conditional on the entire b word.

For each B, the map `(U,H) -> V` is bijective. Therefore S,B,V are independent uniforms on [0,M), T is an independent uniform on [0,R), and

\[
U=(B\bmod R)\oplus\lfloor V/Q\rfloor. \tag{3}
\]

## 3. Average the middle carry exactly

For fixed U,

\[
f(U):=\mathbb E_T[(-1)^{\boldsymbol1_{T>U}}]
=\frac{2U+2-R}{R}.
\]

Let

\[
W(S,B,V)=(-1)^{\boldsymbol1_{B>S}+\boldsymbol1_{S+V\ge M}}.
\]

Equations (1)--(3) yield the exact reduction

\[
\operatorname{Cor}_i=\mathbb E_{S,B,V}[f(U)W(S,B,V)]. \tag{4}
\]

For bits U_k, the elementary integer identity

\[
2U+2-R=1-\sum_{k=0}^{r-1}2^k(-1)^{U_k}
\]

and (3) imply

\[
\operatorname{Cor}_i=\frac1R\left(H_0-\sum_{k=0}^{r-1}2^k H_{k,k+q}\right), \tag{5}
\]

where

\[
H_0=\mathbb E[W],\qquad
H_{k,j}=\mathbb E[(-1)^{B_k+V_j}W].
\]

The remaining sums concern independent uniform integers S,B,V only.

## 4. Compute the constant term

Conditional on S, B and V are independent, so

\[
H_0=\frac1{M^3}\sum_{S=0}^{M-1}(2S+2-M)(M-2S).
\]

Using the exact sums of S and S^2 gives

\[
H_0=-\frac13+\frac4{3M^2}. \tag{6}
\]

The `+2` comes from the inclusive event B<=S; replacing it by a continuous approximation would lose a finite-size correction.

## 5. Compute the mixed terms by square-wave prefix sums

For an integer k>=0 let

\[
\chi_k(x)=(-1)^{\operatorname{bit}_k(x)},\qquad
P_k(t)=\sum_{x=0}^{t-1}\chi_k(x),\quad P_k(0)=0.
\]

P_k is periodic with period 2^(k+1), rising from 0 to 2^k and then falling back to 0. Since M=2^i and k,j<i, its complete sum over [0,M) is zero. Conditional on S,

\[
\mathbb E_B[\chi_k(B)(-1)^{\boldsymbol1_{B>S}}]
=\frac{2P_k(S+1)}M,
\]

\[
\mathbb E_V[\chi_j(V)(-1)^{\boldsymbol1_{S+V\ge M}}]
=\frac{2P_j(M-S)}M=\frac{2P_j(S)}M.
\]

For the last equality, reflect a suffix by `x -> M-1-x`: bit j is complemented, so `P_j(M-S)=P_j(S)`. Consequently,

\[
H_{k,j}=\frac4{M^3}\sum_{S=0}^{M-1}P_k(S+1)P_j(S). \tag{7}
\]

We need only j=k+q>k. Put A=2^k and D=2^j. Then D is a multiple of 2A, and M is a multiple of 2D. The product in (7) has period 2D. For one such period, pair S=x and S=D+x, with 0<=x<D. The short prefix is unchanged because D is a multiple of its period; the long prefixes are x and D-x. Thus

\[
\begin{aligned}
\sum_{S=0}^{2D-1}P_k(S+1)P_j(S)
&=D\sum_{x=0}^{D-1}P_k(x+1)\\
&=D\frac{D}{2A}A^2=\frac{D^2A}{2}.
\end{aligned}
\]

Here the sum of `P_k(x+1)` over a short period is exactly
`1+2+...+A+(A-1)+...+1+0=A^2`.
Multiplying by the M/(2D) periods in [0,M) gives

\[
\sum_{S=0}^{M-1}P_k(S+1)P_j(S)=\frac{MAD}{4},
\qquad H_{k,j}=\frac{2^{k+j}}{M^2}. \tag{8}
\]

This step is where q>=1 is used. When q=0, j=k and the period-pairing argument is invalid.

## 6. Finish the closed form

Substituting (6) and (8) into (5),

\[
\begin{aligned}
\operatorname{Cor}_i
&=\frac1R\left[-\frac13+\frac4{3M^2}
-\frac Q{M^2}\sum_{k=0}^{r-1}8^k\right]\\
&=-\frac1{3R}+\frac4{3RM^2}-\frac{Q(R^3-1)}{7RM^2}\\
&=-\frac1{3R}-\frac1{7Q}+\frac4{3R^3Q^2}+\frac1{7R^3Q}.
\end{aligned}
\]

This proves the claimed formula for every stated n,r,q. No sampling, asymptotic approximation, or carry-independence assumption occurs in the proof.

## 7. Separate finite-sum identity used in the numerical cross-check

One can instead first integrate out S. For fixed B,V, the two negative-sign intervals are `[0,B)` and `[M-V,M)`, so

\[
\mathbb E_S W(S,B,V)=\frac{2|B+V-M|-M}{M}.
\]

Combining this with (3)--(4) gives an independently programmable integer sum:

\[
\operatorname{Cor}_i=
\frac{1}{RM^3}\sum_{B,V=0}^{M-1}
\bigl(2((B\bmod R)\oplus\lfloor V/Q\rfloor)+2-R\bigr)
\bigl(2|B+V-M|-M\bigr).
\]

The Python verifier evaluates this unsimplified sum directly, not through the square-wave lemma or the candidate expression. The C++ verifier separately executes the original five word operations and their XOR-only counterpart.

## 8. Sign, standard parameters, and limits

`Cor = Pr[error bit=0] - Pr[error bit=1]` is signed. The signed bias relative to 1/2 is `Cor/2`, while the absolute correlation is `abs(Cor)`.

At n=32,r=16,q=12,i=28, the exact formula reduces to

\[
-\frac{47180567524833621}{1180591620717411303424}
\approx-3.9963495163690355\cdot10^{-5}.
\]

This is a uniform-input three-addition local correlation. At standard parameters, the resulting `w` is also exactly the first output word of a complete ChaCha quarter round, since the remaining quarter-round operations change only `b,c,d`. The XOR-linearized first output likewise remains `L`. Thus the formula is an exact one-bit first-output-word linear correlation of the complete quarter round under the stated distribution. It does not determine the remaining output words or their joint distribution, and is not automatically a distinguisher for a complete ChaCha round, a fixed-key stream, or ChaCha20. Standard stream initial states include fixed constants. No attack complexity or improved public cryptanalytic record is established by this proof alone.

The formula can be evaluated with O(1) arithmetic operations on integers having O(r+q) bits. This is a probability-evaluation cost, not a key-recovery cost. The independent direct word enumeration costs O(n*2^(4n)) when all output bits are accumulated for one rotation pair. The separate threshold sum costs O(2^(2(r+q))) integer steps and O(1) auxiliary loop storage. Neither was attempted as standard-parameter exhaustive search.

## 9. Convention source

RFC8439 sections 2.1 and 2.1.1 define modulo-2^32 addition, left rotation, and the quarter-round test vector used by the verifier:
https://www.rfc-editor.org/rfc/rfc8439.html#section-2.1

Retrieved 2026-10-11; web reference `turn99view0`. The external standard is used only to fix the convention and official test vector; the proof above is the independent verifier's derivation.
