#!/usr/bin/env python3
"""Build deterministic witnesses. Verification is a separate implementation."""
from __future__ import annotations
import hashlib, json
from collections import deque
from itertools import product
from pathlib import Path
import model, ten_state

HERE = Path(__file__).resolve().parent
L6 = [1,2,0,1,2,0, 0,1,2,1,1,0, 2,0,1,2,2,1,
      1,2,1,1,0,0, 1,0,2,1,0,0, 1,0,2,2,2,2]
L4 = [1,1,0,2, 0,1,0,1, 1,2,0,2, 0,0,0,1]


def instance(n, levels, weights):
    E,T,moments,F = model.rotation_moments(n,levels,weights)
    witness = None
    for w in product(range(n),repeat=6):
        if all(w[i:i+4] in F for i in range(3)):
            witness = list(w); break
    return {'n':n, 'levels':levels, 'weights':weights,
            'E':str(E), 'T':str(T), 'moments':{f'{a},{b}':str(v) for (a,b),v in moments.items()},
            'forced_count':len(F), 'consecutive_forced_witness':witness,
            'completion':model.solve_completion(n,levels)}


def bfs_instance(n, code):
    vertices = [w for w in product(range(n),repeat=4) if all(w[i]!=w[i+1] for i in range(3))]
    index = {w:i for i,w in enumerate(vertices)}
    adjacency = [[index[w[1:]+(a,) ] for a in range(n) if a!=w[-1]] for w in vertices]
    D = []
    for source in range(len(vertices)):
        d = [-1]*len(vertices); d[source]=0; todo=deque([source])
        while todo:
            u=todo.popleft()
            for v in adjacency[u]:
                if d[v]<0:d[v]=d[u]+1;todo.append(v)
        D.append(d)
    return {'n':n,'vertices':[list(w) for w in vertices], 'adjacency':adjacency,'distances':D,
            'selected':[index[w] for w in sorted(code) if w in index]}


def main():
    source = HERE.parent/'literature_lifts/jiggs57_words.txt'
    jiggs = {tuple('ABCD'.index(a) for a in w) for w in source.read_text().split()}
    gamma = model.profile_from_code(4,jiggs)
    eta,kappa = model.canonical_hierarchy(4,gamma)
    active = model.reduce_active(4,eta,kappa,gamma)
    data = {'schema':'GP2-stage2-v1',
            'stage1_commit':'b45b04eeab0fc521b789d6d47b4d8b94119e8c90',
            'scope':'Strict-window structural theorem and fixed-array obstructions; no new uniform density endpoint',
            'target':{'profiles':[list(p) for p in model.P],
                      'pair_types':[list(p) for p in model.Q],
                      'letter_types':[list(p) for p in model.R],
                      'allowed':[[int(model.allowed(p,q)) for q in model.P] for p in model.P],
                      'marked':[[int(model.marked(p,q)) for q in model.P] for p in model.P]},
            'six_letter_obstruction':instance(6,L6,[1]*6),
            'jiggs':instance(4,L4,[5,5,3,3])}
    data['jiggs'].update(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                         original_code=[list(w) for w in sorted(jiggs)],
                         eta=[list(eta[x]) for x in range(4)],
                         kappa=[list(kappa[x]) for x in product(range(4),repeat=2)],
                         gamma=[list(gamma[x]) for x in product(range(4),repeat=3)],
                         reduced_gamma=[list(active[x]) for x in product(range(4),repeat=3)])
    data['ten_target'] = {'profiles':[list(p)for p in ten_state.P],
        'pair_types':[list(q)for q in ten_state.Q], 'letter_types':[list(r)for r in ten_state.R],
        'allowed':[[int(model.allowed(p,q))for q in ten_state.P]for p in ten_state.P],
        'marked':[[int(model.marked(p,q))for q in ten_state.P]for p in ten_state.P]}
    data['canonical_forced_obstacle'] = {'n':3,'code':[[2,1,0,0],[2,1,1,0]],
        'levels':[1,0,0,1,0,0,0,0,0], 'word':[2,0,1,0,0,1,0,0], 'starts':[0,1,4]}
    data['actual_kautz'] = [bfs_instance(3,{w for w in jiggs if max(w)<3}),bfs_instance(4,jiggs)]
    path = HERE/'certificate.json'
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print('wrote',path.name)
    print('six-letter forced witness:',data['six_letter_obstruction']['consecutive_forced_witness'])
    print('Jiggs letter types:',data['jiggs']['eta'])
    print('certificate SHA256:',hashlib.sha256(path.read_bytes()).hexdigest())

if __name__=='__main__':
    main()
