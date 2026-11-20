import heapq
import numpy as np
from common import *

class SmallHNSW:
    """Bounded experimental hierarchical navigable graph, not hnswlib."""
    def __init__(self,x,m=6):
        self.x=x;self.levels=[];self.graph=[];r=rng(19)
        self.levels=np.minimum(r.geometric(.65,len(x))-1,5)
        for level in range(int(max(self.levels))+1):
            ids=np.where(self.levels>=level)[0];g={int(i):set() for i in ids}
            for at,i in enumerate(ids):
                previous=ids[:at]
                nearest=previous[np.argsort(np.sum((x[previous]-x[i])**2,axis=1))[:m]]
                for j in nearest:g[int(i)].add(int(j));g[int(j)].add(int(i))
            self.graph.append(g)
        self.entry=int(np.argmax(self.levels))
    def query(self,q,k=5,ef=20):
        def dist(i):return float(np.sum((self.x[i]-q)**2))
        entry=self.entry
        for g in reversed(self.graph[1:]):
            changed=True
            while changed:
                best=min([entry,*g[entry]],key=dist);changed=best!=entry;entry=best
        candidates=[(dist(entry),entry)];seen={entry};best=[]
        while candidates and len(best)<ef:
            d,i=heapq.heappop(candidates);best.append((d,i))
            for j in self.graph[0][i]:
                if j not in seen:seen.add(j);heapq.heappush(candidates,(dist(j),j))
        return [i for d,i in sorted(best)[:k]]
def run():
    r=rng(6);x=normalize(r.normal(size=(300,24)));queries=normalize(r.normal(size=(40,24)))
    start=time.perf_counter();index=SmallHNSW(x);build=time.perf_counter()-start
    exact=np.argsort(-(queries@x.T),axis=1)[:,:5]
    rows=[]
    for ef in [10,30,80]:
        start=time.perf_counter();out=[index.query(q,5,ef) for q in queries];elapsed=time.perf_counter()-start
        rows.append({'ef':ef,'recall_at_5':float(np.mean([len(set(a)&set(b))/5 for a,b in zip(out,exact)])),'query_seconds':elapsed})
    return {'build_seconds':build,'operating_points':rows,'vector_bytes':x.nbytes,
            'directed_graph_edges':sum(len(v) for g in index.graph for v in g.values()),
            'checks':[check(len(index.query(x[0]))==5,'Query returns bounded five neighbours'),check(all(0<=r['recall_at_5']<=1 for r in rows),'Measured recall within bounds')],
            'scope':'Small authored HNSW-style graph over synthetic random vectors. Build uses exact neighbour selection; no optimized HNSW library or large-scale claim.'}
