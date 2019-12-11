#!/usr/bin/env python
# coding: utf-8

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.Graph()
G = nx.powerlaw_cluster_graph(n=10, m=2, p=0.1, seed=143)

# Graph before assigning creditworthiness
nx.draw(G, with_labels=True, node_size=700)
plt.show()


for v in G.nodes():
    #assign_credit(v)
    G.nodes[v]['creditw'] = False
    G.nodes[v]['recommender'] = None
    G.nodes[v]['round_visited'] = None
    if np.random.random() > 0.6:
        G.nodes[v]['creditw'] = True

print('Initial Data for all nodes', G.nodes(data=True))


# Plot current graph status, with colors for creditw or not
colors = [G.nodes[n]['creditw'] for n in G.nodes]
labels = {n: str(n) + ';   ' +           str(G.nodes[n]['creditw']) for n in G.nodes}

nx.draw(G, with_labels=True, labels=labels, node_color=colors)
print(G.number_of_nodes())
print(G.nodes[2]['creditw'])
print(list(G.neighbors(2)))



# Begin algorithm 1
rec_start = set([2,3]) # initial recommendations
currently_checking = rec_start
visited_list = set([])
round_num = 0
next_round = set([])

while len(visited_list) < G.number_of_nodes():
    round_num += 1
    print('round num, visitied list', round_num, visited_list)

    for i in currently_checking:
        visited_list.add(i)
        G.nodes[i]['round_visited'] = round_num
        for neigh in G.neighbors(i): 
            if G.nodes[neigh]['creditw'] == True and G.nodes[neigh]['round_visited'] is None: # not visited yet
                #print('they were credit worth, check next round')
                next_round.add(neigh)
            else:
                pass # recommender lied :(
    if len(next_round) == 0:
        print('We hit a dead end :( ')
        break
    print('just checked, ', currently_checking)
    print('next checked, ', next_round )
    currently_checking = next_round
    next_round = set([])

print('Done, round numbs = ', round_num)
print('% Nodes visited', len(visited_list) / G.number_of_nodes())


print('Status after algorithm 1', G.nodes(data=True))


# Plot result of algorithm 1, with round visited noted by color and label
colors = []
labels = {n: '(' + str(n) + ') '  + str(G.nodes[n]['round_visited']) for n in G.nodes}

for n in G.nodes:
    if G.nodes[n]['round_visited'] != None:
        colors.append(G.nodes[n]['round_visited'])
    else:
        colors.append(-1)

nx.draw(G, with_labels=True, labels=labels, node_color=colors, cmap=plt.get_cmap('viridis'))
plt.show()

