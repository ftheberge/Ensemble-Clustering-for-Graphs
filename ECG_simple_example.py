import igraph as ig
import numpy as np
from sklearn.metrics import adjusted_rand_score as ARI
import sys

## needs 5 arguments
if len(sys.argv) != 6:
    print('Usage: ',sys.argv[0],' #nodes #communities p_in p_out #runs')
    exit(-1)

## arguments
n = int(sys.argv[1])
comm = int(sys.argv[2])
pin = float(sys.argv[3])
pout = float(sys.argv[4])
runs = int(sys.argv[5])

## add ECG to the choice of community algorithms
def community_ecg(self, weights=None, ens_size=16, min_weight=0.05):
    W = [0]*self.ecount()
    ## Ensemble of level-1 Louvain 
    for i in range(ens_size):
        p = np.random.permutation(self.vcount()).tolist()
        g = self.permute_vertices(p)
        l = g.community_multilevel(weights=weights, return_levels=True)[0].membership
        b = [l[p[x.tuple[0]]]==l[p[x.tuple[1]]] for x in self.es]
        W = [W[i]+b[i] for i in range(len(W))]
    W = [min_weight + (1-min_weight)*W[i]/ens_size for i in range(len(W))]
    part = self.community_multilevel(weights=W)
    ## Force min_weight outside 2-core
    core = self.shell_index()
    ecore = [min(core[x.tuple[0]],core[x.tuple[1]]) for x in self.es]
    part.W = [W[i] if ecore[i]>1 else min_weight for i in range(len(ecore))]
    part.CSI = 1-2*np.sum([min(1-i,i) for i in part.W])/len(part.W)
    return part
ig.Graph.community_ecg = community_ecg

## Planted partition model with communities of equal expected size
td = [1/comm]*comm
P = np.full((comm,comm),pout)
np.fill_diagonal(P,pin)
for r in range(runs):
    print('\nRun #',r+1)
    g = ig.Graph.Preference(n=n,type_dist=td,pref_matrix=P.tolist(),attribute='class')
    ie = 0
    for e in g.es():
        if(g.vs['class'][e.tuple[0]] == g.vs['class'][e.tuple[1]]):
            ie+=1
    
    im = g.community_infomap().membership
    ml = g.community_multilevel().membership
    ec = g.community_ecg(ens_size=50)
    print('ARI with Infomap:',ARI(im,g.vs['class']),'with',max(im)+1,'communities')
    print('ARI with Louvain:',ARI(ml,g.vs['class']),'with',max(ml)+1,'communities')
    print('ARI with ECG:',ARI(ec.membership,g.vs['class']),'with',max(ec.membership)+1,'communities')
    print('CSI:',ec.CSI)
    print('mu:',1.0-ie/g.ecount())
