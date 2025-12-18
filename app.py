import streamlit as st

## TODO: for dev, make sure to use streamlit run app.py in the terminal to access the local host
## TODO: create color theme, get very familiar with streamlit 
st.title("Graph Visualizer")

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


st.markdown('### Create Graph')
graphType = st.selectbox("Graph Type", ("-","Directed", "Undirected", "DAG"))
edgeType = st.radio("Edge Type", ["Weighted", "Unweighted"])
nodes = st.slider("Number of Nodes")



st.markdown('### Failure Graph')
st.selectbox("Failure Graphs", ("ex1")) ##TODO: add failure graphs for selection