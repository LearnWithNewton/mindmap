import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd

# Title of the app
st.title("Mind Map Generator from CSV")

# File uploader for CSV input
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    
    # Ensure that the CSV has the correct columns
    if 'Node1' in data.columns and 'Node2' in data.columns:
        # Create a new graph
        graph = nx.Graph()

        # Add edges to the graph based on the CSV data
        for index, row in data.iterrows():
            node1 = str(row['Node1'])  # Ensure node is a string
            node2 = str(row['Node2'])  # Ensure node is a string
            graph.add_node(node1)
            graph.add_node(node2)
            graph.add_edge(node1, node2)

        # --- Visualization of the Graph ---
        st.subheader("Graph Visualization")

        if len(graph.nodes) > 0:
            net = Network(notebook=True, height='1280px', width='1080px', directed=True)

            # Disable zoom, pan, and physics
            #net.hrepulsion()  # You can use this to remove interaction physics

            # Populate the graph
            net.from_nx(graph)

            # Save and show the graph in Streamlit
            net.show("mindmap_csv.html")

            HtmlFile = open("mindmap_csv.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            components.html(source_code, height=1280, width=1080)
        else:
            st.info("The CSV file doesn't contain any valid nodes or edges.")
    else:
        st.error("The CSV file must contain 'Node1' and 'Node2' columns.")
else:
    st.info("Please upload a CSV file to generate the mind map.")
