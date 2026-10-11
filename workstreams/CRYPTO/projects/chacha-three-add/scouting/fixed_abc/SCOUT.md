# Fixed a,b,c and uniform d: bounded input-model scout

Date: 2026-10-11. Classification target: L0 modeling clarification and direct application of known signed finite-state counting. No original cryptanalytic method or attack is claimed. This scout is isolated from the frozen project proofs, implementations, and Git history.

## 1. Question and stopping criteria, fixed before computation

Fix all three words `a,b,c`; only `d` is uniform over the `n`-bit words. Study the same signed coefficient `E_d[(-1)^(w_i XOR L_i)]` for the three-add local function. This addresses whether a coefficient averaged over random `b,c` can be transferred to fixed `b,c`; it does not initiate a key-recovery or multi-round attack.

The scout succeeds if it obtains an exact constant-width state model, proves its resource bound, and checks a few bounded original-word examples. It should stop as an L0 application if that model is an ordinary product of constant-addition kernels. It should report a failure if rotated dependencies require extra retained bits, if the constant phase is wrong, or if any exact original-word count disagrees.

The predetermined computational budget is 17 fixed parameter tuples of width at most four, enumerating only `d` in each tuple. This visits 188 input words and compares all 54 output-bit coefficients. Two chosen negative controls target omission of the fixed first-add carry sign and a false product of marginal carry correlations. Once the exact small-state proof holds, six synthetic standard-32 examples at bit 28 may be evaluated analytically. No 32-bit enumeration or larger fixed-word search is authorized by this scout.

## 2. Exact model and constant sign

Let `n>=1`, `0<=r,q<n`, and `0<=i<n`. All additions and subtractions are modulo `2^n`. Define

```
S = a+b
T = R_r(d XOR S)
U = c+T
Y = R_q(b XOR U)
w = S+Y
L = a XOR b XOR R_q(b XOR c) XOR R_(r+q)(a XOR b XOR d).
```

Write `K1=a XOR b XOR S`, which is the carry-into-bit word of the fixed first addition, and set

\[
j=(i-q)\bmod n,\qquad k=(i-r-q)\bmod n,
\]

\[
\sigma=(-1)^{(K1)_i\oplus(K1)_k}.
\]

The map `d -> T -> U` is a permutation of the `n`-bit words, with inverse `d=R_(-r)(U-c) XOR S`. Thus `U` is uniform. The exact carry identity gives

\[
\boxed{C_i(a,b,c)=\sigma E_U[(-1)^{\beta_j\oplus\gamma_i}],}
\]

where

\[
\beta_j=[U\bmod2^j<c\bmod2^j],\qquad
\gamma_i=[(S\bmod2^i)+(Y\bmod2^i)\ge2^i].
\]

In particular, the random part depends on `n,q,i,S,b,c`, but not on `r`. Changing `r` can change only the known sign `sigma`, so the absolute correlation is independent of `r` for fixed other parameters. This is an immediate change-of-variable consequence, not a new security result.

## 3. Nonwrapped case: i>=q

Here `j=i-q`. The final-addition carry first consumes source bits `U[n-q,n)` through output positions `0,...,q-1`, then consumes `U[0,j)` through positions `q,...,i-1`. Since `i<n`, we have `j<n-q`; these two source blocks are disjoint.

The first block is uniform even after XOR with the fixed bits of `b`. Consequently the carry entering position `q` has distribution

\[
\Pr[\gamma_q=1]=(S\bmod2^q)/2^q.
\]

It is independent of the remaining source bits. Initialize a four-state process with `beta_0=0` and that Bernoulli `gamma_q`. For `t=0,...,j-1`, average the two possible values `u=U_t`, using

\[
\beta'=[c_t+\beta>u],
\qquad
\gamma'=\left\lfloor\frac{S_{q+t}+(u\oplus b_t)+\gamma}{2}\right\rfloor.
\]

At the end the state is `(beta_j,gamma_i)`. If `q=0`, the initial carry is zero. If `i=q`, there are no shared-source steps, which is handled by the same formula.

