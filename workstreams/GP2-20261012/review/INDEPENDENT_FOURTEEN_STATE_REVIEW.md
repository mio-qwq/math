# Independent review: the fourteen-state representation of strict four-window codes

## Verdict and binding

**PASS.** The all-alphabet representation, count-preserving completion, idempotence, and finite weighted optimization reformulation are correct. The proof does not determine the optimum and does not bound the number of alphabet blocks by fourteen.

The reviewed source is `../construction/FOURTEEN_STATE_REDUCTION.md`, SHA256:

`3cdcefd81b32054db42c9efb1c663d17e30e65d022cf95cf157a190958db6898`.

This review reconstructs the statement from full shift adjacency and literal window membership. The accompanying checker imports no discovery program. The theorem below concerns strict codes on a full alphabet, including repeated letters. Its application to the original directed Kautz general-position problem uses the separate repair and block-lift bridge, reviewed in `INDEPENDENT_REPAIR_REVIEW.md` (SHA256 `6f638a60f6724b2d5e01e112f4d7110a255f06dc84e0adf5be6becd88b9a9f2e`). No additional assumption that an arbitrary full-shift walk is a Kautz geodesic is made here.

## 1. Definitions and a direct overlap criterion

Let $A$ be a finite nonempty alphabet. A code $C\subseteq A^4$ is **strict** if every $x_0\cdots x_7\in A^8$ has at most two indices $i\in\{0,1,2,3,4\}$ with $x_i x_{i+1}x_{i+2}x_{i+3}\in C$. The indices, rather than the distinct selected words, are counted. Thus three occurrences of one periodic selected word violate strictness.

For $v\in C$, let $d_-(v)$ be the smallest $d\in\{1,2,3\}$ for which a selected word has suffix of length $4-d$ equal to the corresponding prefix of $v$. Put $d_-(v)=4$ if this does not occur. Define $d_+(v)$ using a suffix of $v$ and a prefix of a selected word.

Then

\[
C\text{ is strict}\quad\Longleftrightarrow\quad
d_-(v)+d_+(v)\ge5\quad\text{for every }v\in C.
\]

Indeed, any three selected occurrences in five consecutive windows have consecutive gaps $a,b\ge1$, with $a+b\le4$. The middle word has $d_-\le a$ and $d_+\le b$, so the displayed condition fails. Conversely, if it fails, both minimum gaps lie in $\{1,2,3\}$. Place their witnessing selected words on either side of $v$. The first witness occupies coordinates $[-d_-,3-d_-]$, the middle word coordinates $[0,3]$, and the last witness coordinates $[d_+,3+d_+]$. Any overlap between the witnesses lies inside the middle word, where both already agree with it. The words therefore glue consistently. Their total span is at most eight letters; pad with arbitrary letters if necessary. This gives three selected occurrences. Distinctness of the three words is unnecessary.

## 2. Reconstructing the fourteen profiles

Construct the full shift digraph on $A^3$ directly: each word $xyzt\in A^4$ gives the arc $xyz\to yzt$. All letters and loops are retained. A walk of length $t$ corresponds to one word of length $t+3$, so its selected-edge count is exactly its number of selected four-letter window occurrences.

For each state $s\in A^3$, define $F_t(s)$, for $0\le t\le5$, to be the largest number of selected edges on a $t$-arc walk ending at $s$. The initial state is unrestricted. Since the graph is finite and has incoming arcs at every state, these maxima exist. We have

\[
F_0(s)=0,\qquad F_t(s)\le F_{t+1}(s)\le F_t(s)+1.
\]

For the first inequality, prepend an incoming arc to a maximizing walk. For the second, delete the first arc of an arbitrary longer walk. Strictness is equivalent to $F_5(s)\le2$ for every state, directly from the length-eight word correspondence.

If $C\ne\varnothing$, choose one selected arc. From its endpoint, appending the three coordinates of any prescribed $s$ reaches $s$. The resulting four-arc walk has a selected edge; hence $F_4(s)\ge1$ for every $s$.

Consequently each sequence $F_0(s),\ldots,F_5(s)$ starts at zero, increases in steps of zero or one, reaches one by time four, and never exceeds two. Its unique description is

