# Independent review: the low-12 coupled-sigma obstruction

**Verdict: PASS for the precisely stated local theorem and its seven
conditional support applications.** This is independent AI mathematical
and finite-certificate checking, not human peer review, Lean
formalization, main integration, or a new global distance bound.

The reviewed author text is `../coupled-boundary/PROOF.md`, SHA256
`36dd1c96de0aef7572a4e3973480a989de5d5b50b530a95fde14f7b840e0acc6`,
and its separately frozen support-5 addendum is `SUPPORT5.md`, SHA256
`38bb2204f2ae853e4d4d0ba20f71e5d013bc67012a00713c9ca14135497037ab`.
`REVIEW_RECEIPT.json` pins the complete reviewed dependency list.

## 1. Accepted mathematical statement

All arithmetic differences and sums here are in (R=\mathbb Z/(2^{32})).
Let (f=\sigma_0) and (g=\sigma_1) be the original SHA-256 small sigmas,
with the rotations and shifts specified by
[FIPS 180-4, §4.1.2][fips]. There are no arbitrary words (p,p',q,q')
satisfying all of

\[
p'-p=q'-q=D\ne0,\qquad 2^{12}\mid D,
\]
\[
g(q')-g(q)=-D,\qquad
f(p')-f(p)=-\bigl(f(q')-f(q)\bigr).
\]

Divisibility refers to a residue's unsigned representative. Since
(2^{12}\mid2^{32}), it is equivalently equality of the low twelve
bits of either word pair. No base word is fixed to zero. No fixed
**additive** difference is substituted for (D).

The proof has three logically separate parts: a complete necessary
XOR-mask classification, an exact CNF of the surviving case, and a
verified propositional contradiction. Their combination is valid for
all base words.

## 2. Independence and the word-to-CNF mapping

Before reading `coupled-boundary/`, this reviewer wrote
`RECONSTRUCTION.md` and `reconstruct.py` directly from the three
supplied equations and the original sigma definitions. The alleged
UNSAT result and reported source sizes were already known, which is
explicitly disclosed. `RECONSTRUCTION_FREEZE.json` records the files
frozen before source comparison.

The independent encoding uses three-input XOR/majority truth tables,
**667 variables and 4,753 clauses**. Its exact CNF hash is

```
4624329575e3cb0c187c521befb923e4296ba87eaa054c8b05caac7f37caa256
```

