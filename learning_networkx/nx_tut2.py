# https://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
# G.add_node(0, weight=8)
# G.add_node(1, weight=5)
# G.add_node(2, weight=3)
# labels = {n: G.nodes[n]['weight'] for n in G.nodes}

#labels = {n: str(n) + ';   ' + str(G.nodes[n]['weight']) for n in G.nodes}
# labels = {
    # n: str(n) + '\nweight=' + str(G.nodes[n]['weight']) if 'weight' in G.nodes[n] else str(n)
    # for n in G.nodes
# }

#colors = [G.nodes[n]['weight'] for n in G.nodes]
#nx.draw(G, with_labels=True, labels=labels, node_color=colors)
#plt.show()


G = nx.powerlaw_cluster_graph(n=12, m=2, p=0.1, seed=143)
G.add_node('abc', dob=1185, pob='u
