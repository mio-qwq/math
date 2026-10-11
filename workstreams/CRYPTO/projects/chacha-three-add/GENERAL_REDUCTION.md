# Exact arbitrary-bit reduction to four-state signed counting

Date: 2026-10-11. Mathematical scope: the three-addition local program below. Status: written derivation, independent reconstruction, independent original-word checks and two standard-width implementations agree; see verification/GENERAL_VERIFICATION_REPORT.md and tooling/results/standard_comparison.json. Originality is a separate, unresolved literature question. General finite-state ARX correlation methods already exist.

## 1. Definitions and target

For n>=1, 0<=r,q<n and n-bit unsigned words, all additions are modulo 2^n and R denotes **left** rotation:

```
s = a + b
t = R_r(d XOR s)
u = c + t
v = R_q(b XOR u)
w = s + v
L = a XOR b XOR R_q(b XOR c) XOR R_(r+q)(a XOR b XOR d)
```

`L` is the result of replacing all three additions by XOR in this same program. Bit zero is least significant. For any 0<=i<n the target is

\[
C_i=\mathbb E[(-1)^{w_i\oplus L_i}].
\]

Two distributions are treated separately: (U) all four input words are independent uniform; (A) `a=A` is fixed and `b,c,d` are independent uniform. This document does not model a fixed secret key, counter schedule, nonce restrictions, or a complete ChaCha round.

In the full ChaCha quarter round, the operations after w only update the other three words. Thus w also equals its first final output word. The reduction evaluates that one component; it gives no statement about the remaining output words or their joint correlation.

Unlike the special-bit closed form, this reduction permits zero rotations and wraparound. In particular it must be valid when two indicated carry bits coincide or an indicated carry is bit zero.

## 2. Exact carry identity

Let K1, K2 and K3 denote the carry-into-bit words of the three actual additions. Since sum = operand XOR operand XOR carry word,

\[
w\oplus L=K1\oplus R_{r+q}(K1)\oplus R_q(K2)\oplus K3.
\]

Set

\[
j=(i-q)\bmod n,\qquad k=(i-r-q)\bmod n.
\]

The error bit is exactly

\[
e_i=K1_i\oplus K1_k\oplus K2_j\oplus K3_i.
\]

No factorization of dependent carry probabilities has been made.

## 3. Bijection and removal of the middle addition

In distribution U use variables `(S,B,U,T)=(s,b,u,t)`. Their inverse is

```
a = S-B
b = B
c = U-T
d = R_(-r)(T) XOR S.
```

Thus they are four independent uniform n-bit words. In distribution A, the inverse is the same with `B=S-A`, and `(S,U,T)` are three independent uniform words.

For any h, write low_h(X)=X mod 2^h. The first carry equals a borrow in a subtraction:

- Distribution U: `K1_h = [low_h(B)>low_h(S)]`, the borrow into bit h of `S-B`.
- Distribution A: `K1_h = [low_h(A)>low_h(S)]`, the borrow into bit h of `S-A`.

Similarly `K2_j=[low_j(T)>low_j(U)]`. For N=2^j, averaging the independent T gives

\[
g_j(U)=\frac{2\operatorname{low}_j(U)+2-N}{N}
=2^{-j}\left(1-\sum_{h=0}^{j-1}2^h(-1)^{U_h}\right).
\]

For j=0 the sum is empty and g_0=1, as required for a carry into the least significant bit.

Now let `Y=R_q(B XOR U)`. In distribution U, S,B,Y are independent uniform; in distribution A, S,Y are independent uniform and B=S-A. The last carry is the carry into bit i of S+Y. Also

\[
(-1)^{U_h}=(-1)^{B_h}(-1)^{Y_{(h+q)\bmod n}}.
\]

The last carry depends only on Y bits below i. Every other factor is independent of Y. Hence a Walsh term whose Y index is at least i has zero expectation by summing that fresh uniform Y bit. This cancellation is exact even when B is a deterministic function of S.

## 4. Reduction theorem

Write beta_h for the subtraction borrow defined above and gamma_h for the addition carry of S+Y. Set

\[
M_0=\mathbb E[(-1)^{\beta_i\oplus\beta_k\oplus\gamma_i}],
\]

