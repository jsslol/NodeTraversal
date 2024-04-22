# Created By: Jared Schneider
#
# Program: Implements Dijkstra's,DFS, and BFS algorithims to find the shortest path from node 1 to all other nodes and draws
# the graphs showing the paths taken. 
#
# Note: Change title of 'Graph_file' to use different graphs
#
# Compile: "python NodeTraversal.py"
#          
# Documentation used:
# Networkx - https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html
# Matplotlib - https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html
# Re - https://docs.python.org/3/library/re.html

import re
import networkx as nx
import scipy as sp
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

# CHANGE THIS TO USE DIFFERENT FILES
graph_file = '10nodegraph'

# Function to read the graph from a DOT file
def read_dot_graph(file_name):
    graph = {}
    with open(file_name, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Extract edges using regular expression
        edge_match = re.match(r'\s*(\d+)\s*->\s*(\d+)\s*\[label="(\d+)"\];', line)
        if edge_match:
            source, dest, weight = edge_match.groups()
            source, dest, weight = int(source), int(dest), int(weight)
            if source not in graph:
                graph[source] = {}
            graph[source][dest] = weight

    return graph

# Function to run Dijkstra's algorithm
def run_dijkstra(graph, start_node):
    # Initialize distances and visited nodes
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    visited = set()

    while len(visited) < len(graph):
        # Find the node with the minimum distance
        min_distance_node = None
        for node in graph:
            if node not in visited and (min_distance_node is None or distances[node] < distances[min_distance_node]):
                min_distance_node = node

        visited.add(min_distance_node)

        # Update distances for neighbors
        for neighbor, weight in graph[min_distance_node].items():
            new_distance = distances[min_distance_node] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

    return distances

# Function to run BFS
def run_bfs(graph, start_node):
    visited = set()
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    queue = [start_node]

    while queue:
        current_node = queue.pop(0)
        visited.add(current_node)
        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                queue.append(neighbor)
                new_distance = distances[current_node] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

    return distances

# Function to run DFS
def run_dfs(graph, start_node):
    visited = set()
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0

    def dfs(node):
        visited.add(node)
        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                distances[neighbor] = distances[node] + weight
                dfs(neighbor)

    dfs(start_node)
    return distances

# Create a directed graph from the file
graph = read_dot_graph(graph_file)

# Run Dijkstra's algorithm to find the shortest paths from node 1 to all other nodes
start_node = 1
dijkstra_distances = run_dijkstra(graph, start_node)

# Run BFS to find the shortest paths from node 1 to all other nodes
bfs_distances = run_bfs(graph, start_node)

# Run DFS to find the shortest paths from node 1 to all other nodes
dfs_distances = run_dfs(graph, start_node)

# Print the shortest paths and distances for Dijkstra's algorithm
print("Dijkstra's Algorithm:")
for node, distance in dijkstra_distances.items():
    print(f"Shortest Distance from Node {start_node} to Node {node}: {distance}")

# Print the shortest paths and distances for BFS
print("\nBreadth-First Search:")
for node, distance in bfs_distances.items():
    print(f"Shortest Distance from Node {start_node} to Node {node}: {distance}")

# Print the shortest paths and distances for DFS
print("\nDepth-First Search:")
for node, distance in dfs_distances.items():
    print(f"Shortest Distance from Node {start_node} to Node {node}: {distance}")

# Create a directed graph from the adjacency list representation
G = nx.DiGraph()

# Add nodes to the graph
for source, destinations in graph.items():
    G.add_node(source)
    for dest, weight in destinations.items():
        G.add_node(dest)
        G.add_edge(source, dest, weight=weight)

# Create a list of colors for edges based on whether they are part of the shortest path
edge_colors = ['red' if G[u][v]['weight'] == dijkstra_distances[v] - dijkstra_distances[u] else 'gray' for u, v in G.edges()]

# Position nodes using Spring layout
pos = nx.spring_layout(G)

# Draw nodes and edges
nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black', edge_color=edge_colors, width=2)

# Create a legend for edge colors
red_patch = plt.Line2D([0], [0], color='red', lw=2, label='Shortest Path')
gray_patch = plt.Line2D([0], [0], color='gray', lw=2, label='Other Paths')
plt.legend(handles=[red_patch, gray_patch], loc='upper right')

# Display the graph
plt.title("Dijkstra's Algorithm Visualization")
plt.show()