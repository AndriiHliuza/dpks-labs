import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def rotate_position(pos, angle, origin=(0, 0)):
    ox, oy = origin
    px, py = pos
    angle_rad = np.radians(angle)
    qx = ox + np.cos(angle_rad) * (px - ox) - np.sin(angle_rad) * (py - oy)
    qy = oy + np.sin(angle_rad) * (px - ox) + np.cos(angle_rad) * (py - oy)
    return qx, qy

def generate_cluster(n, angle_offset, radius, is_center=False):
    G = nx.Graph()

    # Створюємо вузли
    node_values = [6 * n - i for i in range(5, -1, -1)]
    G.add_nodes_from(node_values)

    # Визначаємо внутрішні ребра між вузлами
    intra_edges = [
        (6*n-5, 6*n-4),
        (6*n-5, 6*n-1),
        (6*n-5, 6*n),
        (6*n-4, 6*n-3),
        (6*n-4, 6*n-2),
        (6*n-3, 6*n-2),
        (6*n-3, 6*n-1),
        (6*n-2, 6*n),
        (6*n-1, 6*n)
    ]
    G.add_edges_from(intra_edges)
    # Визначаємо позиції вузлів

    base_pos = {
        6*n-5: (0, radius),
        6*n-4: (0, radius-1),
        6*n-2: (1, radius - 3),
        6*n-3: (-1, radius - 3),
        6*n-1: (-2, radius - 3.7),
        6*n: (2, radius - 3.7),
    }
    # Визначаємо позиції вузлів першого кластера
    if is_center:
        center_pos = {
            6*n-5: (0, 2),
            6*n-4: (0, 0.75),
            6*n-2: (0.75, -1),
            6*n-3: (-0.75, -1),
            6*n-1: (-2, -2),
            6*n: (2, -2),
        }
        rotated_pos = center_pos
    else:
        rotated_pos = {node: rotate_position(pos, angle_offset) for node, pos in base_pos.items()}

    return G, rotated_pos, intra_edges

def draw_edges(G, pos, edges, color, width, style, curve=0):
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=width, style=style, arrows=True, connectionstyle=f"arc3,rad={curve}")

def connect_last_to_second(node_groups, group, edge_type, edge_color, G_inter_cluster, edge_types):
    last_cluster_node = node_groups[group][-1]
    second_cluster_node = node_groups[group][1]
    edge = (last_cluster_node, second_cluster_node)
    edge_types[edge_color]["edges"].append(edge)
    G_inter_cluster.add_edge(*edge)

def build_graph(G_total, pos_total, edge_types, num_clusters):
    if not isinstance(num_clusters, int):
        raise TypeError(f"Expected integer for num_clusters, got {type(num_clusters).__name__}")

    radius = num_clusters * (1.5 if num_clusters < 10 else 2)
    figsize = (radius, radius)

    nodes_in_pos = set(pos_total.keys())
    nodes_in_graph = set(G_total.nodes)
    missing_nodes = nodes_in_pos - nodes_in_graph
    if missing_nodes:
        print(f"Warning: The following nodes are in pos_total but not in G_total: {missing_nodes}")

    subgraph = G_total.subgraph(nodes_in_pos.intersection(nodes_in_graph))
    pos_subgraph = {node: pos_total[node] for node in subgraph.nodes}
    plt.figure(figsize=figsize)
    nx.draw(G_total, pos_total, with_labels=True, node_size=500, node_color="white", edgecolors="black", font_size=10, font_weight="bold")

    for key, style in edge_types.items():
        edges = style["edges"]
        color = style["color"]
        width = style["width"]
        style_name = style["style"]

        valid_edges = [(u, v) for u, v in edges if u in subgraph.nodes and v in subgraph.nodes]
        nx.draw_networkx_edges(subgraph, pos=pos_subgraph, edgelist=valid_edges, edge_color=color, style=style_name, width=width)

        plt.title(f"{num_clusters} clusters")
        plt.show()

def compute_diameter(G):
    all_distances = dict(nx.all_pairs_dijkstra_path_length(G))

    max_distance = 0
    node_pair = (None, None)
    for node, lengths in all_distances.items():
        for target, distance in lengths.items():
            if distance > max_distance:
                max_distance = distance
                node_pair = (node, target)

    return max_distance, node_pair

def compute_average_diameter(G):
    n = len(G.nodes())
    all_distances = dict(nx.all_pairs_dijkstra_path_length(G))

    total_distance = 0
    pair_count = 0

    for node, lengths in all_distances.items():
        for target, distance in lengths.items():
            if node != target:
                total_distance += distance
                pair_count += 1

        average_diameter = round(total_distance / pair_count, 3) if pair_count > 0 else 0

        return average_diameter


