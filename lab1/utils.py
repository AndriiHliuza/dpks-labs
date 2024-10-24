import math
import networkx as nx
import matplotlib.pyplot as plt

def rotate_dot(dot, angle, origin_dot=(0, 0)):
    x0, y0 = origin_dot
    x, y = dot
    radians = math.radians(angle * -1)

    x_prime = x - x0
    y_prime = y - y0

    rotated_x = x_prime * math.cos(radians) - y_prime * math.sin(radians)
    rotated_y = x_prime * math.sin(radians) + y_prime * math.cos(radians)

    rotated_x += x0
    rotated_y += y0

    return rotated_x, rotated_y


def draw_graph_edges(graph, nodes_positions, edges, edge_color, style):
    nx.draw_networkx_edges(
        graph,
        pos = nodes_positions,
        edgelist = edges,
        edge_color = edge_color,
        style = style
    )

def draw_graph(graph, positions, edges_data, number_of_clusters):
    radius = number_of_clusters * (1.25 if number_of_clusters < 10 else 1)
    font_size = 10 if number_of_clusters < 10 else 1
    node_size = 300 if number_of_clusters < 10 else 5
    figure_size = (radius, radius)
    plt.figure(figsize = figure_size)

    nx.draw(
        graph,
        positions,
        with_labels=True,
        node_size=node_size,
        node_color="white",
        edgecolors="black",
        font_size=font_size
    )

    for edge_props in edges_data.values():
        draw_graph_edges(
            graph,
            positions,
            edge_props["edges"],
            edge_props["color"],
            edge_props["style"]
        )

    plt.title(f"{number_of_clusters} clusters")
    plt.show()


def calculate_diameter(graph):
    all_shortest_distances_from_all_nodes = dict(nx.all_pairs_dijkstra_path_length(graph))
    max_distance = 0
    node_pair = (None, None)

    for node, shortest_lengths in all_shortest_distances_from_all_nodes.items():
        for target, distance in shortest_lengths.items():
            if distance > max_distance:
                max_distance = distance
                node_pair = (node, target)

    return max_distance, node_pair

def calculate_avr_diameter(graph):
    all_distances = dict(nx.all_pairs_dijkstra_path_length(graph))
    total_distance = 0
    pair_count = 0

    for node, lengths in all_distances.items():
        for target, distance in lengths.items():
            if node != target:
                total_distance += distance
                pair_count += 1
    average_diameter = round(total_distance / pair_count, 3) if pair_count > 0 else 0

    return average_diameter

def calculate_degree(graph):
    return max(dict(graph.degree()).values())


def calculate_cost(graph):
    return len(graph.edges)

def calculate_traffic(avg_diameter, degree):
    return round(2 * avg_diameter / degree, 3)
