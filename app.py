import streamlit as st
import matplotlib.pyplot as plt

## TODO: for dev, make sure to use streamlit run app.py in the terminal to access the local host
## TODO: create color theme, get very familiar with streamlit 
## TODO: proper documentation needed
st.title("Graph Visualizer")

st.markdown('### Create Graph')
graph_type = st.selectbox("Graph Type", ("-","Directed", "Undirected", "DAG"))
edge_type = st.radio("Edge Type", ["Weighted", "Unweighted"])
spans = st.radio("Spanning", ["Yes", "No"])
node_count = st.slider("Number of Nodes")
edge_count = st.slider("Number of Edges")
st.markdown('#### Edge Weight Range')
edge_upper = st.slider("Upper", min_value=-100, max_value=100, value=0)
edge_lower = st.slider("Lower", min_value=-100, max_value=100, value=0)


st.markdown('### Failure Graph')
st.selectbox("Failure Graphs", ("ex1")) ##TODO: add failure graphs for selection

st.sidebar.text("Click here to Generate!")
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

##Output creation
##TODO: pass inputs to graph utils

