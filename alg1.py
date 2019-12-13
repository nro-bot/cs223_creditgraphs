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
def discovery_alg(G, p_creditw, p_truepos, p_falsepos, p_initrec):
    # TODD: need this?
    std_dev = 0.1
    num_nodes = G.number_of_nodes()
    for v in G.nodes():
        G.nodes[v]['creditw'] = False
        G.nodes[v]['round_visited'] = None
        # Assign randomly to be crediworthy
        if np.random.random() < p_creditw:
            G.nodes[v]['creditw'] = True
    # if display:
        # colors = [G.nodes[n]['creditw'] for n in G.nodes]
        # labels = {n: str(n) + ';   ' + \
                  # str(G.nodes[n]['creditw']) for n in G.nodes}
        # nx.draw(G, with_labels=True, labels=labels, node_color=colors)


    # create initial recommend list
    init_recmdrs = []
    for i in range(num_nodes):
        if G.nodes[i]['creditw'] == True:
            if np.random.random() < p_initrec:
                init_recmdrs.append(i)
    if debug:
        print('init recmders', init_recmdrs)
    #init_recmdrs = np.random.random(num_nodes) < p_initrec
    #init_recmdrs = np.where(init_recmdrs == 1)

    if debug:
        print('begin rec list', init_recmdrs)

    curr_cost = 0
    currently_checking = init_recmdrs

    visited_list = set([])
    next_recmders = set([])
    round_num = 0

    if debug:
        print('init recs', init_recmdrs)
    good_list = set(init_recmdrs)
    # TODO FIX
    discard_list = set([])

    num_fkups = 0

    num_truly_creditw = np.sum(np.array( list(
        nx.get_node_attributes(G, 'creditw').values())))
    if debug:
        print('truly creditw sum', num_truly_creditw)
    #print('\n, \n', G.nodes(data=True), '\n\n')

    while len(visited_list) < num_nodes:
        round_num += 1
        if debug:
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
                            # recommended, but was bad :'(
                            num_fkups += 1
                            discard_list.add(neigh)
                            curr_cost += 5

                    else: # not rec'd
                        discard_list.add(neigh)

        if len(next_recmders) == 0:
            if debug:
                print('1 COST', curr_cost)
            if (len(good_list) + num_fkups) != 0:
                fpos = num_fkups / (len(good_list) + num_fkups)
            else:
                print('NO FPOS DATA, DIVISON BY ZERO')
                fpos = -9999
            if debug:
                print('2 NICE, percent mistake of false positive')
            if debug:
                print('We hit a dead end :(')
                print('num mistakes', num_fkups)
                print('!-- FINAL ROUND NUMBER', round_num, visited_list, '\n')
            break

        currently_checking = next_recmders
        next_recmders = set([])


    percent_discovered = len(good_list) / num_truly_creditw
    if debug:
        print('3 percent creditw discovered', percent_discovered)
        print('4 Done, round numbs = ', round_num)
    if debug:
        print('% Nodes visited', len(visited_list) / G.number_of_nodes())
        print('\nthe good list', good_list,) # '\n', nx.get_node_attributes(G, 'creditw'))
        print('\nthe discard list', discard_list)
        print('\ntotal visited', len(good_list) + len(discard_list))
        #print('\nout of total good', nx.get_node_attributes(G, 'creditw').values())

    return curr_cost, fpos, percent_discovered, round_num # false positive?, 


np.set_printoptions(precision=3, suppress=True)

results = []

subgraphs_complete = False # run with 3 subgraphs
subgraphs_bipartite = True 
for p_truepos, p_falsepos in [(.8,.2), (.95,.05)]:
    for p_initrec in [.1, .2]:
        for p_creditw in [.5, .8, .95]:
            cost_avg, fpos_avg, percdisc_avg, rounds_avg = [], [], [], []
            print("\n!-----------------!\n")
            if debug:
                print("CONDITIONS: pCW %0.2f, pinit %.2f" % (p_creditw, p_initrec),
                      " truepos, false pos: ", p_truepos, p_falsepos)
            for i in range(10):
                if subgraphs_complete:
                    # NOTE!
                    num_nodes = 10

                    sub_complete = nx.complete_graph(num_nodes)

                    curr_cost_total, fp_list, cdisc_list = 0, [], []
                    for i in range(3):
                        curr_cost, fpos, percent_discovered, round_num = \
                            discovery_alg(sub_complete, p_creditw, p_truepos,
                                          p_falsepos, p_initrec)
                        curr_cost_total += curr_cost
                        fp_list.append(fpos)
                        cdisc_list.append(percent_discovered)
                    curr_cost = curr_cost_total
                    fpos = np.average(fp_list)
                    percent_discovered = np.average(cdisc_list)
                    # round_num = round_num
                elif subgraphs_bipartite:
                    # NOTE!
                    n_part = 5
                    p_connect = 0.9
                    sub_bipartite = nx.bipartite.generators.random_graph(n_part, n_part, p_connect, seed=88)
                    curr_cost_total, fp_list, cdisc_list = 0, [], []
                    for i in range(3):
                        curr_cost, fpos, percent_discovered, round_num = \
                            discovery_alg(sub_bipartite, p_creditw, p_truepos,
                                          p_falsepos, p_initrec)
                        curr_cost_total += curr_cost
                        fp_list.append(fpos)
                        cdisc_list.append(percent_discovered)
                    curr_cost = curr_cost_total
                    fpos = np.average(fp_list)
                    percent_discovered = np.average(cdisc_list)
                    # round_num = round_num

                else:
                    curr_cost, fpos, percent_discovered, round_num = \
                        discovery_alg(my_graphs.G_COMPLETE, p_creditw, p_truepos,
                                      p_falsepos, p_initrec)
                #discovery_alg(my_graphs.G_COMPLETE, p_creditw, p_truepos,
                cost_avg.append(curr_cost)
                fpos_avg.append(fpos)
                percdisc_avg.append(percent_discovered)
                rounds_avg.append(round_num)

            # print('cost per run, cost avg', cost_avg, len(cost_avg))
            # print('fpos per run, fpos avg', fpos_avg)
            c = np.average(cost_avg)
            fp = np.average(fpos_avg)
            pd = np.average(percdisc_avg)
            r = np.average(rounds_avg)
            results.append([c, fp, pd, r])
            if debug:
                print('%.2f, %.3f, %.3f, %.1f\n' %(c, fp, pd, r))
            if debug:
                print('AVERAGED cost: %.2f, fpos: %.3f, p_disc: %.3f, round: %.1f'
                      %(c, fp, pd, r))
                print("\n!-----------------!\n")
print(np.array(results))
np.savetxt('./data.csv', np.array(results))

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
