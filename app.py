import streamlit as st
import matplotlib.pyplot as plt
import random
from graphs import graph_utils as gu
from graphs import constants as c

## TODO: for dev, make sure to use streamlit run app.py in the terminal to access the local host
## TODO: create color theme, get very familiar with streamlit 
## TODO: proper documentation needed
st.title("Graph Visualizer")

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


    st.markdown('### Failure Graph')
    st.selectbox("Failure Graphs", ("ex1")) ##TODO: add failure graphs for selection

    
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
    edge_type = st.radio("Edge Type", ["Weighted", "Unweighted"]) ##TODO: if unweighted, set edge upper/lower to 0
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

fig = None

##if unweighted, set weights to 0
with st.sidebar.container(horizontal=False, vertical_alignment="distribute"):
    if st.button("Generate Custom", type="primary", shortcut="G"):
        ##TODO: generate graph 
        print("user selected user graph")
        G = gu.Graph(input_id, input_weighted)
        G.create_nodes(input_node_count)
        G.assign_edges(input_edge_count, input_edge_lower, input_edge_upper, input_spans, input_sources)
        fig = G.display()
      


    if st.button("Generate Random", type="primary", shortcut="Shift+G"):
        ##TODO: generate graph
        print("user selected random graph")
        G = gu.Graph(random.choice([c.GRAPH, c.DIGRAPH, c.DAG]), random.choice([True, False]))
        rand_nodes = random.randint(1, 100)
        rand_lower = random.randint(-100, 100)
        rand_upper = random.randint(rand_lower, 100)

        G.create_nodes(rand_nodes)
        G.assign_edges(random.randint(1, 100), rand_lower, rand_upper, random.choice([True, False]), random.randint(1, rand_nodes))
        fig = G.display()



    if st.button("Generate **FAILURE** Graph", type="primary", shortcut="F"):
        ##TODO: generate graph
        print("user selected failure graph")
        ##TODO: make failure graphs

st.pyplot(fig, clear_figure=False)  # Add clear_figure parameter

st.markdown("## Node Colorings:")
st.markdown("- Orange: Nodes with 2+ incoming edges \n - Navy Blue: Nodes with exactly 1 incoming edge \n - White: Source nodes (0 incoming edges)")
##Output creation
##TODO: pass inputs to graph utils

##TODO: create output page after input (where the algs are run)