\[
h_t(a,b)=\mathbf 1_{a\le t}+\mathbf 1_{b\le t},\qquad
(a,b)\in P:=\{(a,b):1\le a\le4, a+1\le b\le6\}.
\]

Here $a$ is the first time the value becomes one, and $b=6$ means that it has not become two by time five. There are $5+4+3+2=14$ such profiles. This classification uses only the preceding path-count properties, without assuming any particular code construction.

## 3. Deriving every target transition

Call $p\to q$ allowed when

\[
h_t(q)\ge h_{t-1}(p)\qquad(1\le t\le5),
\]

and call it marked when the same five inequalities hold with an additional $1$ on the right. Every marked transition is allowed. For $p=(a,b)$ and $q=(c,d)$, these definitions give exactly

\[
\begin{aligned}
\text{allowed}:&\quad c\le a+1\quad\text{and}\quad (b\ge5\text{ or }d\le b+1),\\
\text{marked}:&\quad c=1,\quad b\ge5,\quad d\le a+1.
\end{aligned}
\]

For allowed transitions, the first source hit requires a first destination hit by time $a+1$. A second source hit creates a further constraint precisely when $b+1\le5$. These are all constraints. For a marked transition, time one forces $c=1$; time $a+1$ forces $d\le a+1$; and any source second hit by time four would require a destination count of three. Therefore $b\ge5$. These conditions conversely satisfy every inequality, as the source count at times zero through four is then either zero or one.

Let $p_0\to p_1\to\cdots\to p_t$ be an allowed walk of length $t\le5$, and let $e_j\in\{0,1\}$ indicate whether its $j$-th transition is marked. Use the transition inequality at time $j$:

\[
e_j\le h_j(p_j)-h_{j-1}(p_{j-1}).
\]

Summing gives

\[
\sum_{j=1}^t e_j\le h_t(p_t)-h_0(p_0)=h_t(p_t)\le2.
\]

This proves the five-walk restriction on the fixed graph. The independently generated graph has 138 allowed transitions and 20 marked transitions; these finite counts are checks, not premises of the proof.

## 4. Exact representation and preservation under completion

Suppose $\gamma:A^3\to P$ sends every full-shift arc to an allowed transition. Define

\[
C_\gamma=\{xyzt:\gamma(xyz)\to\gamma(yzt)\text{ is marked}\}.
\]

Every eight-letter word maps to an allowed five-arc walk, which has at most two marked transitions by Section 3. Thus $C_\gamma$ is strict, including for words with arbitrary repetitions.

Conversely, let $C\ne\varnothing$ be strict and assign to $s$ the profile of its counts $F_t(s)$. For any full-shift arc $u\to v$ represented by $w\in A^4$, appending that arc to a maximizing shorter walk proves

\[
F_t(v)\ge F_{t-1}(u)+\mathbf 1_{w\in C}\qquad(1\le t\le5).
\]

Every transition is therefore allowed, and every selected word maps to a marked transition. In particular, $C\subseteq C_\gamma$.

Write $G_t$ for the path-count maxima of the completed code $C_\gamma$. Along any walk of length $t\le5$, the inequalities defining allowed and marked transitions telescope exactly as in Section 3. Its completed selected-edge count is at most $h_t(\gamma(s))=F_t(s)$ at its endpoint. Taking the maximum gives $G_t(s)\le F_t(s)$. Containment gives the reverse inequality. Hence

\[
G_t(s)=F_t(s)\qquad\text{for every }s\in A^3,\quad0\le t\le5.
\]

This is equality of all count functions, not merely equality of their global maximum. The canonical profiles of the nonempty completed code consequently remain the same, so a second completion changes nothing.

For the empty code use the constant profile $(4,6)$. Its loop is allowed and unmarked, so the completed code is again empty. Idempotence holds here as well, even though this constant profile is not the all-zero count sequence. The separate treatment of the empty code is essential to the fourteen-profile statement.

Thus every strict code lies in an admissible marked code. Every inclusion-maximal strict code equals its completion. No monotonicity of the completion operation under arbitrary code inclusion, and no maximality of every completed code, is required or asserted.

