# A stronger restriction from coupling both SHA-256 small sigmas

**Candidate computer-assisted lemma; independent-agent review pending.**
The proof below uses a fully recorded propositional contradiction, checked
by reverse unit propagation. A solver's UNSAT status is not a premise.
The original global schedule distance bound remains 13, with no genuine
distance-13 message pair and no complete support exclusion in this note.

## 1. Precise statements

All words belong to R=Z/(2^32), with bit 0 the least significant bit.
Let f and g be the original SHA-256 small sigma0 and sigma1:

```
f(x) = ROTR7(x) XOR ROTR18(x) XOR SHR3(x)
g(x) = ROTR17(x) XOR ROTR19(x) XOR SHR10(x)
```

The operations are those of
[FIPS 180-4, Sections 4.1.2 and 6.2.2](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf).
All base words remain arbitrary.

**Local theorem.** There are no four words p,p',q,q' such that

```
p'-p = q'-q = D != 0,
4096 divides D,
g(q')-g(q) = -D,
f(p')-f(p) = -(f(q')-f(q)).
```

Here divisibility of a residue means divisibility of its unsigned
representative, equivalently equality of the corresponding low input
bits. No word is fixed to zero and D is not set to a constant.

**Schedule corollary.** On each frozen support numbered 0,1,2,4,8,9,
the common nonzero difference specified in Section 5 has valuation at
most **11**. This strengthens the earlier valuation-at-most-12
restriction for those six supports by using sigma0 compatibility on a
second actual word pair. No sharpness for the new bound is asserted.

## 2. Reduction to one exact XOR mask

The complete low-12 mask lemma in
`../local-review/INDEPENDENT_PROOF.md` states that every nontrivial
collision of h(x)=x+g(x) with common low twelve bits has

```
q XOR q' = K = 0xfbca7000,
g(q) XOR g(q') = g(K) = 0x763e9000.
```

That lemma has its own complete certificate: the low-12 binary kernel
has dimension eight, and 254 of its 255 nonzero masks fail a necessary
carry condition. The only surviving mask is K. It is a necessary
classification, not a completeness claim about all base-word solutions.

The local theorem's h-collision and divisibility assumptions therefore
force q'=q XOR K. Its remaining equations are precisely

```
q+g(q) = q'+g(q')                         (E1)
p'+q = p+q'                             (E2)
f(p')+f(q') = f(p)+f(q)                  (E3)
```

as equalities in R. In particular, E2 has not dropped the common input
difference, and E3 computes both f derivatives on the same word pairs
as E1 and E2. It suffices to prove this three-equality system impossible
with q,p,p' all unconstrained 32-bit words.

## 3. Exact finite encoding

`build_cnf.py` builds a Boolean circuit for E1–E3. It introduces 96 free
input bits, one variable constrained to false, and gate variables. The
bits of q' are the corresponding q literals, complemented exactly at
the set bits of K. Both sigmas are constructed directly by selecting
their rotation/shift input bits and XORing; the absent SHR input is
the false variable.

Addition uses a ripple carry with carry-in false:

```
t_i = a_i XOR b_i
s_i = t_i XOR c_i
c_(i+1) = (a_i AND b_i) OR (t_i AND c_i).
```

Only bits 0 through 31 of each sum are retained. There is no condition
on final overflow; the final unused carry need not be created. Thus
addition is exactly modulo 2^32. Each of the three equations compares
all 32 resulting bits.

For a gate z=a XOR b, the clauses are

```
(-a OR -b OR -z), (a OR b OR -z),
(a OR -b OR z), (-a OR b OR z).
```

For z=a AND b they are

```
(-a OR -b OR z), (a OR -z), (b OR -z),
```

and for z=a OR b they are

```
(a OR b OR -z), (-a OR z), (-b OR z).
```

An equality a=b contributes `(-a OR b)` and `(a OR -b)`.
These truth-table equivalences also hold for signed input literals.
Induction along the circuit proves that its satisfying assignments
project exactly to the word solutions of E1–E3, and that any such word
solution has a consistent gate extension. Thus the encoding does not
exclude a word assignment by adding an auxiliary assumption.

The recorded CNF has **1,423 variables and 4,939 clauses**. Exact bytes:

