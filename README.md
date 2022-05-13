# Ensemble-Clustering-for-Graphs
Code, notebooks and examples with ECG: Ensemble Clustering for Graphs

This code is now pip installable and integrated with several new measures, see: https://github.com/ftheberge/graph-partition-and-measures

## Reference papers:

* Valérie Poulin and François Théberge, Ensemble Clustering for Graphs. in: Aiello L., Cherifi C., Cherifi H., Lambiotte R., Lió P., Rocha L. (eds) Complex Networks and Their Applications VII. COMPLEX NETWORKS 2018. Studies in Computational Intelligence, vol 812. Springer (2019), https://doi.org/10.1007/978-3-030-05411-3_19 or https://link.springer.com/chapter/10.1007/978-3-030-05411-3_19 

* Pre-print: https://arxiv.org/abs/1809.05578

* V. Poulin and F. Théberge, Ensemble clustering for graphs: comparisons and applications, Network Science (2019) 4:51 https://doi.org/10.1007/s41109-019-0162-z or https://rdcu.be/bLn9i

* Pre-print: https://arxiv.org/abs/1903.08012

## Adding ECG to igraph

You can simply import or copy the content of 'ecg.py' into your Notebook.

It is also possible to pip install ECG for igraph via: pip install partition-igraph

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

