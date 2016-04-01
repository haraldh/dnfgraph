#

import networkx as nx
import sys
import itertools
import subprocess
import os

d = os.path.dirname("html")
if not os.path.exists("html"):
    os.makedirs("html")

DOT = "html/MAIN.dot"
MAIN_PKGS = [i for i in sys.argv[1:] if i[:2] != '--']
EXTRA_ARGS = [i for i in sys.argv[1:] if i[:2] == '--']

print("Querying dnf for dependencies", file=sys.stderr)
cmd = "dnf -q repoquery --installroot=$PWD " + " ".join(EXTRA_ARGS) + " --requires --graphviz " \
                         + " ".join(MAIN_PKGS) + " > " + DOT

print("Executing: " + cmd, file=sys.stderr)

status = subprocess.call(cmd, shell=True)

print("Reading result", file=sys.stderr)
G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(DOT))

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
            nx.shortest_path(G, "MAIN", n) for n in pn
        ))

    GS = G.subgraph(gs.union(s)).copy()

    for n in pn.difference(s):
        GS.node[n]["fontcolor"] = "#FF0000"
        GS.node[n]["remove"] = "1"

    for n in s:
        GS.node[n]["fontcolor"] = "#006600"

    GS.remove_node("MAIN")

    return S, GS

def subtree_size(G):
    return sum(int(v) for k,v in nx.get_node_attributes(G, "size").items())

def remove_nodes(G):
    return nx.get_node_attributes(G, "remove").keys()

sizes=[]

print("Calculating SVG for main tree", file=sys.stderr)
status = subprocess.call("dot -Gsmoothing=1 -Goverlap=prism -Gsplines=spline -Ecolor=#00000040 -Tsvg " \
                         + DOT + " > html/MAIN.svg", shell=True)

for n in G.node:
    if n == "MAIN":
        continue
    print("Calculating subtree of " + n, file=sys.stderr)
    S, GS = subtree(G, n)
    nx.drawing.nx_pydot.write_dot(GS, "html/Tree-" + n + ".dot")
    print("Calculating SVG for subtree of " + n, file=sys.stderr)
    status = subprocess.call("dot -Gsmoothing=1 -Goverlap=prism -Gsplines=spline -Ecolor=#00000040 -Tsvg " \
                             + "html/Tree-" + n + ".dot > html/Tree-" + n + ".svg", shell=True)
    sizes.append((n, subtree_size(S), len(S.node), len(GS.node) - len(S.node), remove_nodes(GS)))

index_file = open('html/index.html', 'w')

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
""", file=index_file)

print("<h3>Graph:</h3><p><a href=\"MAIN.svg\">Dependency Graph</a> of the following packages:<ul>", file=index_file)
for n in sorted(MAIN_PKGS):
    print("<li>" + n + "</li>", file=index_file)
print("</ul></p>", file=index_file)
print("<p>Installation size: %d" % (subtree_size(G)), file=index_file)
print("<h3>Cycles:</h3><p><ul>", file=index_file)
for n in nx.simple_cycles(G):
    print("<li>" + " ".join(n) + "</li>", file=index_file)
print("</ul></p>", file=index_file)

print("<h3>Removal:</h3>", file=index_file)
print("<p>Filesystem space to save, if package is removed:<ul>", file=index_file)
print("<li>Size = kB saved on the filesystem</li>", file=index_file)
print("<li>Saved = number of rpm packages, which can be removed</li>", file=index_file)
print("<li>Reqs  = number of rpm packages, where the dependency has to be removed</li></ul>", file=index_file)
print("<ul><li>Green = packages which can be removed</li>", file=index_file)
print("<li>Red = packages where the dependency has to be removed</li></ul>", file=index_file)
print("<table>", file=index_file)
print("<tr><th>Size</th><th>Saved</th><th>Reqs</th><th>SVG</th><th>DOT</th><th>Name</th><th>Remove Dep from</th></tr>", file=index_file)
for n,s,l,r,p in sorted(sizes, key=lambda x: x[1], reverse=True):
    print("<tr><td>%d</td><td>%d</td><td>%d</td><td><a href=\"%s\">SVG</a></td><td><a href=\"%s\">DOT</a></td><td>%s</td><td>%s</td></tr>" % (s/1024, l, r, "Tree-" + n + ".svg", "Tree-" + n + ".dot", n, ", ".join(p)), file=index_file)
print("</table>", file=index_file)
print("""
  </body>
</html>
""", file=index_file)
