# Exact 18-word support-12 base/factor normal form

**Status: complete author-written bidirectional equivalence theorem, with a
deterministic symbolic term audit. Independent AI acceptance and Lean
formalisation remain separate.** This theorem neither supplies nor excludes a
solution.

All arithmetic is in (R=\mathbb Z/(2^{32})). Let (f=\sigma_0) and
(g=\sigma_1) be the SHA-256 small sigmas and write

\[
D_0(x,d)=f(x+d)-f(x),\qquad D_1(x,d)=g(x+d)-g(x).
\]

The exact support is

\[
S=\{10,11,13,15,18,20,26,28,29,34,42,43,57\}.
\]

## 1. Frozen accepted inputs

The proof composes exactly these previously accepted theorems. The hashes are
checked by `check_symbolic.py` before any symbolic assertion is evaluated.

1. `support12-full-factor-v9/PROOF.md`, SHA-256
   `efba27236a949965e8689462703b4ed675a0484c0c5a84302b621c59d9bd0395`,
   independently accepted by `support12-full-factor-review-v8/REVIEW_V9.md`,
   SHA-256
   `04cd55432d18f2abb3dbca2d16f651ceb4451ac550048c5b0e84db4c82da63e8`.
   It proves the exact thirteen-factor table and its seven distinct nonzero
   difference conditions.
2. `support12-base-lift-v8/PROOF.md`, SHA-256
   `40305b2a0ec9dc1d5776626cbde09cbaddb857cc24e627f6dabec20c7ee4ab3a`,
   independently accepted by `support12-base-review-v8/REVIEW.md`, SHA-256
   `8c3ab0fb544c487e065316149fcf791630062aea5bc359a3ead53f748e033527`.
   It proves the five-anchor interpolation bijection with residual rows 33 and
   57.
3. `support12-base-residual-v9/PROOF.md`, SHA-256
   `d9fcb05b5bd21bd7b34fd16fdd6df61c9d6a351dc4b83bd63b6d1b91c5dc808c`,
   independently accepted by `support12-base-residual-review-v9/REVIEW.md`,
   SHA-256
   `92017f34d561a9db3a4220c1c1f67fff429b54ff378ef3134cc900b239330cf0`.
   It proves that (H,R_{33}) are independent of the temporary (u_{57}),
   that (R_{57}=u_{57}-H), and that the word-57 factor must be evaluated at
   the forced first endpoint (H).

The v10 candidate and its fixed-seed 10,000-trial run are also hash-pinned and
replayed, but they are only a non-proof transcription control.

## 2. Eighteen free words and definitions

Take the eighteen freely quantified words

\[
 A;\quad X_{10},X_{11},X_{13},X_{15},X_{18},X_{20},X_{26},X_{28},
 X_{29},X_{34},X_{42},X_{43};\quad P_9,P_{12},P_{14},P_{19},P_{22}.
\]

Define, in the displayed order,

\[
\begin{aligned}
B&=-D_0(X_{10},A),& C&=-D_1(X_{43},-B),\\
K&=-D_1(X_{29},C),& P&=D_0(X_{11},B),\\
Q&=D_0(X_{13},C),& L&=D_0(X_{15},K),\\
T&=D_1(X_{26},P+A),& W&=D_0(X_{29},C),\\
Z&=D_0(X_{42},P+A).&&
\end{aligned}
\]

The letter (T) is used here for the v10 scalar called `S`, to avoid
confusion with the support set (S).

Run the accepted base chart with first endpoints (X_i) at the twelve
indices (S\setminus\{57\}), temporary (u_{57}=0), and the five displayed
anchors. Denote its words by (C_i), and put

\[
H=g(C_{55})+C_{50}+f(C_{42})+C_{41}.
\]

By the accepted sink lemma, this is the same (H) for every temporary
(u_{57}), and (R_{33}) is likewise unchanged.

## 3. The fourteen equations and seven inequalities

Let `NF` be the conjunction of (R_{33}=0), the following thirteen
equalities,

\[
\begin{array}{rclcrcl}
D_1(X_{15},K)&=&-A,&&D_0(X_{18},B)&=&-P-A,\\
D_1(X_{18},B)&=&-B-C,&&D_0(X_{20},-B)&=&-Q-T,\\
D_1(X_{20},-B)&=&-K,&&D_0(X_{26},P+A)&=&-B,\\
D_0(X_{28},Q+T)&=&-B,&&D_1(X_{28},Q+T)&=&-L,\\
D_0(X_{34},B)&=&-P-A,&&D_1(X_{34},B)&=&B-C,\\
D_1(X_{42},P+A)&=&-W-Q-T,&&D_0(X_{43},-B)&=&-P-A,\\
D_1(H,Z)&=&B,&&&
\end{array}
\]

and the seven exact-support conditions

\[
A,B,C,K,P+A,Q+T,Z\ne0. \tag{NF}
\]

