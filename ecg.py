import igraph
import numpy as np

def community_ecg(self, weights=None, ens_size = 16, min_weight = 0.05):
    """
    Runs an ensemble of single-level randomized Louvain; 
    each member of the ensemble gets a "vote" to determine if the edges 
    are intra-community or not;
    the votes are aggregated into an "ECG edge weights" in range [0,1]; 
    a final (full depth) Louvain (using the louvain package) is run 
    using those edge weights;
    
    Parameters
    ----------
    self : :class:`igraph.Graph`
      Graph to define the partition on.

    weights: list of double, optional 
      the edge weights

    ens_size: int 
      the size of the ensemble of single-level Louvain.

    min_weight: double in range [0,1] 
      the ECG edge weight for edges with zero votes from the ensemble.

    Returns
    -------
    partition
      The optimised partition, of class `igraph.clustering.VertexClustering`.

    partition.W
      The ECG edge weights

    partition.CSI
      The community strength index

    Notes
    -----
    The ECG edge weight function is defined as:
      
      min_weight + ( 1 - min_weight ) x (#votes_in_ensemble) / ens_size

    The weights are linear in terms of the #votes, in the range [min_weight,1].
    

    Examples
    --------
    >>> g = igraph.Graph.Famous('Zachary')
    >>> part = g.community_ecg(ens_size=25, min_weight = .1)
    """
    W = [0]*self.ecount()
    ## Ensemble of level-1 Louvain
    for i in range(ens_size):
        p = np.random.permutation(self.vcount()).tolist()
        g = self.permute_vertices(p)
        l1 = g.community_multilevel(weights=weights, return_levels=True)[0].membership
        b = [l1[p[x.tuple[0]]]==l1[p[x.tuple[1]]] for x in self.es]
        W = [W[i]+b[i] for i in range(len(W))]
    W = [min_weight + (1-min_weight)*W[i]/ens_size for i in range(len(W))]
    ## Force min_weight outside 2-core
    core = self.shell_index()
    ecore = [min(core[x.tuple[0]],core[x.tuple[1]]) for x in self.es]
    w = [W[i] if ecore[i]>1 else min_weight for i in range(len(ecore))]
    part = self.community_multilevel(weights=w)
    part._modularity_params['weights'] = weights
    part.W = w
    part.CSI = 1-2*np.sum([min(1-i,i) for i in w])/len(w)
    return part

igraph.Graph.community_ecg = community_ecg
