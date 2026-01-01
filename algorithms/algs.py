import networkx as nx
from collections import deque
import heapq as hq

class Alg_Engine:
    
    def __init__(self, graph):
        """
        Docstring for __init__
        
        :param self: Alg_Engine object
        :param graph: Graph object
        """
        self.graph = graph
        

    def breadth_first_search(self, source): ##TODO: check implementation
        """
        Docstring for breadth_first_search
        guarentees shortest path for uneweighted graphs
        index 0 -> node 1 for marked, dist_to, edge_to
        
        :param self: Alg_Engine object
        returns marked, edge_to, dist_to, order arrays for visualization in app
        """
        num_nodes = self.graph.number_of_nodes()
        marked = [False] * num_nodes #tracks if nodes are marked
        dist_to = [-1] * num_nodes #tracks distance from source
        edge_to = [-1] * num_nodes #tracks previous node 
        order = []

        q = deque([])
        marked[source - 1] = True
        dist_to[source - 1] = 0
        q.append(source) ## enqueues first node
        
        while len(q) > 0:
            v = q.popleft() ##dequeue leading node
            order.append(v) ##adds popped node to order


            for w in self.graph.neighbors(v):
                if not marked[w - 1]:
                    ##updates w's information in arrays, adds to queue
                    marked[w - 1] = True
                    edge_to[w - 1] = v
                    dist_to[w - 1] = dist_to[v - 1] + 1
                    q.append(w)
        
        return marked, edge_to, dist_to, order

        

    @staticmethod
    def _dfs_helper(graph, source, marked, edge_to, dist_to, order):
        """
        Docstring for _dfs_helper
        
        :param source: (int) starting node
        :param marked: (boolean array) array marking if each node has been visited -> index 0 = node 1
        :param edge_to: (int array) array holding the node visited before a particular node -> index 0 = node 1
        :param dist_to: (int array) array tracking distance from source node for each node -> index 0 = node 1
        """
        order.append(source)

        ##iterates through nodes
        for w in graph.neighbors(source):

            ##if node isn't marked, runs dfs on that node
            if not marked[w-1]:
                marked[w-1] = True
                edge_to[w-1] = source
                dist_to[w-1] = dist_to[source-1] + 1
                Alg_Engine._dfs_helper(graph, w, marked, edge_to, dist_to, order)
    

        

    def depth_first_search(self, source):
        """
        Docstring for breadth_first_search
        nodes are always numbered 1 -> n
        
        :param self: Alg_Engine object
        returns marked, edge_to, dist_to, and order arrays for visualization in app
        """

        num_nodes = self.graph.number_of_nodes()

        ##tracks if nodes are marked
        marked = [False] * num_nodes

        ##tracks previous node
        edge_to = [-1] * num_nodes

        ##tracks distance from source
        dist_to = [-1] * num_nodes
        order = []

        marked[source-1] = True
        dist_to[source-1] = 0
        Alg_Engine._dfs_helper(self.graph, source, marked, edge_to, dist_to, order)

        
        return marked, edge_to, dist_to, order
    
    @staticmethod
    def _update_heap(new_tup, del_tup, pq):

        ##removes the specified tuple
        filtered_pq = [t for t in pq if t != del_tup]
        print(filtered_pq)

        ##appends and re heapifies the pq
        hq.heappush(filtered_pq, new_tup)

        return filtered_pq


    @staticmethod
    def _relax_edges(pq, dist_to, edge_to, graph, p):
        """
        Docstring for _relax_edges
        
        :param pq: priority queue
        :param dist_to: distance data (index 0 -> node 1)
        :param edge_to: previous node visited before a node (index 0 -> node 1)
        :param graph: networkx graph
        :param p: starting node
        """
        print("node " + str(p) + " being relaxed")

        ##iterates through adjacent nodes
        for q in graph.neighbors(p):
            curr_edge = graph.get_edge_data(p, q)["weight"]
            curr_dist = dist_to[q - 1]
            new_dist = dist_to[p-1] + curr_edge
            if new_dist < curr_dist:
                dist_to[q - 1] = dist_to[p-1] + curr_edge
                edge_to[q - 1] = p
                pq = Alg_Engine._update_heap((new_dist, q), (curr_dist, q), pq)
        
        return pq



    
    def dijkstras (self, source):
        """
        Docstring for dijkstras
        
        :param self: Alg_Engine object
        returns edge_to, dist_to, order, for visualization in app
        """
        num_nodes = self.graph.number_of_nodes()
        marked = [False] * num_nodes 
        dist_to = [float('inf')] * num_nodes #tracks distance from source
        edge_to = [-1] * num_nodes #tracks previous node 
        order = []

        dist_to[source - 1] = 0

        pq = []

        ##intializing pq with tuples of (dist, node)
        for node in range(0, num_nodes):
            pq.append((dist_to[node], node + 1))
            

        while len(pq) > 0:

            ##parsing tuple 
            curr_dist, p = hq.heappop(pq)

            ##skips node if already marked (protection from duplicates)
            if marked[p - 1]:
                print(f"  Node {p} already marked")
                continue

            order.append(p)
            print(f"  Marked node {p}, order so far: {order}")
            marked[p-1] = True
            pq = Alg_Engine._relax_edges(pq, dist_to, edge_to, self.graph, p)

        return edge_to, dist_to, order



    
    def prims (self, source):
        """
        Docstring for prims
        
        :param self: Alg_Engine object
        """