```
boundary.cnf
f7baab8106897f1359fe20e69ac350a088f486b47260dc0825a4f1ce3c162262
```

The input literals, false variable and gate list are also recorded in
`circuit.json`. Independent review must check the sigma constants,
literal complement mask, equations, all bit positions and modular
overflow convention, not just the propositional proof.

## 4. An independently checkable contradiction

The search produced `boundary.drup`, SHA256

```
223d0c90cd7d7bf3ee85a290371828c27974691c348fb93fe8e88aacebe4c8f7
```

It has 19,460 clause additions and 10,328 deletions. The last added
clause is empty. Every addition is checked by **reverse unit
propagation (RUP)**: negate all literals of the proposed clause,
temporarily assume those negations, and derive contradiction by ordinary
unit propagation using only original and previously checked clauses.

RUP soundness is elementary. If the preceding clauses had a model
falsifying the new clause, that model would satisfy all temporary
assumptions; each forced unit would remain true in it, so a unit
contradiction is impossible. Therefore a RUP clause is entailed by the
preceding clauses. Induction shows all accepted additions are entailed
by the original CNF. An accepted empty clause proves the original CNF
has no model.

The checker safely ignores deletions: retaining earlier entailed
clauses preserves this induction. This is RUP-only verification; there
is no unverified RAT transformation, solver oracle call, trusted learned
clause, or initial empty clause. `check_drup.py` imports only the Python
standard library and actually accepted all 19,460 additions and the
final empty clause. It also emits `boundary.rup.jsonl`: every added
clause is accompanied by the ordered IDs of clauses used as units and
for the terminal conflict. This allows a second verifier to check the
proof without reproducing the watch-list implementation.

Proof production used Glucose3 through PySAT 1.9.dev15 and a 200,000
conflict budget; it completed with 19,460 conflicts. The particular
solver, budget and measured search time do not affect the proof's
validity. DRUP is a standard proof format, documented by
[PySAT](https://pysathq.github.io/docs/html/api/solvers.html) and the
[DRAT-trim project](https://github.com/marijnheule/drat-trim).
No claim of a new generic SAT method is made.

The contradiction, together with the low-12 mask lemma, proves the
local theorem. No claim is based on the earlier exploratory SMT UNSAT.

## 5. Exact bridges to six full support patterns

For two actual expansions write d_i=W'_i-W_i and define F_i,G_i as
the f and g differences on that same pair. Subtracting the original
recurrence gives

```
d_t = G_(t-2)+d_(t-7)+F_(t-15)+d_(t-16), 16<=t<64.
```

Use the following values of u from the frozen support file:

| Support | u | p index=u+7 | q index=u+14 | r index=u+22 |
|---|---:|---:|---:|---:|
| 0 | 30 | 37 | 44 | 52 |
| 1 | 31 | 38 | 45 | 53 |
| 2 | 32 | 39 | 46 | 54 |
| 4 | 33 | 40 | 47 | 55 |
| 8 | 29 | 36 | 43 | 51 |
| 9 | 29 | 36 | 43 | 51 |

In each row the original recurrences at
`u+7,u+14,u+16,u+22,u+29` reduce, respectively, to

```
d_p=d_u,
d_q=d_p,
0=G_q+d_u,
d_r=F_p,
0=d_r+F_q.
```

Thus D=d_p=d_q=d_u is nonzero (all these coordinates are active),
G_q=-D, and F_p=-F_q. These are exactly the local theorem's premises
except the hypothetical divisibility by 4096, which is consequently
impossible. All thirty substitutions retain the exact support, use
only recurrence indices 16 through 63, and include the distinct early
boundaries of supports 8 and 9. They do not assume either base block
is zero or replace the actual base equations with independent inputs.

The source remains commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`, the exact support copy
`../supports-v2.json`, SHA256
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.
These conditional consequences do not rerun or reprove the old
fifteen-support classification.

## Limits and review gate

The theorem excludes a divisibility stratum of six possible supports.
It does not exclude any one of those supports entirely, construct
complete message blocks, establish global distance 14, estimate a
differential probability, or supply a SHA collision attack.

The finite proof is not a Lean formalization. Independent-agent review
must bind the exact word-to-CNF correspondence, RUP evidence, low-12
dependency and all thirty support substitutions. Its receipt is kept
separately and distinguishes AI checking from human peer review.
