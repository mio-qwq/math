"""Independent operational replay and Bellman lower-bound certificate checker.

Does not import rob.py. Uses sets/explicit admission and checks every successor;
trust is not delegated to the solver's claimed action list or state count.
"""
from itertools import combinations
import argparse
import json


def validate_instance(n, edges, b, w):
    if type(n) is not int or n < 0:
        raise ValueError("invalid size")
    if type(b) is not int or type(w) is not int or b <= 0 or w <= 0:
        raise ValueError("invalid resources")
    parents = [set() for _ in range(n)]
    for i, j in edges:
        if type(i) is not int or type(j) is not int or not 0 <= i < j < n:
            raise ValueError("invalid dependency")
        parents[j].add(i)
    return parents


def replay(n, edges, b, w, schedule):
    parents = validate_instance(n,edges,b,w)
    if n == 0 and schedule:
        raise ValueError("cycles after initial termination")
    completed, entered, head = set(), 0, 0
    for c, action in enumerate(schedule):
        while entered < n and entered-head < b:
            entered += 1
        if len(action) != len(set(action)) or len(action) > w:
            raise ValueError("duplicate instruction or excessive issue width")
        for j in action:
            if type(j) is not int or not head <= j < entered or j in completed:
                raise ValueError("instruction is not an incomplete window entry")
            if not parents[j] <= completed:
                raise ValueError("dependency is not complete before this cycle")
        completed.update(action)
        while head in completed:
            head += 1
        if head == n and c+1 < len(schedule):
            raise ValueError("cycles after termination")
    if len(completed) != n:
        raise ValueError("incomplete schedule")
    return len(schedule)


def check_certificate(x):
    n, edges, b, w = x["n"],x["edges"],x["B"],x["W"]
    parents = validate_instance(n,edges,b,w)
    cost = replay(n,edges,b,w,x["schedule"])
    if type(x["cycles"]) is not int or cost != x["cycles"]:
        raise ValueError("duration mismatch")
    potential = x["potential"]
    terminal = frozenset(range(n))

    def p(d):
        key = str(sum(2**j for j in d))
        if key not in potential or type(potential[key]) is not int or potential[key] < 0:
            raise ValueError("missing or invalid potential")
        return potential[key]

    queue, seen = [frozenset()], {frozenset()}
    while queue:
        d = queue.pop()
        if d == terminal:
            if p(d) != 0:
                raise ValueError("nonzero terminal potential")
            continue
        head = next(j for j in range(n) if j not in d)
        ready = [j for j in range(head,min(n,head+b))
                 if j not in d and parents[j] <= d]
        for k in range(1,min(len(ready),w)+1):
            for action in combinations(ready,k):
                after = d.union(action)
                if p(d) > 1+p(after):
                    raise ValueError("Bellman lower-bound inequality violated")
                if after not in seen:
                    seen.add(after)
                    queue.append(after)
    if p(frozenset()) != cost:
        raise ValueError("witness does not meet certified lower bound")
    return {"valid":True,"optimum":cost,"checked_states":len(seen)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate")
    args = parser.parse_args()
    with open(args.certificate) as f:
        print(json.dumps(check_certificate(json.load(f)),sort_keys=True))