##testing
# Create test graph
# Graph structure:
#     1 --4-- 2
#     |       |
#     1       2
#     |       |
#     3 --1-- 4
#         \   |
#          3  5
#           \ |
#             5

G = nx.Graph()
G.add_edge(1, 2, weight=4)
G.add_edge(1, 3, weight=1)
G.add_edge(2, 4, weight=2)
G.add_edge(3, 4, weight=1)
G.add_edge(3, 5, weight=3)
G.add_edge(4, 5, weight=5)

print("Test Graph Edges:")
for edge in G.edges(data=True):
    print(f"  {edge[0]} -- {edge[1]}: weight={edge[2]['weight']}")

print("\n" + "="*60)
print("Running Dijkstra's from source node 1")
print("="*60)

engine = Alg_Engine(G)
edge_to, dist_to, order = engine.dijkstras(source=1)

print("\n" + "="*60)
print("RESULTS:")
print("="*60)
print(f"Visit order: {order}")
print(f"\nDistances from node 1:")
for i in range(len(dist_to)):
    print(f"  Node {i+1}: {dist_to[i]}")
print(f"\nPrevious nodes (edge_to):")
for i in range(len(edge_to)):
    print(f"  Node {i+1}: came from node {edge_to[i]}")

print("\n" + "="*60)
print("EXPECTED RESULTS:")
print("="*60)
print("Visit order: [1, 3, 4, 2, 5]")
print("Distances: [0, 4, 1, 2, 4]")
print("  Node 1: 0 (source)")
print("  Node 2: 4 (via 1)")
print("  Node 3: 1 (via 1)")
print("  Node 4: 2 (via 3)")
print("  Node 5: 4 (via 3)")


##bfs testing 

print("Test Graph Edges (unweighted):")
for edge in G.edges():
    print(f"  {edge[0]} -- {edge[1]}")

print("\n" + "="*60)
print("Running BFS from source node 1")
print("="*60 + "\n")

engine = Alg_Engine(G)
marked, edge_to, dist_to, order = engine.breadth_first_search(source=1)

print("="*60)
print("RESULTS:")
print("="*60)
print(f"Visit order: {order}")

print(f"\nMarked nodes:")
for i in range(len(marked)):
    print(f"  Node {i+1}: {marked[i]}")

print(f"\nDistances from node 1 (BFS levels):")
for i in range(len(dist_to)):
    print(f"  Node {i+1}: {dist_to[i]}")

print(f"\nPrevious nodes (edge_to - BFS tree):")
for i in range(len(edge_to)):
    print(f"  Node {i+1}: came from node {edge_to[i]}")

print("\n" + "="*60)
print("EXPECTED RESULTS:")
print("="*60)
print("Visit order: [1, 2, 3, 4, 5] or [1, 3, 2, 4, 5]")
print("  (Order depends on how NetworkX stores neighbors)")
print("\nAll nodes should be marked: True")
print("\nDistances (shortest path in # of edges):")
print("  Node 1: 0 (source)")
print("  Node 2: 1 (1 edge from source)")
print("  Node 3: 1 (1 edge from source)")
print("  Node 4: 2 (2 edges from source)")
print("  Node 5: 2 (2 edges from source)")
print("\nPrevious nodes will show BFS tree structure")
print("  Node 1: -1 (source)")
print("  Nodes 2,3: should come from 1")
print("  Nodes 4,5: should come from either 2 or 3")