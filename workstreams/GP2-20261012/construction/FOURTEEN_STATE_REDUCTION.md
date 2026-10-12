# An exact fourteen-state representation of strict four-window codes

GP2-20261012, candidate structural theorem. This note concerns the strict window codes defined in `STRICT_WINDOW_REPAIR.md`. Combined with that note it describes the original Ka(m,4) limiting problem. It does not determine the optimum or assert that fourteen letter blocks suffice.

## 1. A complete local signature

Let `C subset A^4`, with `A` a finite nonempty alphabet. For a selected word `v`, let `d_in(v)` be the least `l in {1,2,3}` for which some word of `C` ends in `prefix_(4-l)(v)`; use the value four if no such `l` exists. Define `d_out(v)` analogously using a selected word starting in `suffix_(4-l)(v)`.

Then `C` is a strict code if and only if

`d_in(v)+d_out(v) >= 5` for every `v in C`.

Indeed, three selected occurrences at positions `0,a,a+b` give positive gaps with `a+b<=4`, and therefore the two matching fibers are nonempty. Conversely, selected words in the two matching fibers can be put to the left and right of `v`: the free coordinates of the two endpoints are outside `v` on opposite sides, so no additional consistency condition is needed. The resulting word has three selected occurrences within five consecutive windows. This equivalence counts repeated occurrences and uses the full shift graph; it does not assume that the resulting walk is a geodesic.

The four-valued signature is exact, but it is attached to already selected four-letter words. The next construction moves all variables to **three-letter states** and gives a fixed target graph.

## 2. Fourteen profiles and a fixed marked graph

Let

`P = {(a,b): 1<=a<=4, a+1<=b<=6}`.

There are fourteen profiles. For `p=(a,b)` and `0<=t<=5`, put

`h_t(p) = 1_(a<=t) + 1_(b<=t)`.

The value `b=6` means that a second hit has not occurred within five steps. Define a fixed directed graph `H` on `P`, retaining loops, by

`(a,b) -> (c,d)` is **allowed** exactly when

`c <= a+1` and `(b>=5 or d<=b+1)`.

An allowed arc is **marked** exactly when

`c=1`, `b>=5`, and `d<=a+1`.

The graph has 138 allowed arcs, of which twenty are marked. These counts are convenient checks, not assumptions in the theorem.

The definitions have the following equivalent interpretation:

- An arc `p->q` is allowed if and only if `h_t(q)>=h_(t-1)(p)` for every `1<=t<=5`.
- It is marked if and only if `h_t(q)>=h_(t-1)(p)+1` for every `1<=t<=5`.

For the first assertion, the first hit at time `a` must be present at the destination by `a+1`; the second hit gives another constraint exactly when `b+1<=5`. For the second, time one forces `c=1`, the first source hit forces `d<=a+1`, and a second source hit by time four would require three destination hits, which is impossible. These implications also prove the converses.

Every allowed walk of length five in `H` has at most two marked arcs. Apply the respective inequality along its first arc at `t=1`, its second arc at `t=2`, and so on: the number of marked arcs among the first `t` arcs is at most `h_t` of its endpoint. At `t=5` this is at most two.

## 3. Exact representation theorem

Write `B(A,3)` for the full de Bruijn digraph on triples from `A`: its arcs are `xyz -> yzt` for all `x,y,z,t in A`, including all repetitions. An **admissible profile assignment** is a function

`gamma: A^3 -> P`

which sends every such arc to an allowed arc of `H`. Its marked code is

`C_gamma = {xyzt in A^4 : gamma(xyz)->gamma(yzt) is marked}`.

**Theorem.** Every `C_gamma` is a strict code. Conversely, every strict code `C` has an admissible profile assignment with `C subset C_gamma`. When `C` is nonempty this assignment is canonically determined by the maximum counts defined below, and passing from `C` to `C_gamma` leaves all those maximum counts unchanged.

The first assertion follows immediately from the allowed-walk bound: an eight-letter word is a five-arc walk in `B(A,3)`, so at most two of its windows map to marked arcs.

For the converse, for each state `s in A^3` and `0<=t<=5`, define

`F_t(s) = maximum number of C-windows on a t-arc walk ending at s`,

