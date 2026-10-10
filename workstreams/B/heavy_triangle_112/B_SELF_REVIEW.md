# B personal self-review — not independent peer acceptance

Original scope: checked original Section5 Conjecture6 and heavy/local-girth definitions. The new PROOF.md covers all finite graphs in the statement, not only the initial perfect-matching construction. No new research agents were used.

Checked points:
- Leaf peeling cannot newly create heavy vertices, and triangles survive the peeling. Restored vertices only need the two independent colors.
- Overlapping triangles give diamonds or excluded K4. Two external diamond ports would force adjacent heavy shared-edge vertices, so diamonds have at most one port.
- Core loops/parallel edges are retained. Each degree-three triangle node has at least two ordinary incidences. Hall counts incidences with multiplicity two per loop, while matching uses distinct edge objects.
- Initial selections are unique edge owners. In an exchange, a selected edge leaving a residual cycle cannot return to that cycle; its far end lies in a residual path. Returning it cannot create another cycle.
- Remaining direct-edge cycles have only degree-two triangle nodes and lift to even cycles of twice the core length.
- The radius-two set is checked in original graph distances, including connectors of length1,2 and longer. Two-connector routes already have length at least3 because ports are distinct.
- The constructive implementation decomposes the actual original adjacency, not a supplied abstract core. A separate checker imports none of its construction or discovery logic and rebuilds every original distance by BFS.

Actual commands and results are in regression.log and check_matched_family.log. The first regression had zero accepted random leaf attachments (the attempted additions violated the heavy condition); explicit admissible pendant/disconnected fixtures were then added and the whole suite rerun. No coverage is inferred from rejected fixtures.

Earlier odd-cycle discovery was stopped after the full matched-heavy family acquired an all-length proof. Its log retains SAT and UNKNOWN checkpoints; unlogged partially processed cases and planned later modes are not counted as completed. The universal proof supersedes this search mechanism without pretending timed-out computations finished.

Pending: independent review, prior-art/human review, and optional full-statement formalization. No signed publication, Lean, minimality or world-first assertion by B. Proof changes after freeze must receive a new version.
