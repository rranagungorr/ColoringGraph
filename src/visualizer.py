import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(num_nodes, edges, colors):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    G.add_edges_from(edges)

    color_map = [colors[i] for i in G.nodes()]
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, node_color=color_map, with_labels=True, node_size=500, cmap=plt.cm.get_cmap('tab20'))
    plt.title("Graph Coloring Solution")
