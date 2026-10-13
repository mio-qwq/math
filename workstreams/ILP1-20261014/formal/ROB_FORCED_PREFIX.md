# First-clear decomposition of actual non-delay executions

Status: LEAN_VERIFIED, 18 audited declarations; independent review pending
for this increment. The fixed environment is Lean 4.34.1 (commit
`5045d0056413266e57c625dcd7c365b10e377c52`), Std-only, no Mathlib.

This is an actual-model structure bridge for the written prefix-macro
argument. It does not assume a macro recurrence or an optimality inequality.
It does not by itself claim a fully formalized dynamic program or a new
historical result.

## Definitions

`Clear s` means every completed job lies strictly before `s.retired`, with
all those prefix jobs complete. `prefixState n b r` is this state with eager
admission `min n (r+b)`; it is coherent for `r ≤ n`. Every coherent clear
state equals the corresponding `prefixState` by actual field equality.

`ForcedTail dep w s actions final` uses the existing `ROBStep` at resources
`b = w+1`. It has exactly two constructors:

* Stop with no action when `Clear s`.
* If `¬Clear s`, execute the actual all-ready action `CanIssue dep s`,
  then continue as another `ForcedTail`.

The guards make this a **first-clear** segment: it cannot stop at a
nonclear state or continue once it reaches a clear state. Its endpoint is
clear. If its initial state is coherent, each step is non-delay and it is
an actual `Profile` retaining precisely the same actions and endpoints.

`PrefixMacro dep w s actions final` consists of one actual non-delay step
from a clear state, then a `ForcedTail` from that step's successor. It always
has at least one cycle. The definition permits terminal idle macros;
the decomposition theorem below explicitly assumes the start is
nonterminal. Strict growth and acyclicity are a later proof obligation.

## Closed results

1. `step_unique`: actual completion union, maximal retirement, and eager
   admission determine the next state uniquely from the start and action.
   Even coherence of the start is unnecessary for this equality theorem.
2. `nonclear_step_unique`: from a coherent nonclear state at `B=W+1`, two
   actual non-delay steps have equal action predicates and equal successors.
   The proof uses the previously proved `ready+holes ≤ B` count bound.
3. `forcedTail_unique`: two forced tails from the same state have exactly
   the same action list and final state. Stop/continue mismatches contradict
   the first-clear guards; equal actual first actions give equal successors.
4. `forcedTail_exists`: for arbitrary finite forward dependencies and
   positive width, every coherent state has a forced tail of length at most
   `N - completedCountOfState s`. The endpoint remains coherent. The proof
   is strong induction on the genuine number of unfinished jobs, using the
   already proved actual non-delay step progress. It does not assume a
   surrounding finishing schedule. Empty and already clear states stop at
   length zero.
5. `profile_first_clear`: every finishing non-delay actual profile splits
   as `actions = first ++ rest`, with a forced tail for `first` and the
   actual original profile suffix for `rest`. Coherence of the start and
   `final.retired=N` suffice; neither forwardness nor positive width is
   needed once that finishing profile is given.
6. `profile_first_macro`: if the start is additionally clear and
   nonterminal, the same profile splits into an actual `PrefixMacro` and
   its original remaining profile. The first macro has at least one cycle,
   and stops at the first subsequent clear state.

This establishes the action-level first-clear decomposition, including
the omitted-oldest case: no oldest-first assumption occurs anywhere.
All original unit-latency, no-same-cycle-dependency, eager admission, and
in-order unlimited retirement semantics remain inherited from `ROBStep`.

## Verification

```
python workstreams/ILP1-20261014/formal/verify_forced_prefix.py \
  --lean /path/to/lean-4.34.1-linux/bin/lean --proc-self-compat
```

The runner rebuilds the complete import chain into a fresh temporary
directory, fixes Lean 4.34.1, and records source hashes, real output,
durations, and all `#print axioms` results under
`subagents/lean/evidence/rob-forced-prefix/`. The sandbox-only compatibility
flag is documented in the original Lean environment note.

The 18 new audit endpoints have no axioms beyond standard `propext`,
`Classical.choice`, and `Quot.sound`; several are axiom-free. No `sorry`,
`admit`, or custom axiom is introduced. Earlier reviewed Lean modules
are unchanged.

Remaining work: prove the positive macro endpoint advance and `N-r`
length bound, connect macro concatenation and decomposition to optimal
continuation costs, then prove any executable first-action enumeration
and dynamic program correct. The current module does not formalize the
algorithmic complexity bound or the general excess-window XP extension.
