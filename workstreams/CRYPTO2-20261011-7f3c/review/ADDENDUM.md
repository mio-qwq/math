# Review addendum: MDS inheritance under periodic restriction

**Amended verdict:** PASS for the universal existence theorem and PASS for the new branch-number inequality and MDS-inheritance lemma. One ancillary sentence in the pinned proof is misleading, or false if read as an assertion of possible nonpreservation, and requires correction. My previous review repeated that misleading implication; this addendum explicitly corrects it. The main proof does not depend on it and remains valid.

## Preserved review record

No earlier review artifact or parent proof was edited. The relevant immutable hashes are:

* Original `PROOF.md`: `5526707c49ab8864f54a11c816f6bebd95bf981115577dc584ab25c221956fd4`.
* `PRE-DISCLOSURE.md`: `4204393f57b58417536e2db262e12e7dcd2648917cda7c86db3ea732a1ffc92a`.
* Original `REVIEW.md`: `957c0364ffa4d9848a915223cadb262880af95c376506c771fa376cd525a193b`.

The parent identified the possible strengthening after the original review and asked for independent assessment. The analysis below independently verifies the statement and its implications. It is not a claim that I independently discovered the strengthening before being told it.

## Independent verification of the branch-number inequality

For a square matrix A of order m over any field, define its differential Hamming branch number by

\[
\beta(A)=\min_{0\ne x\in K^m}\bigl(\operatorname{wt}(x)+\operatorname{wt}(Ax)\bigr).
\]

This minimum is well defined even for an infinite field: the set of achieved weights is a nonempty subset of a finite set of integers.

Let M be an n-by-n circulant, let d divide n, and write n=td. With the first-column convention, define the period-d circulant B by

\[
b_r=\sum_{k=0}^{t-1}a_{r+kd},\qquad B_{rs}=b_{r-s\bmod d}.
\]

Let J repeat a d-vector t times, so \((Jx)_i=x_{i\bmod d}\). The already verified identity is MJ=JB. For every nonzero x in K^d, Jx is nonzero and

\[
\begin{aligned}
 t\bigl(\operatorname{wt}(x)+\operatorname{wt}(Bx)\bigr)
 &=\operatorname{wt}(Jx)+\operatorname{wt}(JBx)\\
 &=\operatorname{wt}(Jx)+\operatorname{wt}(MJx)\\
 &\ge\beta(M).
\end{aligned}
\]

The parenthesized quantity is an integer, so it is at least \(\lceil\beta(M)/t\rceil\). Taking the minimum over nonzero x proves

\[
\boxed{\beta(B)\ge\left\lceil\frac{\beta(M)}{t}\right\rceil.}
\]

**The inequality is correct for every divisor d and over every field.** It does not require invertibility, MDS, characteristic 2, or finiteness of the field. In particular, multiplication by t in this calculation is multiplication of integer Hamming weights, not multiplication by the field element t; characteristic 2 creates no exception when t=2.

## MDS inheritance, including the exact equivalence used

For an m-by-m matrix A, the following equivalence holds over every field:

\[
 A\text{ has every square submatrix nonsingular}
 \quad\Longleftrightarrow\quad \beta(A)=m+1.
\]

To check it directly, suppose a square r-by-r minor is singular. A nonzero kernel vector, extended by zero outside the selected columns, gives an input of weight at most r and an output with at least r zero coordinates. Hence \(\beta(A)\le m\). Conversely, if every square minor is nonsingular and x has support size r, Ax cannot have r zero coordinates: restricting to those rows and the input support would give a nonzero vector in the kernel of an r-by-r minor. Therefore \(\operatorname{wt}(Ax)\ge m-r+1\), and every nonzero x has total weight at least m+1. The universal upper bound \(\beta(A)\le m+1\) follows by testing any coordinate vector.

If M is MDS of order n=td, the inequality now gives

\[
\beta(B)\ge\left\lceil\frac{td+1}{t}\right\rceil=d+1.
\]

Since \(\beta(B)\le d+1\), equality holds, and B is MDS. Thus:

> Every period-d quotient of an MDS circulant, for every positive divisor d of its order, is MDS.

This assertion includes d=1 and d=n. It is stronger than the invertibility-inheritance statement in the original proof, and is compatible with it. It does not imply that an arbitrary compression of an MDS matrix is MDS; the exact repetition identity is the essential hypothesis here.

## Required corrections to the earlier wording

The pinned proof says:

> MDS need not be retained by a later quotient; only invertibility is needed.

If “need not” means “is not needed as a hypothesis of this proof,” its intended point is valid. If it means “may fail to be preserved,” it is false for the periodic quotient at issue. The ambiguity is substantive enough to remove. A precise replacement is:

> The periodic quotient of an MDS circulant is also MDS. For the full theorem about invertible circulants, only its invertibility is needed.

My original `REVIEW.md` likewise says that the reduction is “not invalidated by failure of MDS to descend to B.” I retract the implication that such failure can occur when M is MDS and B is this periodic quotient. The correct statement is that the existing full invertible proof is logically independent of MDS inheritance, while the additional inheritance lemma simplifies the MDS specialization.

The earlier review's conclusion that “no mathematical revision is required” must therefore be qualified: **the main theorem and its proof remain valid, but the quoted ancillary wording should be corrected.** None of the previously verified kernel, symmetric-block, convolution, or lifting constructions needs alteration. Statements merely saying that the proof did not assume MDS inheritance remain correct.

## Shorter solution for the source's remaining MDS cases

This strengthening gives a particularly short route for exactly the finite-field MDS question indicated by Kumar–Yadav–Samanta.

Let M be an MDS circulant of order n congruent to +2 or -2 modulo 12, with n>2. Then n=2d for an odd d>=3. Form the period-d quotient B using coefficient sums \(b_i=a_i+a_{i+d}\). The branch-number lemma proves that B is MDS. Reversing its row indices makes it symmetric, while preserving MDS and invertibility. The original odd symmetric MDS theorem supplies a nontrivial related-differential pair for this row-permuted B, hence for B itself. Repetition lifts it to a pair for M.

Thus the remaining MDS orders can be handled directly from the odd MDS base. **The non-MDS fallback is not needed for this MDS specialization.** It remains a valid and useful ingredient in the stronger theorem for all invertible circulants, since an arbitrary invertible M can be non-MDS and so can its quotient.

Source: Yogesh Kumar, Akshay Ankush Yadav, and Susanta Samanta, *Analyzing Linear Layers in Related-Differential Cryptanalysis*, arXiv:2605.27535v1:

* Odd symmetric MDS base, Theorem 4: https://arxiv.org/html/2605.27535v1#Thmtheorem4
* Covered circulant orders, Theorem 5: https://arxiv.org/html/2605.27535v1#Thmtheorem5
* Informal remaining-case direction, Section VI: https://arxiv.org/html/2605.27535v1#S6.p2

The earlier source audit still applies: Section VI does not print a fully quantified numbered conjecture, and nonzero distinct witnesses are required under the original convention. The d>=3 condition is necessary for invoking the odd base; n=2 is not covered by this reasoning or by the full theorem.

## Scope of this addendum

The corrected theorem is established by the symbolic argument above; no additional computation is needed to resolve this issue, and no enumeration was repeated. I have not reviewed an as-yet-unseen version-2 file or its hash. This addendum approves the stated strengthening and the specified wording repair, and preserves the original review history.

No historical novelty, external peer-review acceptance, Lean formalization, or cipher-attack claim follows from this mathematical assessment.
