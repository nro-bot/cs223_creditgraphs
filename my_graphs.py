import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


# COMPLETE
# actual graph example for paper


small =  {0: [2, 8],
 1: [2, 3, 5, 6, 7, 9],
 2: [0, 1, 3, 4, 5, 9],
 3: [1, 2, 4, 7, 8],
 4: [2, 3, 6],
 5: [1, 2],
 6: [1, 4],
 7: [1, 3],
 8: [0, 3],
 9: [1, 2]}

G_SMALL = nx.from_dict_of_lists(small)


G_COMPLETE = nx.from_dict_of_lists({0: [1, 2, 3, 4, 5, 6, 7, 8, 9], 1: [0, 2, 3, 4, 5, 6, 7, 8, 9, 11, 21], 2: [0, 1, 3, 4, 5, 6, 7, 8, 9, 12, 22], 3: [0, 1, 2, 4, 5, 6, 7, 8, 9], 4: [0, 1, 2, 3, 5, 6, 7, 8, 9], 5: [0, 1, 2, 3, 4, 6, 7, 8, 9], 6: [0, 1, 2, 3, 4, 5, 7, 8, 9], 7: [0, 1, 2, 3, 4, 5, 6, 8, 9], 8: [0, 1, 2, 3, 4, 5, 6, 7, 9], 9: [0, 1, 2, 3, 4, 5, 6, 7, 8], 10: [11, 12, 13, 14, 15, 16, 17, 18, 19], 11: [10, 12, 13, 14, 15, 16, 17, 18, 19, 1, 21], 12: [10, 11, 13, 14, 15, 16, 17, 18, 19, 2, 22], 13: [10, 11, 12, 14, 15, 16, 17, 18, 19], 14: [10, 11, 12, 13, 15, 16, 17, 18, 19], 15: [10, 11, 12, 13, 14, 16, 17, 18, 19], 16: [10, 11, 12, 13, 14, 15, 17, 18, 19], 17: [10, 11, 12, 13, 14, 15, 16, 18, 19], 18: [10, 11, 12, 13, 14, 15, 16, 17, 19], 19: [10, 11, 12, 13, 14, 15, 16, 17, 18], 20: [21, 22, 23, 24, 25, 26, 27, 28, 29], 21: [20, 22, 23, 24, 25, 26, 27, 28, 29, 11, 1], 22: [20, 21, 23, 24, 25, 26, 27, 28, 29, 12, 2], 23: [20, 21, 22, 24, 25, 26, 27, 28, 29], 24: [20, 21, 22, 23, 25, 26, 27, 28, 29], 25: [20, 21, 22, 23, 24, 26, 27, 28, 29], 26: [20, 21, 22, 23, 24, 25, 27, 28, 29], 27: [20, 21, 22, 23, 24, 25, 26, 28, 29], 28: [20, 21, 22, 23, 24, 25, 26, 27, 29], 29: [20, 21, 22, 23, 24, 25, 26, 27, 28]}
              )
G_COMPLETE_SUB1 = G_COMPLETE.subgraph(range(10))
G_COMPLETE_SUB2 = G_COMPLETE.subgraph(range(10, 20))
G_COMPLETE_SUB3 = G_COMPLETE.subgraph(range(20, 30))



G_BIPARTITE = nx.from_dict_of_lists({0: [5, 6, 8, 9, 22], 1: [5, 6, 7, 8, 9, 24], 2: [7, 8, 9], 3: [5, 6, 7, 8, 9], 4: [5, 6, 7, 9], 5: [0, 1, 3, 4], 6: [0, 1, 3, 4], 7: [1, 2, 3, 4, 29], 8: [0, 1, 2, 3, 10], 9: [0, 1, 2, 3, 4], 10: [15, 16, 18, 19, 8, 25], 11: [15, 16, 17, 18, 19, 24], 12: [17, 18, 19], 13: [15, 16, 17, 18, 19], 14: [15, 16, 17, 19], 15: [10, 11, 13, 14, 21], 16: [10, 11, 13, 14], 17: [11, 12, 13, 14], 18: [10, 11, 12, 13], 19: [10, 11, 12, 13, 14], 20: [25, 26, 28, 29], 21: [25, 26, 27, 28, 29, 15], 22: [27, 28, 29, 0], 23: [25, 26, 27, 28, 29], 24: [25, 26, 27, 29, 11, 1], 25: [20, 21, 23, 24, 10], 26: [20, 21, 23, 24], 27: [21, 22, 23, 24], 28: [20, 21, 22, 23], 29: [20, 21, 22, 23, 24, 7]}
                                    )
