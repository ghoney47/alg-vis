import streamlit as st
import matplotlib.pyplot as plt
import random
from graphs import graph_utils as gu
from graphs import constants as c
from algorithms import algs

st.title("Graph Visualizer")

##for display functionality
if "graph_obj" not in st.session_state:
    st.session_state.graph_obj = None

##maintaining graphs once created
if "graph" not in st.session_state:
    st.session_state.graph = None

if "fig" not in st.session_state:
    st.session_state.fig = None

if "begin" not in st.session_state:
    st.session_state.begin = False

##stores algorithm arrays in a tuple
if "results" not in st.session_state:
    st.session_state.results = ()

if "node_colors" not in st.session_state:
    st.session_state.node_colors = []

if "counter" not in st.session_state:
    st.session_state.counter = 0

##creation options
if st.session_state.graph is None:
    st.markdown('### Create Graph')
    graph_type = st.selectbox("Graph Type", ("-","Directed", "Undirected", "DAG"))

    ##variables for graph creation
    input_id = c.DIGRAPH
    input_weighted = False
    input_node_count = 0
    input_edge_count = 0
    input_edge_lower = 0
    input_edge_upper = 0
    input_spans = False
    input_sources = 0

    ##non-dag options
    if graph_type == "Directed" or graph_type == "Undirected":
        edge_type = st.radio("Edge Type", ["Weighted", "Unweighted"]) ##TODO: if unweighted, set edge upper/lower to 0
        node_count = st.slider("Number of Nodes")
        edge_count = st.slider("Number of Edges")

        if edge_count + 1 >= node_count and node_count != 0 and edge_count != 0:
                spans = st.radio("Spanning", ["Yes", "No"])
                if spans == "Yes":
                    input_spans = True
        ##sliders for weights
        if edge_type == "Weighted":
            st.markdown('#### Edge Weight Range')
            edge_upper = st.slider("Upper", min_value=-100, max_value=100, value=0)
            edge_lower = st.slider("Lower", min_value=-100, max_value=100, value=0)

        
        if graph_type == "Undirected":
            input_id = c.GRAPH


    
        if edge_type == "Weighted":
            input_weighted = True
            input_edge_lower = edge_lower
            input_edge_upper = edge_upper
        
        input_node_count = node_count
        input_edge_count = edge_count



    ##DAG creation
    else:
        edge_type = st.radio("Edge Type", ["Weighted", "Unweighted"])
        node_count = st.slider("Number of Nodes")
        edge_count = st.slider("Number of Edges")
        ##will never 
        if edge_count + 1 >= node_count and node_count != 0 and edge_count != 0:
            spans = st.radio("Reaches All Nodes", ["Yes", "No"])
            if spans == "Yes":
                input_spans = True

        ##only allows source selection with valid nodes
        if node_count > 0:
            sources = st.slider("Sources", min_value=1, max_value=node_count)
            input_sources = sources


        ##sliders for weights
        if edge_type == "Weighted":
            st.markdown('#### Edge Weight Range')
            edge_upper = st.slider("Upper", min_value=-100, max_value=100, value=0)
            edge_lower = st.slider("Lower", min_value=-100, max_value=100, value=0)

        input_id = c.DAG
    
        if edge_type == "Weighted":
            input_weighted = True
            input_edge_lower = edge_lower
            input_edge_upper = edge_upper
        
        input_node_count = node_count
        input_edge_count = edge_count




st.sidebar.text("Click here to Generate!")

##if unweighted, set weights to 0
with st.sidebar.container(horizontal=False, vertical_alignment="distribute"):
    if st.button("Generate Custom", type="primary", shortcut="G"):
        print("user selected user graph")
        G = gu.Graph(input_id, input_weighted)
        G.create_nodes(input_node_count)
        G.assign_edges(input_edge_count, input_edge_lower, input_edge_upper, input_spans, input_sources)
        st.session_state.fig, st.session_state.node_colors = G.display()
        st.session_state.graph = G.graph
        st.session_state.graph_obj = G
      


    if st.button("Generate Random", type="primary", shortcut="Shift+G"):
        print("user selected random graph")
        G = gu.Graph(random.choice([c.GRAPH, c.DIGRAPH, c.DAG]), random.choice([True, False]))
        rand_nodes = random.randint(1, 100)
        rand_lower = random.randint(-100, 100)
        rand_upper = random.randint(rand_lower, 100)

        G.create_nodes(rand_nodes)
        G.assign_edges(random.randint(1, 100), rand_lower, rand_upper, random.choice([True, False]), random.randint(1, rand_nodes))
        st.session_state.fig, st.session_state.node_colors = G.display()
        st.session_state.graph = G.graph
        st.session_state.graph_obj = G


    ##resetting all known states
    if st.button("Reset Graph"):
        print("user has reset")
        st.session_state.graph = None
        st.session_state.fig = None
        st.session_state.graph_obj = None
        st.session_state.begin = False
        st.session_state.results = ()
        st.session_state.node_colors = []
        st.rerun()
    st.markdown("## Node Colorings:")
    st.markdown("- Orange: Nodes with 2+ incoming edges \n - Navy Blue: Nodes with exactly 1 incoming edge \n - White: Source nodes (0 incoming edges)")

        
            



if st.session_state.graph is not None:
    st.pyplot(st.session_state.fig, clear_figure=False) 

    engine = algs.Alg_Engine(st.session_state.graph)

    alg_select = st.selectbox("Algorithm", ["DFS", "BFS", "Dijkstra's", "Prim's"])
    source = st.slider("Source Node", min_value= 1, max_value = st.session_state.graph.number_of_nodes())

    if not st.session_state.begin:
        if st.button("Begin"):   
            print("Running " + alg_select)
            st.session_state.counter = 0

            ##selecting algorithm
            if alg_select == "DFS":
                st.session_state.results = engine.depth_first_search(source)
            elif alg_select == "BFS":
                st.session_state.results = engine.breadth_first_search(source)
            elif alg_select == "Dijkstra's":
                st.session_state.results = engine.dijkstra(source)
            elif alg_select == "Prim's":
                st.session_state.results = engine.prim(source)




            st.session_state.begin = True
            st.rerun()
    elif st.button("Next Step"):
        print("next step")

        ## parsing results into variables
        if alg_select in ["DFS", "BFS"]:
            marked, edge_to, dist_to, order = st.session_state.results
        elif alg_select == "Dijkstra's":
            edge_to, dist_to, order = st.session_state.results
        elif alg_select == "Prim's":
            mst_edges, order = st.session_state.results


        curr_step = st.session_state.counter
        
        ##take first node in order, update that color in the session state, go from there
        curr_node = order[curr_step] 

        ##changes color at necessary node to be red (marks visited)
        st.session_state.node_colors[curr_node] =  "#FF0000"

        ## updates current figure and colors for session state
        st.session_state.fig, st.session_state.node_colors = st.session_state.graph_obj.display(st.session_state.node_colors)
        
        ##increments step
        st.session_state.counter += 1

        ##display arrays at each step (for walkthrough)


        if st.session_state.counter >= len(order):
            st.markdown("## Algorithm complete:")
            ##TODO: add the current state data with st.session_state.results



        
        



    
    