where the starting state is unrestricted. Thus `F_0(s)=0`. Walks and repeated windows are counted with multiplicity. Every state has incoming arcs, so a maximizing walk can be extended by one arc at its beginning; hence `F_(t+1)(s)>=F_t(s)`. Removing the first arc of a `(t+1)`-arc walk shows `F_(t+1)(s)<=F_t(s)+1`. Strictness is precisely the bound `F_5(s)<=2` at all states.

If `C` is nonempty, choose one selected arc. Its endpoint can reach any prescribed triple by appending three letters, so a four-arc walk to every state contains a selected arc. Thus `F_4(s)>=1`. Consequently the sequence `F_0(s),...,F_5(s)` has the form `h_t(a,b)` for a unique pair `(a,b) in P`: `a` is its first time reaching one, and `b` is its first time reaching two, or six if it never reaches two by time five. Define `gamma(s)=(a,b)`.

For each arc `u->v` in the triple graph and each `1<=t<=5`, appending that arc to a maximizing `(t-1)`-arc walk gives

`F_t(v) >= F_(t-1)(u) + 1_C(the corresponding four-letter word)`.

The target-graph equivalences therefore show that every arc is allowed and every originally selected word is marked. This proves `C subset C_gamma`.

For the empty code use the constant assignment `(4,6)`, whose only used target arc is an unmarked loop.

To check preservation of the counts in the nonempty case, consider an arbitrary `t`-arc walk for the completed code. Every newly marked arc also satisfies all the `+1` profile inequalities, and every unmarked arc satisfies the zero inequality. The same successive-time argument bounds its count by `h_t` at the endpoint, which equals the original `F_t`. Therefore its new maximum is at most the old maximum; containment of the old code gives the reverse inequality. All six count functions agree.

It follows that this completion operation is idempotent. We do not assert that it is monotone under code inclusion, or that every completed code is globally maximal. Every inclusion-maximal strict code does equal its own completion, since the completion is a strict superset otherwise.

## 4. Consequence for exact optimization and the limiting problem

Let `w(r)` be the maximum size of a strict code in `[r]^4`. The theorem gives the exact finite reformulation

`w(r) = max_gamma |{xyzt : gamma(xyz)->gamma(yzt) is marked}|`,

where the maximum ranges over admissible assignments of fourteen profiles to the `r^3` triple states. The forward inequality uses that all such marked codes are strict. For the reverse inequality, complete an optimal strict code by its canonical assignment.

For a probability distribution on a finite alphabet, use its product weights on the four letters in the same formula. The completion only adds selected words and therefore cannot decrease a nonnegative weighted objective. Combining this result with Theorem 2 of `STRICT_WINDOW_REPAIR.md` gives an equivalent variational model for `lambda_4`: take the supremum of the weighted marked-edge density over finite alphabets and admissible triple-profile assignments.

This replaces an arbitrary four-ary selection relation by a ternary fourteen-valued relation plus an explicit fixed transition rule. An exact search can use `r^3` variables with fourteen values and `r^4` local transition constraints. This statement concerns the number and kind of variables; it is not a claim of a polynomial-time optimization algorithm. The transition constraints still enforce compatibility across every shared two-letter overlap.

Fourteen is a number of **profiles of triples**, not a bound on the number of alphabet blocks. A general assignment may depend on a three-letter relation that cannot be described by finitely many prescribed single-letter block types. No fixed optimal alphabet size, attainment of the supremum, or improved numerical lower bound is claimed.

## 5. Verification and scope

`verify_fourteen_state_reduction.py` reconstructs all fourteen profiles from their two hit times, checks the closed transition formulas against all five pointwise inequalities, and runs an exact five-step dynamic program on all 138 allowed target arcs. It then builds several small full triple graphs from shift adjacency, constructs their profiles from literal code membership, checks containment and exact profile preservation, and checks the completed codes directly on all eight-letter words. Corrupted target labels, a spurious marked loop, and a non-strict input code must fail.

The all-alphabet theorem rests on the elementary proof above. The small target-graph enumeration and example checks are semantic validation. There is no optimization claim, Lean compilation, historical-priority certification, or external human review in this note. The primary mathematical scope remains the original fixed-length-four part of Chandran et al., [arXiv:2604.15909v1, Problem 5.2](https://arxiv.org/html/2604.15909v1#S5), reached through the separately proved repair theorem.