def generate_system(num_clusters):
    results = []

    edge_types = {
        "6n": {"edges": [], "color": "#954ECA", "width": 2, "style": "solid"},
        "6n1": {"edges": [], "color": "#9F000F", "width": 2, "style": "solid"},
        "6n2": {"edges": [], "color": "#0059FF", "width": 2, "style": "solid"},
        "6n3": {"edges": [], "color": "#F660AB", "width": 2, "style": "solid"},
        "6n4": {"edges": [], "color": "#728C00", "width": 2, "style": "solid"},
        "6n5": {"edges": [], "color": "#FFD801", "width": 2, "style": "solid"},
        "red": {"edges": [], "color": "#FF0000", "width": 2, "style": "dashed"},
        "pink": {"edges": [], "color": "#FF7DD7", "width": 2, "style": "dashed"},
        "mint": {"edges": [], "color": "#99FF99", "width": 2, "style": "dashed"},
    }

    node_groups = {
        "6n": [], "6n1": [], "6n2": [], "6n3": [], "6n4": [], "6n5": []
    }

    G_total = nx.Graph()
    G_intra_cluster = nx.Graph()
    G_inter_cluster = nx.Graph()
    G_intra_inter_cluster = nx.Graph()

    pos_total = {}
    angle_step = 360 / (num_clusters - 1) if num_clusters > 1 else 0
    radius = num_clusters * (1.5 if num_clusters < 15 else 1)

    G_cluster, pos_cluster, intra_edges = generate_cluster(1, 0, radius, is_center=True)
    G_intra_cluster.add_edges_from(intra_edges)
    G_total = nx.compose(G_total, G_cluster)
    pos_total.update(pos_cluster)

    for i, group in enumerate(["6n", "6n1", "6n2", "6n3", "6n4", "6n5"]):
        node_groups[group].append(6 * 1 - i)

    for n in range(2, num_clusters + 1):
        angle_offset = angle_step * (n - 2)
        G_cluster, pos_cluster, intra_edges = generate_cluster(n, angle_offset, radius)
        G_intra_cluster.add_edges_from(intra_edges)
        G_total = nx.compose(G_total, G_cluster)
        pos_total.update(pos_cluster)

        for i, group in enumerate(["6n", "6n1", "6n2", "6n3", "6n4", "6n5"]):
            node_groups[group].append(6 * n - i)

    G_intra_inter_cluster = nx.compose(G_intra_inter_cluster, G_intra_cluster)

    if num_clusters > 1:
        for group in ["6n", "6n1", "6n2", "6n3", "6n4", "6n5"]:
            for n in range(1, num_clusters):
                edge = (node_groups[group][-n], node_groups[group][0])
                edge_types[group]["edges"].append(edge)
                G_inter_cluster.add_edge(*edge)

        for n in range(3, num_clusters + 1, 2):
            if (n + 2) <= num_clusters + 1:
                current_node = node_groups["6n1"][n - 1]
                next_node = node_groups["6n"][(n + 1 - 1) % len(node_groups["6n"])]
                edge = (current_node, next_node)
                edge_types["red"]["edges"].append(edge)
                G_inter_cluster.add_edge(*edge)

                last_cluster_node = node_groups["6n1"][-1]
                second_cluster_node = node_groups["6n"][1]
                edge = (last_cluster_node, second_cluster_node)
                edge_types["red"]["edges"].append(edge)
                G_inter_cluster.add_edge(*edge)

        for n in range(2, num_clusters + 1, 2):
            if (n + 2) <= num_clusters + 1:
                current_node = node_groups["6n4"][n - 1]
                next_node = node_groups["6n4"][(n + 1 - 1) % len(node_groups["6n"])]
                edge = (current_node, next_node)
                edge_types["pink"]["edges"].append(edge)
                G_inter_cluster.add_edge(*edge)

        for n in range(2, num_clusters + 1):
            if (n + 2) <= num_clusters + 1:
                current_node = node_groups["6n5"][n - 1]
                next_node = node_groups["6n5"][(n + 1 - 1) % len(node_groups["6n"])]
                edge = (current_node, next_node)
                edge_types["mint"]["edges"].append(edge)
                G_inter_cluster.add_edge(*edge)

                last_cluster_node = node_groups["6n5"][-1]
                second_cluster_node = node_groups["6n5"][1]
                edge = (last_cluster_node, second_cluster_node)
                edge_types["mint"]["edges"].append(edge)
                G_inter_cluster.add_edge(*edge)

            G_intra_inter_cluster = nx.compose(G_intra_inter_cluster, G_inter_cluster)

    diameter, _ = compute_diameter(G_intra_inter_cluster)
    avg_diameter = compute_average_diameter(G_intra_inter_cluster)
    degrees = [G_intra_inter_cluster.degree(n) for n in G_intra_inter_cluster.nodes()]
    degree = max(degrees)
    cost = len(G_intra_inter_cluster.edges())
    traffic = round(2 *avg_diameter / degree, 3)

    results.append({
        "Number of Clusters": num_clusters,
        "Number of Nodes": len(G_intra_inter_cluster.nodes()),
        "Diameter": diameter,
        "Average Diameter": avg_diameter,
        "Degree": degree,
        "Cost": cost,
        "Traffic": traffic
    })

    return G_total, G_intra_cluster, G_inter_cluster, pos_total, edge_types, results

def main(max_clusters):
    all_results = []

    for num_clusters in range(1, max_clusters + 1):
        G_total, G_intra_cluster, G_inter_cluster, pos_total, edge_types, results = generate_system(num_clusters)
        all_results.extend(results)

    df_results = pd.DataFrame(all_results)
    df_results.to_csv("lab2.csv", index=False)
    build_graph(G_total, pos_total, edge_types, num_clusters)

main(64)