It retains 96 arbitrary input bits for (p,p',q). The value
(q'=q\oplus\mathtt{fbca7000}) is a literal complement pattern. All six
sums in the three equalities are evaluated modulo (2^{32}). The final
carry is discarded. This independent encoding returned UNSAT under
CaDiCaL195, but **that solver result is not a proof premise**.

After freezing this reconstruction, `audit_mapping.py` independently
recognized the author's recorded graph and accounted for every clause
of the CNF that the certificate actually proves unsatisfiable. It does
not import or execute the author's builder. It checked:

- 96 distinct free input bits, one false constant, and no undeclared or
  multiply defined variable;
- all 1,326 gates, their signed input literals and topological order;
- all six original sigma computations, including each rotation/shift
  source bit and each missing logical-shift bit;
- six ripple additions, three complete 32-bit equalities, and no final
  carry constraint;
- exact equality, as clause multisets, between the 4,939 recorded
  clauses and all required gate, constant, and equality clauses.

The author's two-input gate clauses are equivalent to their Boolean
functions. The full-adder identity gives the word addition by induction
through bits 0–31. Acyclic gate equivalences give every word assignment a
unique gate extension. Consequently the source CNF is satisfiable
exactly when the displayed three modular equations admit a solution.
The extra variables introduce no base-word assumption.

`MAPPING_RUN.json` records this comparison. Six corruptions were rejected:
a wrong complement mask, a wrong sigma source bit, identification of two
free base bits, a missing gate clause, an extra unit assumption, and a
damaged equality. Separately, the precomparison reconstruction evaluated
99 deterministic input fixtures, including nonzero basis and overflow
cases: 594 sigma words and 594 sums matched a direct integer
implementation. A corrupted gate bit, wrong constant and wrong rotation
were detected. These fixtures check implementations; universality comes
from the gate/adder equivalences, not sample coverage.

## 3. The complete RUP proof was independently replayed

The exact source CNF is `boundary.cnf`, SHA256

```
f7baab8106897f1359fe20e69ac350a088f486b47260dc0825a4f1ce3c162262
```

The original proof is `boundary.drup`, SHA256

```
223d0c90cd7d7bf3ee85a290371828c27974691c348fb93fe8e88aacebe4c8f7
```

The hints are `boundary.rup.jsonl`, SHA256

```
cd1845cdde5fca010b4b8557bcb27947eb5aef50b45856619cce7d54608540c5
```

`check_hints.py` is a separate standard-library verifier. It does not
import the author's checker or use its watch-list algorithm. For each
proposed clause, it assumes the negation of every literal and checks
the specified prior clause IDs sequentially. Each hinted clause must
have exactly one unassigned literal, which is then forced, or be the
final all-false conflict. Satisfied and nonunit clauses cannot act as
hints. Future IDs are rejected. Every recorded addition is compared
literally with the corresponding addition in the original DRUP file.

The full replay accepted **19,460 additions**, performed **2,278,157
unit inferences**, and checked the final empty clause. There was no
initial empty clause. The verifier ignored **10,328 deletions**, retained
only original or already proved clauses, and found no missing or extra
hint row. `RUP_RUN.json` records the complete replay, and `RUNS.json`
records the actual exit code 0. The first replay took about 1.78 seconds
internally; the frozen run record gives the measured final invocation.

The logical justification for retaining deletions is direct. Inductively
assume every prior added clause follows from the original CNF. If a
model of the original CNF falsified the next clause, it would satisfy
the temporary negations. Each verified unit step would preserve
consistency with that model, so the recorded conflict would be
impossible. Thus the new clause is entailed by the original CNF. This
induction remains valid when old entailed clauses are retained, and the
entailed empty clause proves unsatisfiability. No RAT rule, solver
oracle, or unproved learned clause is used.

Six negative controls exercise future IDs, satisfied hints, nonunit
hints, a missing conflict, trailing hints after conflict, and a damaged
target literal. All were rejected, while a small valid implication
control passed. The exact full input evidence, not those controls,
establishes the recorded contradiction.

## 4. The low-12 dependency was checked in full

The relevant prior certificate is
`../local-review/independent_certificate.json`, SHA256
`5a884c9a2af33e15ea04ec1a62b40e30d733f4d6f42f13975dfcc05661b1d342`.
The mathematical necessity argument in its companion proof is sound:
for a collision of (h(x)=x+g(x)), put (d=x\oplus y) and (e=g(d)).
The signed bit differences of the two summands have a carry in
(\{-1,0,1\}). If the preceding bit of both masks is zero, that
incoming carry must be zero. Exactly one active mask at the next bit
would give an odd total, which is impossible. Bit zero starts with
carry zero. There is no restriction that the final signed carry be
zero, so this remains a modular argument.

For equal low twelve input bits, both (d) and (g(d)) have zero low
twelve bits. `audit_dependencies.py` rebuilt the resulting 24 binary
equations using row elimination, instead of the prior checker's column
elimination. The rank is 24 and the kernel dimension is eight. It
reconstructed all 255 nonzero masks and compared **every** supplied
selector, mask, sigma image and first obstructing bit. Precisely 254
masks fail the proved carry condition. The sole survivor is

\[
d=\mathtt{fbca7000},\qquad g(d)=\mathtt{763e9000}.
\]

The first obstruction counts sum to 254; there is exactly one survivor.
The survivor is only a necessary mask, not a claim that all base values
with that mask collide. The already reviewed CNF keeps the complete
base-word equations for this remaining mask and excludes them jointly.
That establishes the local theorem in Section 1.

For the signed-power corollary cited by the support-5 addendum, the
review also independently checked all 528 contiguous carry-run input
masks. There is one same-start interval image; the two actual input
pairs compatible with that full-width carry run have unequal (h).
This verifies the needed previously established exclusion of
(D=\pm2^k), including modular wraparound. It is not a new claim made
by this review. The unrelated low-13 classification and earlier large
support/potential enumerations were not replayed here.

## 5. All seven actual-schedule bridges are valid

Subtracting the original FIPS schedule recurrence gives

\[
d_t=G_{t-2}+d_{t-7}+F_{t-15}+d_{t-16},\qquad16\le t<64,
\]

where every difference is taken on the same actual word pair. An
inactive coordinate makes its (d,F,G) terms all zero. The support
input is the exact frozen `supports-v2.json`, hash
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.

For supports 0, 1, 2, 4, 8 and 9, the 30 claimed substitutions all
match that original recurrence. With the author's (u), (p=u+7),
(q=u+14), (r=u+22), they give

\[
d_p=d_u,\quad d_q=d_p,\quad G_q=-d_u,\quad
d_r=F_p,\quad F_q=-d_r.
\]

The required (u,p,q,r) are active. Therefore (D=d_u=d_p=d_q\ne0),
(G_q=-D), and (F_p=-F_q), exactly as the local theorem requires.

Support 5 requires a separate orientation. Its six original equations
at (t=24,19,26,33,23,32) give

\[
d_{17}=-d_8=D\ne0,\quad G_{17}=d_{19}=d_{26}=-D,
\quad F_8=F_{17}.
\]

Choose (q=W_{17},q'=W'_{17}), but choose
(p=W'_8,p'=W_8). Then **both** the input difference and the (f)
difference at coordinate 8 reverse sign. Thus
(p'-p=D) and (f(p')-f(p)=-F_8=-F_{17}). This is a valid instance
of the same local theorem. Reversing only one of these two differences
would be invalid; the review's two orientation controls reject it.

| Support | Nonzero difference subject to the conclusion |
|---:|---|
| 0 | (D=d_{30}=d_{37}=d_{44}) |
| 1 | (D=d_{31}=d_{38}=d_{45}) |
| 2 | (D=d_{32}=d_{39}=d_{46}) |
| 4 | (D=d_{33}=d_{40}=d_{47}) |
| 5 | (D=d_{17}=-d_8) |
| 8 | (D=d_{29}=d_{36}=d_{43}) |
| 9 | (D=d_{29}=d_{36}=d_{43}) |

For each row, (2^{12}\nmid D), equivalently **(v_2(D)\le11)**.
`DEPENDENCY_RUN.json` retains all 36 full source-equation term lists
and their surviving terms. Its seven negative controls reject damaged
mask tables, a damaged basis, removal of an active (D) coordinate,
and either incorrect one-sided orientation reversal.

No equation before (t=16) was introduced. No actual base recurrence
was replaced by an unjustified sufficient lifting condition: the
local system is used as a necessary consequence of the actual
recurrences, and its impossibility excludes only the stated divisibility
stratum. All original input blocks remain arbitrary.

## 6. Reproduction and limits

The independent certificate review itself needs only Python's standard
library. From the repository root:

```
python workstreams/CRYPTO3-20261012/sha256-word-distance/coupled-review/audit_mapping.py
python workstreams/CRYPTO3-20261012/sha256-word-distance/coupled-review/check_hints.py
python workstreams/CRYPTO3-20261012/sha256-word-distance/coupled-review/audit_dependencies.py
```

The optional precomparison solver cross-check additionally uses PySAT;
it is not needed to replay the accepted proof. `RUNS.json`,
`REVIEW_RECEIPT.json`, and `SHA256.json` bind the executed code, outputs,
source dependencies, and reconstruction order.
The three review commands above are read-only by default; `--record`
must be explicitly supplied to save a new run record.

The conclusion does **not** eliminate any entire size-13 support,
establish distance 14, supply a pair of real input blocks, or determine
an endpoint differential probability. The actual lower bound remains
13. The old 735-node support classification and 5,308,416 potential
inequalities are outside this review's replay scope. No historical
priority or new generic SAT method is asserted.

[fips]: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
