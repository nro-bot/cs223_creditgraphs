import networkx as nx
import matplotlib.pyplot as plt


# graph with numbers for nodes
g = nx.Graph()
g.add_edge(1,3,weight=0.2)
g.add_edge(3,2,weight=0.3)
nx.draw(g)

plt.show(g)

g2 = nx.Graph()
g2.add_edge('A','B',weight=0.9)
g2.add_node('C')

pos = nx.spring_layout(g2)
nx.draw(g2, pos, node_size=700)
nx.draw_networkx_labels(g2, pos)

labels = nx.get_edge_attributes(g2, 'weight')
nx.draw_networkx_edge_labels(g2, pos, edge_labels=labels)

plt.show(g2)


# graph with labels for nodes

G = nx.Graph()
e = [('a', 'b', 0.3), ('b', 'c', 0.9), ('a', 'c', 0.5), ('c', 'd', 1.2)]
G.add_weighted_edges_from(e)

pos = nx.spring_layout(G)
nx.draw(G,pos,node_size=700)
nx.draw_networkx_labels(G, pos)

labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show(G)


print(nx.dijkstra_path(G, 'a', 'd'))

'''
#Asignment 2 Comparision
for i in range(3):
    GraphA=lstA[i]
    GraphB=lstB[i]

    Aad = nx.adjacency_matrix(GraphA)
    Bad = nx.adjacency_matrix(GraphB)
    count=i
    count=count+1
    print('-------------****************-------------')
    print('Number of nodes: ',count*100)
    for k in range(2,4):
        print('An^k','n',count*100,'k',k)
        A_nk=np.linalg.matrix_power(Aad.todense(), k)
        #print(B_nk)
        plt.plot(A_nk)
        plt.show()
        print('Bn^k','n',count*100,'k',k)
        B_nk=np.linalg.matrix_power(Bad.todense(), k)
        #print(B_nk)
        plt.plot(B_nk)
        plt.show()
    print('------************------')
'''

