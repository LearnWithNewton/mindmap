import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = 'mind_map_data.csv'  # Update with your CSV file path
data = pd.read_csv(csv_file)

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for _, row in data.iterrows():
    G.add_node(row['Node'], description=row['Description'])
    if pd.notna(row['Parent']):
        G.add_edge(row['Parent'], row['Node'])

# Draw the mind map
pos = nx.spring_layout(G)  # Position nodes using Fruchterman-Reingold force-directed algorithm
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, arrows=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
plt.title("Mind Map")
plt.show()
