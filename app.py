import streamlit as st
import matplotlib.pyplot as plt
from graphs import graph_utils as gu

## TODO: for dev, make sure to use streamlit run app.py in the terminal to access the local host
## TODO: create color theme, get very familiar with streamlit 
## TODO: proper documentation needed
st.title("Graph Visualizer")

st.markdown('### Create Graph')
graph_type = st.selectbox("Graph Type", ("-","Directed", "Undirected", "DAG"))

##non-dag options
if graph_type == "Directed" or graph_type == "Undirected":
    edge_type = st.radio("Edge Type", ["Weighted", "Unweighted"]) ##TODO: if unweighted, set edge upper/lower to 0
    spans = st.radio("Spanning", ["Yes", "No"])
    node_count = st.slider("Number of Nodes")
    edge_count = st.slider("Number of Edges")

    ##sliders for weights
    if edge_type == "Weighted":
        st.markdown('#### Edge Weight Range')
        edge_upper = st.slider("Upper", min_value=-100, max_value=100, value=0)
        edge_lower = st.slider("Lower", min_value=-100, max_value=100, value=0)


    st.markdown('### Failure Graph')
    st.selectbox("Failure Graphs", ("ex1")) ##TODO: add failure graphs for selection

    ##TODO: create graphs within this scope

##DAG creation
else:
    edge_type = st.radio("Edge Type", ["Weighted", "Unweighted"]) ##TODO: if unweighted, set edge upper/lower to 0
    node_count = st.slider("Number of Nodes")
    edge_count = st.slider("Number of Edges")
    spans = "No"
    ##will never 
    if edge_count + 1 >= node_count and node_count != 0 and edge_count != 0:
        spans = st.radio("Reaches All Nodes", ["Yes", "No"])

    ##only allows source selection with valid nodes
    if node_count > 0:
        sources = st.slider("Sources", min_value=1, max_value=node_count)

    ##sliders for weights
    if edge_type == "Weighted":
        st.markdown('#### Edge Weight Range')
        edge_upper = st.slider("Upper", min_value=-100, max_value=100, value=0)
        edge_lower = st.slider("Lower", min_value=-100, max_value=100, value=0)

    ##TODO: create DAGs within this scope

st.sidebar.text("Click here to Generate!")

##if unweighted, set weights to 0
with st.sidebar.container(horizontal=False, vertical_alignment="distribute"):
    if st.button("Generate Custom", type="primary", shortcut="G"):
        ##TODO: generate graph 
        print("user selected user graph")
        


    if st.button("Generate Random", type="primary", shortcut="Shift+G"):
        ##TODO: generate graph
        print("user selected random graph")



    if st.button("Generate **FAILURE** Graph", type="primary", shortcut="F"):
        ##TODO: generate graph
        print("user selected failure graph")
        ##TODO: make failure graphs

##Output creation
##TODO: pass inputs to graph utils

##TODO: create output page after input (where the algs are run)

