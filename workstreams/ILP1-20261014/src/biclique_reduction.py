"""Balanced-biclique embedding in the R1 model with B-W=k.

This is a complexity-classification construction, not a two-input program.
Its height-two jobs may have unbounded true fan-in. Related three-cycle
precedence/biclique reductions are prior art; see EXCESS_HARDNESS.md.
"""


def construct(left, right, edges, k):
    if any(type(v) is not int for v in (left, right, k)):
        raise ValueError("integer bipartition sizes and k required")
    if not 1 <= k <= min(left, right):
        raise ValueError("requires 1 <= k <= min(left,right)")
    allowed = set()
    for u, v in edges:
        if type(u) is not int or type(v) is not int or not (0 <= u < left and 0 <= v < right):
            raise ValueError("invalid bipartite edge")
        allowed.add((u, v))
    forced = right + k
    window = forced + left
    width = window - k
    dependency = []
    for v in range(right):
        sink = window + v
        dependency.extend((u, sink) for u in range(forced))
        dependency.extend((forced + u, sink) for u in range(left) if (u, v) not in allowed)
    for sink in range(window + right, 2 * window):
        dependency.extend((u, sink) for u in range(window))
    return {"n": 2 * window, "edges": dependency, "B": window, "W": width,
            "forced_roots": forced, "left": left, "right": right, "k": k}


def three_cycle_witness(instance, selected_left, selected_right):
    """Construct a candidate trace; the caller must independently check it."""
    f, b, k = instance["forced_roots"], instance["B"], instance["k"]
    us, vs = set(selected_left), set(selected_right)
    if len(us) != k or len(vs) != k:
        raise ValueError("exactly k distinct vertices on each side required")
    if any(type(u) is not int or not 0 <= u < instance["left"] for u in us):
        raise ValueError("left vertex out of range")
    if any(type(v) is not int or not 0 <= v < instance["right"] for v in vs):
        raise ValueError("right vertex out of range")
    omitted = {f + u for u in us}
    middle_sinks = {b + v for v in vs}
    return [sorted(set(range(b)) - omitted), sorted(omitted | middle_sinks),
            sorted(set(range(b, 2 * b)) - middle_sinks)]


def four_cycle_witness(instance):
    b, w = instance["B"], instance["W"]
    return [list(range(w)), list(range(w, b)),
            list(range(b, b + w)), list(range(b + w, 2 * b))]
