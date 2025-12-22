import networkx as nx
import random as rand
import matplotlib.pyplot as plt ##TODO: remove after development

##should take a state, and return a matlabplot 
class Graph:

    ## class constants for distinctions
    DIGRAPH = 0
    GRAPH = 1
    DAG = 2


    ## creates a graph or digraph
    def __init__(self, id_num, weighted):
        """
        Docstring for __init__

        :param self: Graph object
        :param id_num: (int) Identifier that corresponds to the class constant
        :param weighted: (boolean) Marks if the graphs will have weighted edges or not
        """
        self.id = id_num
        if id_num == 0 or id_num == 2:
            self.graph = nx.DiGraph()
        else:
            self.graph = nx.Graph()
        self.weighted = weighted ##true is weighted, false is unweighted

    def create_nodes(self, nodeCount):
        """
        Docstring for createNodes
        creates nodes in graph

        :param self: Graph Object
        :param nodeCount: (int) amount of nodes the user has specified 
        """

        for i in range (1, nodeCount + 1):
            self.graph.add_node(i)

    def _create_edges(self, edge_count, edge_lower, edge_upper, spans):
        """
        Docstring for _edges
        helper to generate edges for assign_edges

        :param self: Graph Object
        :param edge_count: (int) number of edges
        :param edge_upper: (int) upper bound for edge weight
        :param edge_lower: (int) lower bound for edge weight
        """
        num_nodes = self.graph.number_of_nodes()

        ##not enough edges to span, or span is not specified
        if not spans or edge_count < num_nodes-1:
            count = edge_count
            while (count > 0):
                    
                ##selects random start node, will allow self loops
                u = rand.randint(1, num_nodes)
                v = rand.randint(1, num_nodes)
                if self.id == Graph.GRAPH or self.id == Graph.DIGRAPH: ##undirected edges 

                    ##randomly adds weight within range if weighted
                    if self.weighted:
                        weight = rand.randint(edge_lower, edge_upper)
                        self.graph.add_weighted_edges_from([(u, v, weight)])
                    else:
                        self.graph.add_edges_from(u, v)
                count -= 1
        else: 
            ##creating a graph that spans 
            
            ##iterates through all nodes 
            for node in list(self.graph.nodes):

                ##checks if nodes has 1 or less connections
                if len(self.graph.adj[node]) < 2:
                    
                    ##selecting random 'to' node
                    rand_node = rand.randint(1, num_nodes+1)

                    ##ensuring node selected has no more than 1 connection, is not the current node, and the edge does not already exist 
                    while (rand_node == node and len(self.graph.adj[rand_node]) > 2 and (not (node in self.graph.adj[rand_node]))):
                        rand_node = rand.randint(1, num_nodes+1)

                    ##randomly adds weight within range if weighted
                    if self.weighted:
                        weight = rand.randint(edge_lower, edge_upper)
                        self.graph.add_weighted_edges_from([(node, rand_node, weight)])
                    else:
                        self.graph.add_edge(node, rand_node)
           
            
            if edge_count - (num_nodes - 1) > 0:
                ##if excess nodes, recursively calls the method to create further random connections
                self._create_edges(edge_count - (num_nodes - 1), edge_lower, edge_upper, False)
            
                
   


                                                    




    def assign_edges(self, edge_count, edge_lower, edge_upper, spans):
        """
        Docstring for createEdges
        creates edges for the graph

        :param self: Graph Object
        :param edge_count: (int) number of edges
        :param edge_upper: (int) upper bound for edge weight
        :param edge_lower: (int) lower bound for edge weight
        :param spans: (boolean) if graph will be guarenteed complete
        """

        if self.id == Graph.GRAPH or self.id == Graph.DIGRAPH: 
            self._create_edges(edge_count, edge_lower, edge_upper, spans)
        else: ##DAG
            print("DAG")


            
    

    def display(self):
        """
        Docstring for display
        
        function draws the stored graph in the object as a matlabplot in a random graph layout
        :param self: Graph Object
        """
        nx.draw(g.graph, with_labels=True, pos=nx.shell_layout(g.graph))



## for testing
## 1 -> graph, 0 -> digraph, 2 -> dag
g = Graph(0, True) ##creates a graph

g.create_nodes(5)
g.assign_edges(4, 0, 100, True) 

nx.draw(g.graph, with_labels=True, pos=nx.shell_layout(g.graph)) ##must call the graph of g


plt.show()


            