"""Tiny certificate checker: no SAT, graph-family search, or frozen data reads."""
T = {4:(1,3,1,2,1), 5:(1,3,1,4,2,1),
     6:(1,3,1,4,1,2,1), 7:(1,3,1,2,1,4,2,1)}
for d,t in T.items():
    assert len(t)==d+1 and t[:2]==(1,3) and t[-2:]==(2,1)
    for i,c in enumerate(t):
        for j in range(i+1,len(t)):
            if t[j]==c: assert j-i>c
# A repeated non-1 color in distinct tiles either occurs in consecutive tiles,
# or has at least one whole intervening tile (>=4 edges); in the latter case
# even color 4 is safe because neither occurrence is an endpoint.
for a,u in T.items():
    for b,v in T.items():
        for i,c in enumerate(u[:-1]):
            for j,e in enumerate(v):
                if c==e: assert a+j-i>c, (a,b,i,j,c)
        # Right 4 cap after final length-4 tile: any previous 4 is far enough.
        if b==4:
            for i,c in enumerate(u):
                if c==4: assert (a+3-i)+1>4
for d,t in T.items():
    # Left cap 2 is one edge from the outgoing terminal at index 1.
    for i,c in enumerate(t):
        if c==2: assert 1+(i-1)>2
    # Right cap 3 when the final tile is not length 4.
    if d>4:
        for i,c in enumerate(t):
            if c==3: assert (d-1-i)+1>3
print('Verified: four tile interiors, all 16 joins, and both triangle cap inequalities.')
