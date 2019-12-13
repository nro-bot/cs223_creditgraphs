# CS223 CreditGraphs
CS223: Efficient Algorithms for Detecting \& Classifying Credit Communities

Final project for Harvard CS 223 fall 2019 (probabilistic analysis of algorithms)

## File listing:

- `my_graphs.py` is where the graphs we're working with are defined; we hold them
    constant, but the code to generate new graphs is present in this file as
    well
- `alg.py` is where we implement discovery algorithm
- `eigen.py` is where we implement eigentrust algorithm
- A copy of our final report is located in the `pdf` in the home directory 

## Graphs

Our two sample graphs are:

- 30 nodes each
- `G_COMPLETE` is made of three complete graphs (10 nodes each), then we
        manually connect two nodes between each of the subgraphs (for 6 total
        added edges) to connect them
- `G_BIPARTITE` is constructed similarly, we create three separate
        subgraphs(they are actually identical due to the identical random seed),
        and add edges to connect the three. But to simulate a more interesting
        graph, subgraph1 to 2 is only connected by one edge. While subgraph 2 to
        3, and 3 to 1, are connected by three edges.
- We also have the subgraphs used to implement the above, as individual
        subgraphs not connected to each other; however these are actually
        defined directly in `alg1.py` and `eigen.py` for our final project
        results

## Usage: 
The code is very simple. To run it for our three comparison

    ``` 
    $ python alg1.py
    $ python eigen.py
    ```
To run it for each of the graphs above, change 

- `G_COMPLETE` to `G_BIPARTITE`
- or for the subgraphs, change the flags `subgraphs_complete` or `subgraphs_bipartite`


The data is written out to a `data.csv` file (warning, it's overwritten each
time -- we manually copied our data into a separate spreadsheet for analysis).

The rows are our parameter:

```
pCW .5, pinit .1, cond .8/.2
pCW .8, pinit .1, cond .8/.2
pCW .95, pinit .1, cond .8/.2
pCW .5, pinit .2, cond .8/.2
pCW .8, pinit .2, cond .8/.2
pCW .95, pinit .2, cond .8/.2
pCW .5, pinit .1, cond .95/.05
pCW .8, pinit .1, cond .95/.05
pCW .95, pinit .1, cond .95/.05
pCW .5, pinit .2, cond .95/.05
pCW .8, pinit .2, cond .95/.05
pCW .95, pinit .2, cond .95/.05
```

where `pCW` indicates the probability a node is creditworthy, `pinit` indicates
the probability a creditworthy node will be in our initial recommenders list,
and `cond` indicates the probability a neighbor is recommended in the true positive and false positive cases.

The columns are our four metrics:

```
COST	False positive rate	Pct Creditworthy Borrowers Disovered	Number of Rounds to Convergence

```
where false positive rate indicates the number of people we lent to, who turned
out not to be crediworthy, over all people who are creditworthy

## Credits

Nao Ouyang, Juspreet Singh Sandhu, Mark York
Dec 2019
