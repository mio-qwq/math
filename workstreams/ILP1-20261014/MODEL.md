# Eager ROB model R1

Research snapshot: 14 October 2026 (Asia/Singapore). This file defines a mathematical model, not a claim about all real processors. Indices in code and all formulas below are **zero based**.

## Program and semantics

A program has N >= 0 operations numbered 0,...,N-1 and a set E of dataflow edges (i,j) with 0 <= i < j < N. Every operation executes exactly once. Operations are deterministic pure functions of at most two operands and produce one value in the initial instruction class. An operand is an immutable external input or a previous operation's output. Duplicate reads of one output yield one graph edge. The solvers accept general forward DAGs; claims restricted to fan-in two say so explicitly.

For a mutable-register straight-line program, assign a fresh version to every write, and direct each read to its most recent earlier write (or the initial register version). Keep the version corresponding to the last write of each observable register. By induction over program order, every version has the same value as the corresponding sequential write. A topological execution computes those same values by induction over execution order. This proves semantic preservation for these pure operations and final outputs. This is syntactic producer/consumer dataflow: value-specific cancellation, dead-operation removal, algebraic rewriting and fewer instructions are not allowed. Names alone do not impose write-after-read or write-after-write edges after versioning.

Excluded: control flow, speculation, loads/stores and aliasing, caches, exceptions, side effects, multi-cycle latency, finite register storage, execution-port classes, admission/retirement bandwidth limits, same-cycle dependency forwarding and instruction transformations. All results depend on these exclusions.

## Parameters and cycle boundaries

B and W are positive integers. B is the capacity of entered but unretired operations, including completed operations blocked behind an earlier incomplete one. W is the issue limit per cycle. B>N and W>B are accepted, with no extra benefit beyond N and B respectively.

Cycles are numbered 0,1,... . At the beginning of cycle c, let D be the set completed in cycles strictly before c, and let

    r(D) = min({i in [0,N): i not in D} union {N}).

The contiguous prefix [0,r(D)) has retired. Eager in-order admission fills all available slots, so the window is [r(D), min(N,r(D)+B)). Already completed entries in this interval still occupy slots. Its incomplete ready set is

    A(D) = {j in [r(D),min(N,r(D)+B)) \ D : pred_E(j) subset D}.

An action is any S subset A(D) with |S|<=W. All members of S execute during c and complete at its end. The next state is D union S. All newly contiguous completed entries retire at that boundary, and new admission is available at the next cycle start. Dependencies within S cannot be satisfied by the current cycle. Empty actions are legal, but are unnecessary in an optimum. There are no external arrivals or time-dependent constraints.

Initial state is D=empty; terminal state is D=[0,N). An unfinished state always has ready operation r(D): every data predecessor is a smaller index and is already completed. Thus the sequential schedule ({0},{1},...,{N-1}) is legal, finishes in N cycles, and supplies a finite upper bound.

## Schedules and optimum

A schedule is a finite sequence of legal actions starting at empty and ending at the terminal set. Its duration includes any idle cycles before completion. An optimal schedule exists: a legal duration N exists, so the nonempty subset of feasible durations in the natural numbers has a least member. T*(E,B,W) denotes that member. For N>0, IPC*=N/T*. For N=0, T*=0 and IPC is left undefined (the software reports null). B=0 or W=0 is outside R1 and is rejected, including for the empty program.

An issue-time assignment t:[0,N)->natural numbers assigns each operation its cycle; its duration is 0 for N=0 and 1+max_j t(j) otherwise. It is feasible exactly when:

1. t(i)<t(j) for every (i,j) in E;
2. at most W operations have any one time value;
3. t(i)<t(j) whenever i+B<=j.

The full proof of this operational equivalence is in THEOREMS.md. Condition 3 adds **every prefix edge**, not only (j-B,j). The augmented DAG is E_B=E union {(i,j):i+B<=j<N}. Its topological order remains the original program order. Ordinary unit-job precedence scheduling on E_B is therefore exactly R1 scheduling, including schedules with idle cycles. This reduction is scoped to the admission and retirement rules above.

## Information models

The offline solver knows N, E, B and W. Its actions nevertheless obey the window. An online policy observes entered instructions, their operand producers, completion history and all previous observations; it does not observe the destinations of future uses in unentered instructions. N may be public. Two programs can share an initial visible prefix but require different optimal actions. Extra metadata such as future use lists or precomputed critical-path lengths is additional advice, not part of this online model.

## Boundary checks and convention traps

* B=1 or W=1 gives T*=N. A single operation takes one cycle. Empty input takes zero.
* Independent operations give ceil(N/min(B,W)); a full dependency chain gives N.
* For B>=N, E_B=E. For W>=B, resource constraints cannot delay an earliest feasible layer; T* is the augmented DAG height.
* Removing completed entries before earlier entries retire is a different model. Charging refill an extra cycle is a different model. Permitting same-cycle dependent issue is a different model.
* Offset edges alone are insufficient. For N=4, B=2, E=empty and W=2, t=(1,0,2,1) satisfies t(0)<t(2) and t(1)<t(3), but violates t(0)<t(3). In cycle 1, operation 3 is still outside the ROB: operation 0 has not yet completed. Independent replay rejects this assignment.
