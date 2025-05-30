def load_graph(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    num_nodes, _ = map(int, lines[0].split())
    edges = [tuple(map(int, line.strip().split())) for line in lines[1:]]
    return num_nodes, edges
