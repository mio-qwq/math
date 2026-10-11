# Independent fixed-`a,b,c`, uniform-`d` distribution verification

Status: **L0 model calibration, mathematically proved and independently checked on a bounded set of original inputs.** This is an elementary application of carry/borrow state counting. There is no novelty, best-attack, fixed-key cipher, or full-ChaCha security claim.

This derivation and `independent_fixed_abc.py` were completed before the verifier read the discovery `scouting/fixed_abc/SCOUT.md`, implementation, result JSON, or run report. The parent supplied the original word model and requested a four-state distribution check; this is independent verification of a specified model, not independent discovery. The verifier had previously derived and reviewed the general first-output carry identity. Earlier frozen raw enumeration files are used only for the explicitly identified three-distribution comparison.

## 1. Exact model and constant phase

Let `n >= 1`, `0 <= r,q < n`, and `0 <= i < n`. All words have `n` bits, additions are modulo `2^n`, and bits are numbered from the least significant bit. Fix `a,b,c`; draw only `d` uniformly. Write

\[
S=a+b,\quad T=R_r(d\mathbin\oplus S),\quad
U=c+T,\quad Y=R_q(b\mathbin\oplus U),\quad w=S+Y.
\]

Here `R` denotes left rotation. Let `L` be the output of the same expression with all three additions replaced by XOR, including the first addition of the fixed inputs. Set

\[
\alpha=S\oplus a\oplus b,\quad
\beta=U\oplus c\oplus T,\quad
\gamma=w\oplus S\oplus Y.
\]

These are the incoming carry words. Expanding the two nested XOR/rotation layers directly gives

\[
w\oplus L=\alpha\oplus R_{r+q}(\alpha)
 \oplus R_q(\beta)\oplus\gamma.
\]

Thus, with

\[
j=(i-q)\bmod n,\quad k=(i-r-q)\bmod n,
\quad\phi=\alpha_i\oplus\alpha_k,
\]

the bit error is exactly `phi XOR beta_j XOR gamma_i`. The first carry phase `phi` is a constant; it must not be discarded.

The map `d -> T -> U` is a permutation of the `n`-bit words: XOR by a fixed word, rotation, then addition of a fixed word are all bijections. Consequently `U` is uniform with independent uniform bits, and `T=U-c`. The incoming carry of `c+T` is the incoming borrow of `U-c`. In threshold form,

\[
\beta_j=[U\bmod2^j<c\bmod2^j],\qquad
\gamma_i=[S\bmod2^i+Y\bmod2^i\ge2^i].
\]

These comparisons also handle bit zero correctly: both are false at their zero boundary. We therefore have the exact signed correlation

\[
C_i(a,b,c)=(-1)^\phi\,2^{-n}
\sum_{U=0}^{2^n-1}
(-1)^{[U\bmod2^j<c\bmod2^j]+[S\bmod2^i+R_q(b\oplus U)\bmod2^i\ge2^i]}.
\]

The sum is a mathematical identity, not an efficient evaluation prescription. Its use in the verifier is limited to the seven small settings listed below. In this distribution, `r` affects `C_i` only through the constant phase: for fixed `n,q,i,a,b,c`, the magnitude is independent of `r`. This follows from the permutation argument, not from a sample pattern.

## 2. Two exact support intervals

All intervals below are half-open bit intervals. A `Y` bit at position `t` uses the `U` bit at `(t-q) mod n`, XORed with the corresponding fixed `b` bit.

### Case A: `i >= q`

Here `j=i-q`. The borrow uses `U[0,j)`. The low `i` bits of `Y`, in carry-propagation order, use

\[
U[n-q,n)\quad\hbox{followed by}\quad U[0,j).
\]

The first block has length `q` and is independent of the overlap, since `j=i-q<n-q`. When `q=0`, the first block is empty. XOR by the fixed `b` bits preserves its uniform distribution. The incoming final-addition carry at the end of that independent prefix has probability

\[
\Pr(\kappa_q=1)=\frac{S\bmod2^q}{2^q}.
\]

The borrow starts at zero. With state index `2*rho+kappa`, initial integer weights are

\[
(2^q-S_q,\ S_q,\ 0,\ 0),\qquad S_q=S\bmod2^q.
\]

For each `h=0,...,j-1`, process one shared uniform bit `u=U_h` through

\[
\rho'=[c_h+\rho>u],\qquad
\kappa'=[S_{q+h}+(b_h\oplus u)+\kappa\ge2].
\]

Sum both bit choices into the new four weights. The denominator after all shared bits is `2^(q+j)=2^i`. No unobserved high `U` bits need to be enumerated: they have already averaged out.

### Case B: `i < q`

Let `d_0=n-q`; here `j=d_0+i`. The borrow uses `U[0,j)`, while the low `i` bits of `Y` use exactly `U[d_0,j)`, in the same order. The independent prefix is now `U[0,d_0)`, which only drives the borrow. Its endpoint probability is

\[
\Pr(\rho_{d_0}=1)=\frac{c\bmod2^{d_0}}{2^{d_0}}.
\]

The final-addition carry starts at zero. Initial integer weights are

