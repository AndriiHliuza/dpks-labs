import math
from typing import Tuple, Dict, List, Any
import networkx as nx
import matplotlib.pyplot as plt


def get_radius_for_cluster_with_provided_number_of_nodes(number_of_clusters: int) -> float:
    return number_of_clusters * (3 if number_of_clusters < 10 else 10)


def get_offset_angle(number_of_clusters: int) -> float:
    return 360 / number_of_clusters


def get_offset_angle_for_current_cluster(offset_angle: float, cluster_number: int) -> float:
    return offset_angle * (cluster_number - 3)


def rotate_dot(
        dot: Tuple[float, float, float],
        offset_angle: float,
        origin: Tuple[float, float, float] = (0, 0, 0)
) -> Tuple[float, float, float]:
    x0, y0, z0 = origin
    x, y, z = dot

    radians: float = math.radians(offset_angle * -1)

    rotated_x: float = (x - x0) * math.cos(radians) - (y - y0) * math.sin(radians)
    rotated_y: float = (x - x0) * math.sin(radians) + (y - y0) * math.cos(radians)

    rotated_x += x0
    rotated_y += y0

    return rotated_x, rotated_y, z


def draw_graph_edges(
        graph: nx.Graph,
        nodes_positions: Dict[int, Tuple[float, float]],
        edges: List[Tuple[int, int]],
        edge_color: str,
        style: str
) -> None:
    nx.draw_networkx_edges(
        graph,
        pos = nodes_positions,
        edgelist = edges,
        edge_color = edge_color,
        style = style
    )


def draw_graph(
        graph: nx.Graph,
        number_of_clusters: int,
        positions: Dict[int, Tuple[float, float]],
        edges_data: Dict[str, Dict[str, Any]]
) -> None:
    figure_size = (7, 7)
    plt.figure(figsize=figure_size)

    # font_size = 10 if number_of_clusters < 10 else 3.5
    font_size = 10 if number_of_clusters < 10 else 3.5 if number_of_clusters < 30 else 2
    # node_size = 300 if number_of_clusters < 10 else 50
    node_size = 300 if number_of_clusters < 10 else 50 if number_of_clusters < 30 else 10

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


# characteristics calculation

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