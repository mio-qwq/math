"""Exact R1 eager-ROB solver. No third-party dependencies.

All instructions execute once. Forward data edges and next-cycle results only.
Nonempty ready subsets of size <= width are all explored: no greedy pruning.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
import argparse
import json


@dataclass(frozen=True)
class Program:
    n: int
    edges: tuple[tuple[int, int], ...] = ()

    def __post_init__(self):
        if type(self.n) is not int or self.n < 0:
            raise ValueError("n must be a nonnegative integer")
        for i, j in self.edges:
            if type(i) is not int or type(j) is not int or not 0 <= i < j < self.n:
                raise ValueError("edges must be forward and within the program")

    @property
    def predecessors(self):
        out = [0] * self.n
        for i, j in self.edges:
            out[j] |= 1 << i
        return tuple(out)


def resources(b: int, w: int):
    if type(b) is not int or type(w) is not int or b < 1 or w < 1:
        raise ValueError("B and W must be positive integers")


def retired(done: int, n: int):
    missing = ((1 << n) - 1) ^ done
    return n if missing == 0 else (missing & -missing).bit_length() - 1


def subsets(items, w):
    for k in range(1, min(w, len(items)) + 1):
        yield from combinations(items, k)


def solve(program: Program, b: int, w: int, certificate=False):
    resources(b, w)
    n, pred = program.n, program.predecessors
    terminal = (1 << n) - 1
    chosen, values = {}, {}

    @lru_cache(None)
    def value(done):
        if done == terminal:
            values[done] = 0
            return 0
        r = retired(done, n)
        ready = [j for j in range(r, min(n, r+b))
                 if not (done >> j) & 1 and pred[j] & done == pred[j]]
        best = n + 1
        for action in subsets(ready, w):
            new = done | sum(1 << j for j in action)
            cost = 1 + value(new)
            if cost < best:
                best, chosen[done] = cost, action
        assert best <= n - done.bit_count()
        values[done] = best
        return best

    optimum = value(0)
    schedule, done = [], 0
    while done != terminal:
        action = chosen[done]
        schedule.append(list(action))
        done |= sum(1 << j for j in action)
    result = {"n": n, "edges": [list(e) for e in program.edges],
              "B": b, "W": w, "cycles": optimum, "schedule": schedule,
              "ipc": n/optimum if n else None, "states": len(values)}
    if certificate:
        result["potential"] = {str(k): v for k, v in sorted(values.items())}
    return result


def augmented_edges(program, b):
    resources(b, 1)
    return tuple(sorted(set(program.edges) |
                        {(i, j) for j in range(program.n) for i in range(max(0,j-b+1))}))


def earliest_times(program, b):
    """O(N+|E|) recurrence without materializing quadratic artificial edges."""
    resources(b, 1)
    pred = [[] for _ in range(program.n)]
    for i, j in program.edges:
        pred[j].append(i)
    times, prefix = [], []
    for j in range(program.n):
        previous = max((times[i] for i in pred[j]), default=-1)
        if j >= b:
            previous = max(previous, prefix[j-b])
        t = previous + 1
        times.append(t)
        prefix.append(max(t, prefix[-1] if prefix else -1))
    return times


def required_window(times):
    """Exact B for a fixed time map (data and width checked separately)."""
    return max([1] + [j-i+1 for j in range(len(times)) for i in range(j)
                      if times[i] >= times[j]])


def schedule_times(schedule, n):
    times = [-1] * n
    for t, action in enumerate(schedule):
        for j in action:
            if not 0 <= j < n or times[j] != -1:
                raise ValueError("out-of-range or repeated instruction")
            times[j] = t
    if any(t < 0 for t in times):
        raise ValueError("incomplete schedule")
    return times


def greedy(program, b, w, priority="oldest"):
    resources(b, w)
    n, pred = program.n, program.predecessors
    done, terminal, schedule = 0, (1 << n)-1, []
    critical = [1]*n
    for j in range(n-1, -1, -1):
        for i, k in program.edges:
            if i == j:
                critical[i] = max(critical[i], 1+critical[k])
    while done != terminal:
        r = retired(done, n)
        ready = [j for j in range(r,min(n,r+b))
                 if not (done >> j)&1 and pred[j]&done == pred[j]]
        if priority == "critical":
            ready.sort(key=lambda j:(-critical[j],j))
        elif priority != "oldest":
            raise ValueError("unknown priority")
        action = ready[:w]
        schedule.append(action)
        done |= sum(1 << j for j in action)
    return schedule


def main():
    p = argparse.ArgumentParser()
    p.add_argument("instance", help="JSON object with n, edges, B, W")
    p.add_argument("--certificate", action="store_true")
    args = p.parse_args()
    with open(args.instance) as f:
        x = json.load(f)
    print(json.dumps(solve(Program(x["n"], tuple(map(tuple,x["edges"]))),
                           x["B"], x["W"], args.certificate), indent=2))


if __name__ == "__main__":
    main()
