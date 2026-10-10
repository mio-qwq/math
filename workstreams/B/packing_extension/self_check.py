#!/usr/bin/env python3
"""B's own post-handoff regression checks, not a new independent review.

Earlier local-audit graph builder is reused only to serialize sample graphs.
The separate direct-definition verifier does not reuse its distance checks.
"""
import copy
import importlib.util
import json
from pathlib import Path
from verify_coloring import verify

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('prior_builder', HERE.parent/'packing_review'/'independent_local_audit.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def serialize(g):
    vs = list(g.a)
    labels = {v:i for i,v in enumerate(vs)}
    return {'adjacency': [sorted(labels[w] for w in g.a[v]) for v in vs],
            'colors': [g.c[v] for v in vs]}

examples = []
# Mixed connector lengths: gaps 4, 11, 18; original connectors 2,9,16.
g = m.build((4,5,6,7,4,7), [0,1,3,6], caps=('square','triangle'))
examples.append(('mixed_chain', serialize(g)))
# Remove the temporary endpoint square: first remaining vertex is a leaf,
# only one edge from the first surviving square's degree-three terminal.
for v in (-1,0,('twin',0),1):
    g.remove(v)
examples.append(('length_one_leaf_mixed_chain', serialize(g)))
for seq, marks in [((5,),[0]), ((4,5,7),[0,1,2]), ((4,5,6,7),[0,2])]:
    examples.append(('necklace_'+str(len(examples)), serialize(m.build(seq,marks,cyclic=True))))
# Both triangle caps on the shortest connector, exercising the special 4 cap.
g = m.build((4,),[0,1],caps=('triangle','triangle'))
examples.append(('two_triangle_short_connector',serialize(g)))
# Disconnected graph with isolated vertex, edge, and triangle.
examples.append(('elementary_disconnected', {'adjacency':[[],[2],[1],[4,5],[3,5],[3,4]],'colors':[1,1,2,1,2,3]}))
receipts = []
for name, cert in examples:
    out = HERE/(name+'.json')
    out.write_text(json.dumps(cert,indent=2)+'\n')
    receipts.append({'name':name, **verify(cert)})

negative = []
bad = serialize(m.build((4,),[0,1],caps=('triangle','triangle'),bad_right=True))
negative.append(('invalid_right_triangle_color', bad))
bad = copy.deepcopy(examples[0][1]); bad['adjacency'][0].append(0)
negative.append(('self_loop',bad))
bad = copy.deepcopy(examples[0][1]); v=0; w=bad['adjacency'][v][0]; bad['adjacency'][w].remove(v)
negative.append(('asymmetric_adjacency',bad))
negative.append(('adjacent_degree_three',{'adjacency':[[1,2,3],[0,2,3],[0,1],[0,1]],'colors':[1,2,3,4]}))
negative.append(('degree_three_without_short_cycle',{'adjacency':[[1,2,3],[0],[0],[0]],'colors':[2,1,1,1]}))
rejected=[]
for name, bad in negative:
    try: verify(bad)
    except ValueError as exc: rejected.append({'name':name,'reason':str(exc)})
    else: raise AssertionError('negative control was accepted: '+name)
print(json.dumps({'positive_examples':receipts,'negative_controls_rejected':rejected},indent=2))
