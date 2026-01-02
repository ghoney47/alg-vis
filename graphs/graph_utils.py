import networkx as nx
import random as rand
from graphs import constants as c
import matplotlib.pyplot as plt
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
        

    def create_nodes(self, node_count):
        """
        Docstring for createNodes
        creates nodes in graph

        :param self: Graph Object
        :param nodeCount: (int) amount of nodes the user has specified 
        """

        for i in range (1, node_count + 1):
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

                print("From node: " + str(u))
                print("To node: " + str(v))

                if self.id == Graph.GRAPH or self.id == Graph.DIGRAPH: ##undirected edges 

                    ##randomly adds weight within range if weighted
                    if self.weighted:
                        weight = rand.randint(edge_lower, edge_upper)
                        self.graph.add_weighted_edges_from([(u, v, weight)])
                    else:
                        self.graph.add_edge(u, v)
                count -= 1
        else: 
            ##creating a graph that spans 
            all_nodes = list(self.graph.nodes)
            
            # Build a spanning tree first (ensures connectivity)
            # Connect nodes sequentially to guarantee spanning
            connected_nodes = [all_nodes[0]]  # Start with first node
            unconnected_nodes = all_nodes[1:]  # Rest are unconnected
            
            # Create spanning tree (n-1 edges for n nodes)
            while unconnected_nodes:
                # Pick a random node from connected set
                from_node = rand.choice(connected_nodes)
                # Pick a random node from unconnected set
                to_node = unconnected_nodes.pop(0)
                
                print("Spanning edge - From node: " + str(from_node))
                print("To node: " + str(to_node))
                
                # Add edge
                if self.weighted:
                    weight = rand.randint(edge_lower, edge_upper)
                    self.graph.add_weighted_edges_from([(from_node, to_node, weight)])
                else:
                    self.graph.add_edge(from_node, to_node)
                
                # Move to_node to connected set
                connected_nodes.append(to_node)
            
            # Calculate remaining edges to add
            edges_used = num_nodes - 1
            remaining_edges = edge_count - edges_used
            
            if remaining_edges > 0:
                # Add remaining edges randomly
                self._create_edges(remaining_edges, edge_lower, edge_upper, False)
            

            
                
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
        num_nodes = self.graph.number_of_nodes()

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
       
        #For testing
        ##DAG_levels = [[1, 2, 3, 4, 5], [6, 7, 8, 9]]


        print("DAG Levels: " + str(DAG_levels))
        self.DAG_levels = DAG_levels
        
                

        ##TODO: remove after testing
        edge_final_create = 0
        

        if not spans:
            print("SPAN FALSE")
            edge_remain = edge_count

            while (edge_remain > 0):

                ##iterating through dag levels
                for i in range(0, len(DAG_levels)):

                    ##if there are more levels
                    if i + 1 < len(DAG_levels):
                        to_nodes = DAG_levels[i+1]
                        from_nodes = DAG_levels[i]

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
                        print ("from node " + str(rand_from_node))

                        ##selecting to random node
                        rand_to_node = rand.randint(to_nodes[0], to_nodes[-1])
                        print ("to node " + str(rand_to_node))

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
                        edge_final_create += 1
                    
            print("Randomly created: " + str(edge_final_create))

        
        ##guarenteed span
        else: 
            print("SPAN TRUE")
            
            edge_remain = edge_count

            ##iterating through DAG levels
            for i in range(0, len(DAG_levels)-1):
                from_nodes = DAG_levels[i]
                to_nodes = DAG_levels[i+1]

                if len(to_nodes) < len(from_nodes):

                    ##tracking current to node
                    t_node_id = 0
                    ##iterating through level nodes and links each to a single node following
                    for f_node in from_nodes:

                        print("from node: " + str(f_node))
                        print("to node: " + str(to_nodes[t_node_id]))

                        ##randomly adds weight within range if weighted
                        if self.weighted:
                            weight = rand.randint(edge_lower, edge_upper)
                            print("weight: " + str(weight))
                            self.graph.add_weighted_edges_from([(f_node, to_nodes[t_node_id], weight)])
                            print("weighted edge created\n")
                        else:
                            self.graph.add_edge(f_node, to_nodes[t_node_id])
                            print("edge created\n")
                        
                        edge_final_create += 1
                        edge_remain -= 1

                        if t_node_id + 1 < len(to_nodes):
                            t_node_id += 1
                        else:
                            t_node_id = 0
                else:
                    
                    ##tracking current from node
                    f_node_id = 0

                    ##iterating through level nodes and links each to a single node following
                    for t_node in to_nodes:

                        print("from node: " + str(from_nodes[f_node_id]))
                        print("to node: " + str(t_node))

                        ##randomly adds weight within range if weighted
                        if self.weighted:
                            weight = rand.randint(edge_lower, edge_upper)
                            print("weight: " + str(weight))
                            self.graph.add_weighted_edges_from([(from_nodes[f_node_id], t_node, weight)])
                            print("weighted edge created\n")
                        else:
                            self.graph.add_edge(from_nodes[f_node_id], t_node)
                            print("edge created\n")
                        
                        edge_final_create += 1
                        edge_remain -= 1

                        if f_node_id + 1 < len(from_nodes):
                            f_node_id += 1
                        else:
                            f_node_id = 0

                    
            print("Hit all nodes: " + str(edge_final_create))
                    

        ##randomly adds edges if there are excess
        if edge_remain > 0:
            self._create_DAG(edge_remain, edge_lower, edge_upper, False, sources)


        print("Inputted: " + str(edge_count))

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



            
    

    def display(self, node_colors=None, edge_colors = None):
        """
        Displays graph with optional custom node colors
        :param self: Graph Object
        :param node_colors: Optional list of colors for nodes (in node order)
        :returns: matplotlib figure for display
        """
        fig = plt.figure(figsize=(10, 8))
        
        if self.id == c.GRAPH or self.id == c.DIGRAPH:
            pos = nx.shell_layout(self.graph)
            
            # If no custom colors provided, calculate default colors
            if node_colors is None:
                node_colors = []
                for node in self.graph.nodes():
                    in_degree = self.graph.in_degree(node) if self.id == c.DIGRAPH else len(list(self.graph.neighbors(node)))
                    if in_degree > 1:
                        node_colors.append('#F7971D')
                    elif in_degree == 1:
                        node_colors.append('#005499')
                    else:
                        node_colors.append('#FEFEFE')
            

            # if no custom edge colors provided, set all to black
            if edge_colors is None:
                edge_colors = ['#231F20'] * self.graph.number_of_edges()
            
            nx.draw(self.graph, pos, with_labels=True, node_size=800, font_size=10, 
                node_color=node_colors, edge_color= edge_colors, linewidths=2)
            
            edge_labels = nx.get_edge_attributes(self.graph, "weight")
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, 
                                        font_size=14, font_weight='bold', 
                                        bbox=dict(facecolor='yellow', alpha=0.8, edgecolor='none'))
        
        else:  # DAG
            pos = {}
            x_spacing = 2
            y_spacing = 1.5
            
            for level_index, nodes_in_level in enumerate(self.DAG_levels):
                num_nodes = len(nodes_in_level)
                for node_index, node in enumerate(nodes_in_level):
                    x = level_index * x_spacing
                    y = (node_index - (num_nodes - 1) / 2) * y_spacing
                    pos[node] = (x, y)
            
            # If no custom colors provided, calculate default colors
            if node_colors is None:
                node_colors = []
                for node in self.graph.nodes():
                    in_degree = self.graph.in_degree(node)
                    if in_degree > 1:
                        node_colors.append('#F7971D')
                    elif in_degree == 1:
                        node_colors.append('#005499')
                    else:
                        node_colors.append('#FEFEFE')
            
            # if no custom edge colors provided, set all to black
            if edge_colors is None:
                edge_colors = ['#231F20'] * self.graph.number_of_edges()
            
            nx.draw(self.graph, pos, with_labels=True, node_size=800, font_size=10, 
                node_color=node_colors, edgecolors = '#231F20', edge_color=edge_colors, linewidths=2)
            edge_labels = nx.get_edge_attributes(self.graph, 'weight')
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=10)
        
        return fig, node_colors, edge_colors




## for testing
## 1 -> graph, 0 -> digraph, 2 -> dag
g = Graph(1, False) ##creates a graph

g.create_nodes(12)


g.assign_edges(11, 0, 100, True, 5) 

g.display()



plt.show()



            