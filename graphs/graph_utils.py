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
        self.DAG_levels = None
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
        :param spans: (boolean) if graph is guarenteed to span all nodes
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
    

            
                
    def _create_DAG(self, edge_count, edge_lower, edge_upper, spans, sources):
        """
        Docstring for create_DAG
        
        :param self: graph object
        :param edge_count: (int) number of edges
        :param edge_lower: (int) weight lower bound
        :param edge_upper: (int) weight upper bound
        :param spans: (boolean) if graph is guarenteed to span all nodes
        :param sources: specifying the number of sources in the DAG
        """

        ##set source nodes
        source_count = sources
        source_nodes = []

        for node in list(self.graph.nodes):

            ##adds nodes as sources 
            if source_count > 0:
                source_nodes.append(node)
                source_count -= 1
            else:
                break
        
        ##creates list representation and adds source nodes
        DAG_levels = [source_nodes]
        
        ##predetermines node placement within levels
        non_source_count = self.graph.number_of_nodes() - len(source_nodes)
        node_id = len(source_nodes) + 1


        
        level = 1

        while (non_source_count > 0):
            appending_nodes = []

            for i in range(0, rand.randint(1, non_source_count)):
                appending_nodes.append(node_id)
                node_id += 1

            DAG_levels.append(appending_nodes)

            ##updates nodes to be linked count
            non_source_count -= len(appending_nodes)

            ##moving to next level
            level += 1
       

        print("DAG Levels: " + str(DAG_levels))
        self.DAG_levels = DAG_levels
                


        ##linking nodes
        ##TODO: node placement works (as tested 12/24), finish connecting logic
        ##no guarenteed span
        if not spans:
            print("SPAN FALSE")
            edge_remain = edge_count

            while (edge_remain > 0):
                for i in range(0, len(DAG_levels)):
                    from_nodes = DAG_levels[i]

                    ##if there are more levels
                    if i + 1 < len(DAG_levels):
                        to_nodes = DAG_levels[i+1]
                

                    else:
                        ##returns the from nodes to previous level
                        from_nodes = DAG_levels[i-1]

                        to_nodes = DAG_levels[i]

                    ##edges to be created within the level
                    level_edges = rand.randint(0, edge_remain)

                    ##updating remaining edge count
                    edge_remain -= level_edges

                    ##creating edges
                    for j in range(0, level_edges):

                        ##selecting from random node
                        rand_from_node = rand.randint(from_nodes[0], from_nodes[-1])
                        print ("from node" + str(rand_from_node))

                        ##selecting to random node
                        rand_to_node = rand.randint(to_nodes[0], to_nodes[-1])
                        print ("to node" + str(rand_to_node))

                        while (rand_to_node == rand_from_node):
                                rand_to_node = rand.randint(to_nodes[0], to_nodes[-1])

                        ##randomly adds weight within range if weighted
                        if self.weighted:
                            weight = rand.randint(edge_lower, edge_upper)
                            print("weight: " + str(weight))
                            self.graph.add_weighted_edges_from([(rand_from_node, rand_to_node, weight)])
                            print("weighted edge created\n")
                        else:
                            self.graph.add_edge(rand_from_node, rand_to_node)
                            print("edge created\n")
                    


        
        ##guarenteed span
        else: 
            print("SPAN TRUE")



                                                    




    def assign_edges(self, edge_count, edge_lower, edge_upper, spans, sources):
        """
        Docstring for createEdges
        creates edges for the graph

        :param self: Graph Object
        :param edge_count: (int) number of edges
        :param edge_upper: (int) upper bound for edge weight
        :param edge_lower: (int) lower bound for edge weight
        :param spans: (boolean) if graph is guarenteed to span all nodes
        """

        ##determines if graph is DAG for creation
        if self.id != 2:
            self._create_edges(edge_count, edge_lower, edge_upper, spans)
        else:
            self._create_DAG(edge_count, edge_lower, edge_upper, spans, sources)



            
    

    def display(self):
        """
        Docstring for display
        
        function draws the stored graph in the object as a matlabplot in a random graph layout
        :param self: Graph Object
        """
        nx.draw(g.graph, with_labels=True, pos=nx.shell_layout(g.graph))



## for testing
## 1 -> graph, 0 -> digraph, 2 -> dag
g = Graph(2, True) ##creates a graph

g.create_nodes(11)


g.assign_edges(10, 0, 100, False, 5) 


if g.id != 2:
    pos = nx.shell_layout(g.graph)  
    # edge weight labels
    edge_labels = nx.get_edge_attributes(g.graph, "weight")
    nx.draw_networkx_edge_labels(g.graph, pos, edge_labels=edge_labels,font_size=14,font_weight='bold', bbox=dict(facecolor='yellow', alpha=0.8, edgecolor='none'))
    nx.draw(g.graph, with_labels=True, pos=pos) ##must call the graph of g
    plt.show()

else: 
    ##this completely works, use in final!!!!!
    pos = {}
    x_spacing = 2  # Horizontal space between levels
    y_spacing = 1.5  # Vertical space between nodes

    for level_index, nodes_in_level in enumerate(g.DAG_levels):
        num_nodes = len(nodes_in_level)
        for node_index, node in enumerate(nodes_in_level):
            x = level_index * x_spacing
            y = (node_index - (num_nodes - 1) / 2) * y_spacing
            pos[node] = (x, y)

    nx.draw(g.graph, pos, with_labels=True, node_size=800, font_size=10)
    edge_labels = nx.get_edge_attributes(g.graph, 'weight')
    nx.draw_networkx_edge_labels(g.graph, pos, edge_labels=edge_labels, font_size=10)
    plt.show()



            