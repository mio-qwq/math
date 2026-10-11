# Independent mathematical audit of the streaming-prefix specification

Date: 2026-10-11. Status: **mathematical specification passed review and targeted checks**. No discovery streaming implementation was read before the initial version of this report and its first check run. The subsequent ordinary implementation review is documented separately in `CODE_REVIEW_REPORT.md`.

This append-only review leaves the preceding 22 verification artifacts and `INDEPENDENT_VERIFICATION_MANIFEST.json` unchanged. Their hashes were verified before and after the checks. The new harness is intentionally a small specification checker that can store all prefixes for `n<=4`; it is not a third production streaming implementation, and its storage behavior is not used to justify the proposed streaming space bound.

## 1. Conventions and kernel reconstruction

Use column state vectors. State `2*rho+kappa` records the subtraction borrow and final-addition carry **entering** the current bit. Rows index outgoing states and columns incoming states. The terminal functional is `f=(1,1,1,1)` and the initial state is `e0=(1,0,0,0)^T`.

In the uniform-word model each bit has eight equally likely choices `(s,b,y)`. In the fixed-first-word model each bit has four choices `(s,y)`, with

`b=(s-A_p-rho) mod 2`, `rho_next=[s-A_p-rho<0]`.

The independently reconstructed unmasked probability kernels are

\[
P_u=\frac18
\begin{pmatrix}
4&1&1&0\\
2&5&1&2\\
2&1&5&2\\
0&1&1&4
\end{pmatrix},
\]

\[
P_0=\frac14
\begin{pmatrix}
3&1&1&0\\
1&3&1&2\\
0&0&2&1\\
0&0&0&1
\end{pmatrix},\qquad
P_1=\frac14
\begin{pmatrix}
1&0&0&0\\
1&2&0&0\\
2&1&3&1\\
0&1&1&3
\end{pmatrix}.
\]

Here `P_0,P_1` depend on the current bit of the fixed word, not on a fixed whole-word value being zero or one. All three columns sum to one.

A separate 24-term Leibniz determinant calculation and exact Gaussian inverses give

\[
\det P_u=\det P_0=\det P_1=\frac1{16}.
\]

The full inverses are recorded in `matrix_spec_run.json`; both multiplication orders with each kernel give the identity. Their entries are half-integers. Their induced matrix one-norms are respectively `5,10,10`.

For a mask `B`, `Y`, or `BY`, define `P^mask` by including the sign of the indicated current input bits in the same transition sum. In particular, the fixed-word `B` sign uses the derived bit above. These masked kernels need not be invertible; the proposed method never requires their inverses.

## 2. Boundary phases: the ordering is essential

Normalize both rotation counts modulo `n` first. For the selected output bit `i`, let `k=(i-r-q) mod n`. At position `p`, define the diagonal phase

\[
D_p(\rho,\kappa)=
(-1)^{\rho[p=i]+\rho[p=k]+\kappa[p=i]}.
\]

All exponents are interpreted modulo two. Coincident borrow boundaries cancel. At bit zero the actual initial state has both carry bits zero, so the boundary contributes no sign to that state.

Since this observes incoming carries, the column-vector transition is

\[
T_p=P_pD_p,\qquad K_p^{\mathrm{mask}}=P_p^{\mathrm{mask}}D_p.
\]

The phase acts first. Each `D_p` is its own inverse, so

`T_p^-1=D_p P_p^-1`.

Every unmasked transition is therefore invertible. Reversing the phase order changes the statistic. A concrete check using original-word data gives

`n=3,r=q=0,i=0`: correct correlation `1`; using `D_p P_p` instead gives `1/2`.

## 3. Insertion operators and chronological order

Define the unmasked prefix

\[
G_0=I,\qquad G_t=T_{t-1}\cdots T_0.
\]

Then the proposed operator is

\[
H_p^{\mathrm{mask}}
=G_p^{-1}T_p^{-1}K_p^{\mathrm{mask}}G_p
=G_{p+1}^{-1}K_p^{\mathrm{mask}}G_p.
\]

For one inserted mask, cancellation gives

