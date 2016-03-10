#

import networkx as nx
import sys
import itertools
import subprocess

DOT = "REPO.dot"
MAIN_PKGS = sys.argv[1:]

print("Querying dnf for dependencies", file=sys.stderr)
status = subprocess.call("dnf -q --disablerepo=*" \
                         + " --enablerepo=rawhide repoquery --enablerepo=fedora-rawhide-kernel-nodebug" \
                         + " --installroot=$PWD" \
                         + " --arch=noarch,x86_64" \
                         + " --exclude=glibc*" \
                         + " --requires --graphviz " \
                         + " ".join(MAIN_PKGS) + " > " + DOT, shell=True)

print("Reading result", file=sys.stderr)
G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(DOT))

G.add_edges_from(("REPO", n) for n in MAIN_PKGS)

def subtree(G, node):
    GS = G.copy()
    GS.remove_node(node)
    sd = nx.descendants(G, node)
    sd.add(node)
    s = set(sd)
    S = G.subgraph(s).copy()

    for n in sd:
        if n == node:
            continue
        ns = nx.ancestors(GS, n)
        if not ns.issubset(sd):
            S.remove_node(n)
            s.discard(n)

    pn = set(G.predecessors_iter(node))

    gs = set(
        itertools.chain.from_iterable(
            nx.shortest_path(G, "REPO", n) for n in pn
        ))

    GS = G.subgraph(gs.union(s)).copy()

    for n in pn.difference(s):
        GS.node[n]["fontcolor"] = "#FF0000"
        GS.node[n]["remove"] = "1"

    for n in s:
        GS.node[n]["fontcolor"] = "#006600"

    GS.remove_node("REPO")

    return S, GS

def subtree_size(G):
    return sum(int(v) for k,v in nx.get_node_attributes(G, "size").items())

def remove_nodes(G):
    return nx.get_node_attributes(G, "remove").keys()

sizes=[]

print("Calculating SVG for main tree", file=sys.stderr)
status = subprocess.call("dot -Gsmoothing=1 -Goverlap=prism -Gsplines=spline -Ecolor=#00000040 -Tsvg " \
                         + DOT + " > REPO.svg", shell=True)

for n in G.node:
    if n == "REPO":
        continue
    print("Calculating subtree of " + n, file=sys.stderr)
    S, GS = subtree(G, n)
    nx.drawing.nx_pydot.write_dot(GS, "Tree-" + n + ".dot")
    print("Calculating SVG for subtree of " + n, file=sys.stderr)
    status = subprocess.call("dot -Gsmoothing=1 -Goverlap=prism -Gsplines=spline -Ecolor=#00000040 -Tsvg " \
                             + "Tree-" + n + ".dot > Tree-" + n + ".svg", shell=True)
    sizes.append((n, subtree_size(S), len(S.node), len(GS.node) - len(S.node), remove_nodes(GS)))

print("""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title></title>
    <style type="text/css">
td {
  vertical-align: top;
  text-align: left;
}
</style>
  </head>
  <body>
""")

print("<h3>Graph:</h3><p><a href=\"REPO.svg\">Dependency Graph</a> of the following packages:<ul>")
for n in sorted(MAIN_PKGS):
    print("<li>" + n + "</li>")
print("</ul></p>")

print("<h3>Cycles:</h3><p><ul>")
for n in nx.simple_cycles(G):
    print("<li>" + " ".join(n) + "</li>")
print("</ul></p>")

print("<h3>Removal:</h3>")
print("<p>Filesystem space to save, if package is removed:<ul>")
print("<li>Size = kB saved on the filesystem</li>")
print("<li>Saved = number of rpm packages, which can be removed</li>")
print("<li>Reqs  = number of rpm packages, where the dependency has to be removed</li></ul>")
print("<ul><li>Green = packages which can be removed</li>")
print("<li>Red = packages where the dependency has to be removed</li></ul>")
print("<table>")
print("<tr><th>Size</th><th>Saved</th><th>Reqs</th><th>SVG</th><th>DOT</th><th>Name</th><th>Remove Dep from</th></tr>")
for n,s,l,r,p in sorted(sizes, key=lambda x: x[1], reverse=True):
    print("<tr><td>%d</td><td>%d</td><td>%d</td><td><a href=\"%s\">SVG</a></td><td><a href=\"%s\">DOT</a></td><td>%s</td><td>%s</td></tr>" % (s/1024, l, r, "Tree-" + n + ".svg", "Tree-" + n + ".dot", n, ", ".join(p)))
print("</table>")
print("""
  </body>
</html>
""")
