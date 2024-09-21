import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# Title of the app
st.title("Mind Map - Add, Modify, Remove Nodes and Edges with Zoom Controls")

# Initialize the graph
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()

# --- Add Section ---
st.subheader("Add Nodes and Connections to the Mind Map")

node1 = st.text_input("Node 1 (Root/Starting Node):", "")
node2 = st.text_input("Node 2 (Child/Connected Node):", "")

if st.button("Add to Mind Map"):
    if node1 and node2:
        st.session_state.graph.add_node(node1)
        st.session_state.graph.add_node(node2)
        st.session_state.graph.add_edge(node1, node2)
        st.success(f"Added node {node2} connected to {node1}.")
    else:
        st.error("Please enter both nodes.")

# --- Modify Section ---
st.subheader("Modify Nodes and Connections")

if len(st.session_state.graph.nodes) > 0:
    # Modify Node
    st.subheader("Modify Node Name")
    existing_node = st.selectbox("Select a Node to Modify:", list(st.session_state.graph.nodes))
    new_node_name = st.text_input("Enter the new name for the node:", "")

    if st.button("Modify Node"):
        if new_node_name:
            edges_to_update = list(st.session_state.graph.edges(existing_node))
            st.session_state.graph = nx.relabel_nodes(st.session_state.graph, {existing_node: new_node_name})
            for edge in edges_to_update:
                st.session_state.graph.add_edge(edge[0].replace(existing_node, new_node_name), edge[1].replace(existing_node, new_node_name))
            st.success(f"Node {existing_node} renamed to {new_node_name}.")
        else:
            st.error("Please enter a new name for the node.")

    # Modify Edge
    st.subheader("Modify Connections (Edges)")
    if len(st.session_state.graph.edges) > 0:
        edge_to_modify = st.selectbox("Select an Edge to Modify:", list(st.session_state.graph.edges))
        node_a, node_b = edge_to_modify

        new_connection = st.text_input(f"Modify connection for edge {node_a} - {node_b}: Enter a new connected node for {node_a}:")

        if st.button("Modify Edge"):
            if new_connection:
                st.session_state.graph.remove_edge(node_a, node_b)
                st.session_state.graph.add_edge(node_a, new_connection)
                st.success(f"Edge {node_a} - {node_b} modified to {node_a} - {new_connection}.")
            else:
                st.error("Please enter a valid node to modify the edge.")

# --- Remove Section ---
st.subheader("Remove Nodes and Connections")

if len(st.session_state.graph.nodes) > 0:
    st.subheader("Remove Node")
    node_to_remove = st.selectbox("Select a Node to Remove:", list(st.session_state.graph.nodes))

    if st.button("Remove Node"):
        st.session_state.graph.remove_node(node_to_remove)
        st.success(f"Node {node_to_remove} has been removed.")

if len(st.session_state.graph.edges) > 0:
    st.subheader("Remove Edge")
    edge_to_remove = st.selectbox("Select an Edge to Remove:", list(st.session_state.graph.edges))

    if st.button("Remove Edge"):
        node_a, node_b = edge_to_remove
        st.session_state.graph.remove_edge(node_a, node_b)
        st.success(f"Edge between {node_a} and {node_b} has been removed.")

# --- Visualization with Zoom Controls ---
st.subheader("Graph Visualization with Zoom Controls")

if len(st.session_state.graph.nodes) > 0:
    net = Network(notebook=True, height='600px', width='800px', directed=False)
    
    # Allow zoom and pan controls
    net.barnes_hut()
    
    # Fit button
    fit_graph = st.checkbox("Fit graph to screen", value=True)

    # Populate the graph
    net.from_nx(st.session_state.graph)

    # Fit to screen if checkbox is checked
    if fit_graph:
        net.toggle_physics(True)  # This ensures that when rendered, the graph fits the canvas

    # Save and show the graph in Streamlit
    net.show("mindmap.html")

    HtmlFile = open("mindmap.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height=600, width=800)
else:
    st.info("No nodes in the graph. Add nodes to create a mind map.")
