import networkx as nx
import random as rand

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
        if id_num == 0 or id_num == 2:
            self.graph = nx.DiGraph
        else:
            self.graph = nx.Graph
        self.weighted = weighted ##true is weighted, false is unweighted

    def create_nodes(self, nodeCount):
        """
        Docstring for createNodes
        creates nodes in graph

        :param self: Graph Object
        :param nodeCount: (int) amount of nodes the user has specified 
        """

        for i in range (0, nodeCount):
            self.graph.add_node(i)

    def _create_edges(self, edge_count, edge_upper, edge_lower, spans):
        """
        Docstring for _edges
        helper to generate edges for assign_edges

        :param self: Graph Object
        :param edge_count: (int) number of edges
        :param edge_upper: (int) upper bound for edge weight
        :param edge_lower: (int) lower bound for edge weight
        """
        if not spans:
            count = edge_count
            while (count > 0):
                    
                ##selects random start node, will allow self loops
                u = rand.randint(1, self.graph.number_of_nodes)
                v = rand.randint(1, self.graph.number_of_nodes)

                ##randomly adds weight within range
                if self.weighted:
                    weight = rand.randint(edge_upper, edge_lower)
                    self.graph.add_weighted_edges_from(u, v, weight=weight)
                else:
                    self.graph.add_edges_from(u, v)
                count -= 1
        else: 
            ##creating a graph that spans 
            count = edge_count
            while (count > 0):
                ##iterates through all nodes 
                for node in list(self.graph.nodes):
                ##TODO: check if edge exists, if not, draws new connection

                    ##checks if connection exists
                    if len(self.graph.adj[node]) == 0:
                        
                        ##selecting random connection 
                        rand_node = rand.randint(0, self.graph.number_of_nodes)

                        ##ensuring node selected has no more than 1 connection, and is not the current node
                        while (rand_node != node and len(self.graph.adj[rand_node]) < 2):
                            rand_node = rand.randint(0, self.graph.number_of_nodes)

                ##randomly adds weight within range
                if self.weighted:
                    weight = rand.randint(edge_upper, edge_lower)
                    self.graph.add_weighted_edges_from(node, rand_node, weight=weight)
                else:
                    self.graph.add_edges_from(node, rand_node)
                count -= 1
                            

                        


                                                    




    def assign_edges(self, edge_count, edge_upper, edge_lower, spans):
        """
        Docstring for createEdges
        creates edges for the graph

        :param self: Graph Object
        :param edge_count: (int) number of edges
        :param edge_upper: (int) upper bound for edge weight
        :param edge_lower: (int) lower bound for edge weight
        :param spans: (boolean) if graph will be guarenteed complete
        """

        ## if edges specified is greater than nodes and called for, complete graph is drawn 
        if edge_count == self.graph.number_of_nodes - 1 and spans:
            if self.weighted:
                self._create_edges(edge_count, edge_upper, edge_lower, spans)
                ##TODO: create weighted complete graph


                ## draws complete graph
            else: 
                self.graph = nx.complete_graph(self.graph.number_of_nodes)

            ##if complete graph specified with more edges than nodes
        elif spans and self.graph.number_of_nodes - 1 < edge_count:
            count = edge_count

    

        else:
            ##randomly draws edges, only graphs at least nodes - 1 edges can be complete


            
    

    def display(self):
        """
        Docstring for display
        
        function draws the stored graph in the object as a matlabplot in a random graph layout
        :param self: Graph Object
        """
        return nx.draw_random(self.graph)

    def get_edge_type(self):
        """
        Docstring for get_ident
        returns weighted or not
        
        :param self: Graph object
        """
        return self.weighted


## for testing
g = Graph(1, True) ##creates a weighted graph

g.create_nodes(20)
g.create_edges(20, 


            