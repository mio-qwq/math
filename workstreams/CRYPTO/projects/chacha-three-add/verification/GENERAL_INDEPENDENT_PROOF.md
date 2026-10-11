# Independent proof of the arbitrary-bit elimination formula

Date: 2026-10-11. Author role: independent verification agent.

The discovery agent supplied the proposed formula and the suggested four-state variables. This document reconstructs its mathematical justification from the original word operations. The verifier has not read the discovery `experiments/` or `tooling/` implementation. The endpoint proof was independently derived before the discovery endpoint manuscript was made available for cross-review.

**Status:** ordinary written proof and independent exact finite verification. This is not a proof-assistant formalization, a novelty determination, or a new full-cipher attack.

## 1. Parameters and word operations

Let `n >= 1`; word values belong to `Z/(2^n)`. Let `r,q` be arbitrary rotation counts, interpreted modulo `n`. Let `0 <= i < n`. Bits are numbered from the least significant position, and `R` denotes left rotation. Define

```
s = a + b
t = R_r(d XOR s)
u = c + t
y = R_q(b XOR u)
w = s + y
```

All additions are modulo `2^n`. Define `L` by replacing **each of the three additions** in these same instructions by XOR. We study

`C_i = E[(-1)^bit_i(w XOR L)]`.

At `(n,r,q)=(32,16,12)`, `w` is exactly the first output word of a complete standard ChaCha quarter round, since its remaining operations change only `b,c,d`. Similarly `L` is the first output word of the completely XOR-linearized quarter round. The theorem therefore also evaluates this one-bit first-output-word linear correlation, without determining the other output words or their joint distribution.

There are two distributions:

1. `a,b,c,d` are independent uniform words;
2. `a=A` is fixed, and `b,c,d` are independent uniform words.

The value is signed correlation. The signed probability bias is `C_i/2`, and the probability that the two bits agree is `(1+C_i)/2`.

For `p=0,...,n-1`, write `borrow_p(X-Z)` for the borrow into bit `p` in unsigned subtraction, and `carry_p(X+Z)` for the carry into bit `p`. Both are zero at `p=0`. Set

`j = (i-q) mod n`, `k = (i-r-q) mod n`.

Unlike the endpoint closed form, the following result does not require positive rotations or a non-wrapping sum of rotations.

## 2. Exact error identity

Let `alpha,beta,gamma` be the carry vectors of the three additions, with bit zero equal to zero. The identity `x+z = x XOR z XOR carry(x+z)` holds at every retained bit. Substitution in the five word operations gives

`w XOR L = alpha XOR R_(r+q)(alpha) XOR R_q(beta) XOR gamma`.

Consequently the error at the arbitrary bit is exactly

`e_i = alpha_i XOR alpha_k XOR beta_j XOR gamma_i`.

No independence of carry bits is used. If `i=k`, the two occurrences of `alpha_i` cancel, which is essential for zero and wrapping rotations.

For any addition `Z=X+V` modulo the word modulus and any retained position `p`,

`carry_p(X+V) = [V mod 2^p > Z mod 2^p] = borrow_p(Z-V)`.

Indeed, `Z_low=X_low+V_low-c*2^p`, where `c` is zero or one. If `c=0`, `Z_low>=V_low`; if `c=1`, `Z_low<V_low` because `X_low<2^p`. This also verifies the zero-bit boundary directly.

## 3. Change of variables and conditional distributions

Write capital letters for the random words `S=s, B=b, U=u, T=t, Y=y`.

In the uniform-input model, `(a,b,c,d) -> (S,B,U,T)` is bijective, with inverse

```
a = S - B
c = U - T
d = R_(-r)(T) XOR S
```

Thus `S,B,U,T` are independent uniform words. Replacing `U` by `Y=R_q(B XOR U)` is another bijection, with inverse

`U = B XOR R_(-q)(Y)`.

Therefore `S,B,Y,T` are independent uniform words. In these coordinates,

`alpha_p = borrow_p(S-B)`, `beta_j = borrow_j(U-T)`, `gamma_i = carry_i(S+Y)`.

For the fixed-word model `a=A`, the map `(b,c,d) -> (S,U,T)` is bijective, with inverse

```
B = S - A
c = U - T
d = R_(-r)(T) XOR S
```

The subsequent substitution of `Y` for `U` is again bijective for each `S`, so `S,Y,T` are independent uniform words and `B=S-A`. The first-addition carry is also

`alpha_p = borrow_p(S-A)`.

This follows from the preceding addition identity with `A` and `B` interchanged. In particular, `borrow_p(S-B)` and `borrow_p(S-A)` agree pointwise for pairs satisfying `S=A+B`. This is why a single subtraction-borrow state suffices in the fixed-word model.

## 4. Eliminating the middle-addition carry

Condition on all variables except the independent uniform word `T`. Put `m=2^j` and `u=U mod m`. Exactly `u+1` of the `m` possible low words of `T` satisfy `T_low<=u`, and `m-u-1` satisfy `T_low>u`. Hence

