import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import my_graphs

#G = nx.Graph()
#G = nx.powerlaw_cluster_graph(n=10, m=2, p=0.1, seed=143)

#print(nx.to_dict_of_lists(my_graphs.G_BIPARTITE))
#print(nx.to_dict_of_lists(my_graphs.G_COMPLETE))
#print('hi')

display = False
def discovery_alg(G, p_creditw, p_truepos, p_falsepos, p_initrec):
    # TODD: need this?
    std_dev = 0.1
    num_nodes = G.number_of_nodes()
    for v in G.nodes():
        G.nodes[v]['creditw'] = False
        G.nodes[v]['round_visited'] = None
        if np.random.random() < p_creditw:
            G.nodes[v]['creditw'] = True
    # if display:
        # colors = [G.nodes[n]['creditw'] for n in G.nodes]
        # labels = {n: str(n) + ';   ' + \
                  # str(G.nodes[n]['creditw']) for n in G.nodes}
        # nx.draw(G, with_labels=True, labels=labels, node_color=colors)


    # create initial recommend list
    init_recmdrs = np.random.random(num_nodes) < p_initrec
    init_recmdrs = np.where(init_recmdrs == 1)
    print('begin rec list', init_recmdrs)

    curr_cost = 0
    currently_checking = init_recmdrs[0]

    visited_list = set([])
    next_recmders = set([])
    round_num = 0

    print(init_recmdrs[0])
    good_list = set(init_recmdrs[0])
    # TODO FIX
    discard_list = set([])

    num_fkups = 0

    num_truly_creditw = np.sum(np.array( list(
        nx.get_node_attributes(G, 'creditw').values())))
    print('truly creditw sum', num_truly_creditw)
    #print('\n, \n', G.nodes(data=True), '\n\n')

    while len(visited_list) < num_nodes:
        round_num += 1
        print('!-- ROUND NUMBER, visited list', round_num, visited_list)

        curr_cost -= len(good_list)

        for i in currently_checking:
            visited_list.add(i)
            G.nodes[i]['round_visited'] = round_num

            for neigh in G.neighbors(i):
                if neigh not in discard_list and neigh not in good_list:
                    # determining whether i think neighbor is trustworthy
                    if G.nodes[neigh]['creditw']:
                        rec = np.random.random() < p_truepos
                    else:
                        rec = np.random.random() < p_falsepos

                    # and calc metrics based on reality
                    if rec == True:
                        if G.nodes[neigh]['creditw']:
                            good_list.add(neigh)
                            curr_cost -= 1
                            next_recmders.add(neigh)
                        else:
                            num_fkups += 1
                            discard_list.add(neigh)
                            curr_cost += 5

                    else: # not rec'd
                        discard_list.add(neigh)

        if len(next_recmders) == 0:
            print('We hit a dead end :( ')
            print('cost', curr_cost)
            print('num mistakes', num_fkups)
            print('percent mistake of false positive', num_fkups /
                  len(discard_list))
            print('!-- FINAL ROUND NUMBER', round_num, visited_list, '\n')
            break

        currently_checking = next_recmders
        next_recmders = set([])


    print('Done, round numbs = ', round_num)
    print('% Nodes visited', len(visited_list) / G.number_of_nodes())
    percent_discovered = len(good_list) / num_truly_creditw
    #print('List of creditworthy borrowers',
    #      list(nx.get_node_attributes(G, 'creditw').values()))

    print('percent creditw discvoered', percent_discovered)
    print('\nthe good list', good_list,) # '\n', nx.get_node_attributes(G, 'creditw'))
    print('\nthe discard list', discard_list)
    print('\ntotal visited', len(good_list) + len(discard_list))
    #print('\nout of total good', nx.get_node_attributes(G, 'creditw').values())

    return curr_cost, round_num, percent_discovered # false positive?, 


p_creditw = 0.8
p_truepos = 0.9
p_falsepos = 0.1
p_initrec = 0.1
discovery_alg(my_graphs.G_COMPLETE, p_creditw, p_truepos, p_falsepos, p_initrec)
'''
print(G.nodes(data=True))
colors = []
# TODO : color correctly by round
#colors = [G.nodes[n]['round_visited'] for n in G.nodes]
labels = {n: '(' + str(n) + ') '  + \
          str(G.nodes[n]['round_visited']) for n in G.nodes}

for n in G.nodes:
    if G.nodes[n]['round_visited'] != None:
        colors.append(G.nodes[n]['round_visited'])
    else:
        colors.append(-1)

#print(colors)
#plt.figure(figsize=(10,10))
nx.draw(G, with_labels=True, labels=labels, node_color=colors, cmap=plt.get_cmap('viridis'))
plt.show()



colors = [G.nodes[n]['visited1'] for n in G.nodes]
nx.draw(G, with_labels=True, labels=labels, node_color=colors)
'''
