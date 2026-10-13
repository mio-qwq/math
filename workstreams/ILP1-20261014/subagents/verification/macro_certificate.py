"""Independent polynomial checker for B=W+1 prefix-potential certificates.

This file contains no optimizer and does not import any primary/theory solver.
It regenerates every non-delay macro and verifies all lower-potential edges.
"""

from itertools import combinations

from constraint_solver import operational_check, validate_input


SCHEMA = "ilp1-c1-prefix-lower-v1"
FIELDS = {"schema","n","window","width","edges","cycles","potentials","schedule"}


def all_prefix_macros(n, edges, width):
    """Yield (prefix, first_action, cycle_count, clear_endpoint) for ALL macros.

    Edges are assumed validated. Set-based direct ROB simulation is deliberately
    independent of the efficient primary counter implementation.
    """
    window = width+1
    pred = [set() for _ in range(n)]
    for u,v in edges:
        pred[v].add(u)

    def ready(done,r):
        return tuple(j for j in range(r,min(n,r+window))
                     if j not in done and pred[j] <= done)

    for prefix in range(n):
        initial = set(range(prefix))
        enabled = ready(initial,prefix)
        for first in combinations(enabled,min(width,len(enabled))):
            done,r,cycles = set(initial),prefix,0
            action = first
            while True:
                # The action is fully chosen before completion is updated.
                assert 1 <= len(action) <= width
                done.update(action)
                cycles += 1
                while r in done:
                    r += 1
                if len(done) == r:
                    assert prefix < r <= n and cycles <= n-prefix
                    yield prefix,first,cycles,r
                    break
                action = ready(done,r)
                # A nonclear state has at most W unfinished window entries.
                assert 1 <= len(action) <= width


def check_certificate(n, edges, window, width, certificate):
    """Return a structured acceptance/rejection; external instance is binding.

    The input graph/resources are independently supplied and must match the
    certificate. Extra fields, including any claimed macro whitelist, reject.
    Accepted certificates prove the actual ROB optimum equals `cycles`,
    conditional on the independently reviewed non-delay/macro theorems.
    """
    def reject(reason, **detail):
        return {"valid":False,"reason":reason,**detail}

    try:
        canonical = validate_input(n,edges,window,width)
    except (ValueError,TypeError,IndexError):
        return reject("invalid external instance")
    if window != width+1:
        return reject("certificate domain requires B=W+1")
    if type(certificate) is not dict or set(certificate) != FIELDS:
        return reject("invalid certificate fields")
    if certificate["schema"] != SCHEMA:
        return reject("unknown certificate schema")
    if any(type(certificate[key]) is not int for key in ("n","window","width","cycles")):
        return reject("metadata must use integers")
    if (certificate["n"],certificate["window"],certificate["width"]) != (n,window,width):
        return reject("certificate instance/resources do not match")
    supplied_edges = certificate["edges"]
    if (type(supplied_edges) is not list or
        any(type(edge) is not list or len(edge) != 2 or
            any(type(j) is not int for j in edge) for edge in supplied_edges) or
        supplied_edges != [list(edge) for edge in canonical]):
        return reject("certificate graph does not match canonical instance")
    potentials = certificate["potentials"]
    if type(potentials) is not list or len(potentials) != n+1:
        return reject("invalid potential vector length")
    if any(type(value) is not int or not 0 <= value <= n-i
           for i,value in enumerate(potentials)):
        return reject("potentials must be integers in 0..N-i")
    cycles = certificate["cycles"]
    if potentials[n] != 0 or potentials[0] != cycles:
        return reject("invalid terminal or initial potential")
    schedule = certificate["schedule"]
    if (type(schedule) is not list or len(schedule) != cycles or
        any(type(action) is not list or any(type(job) is not int for job in action)
            for action in schedule)):
        return reject("invalid schedule representation or cycle count")
    if not operational_check(n,canonical,window,width,schedule):
        return reject("schedule fails direct ROB replay")
    checked = 0
    for i,action,length,j in all_prefix_macros(n,canonical,width):
        checked += 1
        if potentials[i] > length+potentials[j]:
            return reject("lower-potential macro inequality violated",
                          prefix=i,first_action=list(action),macro_length=length,
                          endpoint=j,potential=potentials[i],
                          right_hand_side=length+potentials[j],
                          macro_inequalities_checked=checked)
    return {"valid":True,"cycles":cycles,"macro_inequalities_checked":checked,
            "reason":"legal attaining schedule and all prefix lower-potential inequalities"}