\[
(2^{d_0}-c_{d_0},\ 0,\ c_{d_0},\ 0),\qquad
c_{d_0}=c\bmod2^{d_0}.
\]

For `t=0,...,i-1`, put `h=d_0+t` and apply

\[
\rho'=[c_h+\rho>U_h],\qquad
\kappa'=[S_t+(b_h\oplus U_h)+\kappa\ge2].
\]

The denominator is `2^(d_0+i)=2^j`. At `i=0`, the overlap is empty, and only the independent borrow endpoint and constant phase remain.

### Terminal sign and invariant

In either case, for terminal weights `(v_0,v_1,v_2,v_3)` and denominator `N`,

\[
C_i=(-1)^\phi\frac{v_0-v_1-v_2+v_3}{N}.
\]

The exact invariant is that a weight equals the number of assignments of the processed independent prefix and shared bits yielding its borrow/carry state. Initialization follows from the two threshold counts. Each update extends assignments by the two choices of one previously unused uniform bit, and the displayed recurrences are exactly binary subtraction/addition. Induction therefore proves the terminal distribution for every allowed word size and parameter. This general proof does not rely on the finite checks below.

## 3. Complexity and boundary interpretation

For one selected output bit, at most `n-1` relevant bits are summarized or processed. There are four live integer weights and at most eight transitions per shared bit. The recurrence uses `O(n)` exact integer additions and `O(n)` auxiliary bits: every weight is nonnegative, and their total is at most `2^(n-1)`. The initial threshold count is obtained directly, without a prefix array. Scalar word values and indices also fit in `O(n)` bits. A straightforward implementation has a schoolbook `O(n^2)` bit-cost bound for counting and bit extraction; final exact-fraction normalization must be charged as well. An arithmetic-operation claim is not a linear bit-time or benchmark claim. Computing all `n` output bits independently costs `O(n^2)` arithmetic operations, with output storage accounted separately.

The formulas include `n=1`, zero rotations, `i=0`, `i=q`, empty overlap, and zero fixed words. They describe fixed inputs to this one quarter-round relation. They do not establish a distribution for an actual ChaCha state with a fixed secret key, where several other positions and subsequent rounds impose different dependencies.

For the RFC quarter-round ordering, `w` is the complete quarter-round first output word: the operations after the third addition do not change that word. This observation does not extend the calculation to other outputs, their joint distribution, or the full cipher.

## 4. Independent bounded evidence

Actual command, executed successfully with exit code zero:

```sh
python workstreams/CRYPTO/projects/chacha-three-add/scouting/fixed_abc/verification/independent_fixed_abc.py
```

Working directory: `/workspace/scratch/5f0455e66649/math-crypto`.

The preselected settings `(n,r,q,a,b,c)` were:

| n | r | q | a | b | c | Number of original d inputs |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | 1 | 1 | 1 | 2 |
| 3 | 1 | 0 | 3 | 5 | 2 | 8 |
| 3 | 2 | 2 | 3 | 1 | 6 | 8 |
| 4 | 1 | 3 | 5 | 7 | 9 | 16 |
| 4 | 2 | 2 | 7 | 9 | 13 | 16 |
| 5 | 4 | 2 | 13 | 17 | 23 | 32 |
| 3 | 1 | 1 | 0 | 0 | 0 | 8 |

All **90 original inputs** and **23 bit correlations** agree across:

1. Literal original word arithmetic and separately computed XOR-linearized word, enumerating `d`.
2. An independent threshold sum over `U`, assembling output bits explicitly and computing the first carry phase by prefix-addition thresholds.
3. The four-state integer recurrence, computing the first carry word by `S XOR a XOR b`.

The different carry-phase calculations and rotation implementations reduce shared implementation assumptions. They do not constitute formal verification or human peer review. Complete raw signed counts, state weights, environment, source hash, and exact fractions are in `independent_run.json`. No random sampling, fixed-word search, or large-word enumeration was used.

The constant-phase negative control is `(n,r,q,i,a,b,c)=(3,2,2,0,3,1,6)`. Its exact correlation is `-1`; omitting the constant phase gives the wrong value `+1`.

The conditional-distribution control is `(n,r,q,i)=(3,1,1,2)`:

| Distribution | Exact signed correlation |
|---|---:|
| a,b,c,d all uniform | -3/16 |
| a=0 fixed; b,c,d uniform | 1/8 |
| a=b=c=0 fixed; d uniform | 1 |

The first two entries are read from the previously frozen original-word enumeration records; their SHA-256 values are in this new receipt. The third is checked by original words in the seven-setting run. At `a=b=c=0`, every original addition has a zero operand and the equality `w=L` is pointwise, providing an independent elementary check of the value one. These different distributions should not be substituted for one another.

## 5. Review boundary and freezing

This file, the independent source, and its run receipt are the pre-disclosure independent stage. Their hashes are frozen in `INDEPENDENT_STAGE_MANIFEST.json` before opening the discovery fixed-input files. Any subsequent comparison with those files is an ordinary proof/code review, recorded separately. Earlier verification manifests and streaming-review files are unchanged.
