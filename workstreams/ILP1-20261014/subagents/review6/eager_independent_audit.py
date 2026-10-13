"""Independent set-state callback and explicit virtual-plan lift audit."""
from pathlib import Path
import sys, random, itertools, json, hashlib, time
HERE=Path(__file__).resolve().parent
THEORY=HERE.parent/'theory'
sys.path.insert(0,str(THEORY))
from chunk_lookahead import run_policy
from eager_chunk_lookahead import run_eager_policy, run_random_eager_policy

class Machine:
    def __init__(self, parents, lookahead, nondelay):
        self.parents=parents
        self.n=len(parents)
        self.lookahead=lookahead
        self.nondelay=nondelay
        self.done=set()
        self.trace=[]
        self.reads=[]
    def prefix(self):
        return next((i for i in range(self.n) if i not in self.done),self.n)
    def ready(self):
        r=self.prefix()
        return {i for i in range(r,min(self.n,r+4)) if i not in self.done and self.parents[i]<=self.done}
    def read(self,j):
        assert len(self.done)<self.n, 'query after actual completion'
        assert 0<=j<min(self.n,self.prefix()+4+self.lookahead)
        self.reads.append((len(self.trace),j))
        return sum(2**i for i in self.parents[j])
    def issue(self,action):
        a=set(action)
        assert len(self.done)<self.n, 'issue after completion'
        assert len(a)==len(action) and len(a)<=3
        ready=self.ready()
        assert a<=ready
        if self.nondelay: assert len(a)==min(3,len(ready))
        self.trace.append(tuple(action))
        self.done.update(a)

# This expected implementation never runs the virtual controller or its state
# update code: it transforms a separately captured unmodified plan, with Python
# sets, and makes its own before-cycle readiness computation.
def expected_lift(parents,plan):
    done=set(); n=len(parents); result=[]; skipped=0
    for action in plan:
        if len(done)==n: break
        retained=[i for i in action if i not in done]
        if not retained:
            skipped+=1
            continue
        r=next(i for i in range(n) if i not in done)
        ready=[i for i in range(r,min(n,r+4)) if i not in done and parents[i]<=done]
        selected=retained+[i for i in ready if i not in retained][:3-len(retained)]
        result.append(tuple(selected)); done.update(selected)
    assert len(done)==n
    return result,skipped

def main():
    start=time.monotonic(); seed=2026101406; rng=random.Random(seed)
    counts=dict(instances=0,offsets=0,random_calls=0,real_cycles=0,queries=0,skipped=0,strict_gains=0,early_aborts=0,family_offsets=0)
    def check(parents,L,family_opt=None):
        counts['instances']+=1
        for u in range(1,5+L):
            base=Machine(parents,L,False)
            baseline=run_policy(len(parents),L,base.read,base.issue,initial_chunk_size=u)
            actual=Machine(parents,L,True)
            out=run_eager_policy(len(parents),L,actual.read,actual.issue,initial_chunk_size=u)
            expected,skipped=expected_lift(parents,base.trace)
            assert actual.trace==expected
            assert out['cycles']==len(expected)<=baseline['cycles']
            assert out['skipped_virtual_cycles']==skipped
            assert len(actual.done)==len(parents)
            assert len({j for _,j in actual.reads})==len(actual.reads), 'cache failed'
            counts['offsets']+=1; counts['real_cycles']+=len(expected); counts['queries']+=len(actual.reads)
            counts['skipped']+=skipped
            counts['strict_gains']+=len(expected)<baseline['cycles']
            counts['early_aborts']+=out['virtual_cycles']<baseline['cycles']
            if family_opt is not None:
                assert len(expected)==family_opt
                counts['family_offsets']+=1
        # A controlled tape verifies the wrapper makes exactly one uniform-range
        # call and gives exactly the same execution as its returned offset.
        class Tape:
            calls=0
            def randrange(self,a,b):
                assert (a,b)==(1,5+L)
                self.calls+=1
                return 2 if L%2 else 4+L
        tape=Tape(); actual=Machine(parents,L,True)
        out=run_random_eager_policy(len(parents),L,actual.read,actual.issue,rng=tape)
        assert tape.calls==1
        base=Machine(parents,L,False)
        run_policy(len(parents),L,base.read,base.issue,initial_chunk_size=out['initial_chunk_size'])
        assert actual.trace==expected_lift(parents,base.trace)[0]
        counts['random_calls']+=1
    dags=0
    for n in range(5):
        edges=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(edges)):
            parents=[set() for _ in range(n)]
            for k,(i,j) in enumerate(edges):
                if mask>>k&1: parents[j].add(i)
            dags+=1
            for L in (0,2,7):check(parents,L)
    for _ in range(240):
        n=rng.randrange(5,35)
        parents=[set(rng.sample(range(j),min(j,rng.randrange(5)))) for j in range(n)]
        check(parents,rng.choice((0,1,3,6,11)))
    for blocks in (1,2,4,9):
        parents=[set() for _ in range(6*blocks)]
        for block in range(blocks):
            s=6*block
            for i in (1,2,4,5):parents[s+i].add(s+i-1)
            if block:
                parents[s]={s-4,s-1}; parents[s+3]={s-4,s-1}
        for L in (0,1,2,5,12):check(parents,L,3*blocks)
    receipt={'status':'PASS','seed':seed,'exhaustive_forward_dags':dags,'exhaustive_n_max':4,
             'random_graphs':240,'counts':counts,'elapsed_seconds':time.monotonic()-start,
             'python':sys.version,'source_sha256':{str(p.relative_to(HERE.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),THEORY/'eager_chunk_lookahead.py',THEORY/'chunk_lookahead.py',THEORY/'forced_segment_dp.py']}}
    (HERE/'evidence/eager-independent.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