\[
fG_nH_p^{\mathrm{mask}}e_0
=fT_{n-1}\cdots T_{p+1}K_p^{\mathrm{mask}}T_{p-1}\cdots T_0e_0.
\]

For two distinct positions `a<b`, the correct order is

\[
fG_nH_b^{\mathrm{high}}H_a^{\mathrm{low}}e_0.
\]

Indeed `G_bG_{a+1}^{-1}=T_{b-1}\cdots T_{a+1}`, so the product expands to the literal chain with a masked transition at each of the two positions. The later chronological insertion occurs on the left. No commutativity of the transfer matrices is assumed.

The unmasked moment is `M0=fG_n e0`. These identities hold for both the constant uniform kernel and the bit-dependent fixed-word kernels.

### Same position: use one joint transition

If the `B` and `Y` masks refer to the same position, the event uses the sign of `b_p XOR y_p` on **one** bit transition. It must use

`fG_n H_p^BY e0`.

Replacing it by two single-mask insertion operators would require the generally false identity

`P^BY = P^B P^-1 P^Y`.

For example, in the uniform kernel, the `(row 0,column 0)` entry is `0` on the left and `1/16` on the right. The analogous identity also fails for both fixed-bit kernels. The old carry-elimination formula has these same-position terms precisely when the normalized rotation `q=0`; they cannot be omitted as an irrelevant edge case.

## 4. The mask pairs form one ordered segment

Let `j=(i-q) mod n`, with `0<=q<n`. The general correlation formula is

\[
C_i=2^{-j}\left(M_0-
\sum_{\substack{0\le l<i\\h=(l-q)\bmod n<j}}
2^hM_{h,l}\right).
\]

If `i>=q`, then `j=i-q`. For `l<q`, the wrapped index `h=n-q+l` cannot be below `j`; for `l>=q`, `h=l-q`. Thus the complete sum is

`h=t, l=q+t`, for `t=0,...,j-1`.

For `q>0`, its lower position is a `B` mask and its higher position a `Y` mask, separated by `d=q`. For `q=0`, they coincide and use the joint kernel. If `i=q`, the segment is empty.

If `i<q`, then every `l<i` is below `q`, and

`l=t, h=n-q+t`, for `t=0,...,i-1`.

The condition `h<j=n+i-q` holds automatically. The lower position is now a `Y` mask, the higher a `B` mask, and their distance is `d=n-q`. This order reversal must be reflected in the insertion product. If `i=0`, the segment is empty.

The two nonempty cases therefore use prefix positions `t` and `d+t`, both advancing by one. The rotation normalization is a necessary preprocessing step for these non-modular formulas.

## 5. A correct streaming schedule

For one fixed output bit and its corresponding boundary phases:

1. Compute `G_n` with the forward recurrence `G_(p+1)=T_p G_p`, then form the terminal row `R=fG_n`. Alternatively, a row-only pass must visit the transitions from `n-1` down to `0`; multiplying a row by transitions in increasing position order would reverse the intended product.
2. If the mask segment is empty, return `2^-j M0` immediately.
3. Initialize the low prefix and inverse at `G_0=G_0^-1=I`. Build the high prefix `G_d` and its inverse in a warm-up pass over positions below `d`.
4. At each pair, construct the required two insertion operators from the two current prefixes, or one joint operator for `q=0`, and add the appropriately weighted moment to one scalar accumulator.
5. Advance each maintained prefix and inverse using

   `G_(p+1)=T_p G_p`,

   `G_(p+1)^-1=G_p^-1 T_p^-1`.

   The inverse update multiplies on the right. Apply the transitions for the actual low and high positions respectively.

The `B`-mask weight is `2^t` in the first segment and `2^(d+t)` in the second; each can be maintained by doubling. Every requested higher position remains below `n` by the segment inequalities.

The terminal pass, high-prefix warm-up, and paired scan each have at most `n` steps. Every step uses a fixed number of four-by-four matrix operations. Thus the specification gives **`O(n)` exact rational arithmetic operations for one selected output bit**. Repeating it independently for every output bit takes `O(n^2)` such operations. The terminal matrix depends on `i` and `k`; it cannot be silently reused across different output bits without further justification.