\[
E_T[(-1)^{\operatorname{borrow}_j(U-T)}\mid U]
=\frac{2u+2-m}{m}.
\]

The inclusive threshold supplies the `+2`, including at `u=0`. At `j=0`, `m=1` and the answer is one.

Let `chi_h(X)=(-1)^bit_h(X)`. Since `bit_h(X)=(1-chi_h(X))/2`, the last expression has the exact expansion

\[
g_j(U)=2^{-j}\left(1-\sum_{h=0}^{j-1}2^h\chi_h(U)\right).
\]

The inverse rotation implies

\[
\chi_h(U)=\chi_h(B)\chi_{(h+q)\bmod n}(Y).
\]

Define the remaining sign

\[
W=(-1)^{\operatorname{borrow}_i(S-B)
                  +\operatorname{borrow}_k(S-B)
                  +\operatorname{carry}_i(S+Y)}.
\]

In the fixed-word model the two borrows may equivalently be written for `S-A`. Define

\[
M_0=E[W],\qquad M_{h,l}=E[W\chi_h(B)\chi_l(Y)].
\]

The expectations are over independent `S,B,Y` in the uniform-input model, and independent `S,Y` with `B=S-A` in the fixed-word model.

The variable `Y` enters `W` only through the bits below `i`, because the carry into bit `i` depends on no higher bit. If `l>=i`, the bit `Y_l` is an independent unbiased bit even after conditioning on everything else in the summand. Thus `M_{h,l}=0` exactly for every such `l`. This remains valid when `B` is a function of `S` in the fixed-word model.

Changing the remaining index from `h` to `l=(h+q) mod n` gives the proposed formula:

\[
\boxed{\displaystyle
C_i=2^{-j}\left(M_0-
\sum_{\substack{0\le l<i\\h=(l-q)\bmod n<j}}
2^h M_{h,l}\right).}
\]

This is an exact identity for every word width, every rotation pair, and every output bit in the stated ranges, for both distributions. The set in the sum is empty whenever its conditions cannot be met; in particular it is empty when `j=0` or `i=0`.

## 5. Four-state exact counting algorithm

For any individual moment, scan bits from low to high. The state entering position `p` is `(rho,kappa)`, the current subtraction borrow and addition carry. Initially it is `(0,0)`.

Before processing a bit at a monitored boundary, multiply the path sign by:

- `(-1)^rho` at boundary `i`;
- `(-1)^rho` at boundary `k`;
- `(-1)^kappa` at boundary `i`.

Coincident boundary phases are multiplied, so two identical borrow phases cancel. These signs must be applied **before** consuming the bit at that boundary; otherwise they would refer to outgoing rather than incoming carries.

In the uniform-input model, enumerate all eight equally likely triples `(s_p,b_p,y_p)` at each position. The outgoing states are

```
rho_next   = [s_p - b_p - rho < 0]
kappa_next = [s_p + y_p + kappa >= 2]
```

For a masked moment, multiply additionally by `(-1)^b_p` when `p=h` and by `(-1)^y_p` when `p=l`.

In the fixed-word model, enumerate the four equally likely pairs `(s_p,y_p)` instead. With `A_p=bit_p(A)`, compute

```
delta      = s_p - A_p - rho
b_p        = delta mod 2
rho_next   = [delta < 0]
kappa_next = [s_p + y_p + kappa >= 2]
```

Use the same boundary and mask phases. In both models all four terminal states are summed because overflow beyond the word is discarded. Dividing the final signed count by `8^n` or `4^n`, respectively, gives the desired moment exactly.

To prove the dynamic program, use induction on the processed prefix length: the count in a state equals the sum of the signs of all prefixes realizing that state, with exactly the already-encountered observation phases inserted. The transition formulas are the usual binary subtraction/addition recurrences. Each extension is enumerated once. At the final boundary this invariant is precisely the desired signed count. No further state, carry independence, or probabilistic approximation is needed.

## 6. Cost and scope

One moment uses `n` levels, four states, and at most eight outgoing bit choices per state. The displayed correlation formula calls for at most `n+1` moments. Therefore the direct independent implementation uses `O(n^2)` signed-integer arithmetic operations for one output bit, or `O(n^3)` when separately evaluating all `n` output bits. The signed-count integers and weighted numerator have `O(n)` bits. Four state counts suffice as working storage for each moment; the output spectrum itself requires additional storage. With elementary linear-cost integer addition, a conservative bit-operation bound is `O(n^3)` per output bit before rational reduction.

These are bounds for exact **evaluation of one specified local correlation**, not for key recovery, constructing a full-round distinguisher, or breaking ChaCha20. They are also not evidence that this evaluator improves any published generic ARX algorithm. Literature novelty and comparison against such algorithms are separate requirements.

The endpoint closed form in `INDEPENDENT_PROOF.md` applies only to `r,q>=1`, `i=r+q<n`; the present elimination identity also covers the remaining bits and rotation cases. Its general validity is supplied by the proof above, while finite enumeration is an implementation cross-check. The 32-bit values are computed exactly by this proved recurrence; no 32-bit input-space enumeration has been performed.