G_BIPARTITE_SUB1 = G_BIPARTITE.subgraph(range(10))
G_BIPARTITE_SUB2 = G_BIPARTITE.subgraph(range(10, 20))
G_BIPARTITE_SUB3 = G_BIPARTITE.subgraph(range(20, 30))

graph = False
if __name__ == '__main__':
    print('!---- regenerating graphs\n')
    np.random.seed(88)

    if graph:
        plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

    n_nodes = 10
    sub1 = nx.complete_graph(n_nodes)
    sub2 = nx.complete_graph(n_nodes)
    sub3 = nx.complete_graph(n_nodes)
    G_COMPLETE = nx.disjoint_union(sub1, sub2)
    G_COMPLETE = nx.disjoint_union(G_COMPLETE, sub3)
    # 1 to 2
    G_COMPLETE.add_edge(1,n_nodes+1)
    G_COMPLETE.add_edge(2,n_nodes+2)
    # 2 to 3
    G_COMPLETE.add_edge(n_nodes+1, 2*n_nodes+1)
    G_COMPLETE.add_edge(n_nodes+2, 2*n_nodes+2)
    # 3 to 1
    G_COMPLETE.add_edge(2*n_nodes+1,1)
    G_COMPLETE.add_edge(2*n_nodes+2,2)
    if graph:
        nx.draw(G_COMPLETE, with_labels=True, node_size=700)


    # actual for paper, n = 30

    p_connect = 0.9
    n_part = 5

    sub1 = nx.bipartite.generators.random_graph(n_part, n_part, p_connect, seed=88)
    sub2 = nx.bipartite.generators.random_graph(n_part, n_part, p_connect, seed=88)
    sub3 = nx.bipartite.generators.random_graph(n_part, n_part, p_connect, seed=88)
    G_BIPARTITE = nx.disjoint_union(sub1, sub2)
    G_BIPARTITE = nx.disjoint_union(G_BIPARTITE, sub3)
    # sparse connections
    n_nodes = 2 * n_part

    # connect subgraph 1 to 2
    a, b = np.random.randint(n_nodes), np.random.randint(n_nodes, n_nodes*2)

    # connect subgraph 2 to 3
    # (10,20), (20,30)
    c, d = np.random.randint(n_nodes,n_nodes*2), np.random.randint(n_nodes*2, n_nodes*3)
    e, f = np.random.randint(n_nodes,n_nodes*2), np.random.randint(n_nodes*2, n_nodes*3)
    g, h = np.random.randint(n_nodes,n_nodes*2), np.random.randint(n_nodes*2, n_nodes*3)

    # connect subgraph 1 to 3
    i, j = np.random.randint(n_nodes), np.random.randint(n_nodes*2, n_nodes*3)
    k, l = np.random.randint(n_nodes), np.random.randint(n_nodes*2, n_nodes*3)
    m, n = np.random.randint(n_nodes), np.random.randint(n_nodes*2, n_nodes*3)

    G_BIPARTITE.add_edges_from([(a,b), (c, d), (e,f), (g, h), (i, j), (k, l), (m, n)])
    #print([(a,b), (c, d), (e,f), (g, h), (i, j), (k, l), (m, n)])
    #print(G_BIPARTITE.edges())

    if graph:
        nx.draw(G_BIPARTITE, with_labels=True, node_size=700)
        plt.show()