## 5. Optimization and the original Kautz scope

For a fixed finite alphabet, maximizing over admissible assignments gives the same cardinality optimum as maximizing over all strict codes. One direction follows because every marked code is strict. For the other, complete an optimal strict code; containment cannot reduce its size.

The same argument applies to any nonnegative weight on the four-letter words, including weights equal to zero. In particular it applies to the product weight $\pi(x)\pi(y)\pi(z)\pi(t)$ of any probability distribution $\pi$ on a finite alphabet. By the separately reviewed repair and block-lift bridge, the original Kautz limiting density is therefore the supremum of these weighted marked-code densities over all finite alphabets and all admissible triple-profile assignments.

The variables are fourteen-valued labels on all triples. The result does not replace the alphabet by fourteen colors and does not establish a fixed bound on the alphabet size needed near the supremum. It also does not compute the maximum for a given alphabet. Its all-parameter conclusion is an exact structural reformulation of the strict-code problem, with the original directed GP conclusion obtained only through the separate bridge.

## 6. Independent executable checks

The standard-library checker `independent_fourteen_state_check.py` was executed successfully on 2026-10-12. It generates the profiles from all five-bit increment sequences satisfying the count conditions, before forming their hit-time labels. It tests both closed transition formulas against the five inequalities on all 196 ordered pairs, then computes exact maximum marked counts for every walk length from zero to five in the resulting target graph.

For each fixture below it independently builds the full shift graph from all four-letter words, computes every $F_t$, constructs the completion, checks containment and count preservation, and applies completion twice. It also enumerates every literal eight-letter word over that fixture's alphabet, counting occurrences with multiplicity, and checks the overlap criterion of Section 1.

| Fixture | Alphabet size | Original size | Completed size | Largest completed eight-word count |
|---|---:|---:|---:|---:|
| Empty code | 1 | 0 | 0 | 0 |
| Empty code | 2 | 0 | 0 | 0 |
| Singleton `0001` | 2 | 1 | 1 | 2 |
| `0100, 0110, 1110` | 2 | 3 | 3 | 2 |
| Explicit seven-word ternary subcode | 3 | 7 | 16 | 2 |
| Explicit eighteen-word ternary code | 3 | 18 | 18 | 2 |

The certificate lists the exact input and completed codes, every triple state, all six path-count rows, the assignments, and maximizing eight-word witnesses. The seven-word fixture confirms nontrivial completion: nine words are added while all six functions remain unchanged. The fixture is a semantic check and no finite optimality claim is made.

All fourteen negative controls passed. These include a constant selected word, a period-two selected word with three equal selected occurrences, three distinct overlapping words, incorrect word length, incorrect alphabet binding, duplicate input listing, corrupted profile counts, a corrupted parameter, a wrong source hash, changed selected objects, changed path counts, a wrong assignment, a corrupted completion, and an artificially marked target loop. The last creates a five-hit walk and is rejected by the independent target dynamic program.

Reproduce the frozen certificate without overwriting it:

```sh
python3 workstreams/GP2-20261012/review/independent_fourteen_state_check.py \
  --verify workstreams/GP2-20261012/review/independent_fourteen_state_certificate.json
```

To regenerate a fresh certificate, pass `--write` with a new filename; the program refuses to replace an existing file. The actual generation and replay logs are included.

| Artifact | SHA256 |
|---|---|
| `independent_fourteen_state_check.py` | `0a64d35beda77145499bea00fb334ec6e4c12250dcffd38e7ec6526712570b01` |
| `independent_fourteen_state_certificate.json` | `c32340afba1591fdd4e02f96490b43e5c357593d89342ec7392e072e3a6fb261` |
| `independent_fourteen_state_check.log` | `28583f8f809d46ce6da832a4ba7cbd3381fadebcefd7ded01d7301b6a1b40934` |
| `independent_fourteen_state_replay.log` | `ba4f90097c3a3b68b4c43f3411c706d6f463de2686d45e1c79a1e629129b44a2` |

The elementary proof establishes the all-alphabet result. The finite checks validate semantics and certificate binding. No Lean compilation, new axiom, optimal-density claim, historical-priority certification, or external human review is part of this review.
