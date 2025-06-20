# draw_solution.py
import networkx as nx
import matplotlib.pyplot as plt
from gcp.graph import Graph

def draw_graph(instance_path: str, colors: list[int], save_path: str = None):
    g = Graph(instance_path)
    G = nx.Graph()
    G.add_nodes_from(range(g.n))
    G.add_edges_from(g.edges)

    pos = nx.spring_layout(G, seed=42)
    cmap = plt.cm.get_cmap('tab20')
    node_colors = [colors[i] for i in G.nodes()]

    nx.draw(
        G, pos,
        node_color=node_colors,
        with_labels=True,
        node_size=500,
        cmap=cmap,
        edge_color='black',
        font_color='black'
    )

    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.close()
