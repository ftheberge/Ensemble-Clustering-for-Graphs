# Ensemble-Clustering-for-Graphs
Code, notebooks and examples with ECG: Ensemble Clustering for Graphs

## Reference papers:

ECG papers: https://rdcu.be/bLn9i and https://arxiv.org/abs/1809.05578

## Adding ECG to igraph

You can simply import or copy the content of 'ecg.py' into your Notebook.

It is also possible to pip install ECG, or one can simply add the following
lines to get ECG in igraph:

```
import igraph as ig
import numpy as np
# add ECG to the choice of community algorithms
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
    ## Force min_weight outside 2-core
    core = self.shell_index()
    ecore = [min(core[x.tuple[0]],core[x.tuple[1]]) for x in self.es]
    w = [W[i] if ecore[i]>1 else min_weight for i in range(len(ecore))]
    part = self.community_multilevel(weights=w)
    part.W = w
    part.CSI = 1-2*np.sum([min(1-i,i) for i in w])/len(w)
    return part
ig.Graph.community_ecg = community_ecg

```

## Simple Python Example

A simple illustration of the use of ECG, and comparison with Louvain (ML) and Infomap (IM) 
is provided in the *ECG_simple_example.py* code. 

Format is:

```
ECG_simple_example.py #nodes #communities p_in p_out #runs
```

which will build graphs with the planted partition model.
The communities are obtained for each algorithm and compared with ground truth 
via the adjusted Rand index (ARI).

The community strength index (CSI) and empirical mixing parameter (mu) 
are also results. The latter refers to the proportion of edges between communities.

### Example 1 -- strong communities

```
$ python ECG_simple_example.py 500 5 .1 .01 3

Run # 1
ARI with Infomap: 1.0 with 5 communities
ARI with Louvain: 1.0 with 5 communities
ARI with ECG: 1.0 with 5 communities
CSI: 0.8909330306469911
mu: 0.28688989784335983

Run # 2
ARI with Infomap: 0.9947546661827955 with 5 communities
ARI with Louvain: 0.9947546661827955 with 5 communities
ARI with ECG: 0.9947546661827955 with 5 communities
CSI: 0.862204839617329
mu: 0.2822172200337648

Run # 3
ARI with Infomap: 0.9949740943854817 with 5 communities
ARI with Louvain: 1.0 with 5 communities
ARI with ECG: 1.0 with 5 communities
CSI: 0.889089500860585
mu: 0.28686173264486514
```

### Example #2 -- weak communities

```
$ python ECG_simple_example.py 500 5 .1 .03 3

Run # 1
ARI with Infomap: 0.0 with 1 communities
ARI with Louvain: 0.24617775616265852 with 9 communities
ARI with ECG: 0.7539622612934246 with 5 communities
CSI: 0.5084590400577411
mu: 0.5521472392638036

Run # 2
ARI with Infomap: 0.0 with 1 communities
ARI with Louvain: 0.5421712111811192 with 5 communities
ARI with ECG: 0.7361120897981182 with 5 communities
CSI: 0.5433250355618737
mu: 0.5476529160739687

Run # 3
ARI with Infomap: 0.0 with 1 communities
ARI with Louvain: 0.3901605186770534 with 7 communities
ARI with ECG: 0.7270566337183684 with 5 communities
CSI: 0.5147285348922195
mu: 0.54165144318597
```

