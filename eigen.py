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
debug = False
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
    if debug:
        print(local_trust)

    local_trust = np.array(local_trust)
    if debug:
        print(np.sum(local_trust, axis=1))
    normalized_local_trust = (local_trust.T / np.sum(local_trust, axis=1)).T
    if debug:
        print(normalized_local_trust)


    # iterate until convergence
    e = np.average(normalized_local_trust, axis=0)
    C = normalized_local_trust
    if debug:
        print(e)

    t = np.dot(C.T, e)
    if debug:
        print('t')

    scores = t.copy()
    dist = 999
    while dist > gamma:
        round_num += 1
        new_scores = np.dot(C.T, scores)
        dist = np.linalg.norm(new_scores - scores)
        scores = new_scores
        if debug:
            print('dist: ', dist, 'scores: ', scores)

    #print('percent mistake of false positive', num_fkups /
          #len(discard_list))
    THRESH = 0.03
    final_lend_to = scores > THRESH
    indices = np.where(final_lend_to == 1)
    if debug:
        print('\n!-- 4 Done, round nums = ', round_num)
        print('! -- decided to lend', final_lend_to)#, indices)
        print('creditw truth', creditw_truth)
    correct = np.array(final_lend_to) == np.array(creditw_truth)
    if debug:
        print('i deem these correct! ')
    #fp = fkups / number loans 
    #FAIL  fp = sum(np.invert(correct)) / sum(creditw_truth)
    if debug:
        print('2 FALSE POSE rate', fp)
    # number correctly lent to, over total number of creditworthy people
    if debug:
        print('number of creditworthy people in here',sum(creditw_truth))
    # positive, where it was a negative
    fp = np.logical_not(creditw_truth) *final_lend_to 
    percent_discovered = sum(final_lend_to * creditw_truth * 1)/ sum(creditw_truth)
    if debug:
        print('correct or not?' ,correct * 1)
        print('final lend to', final_lend_to * 1)
        #print('number failed at', sum(np.logical_not(creditw_truth) *final_lend_to))
        print('creditw_truth', creditw_truth * 1)

        print('correctly lent', final_lend_to * creditw_truth * 1)
        print(percent_discovered)
        #if debug:
        print('3 percent creditwoth discovered %0.3f' % percent_discovered)
    #print('\nout of total good', nx.get_node_attributes(G, 'creditw').values())
    curr_cost = -1 * sum(correct) + 5 * fp
    if debug:
        print('1 COST ', curr_cost)
    return curr_cost, fp, percent_discovered, round_num


p_creditw = 0.8
p_truepos = 0.9
p_falsepos = 0.1
p_initrec = 0.1
gamma = 0.001
#discovery_alg(my_graphs.G_COMPLETE, p_creditw, p_truepos, p_falsepos, p_initrec)
eigentrust_alg(my_graphs.G_COMPLETE, p_creditw, p_truepos, p_falsepos, p_initrec)


## --------
## PAPER RUN

results = []
for p_truepos, p_falsepos in [(.8,.2), (.95,.05)]:
    for p_initrec in [.1, .2]:
        for p_creditw in [.5, .8, .95]:
            cost_avg, fpos_avg, percdisc_avg, rounds_avg = [], [], [], []
            if debug:
                print("\n!-----------------!\n")
                print("GAMMA is 0.0001 CONDITIONS: pCW %0.2f, pinit %.2f" % (p_creditw, p_initrec),
                      " truepos, false pos: ", p_truepos, p_falsepos)
            for i in range(10):
                curr_cost, fpos, percent_discovered, round_num = \
                    eigentrust_alg(my_graphs.G_COMPLETE, p_creditw, p_truepos,
                                  p_falsepos, 0.0001)
                #discovery_alg(my_graphs.G_COMPLETE, p_creditw, p_truepos,
                cost_avg.append(curr_cost)
                fpos_avg.append(fpos)
                percdisc_avg.append(percent_discovered)
                rounds_avg.append(round_num)

            # print('cost per run, cost avg', cost_avg, len(cost_avg))
            if debug:
                print('fpos per run, fpos avg', fpos_avg)
            c = np.average(cost_avg)
            fp = np.average(fpos_avg)
            pd = np.average(percdisc_avg)
            r = np.average(rounds_avg)
            results.append([c, fp, pd, r])
            if debug:
                print('AVERAGED cost: %.2f, fpos: %.3f, p_disc: %.3f, round: %.1f'
                  %(c, fp, pd, r))
            print("\n!-----------------!\n")


print(np.array(results))
np.savetxt('./data.csv', np.array(results))

# eigentrust_alg(my_graphs.G_COMPLETE_SUB1
               # , p_creditw, p_truepos, p_falsepos, p_initrec)
# eigentrust_alg(my_graphs.G_COMPLETE_SUB2
               # , p_creditw, p_truepos, p_falsepos, p_initrec)

# eigentrust_alg(my_graphs.G_COMPLETE_SUB3
               # , p_creditw, p_truepos, p_falsepos, p_initrec)




# eigentrust_alg(my_graphs.G_BIPARTITE, p_creditw, p_truepos, p_falsepos, p_initrec)
# eigentrust_alg(my_graphs.G_BIPARTITE_SUB1
               # , p_creditw, p_truepos, p_falsepos, p_initrec)
# eigentrust_alg(my_graphs.G_BIPARTITE_SUB2
               # , p_creditw, p_truepos, p_falsepos, p_initrec)

# eigentrust_alg(my_graphs.G_BIPARTITE_SUB3
               # , p_creditw, p_truepos, p_falsepos, p_initrec)