## 4. Wrapped case: i<q

Set `d0=n-q`; then `j=d0+i<n`. The subtraction borrow first consumes `U[0,d0)`, while the final carry starts at zero and consumes only `U[d0,d0+i)`.

The initial borrow distribution is

\[
\Pr[\beta_{d0}=1]=(c\bmod2^{d0})/2^{d0},
\]

independent of the shared source block. Initialize `(beta_d0,gamma_0)` with this Bernoulli borrow and zero carry. For `t=0,...,i-1`, let `p=d0+t` and average `u=U_p` with

\[
\beta'=[c_p+\beta>u],
\qquad
\gamma'=\left\lfloor\frac{S_t+(u\oplus b_p)+\gamma}{2}\right\rfloor.
\]

Again the terminal state is `(beta_j,gamma_i)`. When `i=0`, the shared block is empty and its signed expectation is taken from the initial borrow distribution.

## 5. Exact integer evaluation and resource bound

No general-purpose solver is needed. Order states as `2*beta+gamma`. In the first case, initialize integer counts with denominator `2^q`:

\[
(2^q-(S\bmod2^q),\ S\bmod2^q,\ 0,\ 0).
\]

In the second case, initialize counts with denominator `2^d0`:

\[
(2^{d0}-(c\bmod2^{d0}),\ 0,\ c\bmod2^{d0},\ 0).
\]

Each shared-bit step sends each state's count along the two transitions `u=0,1` and doubles the denominator. The terminal signed numerator is `count00-count01-count10+count11`, multiplied by `sigma`.

There are `j` shared steps in the first case and `i` in the second. The final denominator is respectively `2^i` or `2^j`, both at most `2^(n-1)`. Every count is nonnegative and bounded by the denominator. Therefore the evaluator uses `O(n)` integer arithmetic operations on `O(n)`-bit integers, `O(n)` auxiliary bits, and an `O(n^2)` elementary bit-operation upper bound for the counting loop. Rational reduction of the final answer is a separate standard integer-gcd cost.

The transition kernels have four states and average one unbiased input bit against fixed bits of `c,S,b`. They are an ordinary instance of signed finite-state analysis of constant operations. The two initial Bernoulli distributions are elementary exact prefix averages. This construction supplies no reason to assign originality beyond L0; increasing the sample or parameter search would not change that classification.

The established general context is Niu, Beyne, Hu and Wang, [Cryptanalytic Properties of Mealy Machines, CRYPTO 2026](https://link.springer.com/chapter/10.1007/978-3-032-35412-9_13), and the project's separately attributed [method comparison](../../literature/METHOD_COMPARISON.md). The present note does not claim that the paper prints this particular fixed-abc coefficient.

## 6. Predetermined checks and negative controls

For each of the 188 small-word inputs, the program compares the original `w XOR L` bit directly with the derived constant-sign-plus-two-carries expression. It then compares the complete average over `d` with the four-state evaluator. This is a discovering-agent self-check, not an independent implementation review.

Two explicit failure controls were selected before running:

- With `(n,r,q,a,b,c,i)=(4,0,3,7,9,0,0)`, the true correlation is `-1`. Dropping `sigma` would give `+1`.
- With `(n,r,q,a,b,c,i)=(2,0,0,1,2,1,1)`, the two random carry bits are complementary. The true correlation is `-1`, while multiplying their marginal signed expectations gives `0`.

Useful exact limiting identities are

\[
c=0\implies C_i=\sigma\left(1-2(S\bmod2^i)/2^i\right),
\]

\[
S=0\implies C_i=\sigma\left(1-2(c\bmod2^j)/2^j\right).
\]

These follow because one of the two carries is identically zero. The selected controls and standard examples include positive, zero, and negative coefficients.

Actual execution results, hashes, and the decision to stop this scout are recorded in `RUN.md` after the bounded run. A changed coefficient under a changed input distribution will not be treated as an original observation or an attack.
