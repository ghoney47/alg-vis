import networkx as nx

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
        self.edge_type = weighted 

    def create_nodes(self, nodeCount):
        """
        Docstring for createNodes
        creates nodes in graph

        :param self: Graph Object
        :param nodeCount: (int) amount of nodes the user has specified 
        """

        for i in range (0, nodeCount):
            self.graph.add_node(i)

    def create_edges(self, edge_count, edge_upper, edge_lower):
        """
        Docstring for createEdges
        
        :param self: Graph Object
        :param edgeCount: (int) amount of edges user has specified
        :param edgeWR: (int) Range of edge weights
        """

        ## if edges specified is greater than nodes, complete graph is drawn 
        if edge_count >= self.graph.number_of_nodes - 1:
            self.graph = nx.complete_graph(self.graph.number_of_nodes)
        else:
            e
    

    def display(self):
        """
        Docstring for display
        
        function draws the stored graph in the object as a matlabplot in a random graph layout
        :param self: Graph Object
        """

    def get_edge_type(self):
        """
        Docstring for get_ident
        returns weighted or not
        
        :param self: Graph object
        """
        return self.edge_type


            