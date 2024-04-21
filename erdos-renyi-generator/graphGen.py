import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import defaultdict
from apsp import APSP
import getopt
import sys
import json

def usage(tool_name):
    print("")
    print ("usage: " + tool_name + " -c <configFile>")
    print ("")


def main(argv):
    configFile = ''
    routers = 0
    p = 0.5
    try:
        opts, args = getopt.getopt(argv[1:],
                                    "hc:o:",
                                    ["configFile="])
    except getopt.GetoptError:
        usage(argv[0])
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv[0])
            sys.exit()
        elif opt in ("-c", "--configFile"):
            configFile = arg
    # Ensure that configFile is provided.
    if configFile == '':
        print("Must specify config file")
        sys.exit(1)

    # Read configuration.
    with open(configFile, 'r') as cFile:
        config = json.load(cFile)

    # Read number of routers from configuration.
    if "routers" in config:
        routers = int(config["routers"])
    else:
        print("Missing number of routers in config")
        sys.exit(1)

    # Read number of clients from configuration.
    if "p-edge" in config:
        p = float(config["p-edge"])
    else:
        print("Missing p-edge in config")
        sys.exit(1)


# Create an Erdős-Rényi graph with 50 nodes and a probability of 0.2 for edge creation
<<<<<<< Updated upstream
    g = nx.erdos_renyi_graph(routers, p, seed=40) # seed 50 for reproducibility
    # if (not nx.is_connected(g)):
    #     print("ERROR: Graph generation failed. Graph is not connected! Please try to increase the value of 'routers', or 'p-edge' in config!")
    #     sys.exit(1)
=======
    g = nx.erdos_renyi_graph(routers, p, seed=50) # seed 50 for reproducibility
    if (not nx.is_connected(g)):
        print("ERROR: Graph generation failed. Graph is not connected! Please try to increase the value of 'routers', or 'p-edge' in config!")
        sys.exit(1)
>>>>>>> Stashed changes

    # Drawing the graph
    plt.figure(figsize=(10, 8))  # Set the size of the figure
    labels = {node: node + 1 for node in g.nodes()} # just to satisfy naming convention (1-indexing in the networks emulator)

    nx.draw(g, with_labels=True, labels=labels, node_color='skyblue', node_size=500, edge_color='k', linewidths=1, font_size=15)
    plt.title("Erdős-Rényi Graph")

    # print({k:v for k,v in g.adjacency()})
    graph = defaultdict(dict)
    for k,v in g.adjacency():
        if k == 0:
            kname = "node"
        else:
            kname = "node"+str(k+1)
        for neighbour, _ in v.items():
            if neighbour == 0:
                neighbourname = "node"
            else:
                neighbourname = "node"+str(neighbour+1)
            graph[kname][neighbourname] = 1


    # Save the plot to a PDF file
    plt.savefig("erdos_renyi_graph.pdf")
    plt.close()

    apsp = APSP(graph)

    apsp.run()

if __name__ == "__main__":
    main(sys.argv)


