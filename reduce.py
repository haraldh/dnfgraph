#

import networkx as nx

G=nx.read_dot("/dev/stdin")

remove_pkg = (
    "coreutils-single",
)

reduce_pkg=(
    "coreutils",
    "systemd",
    "bash",
    "NetworkManager",
    "util-linux",
    "kernel-core",
    "rpm",
    "dnf",
    "docker",
    "glibc",
    "grub2",
    "dracut",
    "grep",
    "bzip2",
    "gzip",
    "xz",
    "zlib",
    "less",
    "iproute",
    "chrony",
    "openssh-clients",
    "procps-ng",
    "rsync",
    "sed",
    "sudo",
    "tar",
    "subscription-manager",
    "filesystem",
    "initscripts",
    "findutils",
    "gcc",
    "libgcc",
    "libstdc++",
)

for p in remove_pkg:
    G.remove_node(p)

a = nx.get_node_attributes(G, "src")

for k,v in a.items():
    G.node[k]["src"]=v.strip('"')

a = nx.get_node_attributes(G, "src")

# for p in reduce_pkg:
#     if not p in G.node:
#         continue

#     p = G.node[p]["src"]
#     for (k,v) in a.items():
#         if p == v:
#             if not k in G.node:
#                 continue
#             G.remove_edges_from(G.in_edges(k))

# for p in reduce_pkg:
#     if not p in G.node:
#         continue

#     p = G.node[p]["src"]
#     for (k,v) in a.items():
#         if p == v:
#             if not k in G.node:
#                 continue
#             if len(G.out_edges(k)) == 0:
#                 G.remove_node(k)
#                 continue

for p in reduce_pkg:
    if not p in G.node:
        continue

    p = G.node[p]["src"]
    for (k,v) in a.items():
        if p == v:
            if not k in G.node:
                continue
            for i in G.successors(k):
                if "recommends" in G.edge[k][i][0]:
                    G.node[i]["color"]="#7777FF"
                else:
                    G.node[i]["color"]="#FF0000"
            G.remove_node(k)

checked = set()

for (a,b,c) in nx.get_edge_attributes(G, "recommends"):
    G.edge[a][b][c]["color"]="#7777FF"
    if b not in checked:
        checked.add(b)
        for (x,y) in G.in_edges(b):
            if not "recommends" in G.edge[x][y][0]:
                break
        else:
            G.node[b]["color"]="#7777FF"

nx.write_dot(G, "/dev/stdout")

