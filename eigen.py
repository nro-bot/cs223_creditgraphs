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
def eigentrust_alg(G, p_creditw, p_truepos, p_falsepos, gamma):
    std_dev = 0.1
    num_nodes = G.number_of_nodes()

    creditw_truth = np.random.random(num_nodes) < p_creditw

    curr_cost = 0
    round_num = 0

    #  Begin eigen trust algorithm 
    G_adj = nx.to_numpy_matrix(G)
    local_trust = np.array(G_adj.copy() )

    for (x,y), element in np.ndenumerate(G_adj):
        if element:
            if creditw_truth[y]:
                rec = min(np.random.normal(p_truepos, std_dev),1)
            else:
                rec = max(np.random.normal(p_falsepos, std_dev),0)
            local_trust[x][y] = rec
        # else, not connected
    np.set_printoptions(precision=3)
    print(local_trust)

    local_trust = np.array(local_trust)
    print(np.sum(local_trust, axis=1))
    normalized_local_trust = (local_trust.T / np.sum(local_trust, axis=1)).T
    print(normalized_local_trust)


    # iterate until convergence
    e = np.average(normalized_local_trust, axis=0)
    C = normalized_local_trust
    print(e)

    t = np.dot(C.T, e)
    print('t')

    scores = t.copy()
    dist = 999
    while dist > gamma:
        round_num += 1
        new_scores = np.dot(C.T, scores)
        dist = np.linalg.norm(new_scores - scores)
        scores = new_scores
        print('dist: ', dist, 'scores: ', scores)

    #print('percent mistake of false positive', num_fkups /
          #len(discard_list))
    final_lend_to = scores > 0.1
    indices = np.where(final_lend_to == 1)
    print('\n!-- Done, round nums = ', round_num)
    print('! -- decided to lend', final_lend_to)#, indices)
    print('creditw truth', creditw_truth)
    correct = np.array(final_lend_to) == np.array(creditw_truth)
    print('i deem these correct! ')
    print('fals positive rate', np.sum(num_nodes - sum(correct)))
    #print('\nout of total good', nx.get_node_attributes(G, 'creditw').values())

    return curr_cost, round_num


p_creditw = 0.8
p_truepos = 0.9
p_falsepos = 0.1
p_initrec = 0.1
gamma = 0.001
#discovery_alg(my_graphs.G_COMPLETE, p_creditw, p_truepos, p_falsepos, p_initrec)
eigentrust_alg(my_graphs.G_COMPLETE, p_creditw, p_truepos, p_falsepos, p_initrec)

eigentrust_alg(my_graphs.G_COMPLETE_SUB1
               , p_creditw, p_truepos, p_falsepos, p_initrec)
eigentrust_alg(my_graphs.G_COMPLETE_SUB2
               , p_creditw, p_truepos, p_falsepos, p_initrec)

eigentrust_alg(my_graphs.G_COMPLETE_SUB3
               , p_creditw, p_truepos, p_falsepos, p_initrec)




eigentrust_alg(my_graphs.G_BIPARTITE, p_creditw, p_truepos, p_falsepos, p_initrec)
eigentrust_alg(my_graphs.G_BIPARTITE_SUB1
               , p_creditw, p_truepos, p_falsepos, p_initrec)
eigentrust_alg(my_graphs.G_BIPARTITE_SUB2
               , p_creditw, p_truepos, p_falsepos, p_initrec)

eigentrust_alg(my_graphs.G_BIPARTITE_SUB3
               , p_creditw, p_truepos, p_falsepos, p_initrec)





