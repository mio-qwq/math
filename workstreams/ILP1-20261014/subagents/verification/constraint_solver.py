"""Independent, finite-horizon assignment solver for the ILP1 ROB model.

The search variables are job execution times, not completed-instruction states.
The only dependencies are Python's standard library. Jobs and cycles are 0-based.
"""

from __future__ import annotations

from math import ceil


def validate_input(n, edges, B, W):
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if type(B) is not int or B <= 0 or type(W) is not int or W <= 0:
        raise ValueError("B and W must be positive integers")
    edges = sorted(set(tuple(e) for e in edges))
    if any(type(i) is not int or type(j) is not int or not (0 <= i < j < n)
           for i, j in edges):
        raise ValueError("dependencies must be forward edges within [0,n)")
    return edges


def augmented_edges(n, edges, B):
    """All prefix-release precedences, including every i <= j-B."""
    return sorted(set(edges) | {(i, j) for j in range(n) for i in range(j - B + 1)})


def bounds(n, edges):
    pred = [[] for _ in range(n)]
    succ = [[] for _ in range(n)]
    for i, j in edges:
        pred[j].append(i)
        succ[i].append(j)
    earliest = [0] * n
    tail = [0] * n
    for i in range(n):
        earliest[i] = max((earliest[p] + 1 for p in pred[i]), default=0)
    for i in reversed(range(n)):
        tail[i] = max((tail[s] + 1 for s in succ[i]), default=0)
    return pred, succ, earliest, tail


def feasible(n, edges, B, W, horizon, *, first_action=None):
    """Return execution times in range(horizon), or None if impossible.

    first_action, if supplied, fixes EXACTLY the set of jobs at cycle zero.
    No maximal-issue assumption is made. All job-time assignments are searched.
    """
    edges = validate_input(n, edges, B, W)
    if horizon < 0:
        return None
    if n == 0:
        return [] if first_action is None or not first_action else None
    if horizon == 0 or n > horizon * W:
        return None
    pred, succ, earliest, tail = bounds(n, augmented_edges(n, edges, B))
    latest = [horizon - 1 - d for d in tail]
    if any(a > b for a, b in zip(earliest, latest)):
        return None
    action = None if first_action is None else frozenset(first_action)
    if action is not None and (len(action) > W or any(i < 0 or i >= n for i in action)):
        return None
    assigned = [-1] * n
    used = [0] * horizon

    def visit(job):
        if job == n:
            return assigned.copy()
        lo = max((assigned[p] + 1 for p in pred[job]), default=0)
        hi = latest[job]
        if action is not None:
            if job in action:
                lo, hi = max(lo, 0), min(hi, 0)
            else:
                lo = max(lo, 1)
        for t in range(lo, hi + 1):
            if used[t] == W:
                continue
            assigned[job] = t
            used[t] += 1
            result = visit(job + 1)
            if result is not None:
                return result
            used[t] -= 1
        assigned[job] = -1
        return None

    return visit(0)


def times_to_schedule(times):
    if not times:
        return []
    return [[i for i, t in enumerate(times) if t == cycle]
            for cycle in range(max(times) + 1)]


def solve(n, edges, B, W):
    """Return exact optimum and a realizing schedule."""
    edges = validate_input(n, edges, B, W)
    if n == 0:
        return 0, []
    _, _, earliest, _ = bounds(n, augmented_edges(n, edges, B))
    lower = max(max(earliest) + 1, ceil(n / min(B, W)))
    for horizon in range(lower, n + 1):
        times = feasible(n, edges, B, W, horizon)
        if times is not None:
            schedule = times_to_schedule(times)
            assert operational_check(n, edges, B, W, schedule)
            return horizon, schedule
    raise AssertionError("sequential topological schedule must be feasible")


def operational_check(n, edges, B, W, schedule):
    """Independent direct ROB replay; no augmented precedences used here."""
    edges = validate_input(n, edges, B, W)
    pred = [set() for _ in range(n)]
    for i, j in edges:
        pred[j].add(i)
    completed, window = set(), set()
    admitted, retired = 0, 0
    for issue in schedule:
        while admitted < n and len(window) < B:
            window.add(admitted)
            admitted += 1
        issue_set = set(issue)
        if len(issue_set) != len(issue) or len(issue) > W:
            return False
        if not issue_set <= window - completed:
            return False
        if any(not pred[i] <= completed for i in issue_set):
            return False
        completed.update(issue_set)
        while retired in completed:
            window.remove(retired)
            retired += 1
    return completed == set(range(n))


def assignment_check(n, edges, B, W, schedule):
    """Test the candidate characterization independently of ROB replay."""
    edges = validate_input(n, edges, B, W)
    times = {}
    for t, jobs in enumerate(schedule):
        if len(jobs) > W:
            return False
        for i in jobs:
            if i in times or not 0 <= i < n:
                return False
            times[i] = t
    return (len(times) == n and all(times[i] < times[j]
                                  for i, j in augmented_edges(n, edges, B)))


def greedy(n, edges, B, W, priority="oldest"):
    """Deterministic work-conserving list policies; smaller index breaks ties."""
    edges = validate_input(n, edges, B, W)
    original_pred, _, _, tail = bounds(n, edges)
    if priority == "augmented_critical_path":
        _, _, _, tail = bounds(n, augmented_edges(n, edges, B))
    completed, schedule = set(), []
    retired = 0
    while len(completed) < n:
        ready = [i for i in range(retired, min(retired + B, n))
                 if i not in completed and set(original_pred[i]) <= completed]
        if priority == "oldest":
            ready.sort()
        elif priority in {"critical_path", "augmented_critical_path"}:
            ready.sort(key=lambda i: (-tail[i], i))
        else:
            raise ValueError(priority)
        issue = ready[:W]
        assert issue
        schedule.append(issue)
        completed.update(issue)
        while retired in completed:
            retired += 1
    assert operational_check(n, edges, B, W, schedule)
    return len(schedule), schedule


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("B", type=int)
    parser.add_argument("W", type=int)
    parser.add_argument("--edges", default="[]", help="JSON list of 0-based pairs")
    args = parser.parse_args()
    result = solve(args.n, json.loads(args.edges), args.B, args.W)
    print(json.dumps({"T": result[0], "schedule": result[1]}, indent=2))