This is streaming in the sense of retaining only the current prefixes and inverse prefixes. It is not necessarily a single-pass online algorithm over an external bit stream: the terminal calculation precedes the pair scan, and the fixed input word is available for bit access during each pass.

## 6. Why the inverse prefixes still require only linear bit space

The distinction between value growth and representation length matters. All entries of `T_p` have denominators dividing eight. Since `D_p` only changes column signs and the underlying probability kernels have column sum one,

`||T_p||_1=1`, and `||G_p||_1<=1`.

Consequently the entries of `G_p` have denominators dividing `8^p` and numerators of `O(p)` bits.

The computed inverse kernels have half-integer entries and one-norm at most ten. Therefore

`G_p^-1=T_0^-1 ... T_(p-1)^-1`

has entries with denominator dividing `2^p`, norm at most `10^p`, and numerator magnitude at most `20^p` when represented over that common denominator. Its entries also require only `O(p)` bits.

Furthermore, `|P_p^mask|` is entrywise bounded by `P_p`, so a masked kernel has one-norm at most one. Each insertion operator involves only a fixed number of prefix, inverse-prefix, and constant-kernel factors. Its entries have `O(p)`-bit numerators and denominators; for example, the displayed product has a denominator dividing `2^(4p+4)`. Multiplying two insertion operators and the terminal row still gives `O(n)`-bit intermediate fractions.

All these numbers are dyadic rationals. Across at most `n` weighted moment terms, a common denominator with exponent `O(n)` suffices; summation does not introduce a product of unrelated large denominators. The final `2^-j` factor and the weights `2^h` add at most `O(n)` bits. The accumulator consequently retains `O(n)`-bit operands as well.

Only a fixed number of four-by-four matrices, rows, and scalar accumulators need remain live. Hence the proposed schedule uses **`O(n)` auxiliary bits for one output bit**, including the stored fixed input word if present. Storing every prefix would instead use `O(n^2)` bits, and would not meet this stronger space claim. The small check harness deliberately uses that simpler storage only to test the specification at `n<=4`.

This proves an arithmetic-operation and storage bound. It is not `O(n)` elementary bit time. Exact multiplication, addition, denominator normalization and GCD costs must be charged to their `O(n)`-bit operands. A generic way to state the dependence is `O(n)` scalar rational operations, each with the applicable multiplication/GCD costs. No measured runtime advantage or improved published complexity follows from this operation count alone.

## 7. Targeted independent checks

Run:

```sh
python /workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add/verification/streaming_review/matrix_spec_checks.py
```

The first execution exited zero. It independently reconstructs all bit kernels, calculates the three determinants, checks both inverse identities, and compares the insertion formula with a literal masked transfer chain. It then checks 18 selected cases against existing direct original-word counts: 10 uniform cases and eight fixed-word cases, all at `n<=4`. They cover zero rotations, bit zero, empty segments, ordinary and wrapping mask pairs, fixed-word bits zero and one, and same-position masks. All 21 inserted moments and all 18 final correlations agree.

The two explicit negative controls above separate the wrong boundary-phase order and the wrong same-position product. No new original-word enumeration or large validation pipeline was run. The old 22-file manifest and every file listed in it matched their frozen hashes before and after the check.

Exact reconstructed matrices, inverses, determinant values, case selection, signed fractions, source hash, command, environment and timestamps are in `matrix_spec_run.json`.

## 8. Review status and originality boundary

The supplied insertion identity, the single-segment reduction, and the streaming arithmetic and auxiliary-space bounds are justified under the stated conventions. The review found no mathematical defect. Production-code inspection was pending at completion of this mathematical phase. It subsequently passed the separately identified ordinary review in `CODE_REVIEW_REPORT.md`; that later phase does not alter the provenance of the earlier mathematical check.

This is an application and optimization within established finite-state matrix techniques. This review makes no claim that the conjugation representation, streaming method, asymptotic evaluation cost, or associated correlations are novel relative to prior ARX literature. Such a conclusion requires the separate literature comparison.
