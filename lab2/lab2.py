from . import utils, lab2_3d
from .basic_clusters_generator import BasicClustersGenerator
import networkx as nx
from typing import Dict, List, Tuple
import pandas as pd

from .irregular_connections_generator import IrregularConnectionsGenerator
from .regular_connections_generator import RegularConnectionsGenerator


def generate_graph(number_of_clusters):
    edges_data = {}

    basic_clusters_generator: BasicClustersGenerator = BasicClustersGenerator(number_of_clusters)
    graph: nx.Graph = basic_clusters_generator.basic_cluster
    positions: Dict[int, Tuple[float, float]] = basic_clusters_generator.positions
    edges_data.update(basic_clusters_generator.edges_data)

    regular_connection_generator: RegularConnectionsGenerator = RegularConnectionsGenerator(graph)
    graph = regular_connection_generator.graph
    edges_data.update(regular_connection_generator.edges_data)

    irregular_connection_generator: IrregularConnectionsGenerator = IrregularConnectionsGenerator(graph, number_of_clusters)
    graph = irregular_connection_generator.graph
    edges_data.update(irregular_connection_generator.edges_data)

    return graph, positions, edges_data

def main(number_of_clusters, draw: bool = False, calculate_topology_characteristics: bool = False, save_topology_characteristics: bool = False):
    if calculate_topology_characteristics:
        data = []
        print("№ processors | № clusters | Diameter |  Avr diameter | S (Degree) | Cost | Traffic")
        for i in range(1, number_of_clusters + 1):
            graph, positions, edges_data = generate_graph(i)

            diameter, node_pair = utils.calculate_diameter(graph)
            avr_diameter = utils.calculate_avr_diameter(graph)
            degree = utils.calculate_degree(graph)
            cost = utils.calculate_cost(graph)
            traffic = utils.calculate_traffic(avr_diameter, degree)
            data.append({
                "Number of clusters": i,
                "Number of nodes": i * 9,
                "Diameter": diameter,
                "Avr diameter": avr_diameter,
                "Degree": degree,
                "Cost": cost,
                "Traffic": traffic
            })
            print(f"{(i * 9):<15}", f"{i:<12}", f"{diameter:<10}", f"{avr_diameter:<16}", f"{degree:<10}", f"{cost:<6}", f"{traffic:<10}")

        if save_topology_characteristics:
            data_frame = pd.DataFrame(data)
            data_frame.to_csv("lab2_results.csv", sep=';', decimal=',', index=False)

    if draw:
        graph, positions, edges_data = generate_graph(number_of_clusters)
        utils.draw_graph(graph, number_of_clusters, positions, edges_data)
        lab2_3d.main(number_of_clusters)
