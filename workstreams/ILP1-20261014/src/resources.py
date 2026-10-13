"""Exact unrestricted-issue window saturation, with compact certificates.

Time O((N+|E|) log N); the certificate needs only O(N) jobs/chain vertices.
This does not solve finite-width saturation in that time bound.
"""
from rob import Program, resources
from checker import validate_instance, replay


def height_certificate(program: Program, b: int):
    resources(b,1)
    pred=[[] for _ in range(program.n)]
    for i,j in program.edges: pred[j].append(i)
    times, previous, prefix=[] , [], []
    for j in range(program.n):
        candidates=pred[j].copy()
        if j>=b: candidates.append(prefix[j-b])
        parent=max(candidates,key=lambda i:times[i],default=None)
        previous.append(parent)
        times.append(0 if parent is None else times[parent]+1)
        prefix.append(j if not prefix or times[j]>times[prefix[-1]] else prefix[-1])
    path=[]
    node=prefix[-1] if prefix else None
    while node is not None:
        path.append(node)
        node=previous[node]
    return {"height":max(times,default=-1)+1,"times":times,"chain":list(reversed(path))}


def saturated_window(program: Program):
    n=program.n
    if n==0:
        raise ValueError("B_sat baseline B=N is defined here only for nonempty programs")
    original=height_certificate(program,n)
    height=original["height"]
    lo,hi=1,n
    while lo<hi:
        mid=(lo+hi)//2
        if height_certificate(program,mid)["height"]==height: hi=mid
        else: lo=mid+1
    attained=height_certificate(program,lo)
    schedule=[[] for _ in range(height)]
    for j,t in enumerate(attained["times"]):
        schedule[t].append(j)
    return {"kind":"unrestricted_issue_window_saturation", "n":n,
            "edges":[list(e) for e in program.edges],"B_sat":lo,"W":n,
            "cycles":height,"schedule":schedule,
            "original_critical_chain":original["chain"],
            "smaller_window_chain":height_certificate(program,lo-1)["chain"] if lo>1 else []}


def check_saturation_certificate(cert):
    """Check only the schedule and two short paths; do not recompute the DP."""
    n,edges,b=cert["n"],cert["edges"],cert["B_sat"]
    if n<=0 or not 1<=b<=n or cert["W"]!=n:
        raise ValueError("wrong certificate domain")
    validate_instance(n,edges,b,n)
    edge_set=set(map(tuple,edges))

    def check_path(path,window):
        if not path or any(type(j) is not int or not 0<=j<n for j in path):
            raise ValueError("invalid path vertices")
        for i,j in zip(path,path[1:]):
            if not i<j or ((i,j) not in edge_set and (window is None or j-i<window)):
                raise ValueError("invalid critical-path edge")
    path=cert["original_critical_chain"]
    check_path(path,None)
    if len(path)!=cert["cycles"] or replay(n,edges,b,n,cert["schedule"])!=len(path):
        raise ValueError("unrestricted optimum lower and upper witnesses disagree")
    if b>1:
        check_path(cert["smaller_window_chain"],b-1)
        if len(cert["smaller_window_chain"])<=len(path):
            raise ValueError("path does not rule out a smaller window")
    elif cert["smaller_window_chain"]:
        raise ValueError("B=1 needs no smaller positive window obstruction")
    return {"valid":True,"B_sat":b,"cycles":len(path)}