These are fourteen word equalities, not fourteen independent scalar or bit
equations.

## 4. Definitional elimination lemma

Substitute the nine definitions into the 22 derivative requirements of the
accepted factor table. Exactly

```
10F, 11F, 13F, 15F, 26G, 29F, 29G, 42F, 43G
```

become the zero term. The other thirteen residual terms are exactly the
thirteen displayed equations, in the order

```
15G,18F,18G,20F,20G,26F,28F,28G,34F,34G,42G,43F,57G.
```

This proves both directions: under the definitions, all 22 original
requirements vanish if and only if the thirteen retained requirements
vanish. There is no division, cancellation by a possibly nonunit word, or
probabilistic identity test. The checker represents every expression as a
canonical additive combination of normalized function-application terms and
compares the resulting terms exactly.

The thirteen active differences in the accepted table are

\[
A,B,C,K,B,-B,P+A,Q+T,C,B,P+A,-B,Z.
\]

Their nonzero conjunction is therefore exactly the seven inequalities in
`NF`; the checker verifies the seven sign classes and their complete coverage.

Finally, (Z=D_0(X_{42},P+A)) is the actual word-42 (F)-difference and the
factor table gives (d_{57}=Z). The base chart forces the word-57 first
endpoint to (H), so its remaining condition is exactly
(D_1(H,Z)=B). This is the checked (42\to57\) cascade, not a free projected
`PG` witness.

## 5. Bidirectional equivalence theorem

**Theorem.** There exists a pair of genuine SHA-256 16-to-64 message
expansions whose wordwise difference has exact support (S) if and only if
there is an eighteen-word tuple from Section 2 satisfying `NF`.

### Forward implication

Let (U,V\in R^{64}) be genuine expansions and suppose their difference has
exact support (S). Orient every active pair from (U_i) to (V_i). From the
accepted full-factor theorem extract its scalars
(a,b,c,k,p,q,l,s,w,z), and set

\[
A=a,\quad X_i=U_i\ (i\in S\setminus\{57\}),\quad
P_j=U_j\ (j\in\{9,12,14,19,22\}).
\]

The factor equations at (10,43,29,11,13,15,26,29,42), in that order,
give precisely

\[
B=b,\ C=c,\ K=k,\ P=p,\ Q=q,\ L=l,\ T=s,\ W=w,\ Z=z.
\]

Thus the other thirteen factor equations become the thirteen equations in
`NF`, and exact support gives its seven inequalities. By the accepted base
bijection the chart reconstructed from (U|_S) and these anchors is (U),
so both residuals vanish. The sink lemma gives (U_{57}=H); since the actual
pair at 57 has (d_{57}=Z) and (G_{57}=B), it gives
(D_1(H,Z)=B). Hence (R_{33}=0) and the full `NF` holds.

### Reverse implication

Now suppose an eighteen-word tuple satisfies `NF`. Apply the definitions and
the base chart with temporary (u_{57}=0), compute (H), and replace its
active input by (u_{57}=H). Independence of (H,R_{33}), the assumed
(R_{33}=0), and (R_{57}=u_{57}-H) imply that the resulting 64-word vector
(U) is a genuine SHA-256 expansion.

Assign the thirteen differences by the accepted table, using the defined
(A,B,C,K,P,Q,L,T,W,Z), and put

\[
V_i=U_i+d_i\quad(i\in S),\qquad V_i=U_i\quad(i\notin S).
\]

At the twelve positions other than 57, the nine definitions and thirteen
retained equations say exactly that the (F,G) derivatives of the actual
pair ((U_i,V_i)) equal the accepted table entries. At 57, the first endpoint
is (H), the difference is (Z), and the last retained equation gives its
required (G)-derivative (B); its private (F_{57}) is unused through row
63. Hence all thirteen same-pair factor conditions hold. The accepted full
factor theorem now gives every one of the 48 schedule-difference rows.
Subtracting the recurrence for (U) from these rows shows that (V) also
satisfies all SHA-256 expansion recurrences. Both are therefore expansions of
their first sixteen words. The seven inequalities make every (d_i) on (S)
nonzero, while all other differences were set to zero, so the support is
exactly (S).

The two constructions are existential inverses at the level required by the
theorem; no uniqueness of the eighteen-word tuple is claimed.

## 6. Reproduction and boundary

From the repository root run

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-base-factor-normal-proof-v11/check_symbolic.py
```

The frozen output is `RUN.json`. The checker also replays the v10 fixed-seed
sampling and requires byte-equivalent JSON, explicitly recording it as
non-proof auxiliary evidence.

This theorem is an exact reformulation only. It does **not** establish that
`NF` is satisfiable or unsatisfiable, does not provide a distance-13 message
pair, does not prove distance at least 14, and is not an independent AI
review, human review, or Lean formalisation.
