#

import networkx as nx
import sys

G = nx.DiGraph(nx.read_dot("/dev/stdin"))

def subtree(G, node):
    GS = G.copy()
    GS.remove_node(node)
    st = nx.descendants(G, node)
    st.add(node)
    S = G.subgraph(st).copy()

    for n in st:
        if n == node:
            continue
        ns = nx.ancestors(GS, n)
        if not ns.issubset(st):
            S.remove_node(n)

    return S

def subtree_size(G):
    return sum(int(v) for k,v in nx.get_node_attributes(G, "size").items())

sizes=[]

for n in G.node:
    S = subtree(G, n)
    nx.write_dot(S, "Tree-" + n + ".dot")
    sizes.append((n, subtree_size(S), len(S.node)))

for n,s,l in sorted(sizes, key=lambda x: x[1], reverse=True):
    print("%6d kB  %s (%d packages)" % (s/1024, n, l))

