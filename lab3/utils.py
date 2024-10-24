import math
from typing import Tuple, Dict, List, Any
import networkx as nx
import matplotlib.pyplot as plt


def get_clusters_nodes_groups(nodes: List[int]) -> List[List[List[int]]]:
    clusters_nodes: List[List[int]] = [nodes[i:i + 8] for i in range(0, len(nodes), 8)]

    size = math.ceil(math.sqrt(len(clusters_nodes)))
    clusters_nodes_groups: List = []
    for i in range(len(clusters_nodes)):
        row = i // size

        if row >= len(clusters_nodes_groups):
            clusters_nodes_groups.append([])

        clusters_nodes_groups[row].append(clusters_nodes[i])

    return clusters_nodes_groups


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