\[
M_{h,\ell}=\mathbb E[(-1)^{\beta_i\oplus\beta_k\oplus\gamma_i\oplus B_h\oplus Y_\ell}].
\]

Expectations use S,B,Y in U and S,Y with B=S-A in A. The exact answer is

\[
\boxed{C_i=2^{-j}\left(M_0-
\sum_{\substack{0\le\ell<i\\h=(\ell-q)\bmod n<j}}
2^h M_{h,\ell}\right).}
\]

Sections 2–3 prove the identity for every parameter in section 1. In particular, two first-carry occurrences at i=k cancel; no distinctness assumption is needed. For i=0 there are no masked terms. For j=0 there are no masked terms either.

## 5. Four-state evaluation of each moment

Process positions p=0,...,n-1, retaining only `(beta_p,gamma_p)` in {0,1}^2 and an integer signed count for each state. The initial state is (0,0) with count one.

**Before processing bit p**, multiply the current weight by the sign contributions `beta_p` if p=i, `beta_p` if p=k, and `gamma_p` if p=i. Contributions combine by XOR; equal indices do not warrant deleting one occurrence without cancellation.

In U, sum over the eight equally likely choices `(s_p,b_p,y_p)` and update

\[
\beta_{p+1}=[b_p+\beta_p>s_p],\qquad
\gamma_{p+1}=\lfloor(s_p+y_p+\gamma_p)/2\rfloor.
\]

In A, sum over the four choices `(s_p,y_p)`, using the fixed a_p, and compute

\[
b_p=(s_p-a_p-\beta_p)\bmod 2,
\quad\beta_{p+1}=[a_p+\beta_p>s_p],
\quad\gamma_{p+1}=\lfloor(s_p+y_p+\gamma_p)/2\rfloor.
\]

For moment M_(h,ell), multiply a transition additionally by (-1)^b_p when p=h and by (-1)^y_p when p=ell. There is no additional phase for M0.

Finally **sum all four terminal counts**. The final carry/borrow is not constrained to zero: the specified arithmetic is modular. Divide by 2^(3n) in U, or 2^(2n) in A, to obtain the moment. The induction invariant is that each state contains the exact signed sum of all processed input-bit assignments reaching it. The phase at a boundary uses the state before its transition, so the invariant incorporates precisely the desired carry-into-bit signs. This proves the counting algorithm.

## 6. Complexity and limitations

There are at most i+1<=n moments. Each uses n positions, four states and at most eight transitions per state. Thus one output-bit correlation takes O(n^2) exact integer arithmetic operations. Counts and the final weighted sum have O(n) bits; using ordinary linear-time integer additions and shifts gives an O(n^3) upper bound on bit operations. Streaming moments uses O(n) auxiliary bits beyond the input and final result; retaining diagnostic rows costs more. Computing all n output bits separately costs O(n^3) arithmetic operations. These are upper bounds on **this specified algorithm**, not a comparison against the best published finite-state method.

For n=32 a direct four-input enumeration would have 2^128 tuples. No such enumeration is performed. The dynamic program sums exactly over its own 2^(3n) or 2^(2n) transformed assignments through integer counts. A standard-width exact result is justified by the derivation and independent checks, not by extrapolation of toy statistics.

The chosen masks are constrained by the all-XOR linearization. No optimal-mask search or multi-round composition has been performed. A computable exact local correlation is not by itself an attack-complexity improvement. See `NOVELTY_REVIEW.md` for predecessor frameworks and unresolved overlap.

## 7. Implementations and review boundary

`tooling/exact_dp.py` is the root agent's implementation of this reduction. It was developed after seeing the independent original-word count file and the discovering agent's special-bit and fixed-word closed forms; it is therefore a third computational method, not a blind discovery of those statements.

The verification agent received the mathematical specification before the root code was written and was instructed to implement independently without reading `tooling/`. The discovering agent independently audited the reduction from the mathematical message only, calling out terminal-state summation, coincident carry indices and pre-transition boundary phases as critical points. Those are agent audits, not human peer review or proof-assistant verification. Actual verification outcomes and source hashes belong in the associated run receipts and verification reports.
