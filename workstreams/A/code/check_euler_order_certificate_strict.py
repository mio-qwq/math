#!/usr/bin/env python3
"""Strict independent verifier for the entire Euler-balanced-root edge-order proof.

No dependency on an edge-order generator, root selector or discovery oracle.
A valid certificate commits to *exactly one* canonical global edge order, its
root sequence, the balanced two-partition colouring, and the actual components.
All checks rebuild the original graph and incident-colour sequences from input.

Input vertices should be a finite set of distinct comparable integers; colours
are 0,...,d-1. This is a finite certificate checker, not a Lean proof.
"""
from collections import deque


def check_strict(vertices, edges, d, order, certificate):
    """Return (pass_boolean, precise_reason) without executing any constructor."""
    try:
        if type(d) is not int or d < 3:
            return False, 'd must be integer >= 3'
        V = set(vertices)
        if not V or len(V) != len(list(vertices)) or any(type(v) is not int for v in V):
            return False, 'invalid vertex universe'
        E=[];pairs=set();bycolour={v:{} for v in V}
        for triple in edges:
            if len(triple)!=3:
                return False, 'edge arity'
            a,b,c=triple
            if type(a) is not int or type(b) is not int or type(c) is not int:
                return False, 'noninteger edge'
            if a not in V or b not in V or a == b or not 0 <= c < d:
                return False, 'invalid coloured edge'
            p=(min(a,b),max(a,b))
            if p in pairs:
                return False, 'duplicate pair (graph not simple)'
            pairs.add(p);E.append(p+(c,))
            for v,w in ((a,b),(b,a)):
                if c in bycolour[v]:
                    return False, 'improper fixed colouring'
                bycolour[v][c]=w
        if any(set(bycolour[v])!=set(range(d)) for v in V):
            return False, 'not d-regular with exactly d colours'
        if len(E)*2!=len(V)*d:
            return False, 'handshaking degree mismatch'
        O=[]
        for triple in order:
            if len(triple)!=3 or any(type(x) is not int for x in triple):
                return False, 'invalid order entry'
            a,b,c=triple;O.append((min(a,b),max(a,b),c))
        if len(O)!=len(E) or set(O)!=set(E) or len(set(O))!=len(O):
            return False, 'order is not a permutation of original edges'

        # Independent whole two-colour cycle reconstruction. Canonical
        # walk starts at each minimum vertex and follows colour 0 first.
        unseen=set(V);cycles=[]
        while unseen:
            v=min(unseen);start=v;colour=0;C=[]
            while v not in C:
                if v not in unseen:
                    return False, '0/1 walk intersects prior factor'
                C.append(v);unseen.remove(v)
                v=bycolour[v][colour];colour^=1
            if v!=start or len(C)<4 or len(C)%2:
                return False, '0/1 factor is not an even simple cycle'
            cycles.append(C)
        if certificate.get('cycles') != cycles:
            return False, 'certificate 0/1 cycles not canonical from input'
        cycle_of={v:j for j,C in enumerate(cycles) for v in C}

        # Independently recover all connected components of leftover colours.
        Q={v:set() for v in V}
        rem_edges=[]
        for a,b,c in E:
            if c>=2:
                Q[a].add(b);Q[b].add(a);rem_edges.append((a,b,c))
        if any(len(Q[v])==0 for v in V):
            return False, 'Q contains isolated vertex'
        S=[];remaining=set(V)
        while remaining:
            root=min(remaining);remaining.remove(root);component={root}
            queue=deque([root])
            while queue:
                v=queue.popleft()
                for w in Q[v]:
                    if w in remaining:
                        remaining.remove(w);component.add(w);queue.append(w)
            S.append(sorted(component))
        if certificate.get('leftover_components')!=S:
            return False, 'Q components differ from actual graph'
        # Verify both partitions simultaneously balanced by exact 2-colouring.
        colours=certificate.get('two_colour_map')
        if not isinstance(colours,dict) or set(colours)!=V:
            return False, 'bad two-partition colour map'
        if any(type(colours[v]) is not int or colours[v] not in (0,1) for v in V):
            return False, 'invalid red/blue label'
        for block in cycles+S:
            red=sum(colours[v]==0 for v in block)
            if abs(2*red-len(block))>1:
                return False, 'two-partition block imbalance exceeds one'

        roots=certificate.get('rootset')
        if not isinstance(roots,list) or roots!=sorted(set(roots)):
            return False, 'roots must be sorted with no duplicate'
        R=set(roots)
        if any(sum(v in R for v in C)!=1 for C in cycles):
            return False, 'root transversal not one per cycle'
        if any(colours[r]!=0 for r in R):
            return False, 'selected root is not coloured red'
        margins=[len(set(T)-R) for T in S]
        if certificate.get('blue_component_margins')!=margins:
            return False, 'wrong Q blue/nonroot margins'
        if any(m < len(T)//2 for m,T in zip(margins,S)):
            return False, 'Q component too heavily occupied by roots'
        ordered_roots=certificate.get('ordered_roots')
        if not isinstance(ordered_roots,list) or len(ordered_roots)!=len(R) or set(ordered_roots)!=R:
            return False, 'bad root order'
        rank={r:i for i,r in enumerate(ordered_roots)}
        if any(not any(w not in R or rank[w]>rank[v] for w in Q[v]) for v in R):
            return False, 'root lacks assigned leftover edge (boundary/forest lemma)'

        # From the certificate and input ONLY (without the generating module),
        # reconstruct every cycle block and the unique ownership of each edge.
        linear_cycles=[];position={}
        for k,r in enumerate(ordered_roots):
            # Root must be from exactly one (unique) actual 0/1 cycle.
            cyc=[];v=r;col=0
            while v not in cyc:
                cyc.append(v);v=bycolour[v][col];col^=1
            if v!=r or set(cyc)!=set(cycles[cycle_of[r]]):
                return False, 'root cannot orient its declared 0/1 cycle'
            linear_cycles.append(cyc)
            for j,x in enumerate(cyc):
                if x in position:
                    return False, 'overlapping ordered cycle blocks'
                position[x]=(k,j)
        if set(position)!=V:
            return False, 'missing vertex in declared cycle blocks'
        slots={v:[] for v in V}
        for a,b,c in rem_edges:
            if a in R and b in R:
                owner=a if rank[a]<rank[b] else b
            elif a in R:
                owner=a
            elif b in R:
                owner=b
            else:
                owner=a if position[a]<position[b] else b
            slots[owner].append((a,b,c))
        if any(not slots[r] for r in R):
            return False, 'root assigned no leftover-colour edge'
        predicted=[]
        for cyc in linear_cycles:
            for j,a in enumerate(cyc):
                b=cyc[(j+1)%len(cyc)]
                predicted.append((min(a,b),max(a,b),j%2))
                predicted.extend(sorted(slots[a],key=lambda e:e[2]))
        if predicted!=O:
            return False, 'claimed global order differs from certified construction'

        # Final original-definition semantics with NO proof shortcut.
        seq={v:[] for v in V}
        for a,b,c in O:
            seq[a].append(c);seq[b].append(c)
        if any(len(seq[v])!=d or len(set(seq[v]))!=d for v in V):
            return False, 'wrong local colour palette'
        if any(seq[a]==seq[b] for a,b,c in E):
            return False, 'an original edge has identical endpoint sequences'
        return True, 'PASS exact certified construction and endpoint sequences'
    except (AssertionError,TypeError,ValueError,KeyError,IndexError,OverflowError) as exc:
        return False, f'bad certificate type or arithmetic: {type(exc).__name__}'
