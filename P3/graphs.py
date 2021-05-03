import networkx as nx
import matplotlib.pyplot as plt
import random

def main():
    graph1 = nx.Graph()
    graph2 = nx.Graph()

    # creation of Erdos Renyi
    graph1.add_nodes_from(range(20))
    
    P = 0.15

    # Add edges to the graph randomly.
    for i in graph1.nodes():
        for j in graph1.nodes():
            if (i < j):
                
                # Take random number R.
                R = random.random()
                
                # Check if R<P add the edge to the graph else ignore.
                if (R < P):
                    graph1.add_edge(i, j)
        pos = nx.circular_layout(graph1)
        
        # Display the social network 
        nx.draw(graph1, pos, with_labels=1)
    plt.show()

    # Creation of Barabasi Albert
    for i in range(3):
        graph2.add_node(i)
    
    for i in range(2):
        graph2.add_edge(i, i+1)

    for i in range(3, 40):
        print(graph2.number_of_nodes())
        
        p = [ ]
        for n in range(graph2.number_of_nodes()):
            p.append(graph2.degree[n] / sum([graph2.degree[deg] for deg in range(graph2.number_of_nodes())]))
            

        nodes = [n for n in range(graph2.number_of_nodes())]
        random.shuffle(nodes)

        graph2.add_node(i)
        R = random.random()    

        for n in range(len(nodes)):
            if R > p[nodes[n]]:
                graph2.add_edge(i, nodes[n])
                break
        if graph2.degree(i) < 1:
            graph2.add_edge(i, random.randint(0,graph2.number_of_nodes()))


    pos = nx.circular_layout(graph2)
        
        # Display the social network 
    nx.draw(graph2, pos, with_labels=1)
    plt.show()


main()