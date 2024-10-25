from typing import Dict, Tuple, List

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import math
import numpy as np
import pandas as pd

from lab3 import utils
from lab3.irregular_connections_generator import IrregularConnectionsGenerator
from lab3.basic_clusters_generator import BasicClustersGenerator
from lab3.regular_connections_generator import RegularConnectionsGenerator


def generate_graph(number_of_clusters):
    edges_data = {}

    basic_clusters_generator: BasicClustersGenerator = BasicClustersGenerator(number_of_clusters)
    graph: nx.Graph = basic_clusters_generator.basic_cluster
    positions: Dict[int, Tuple[float, float, float]] = basic_clusters_generator.positions
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
            data_frame.to_csv("lab3_results.csv", sep=';', decimal=',', index=False)

    if draw:
        basic_clusters_generator: BasicClustersGenerator = BasicClustersGenerator(number_of_clusters)
        graph: nx.Graph = basic_clusters_generator.basic_cluster
        positions: Dict[int, Tuple[float, float, float]] = basic_clusters_generator.positions


        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        x_values = [positions[i][0] for i in graph.nodes()]
        y_values = [positions[i][1] for i in graph.nodes()]
        z_values = [positions[i][2] for i in graph.nodes()]
        ax.scatter(x_values, y_values, z_values, color='white', edgecolor='black', linewidth=1, s=200)

        inter_cluster_edges_data = basic_clusters_generator.edges_data
        for edge in inter_cluster_edges_data["basic_cluster_edges"]["edges"]:
            x_edge = [positions[edge[0]][0], positions[edge[1]][0]]
            y_edge = [positions[edge[0]][1], positions[edge[1]][1]]
            z_edge = [positions[edge[0]][2], positions[edge[1]][2]]
            ax.plot(x_edge, y_edge, z_edge, color='blue')


        regular_connection_generator: RegularConnectionsGenerator = RegularConnectionsGenerator(graph)
        graph = regular_connection_generator.graph
        regular_edges_data = regular_connection_generator.edges_data

        for edge in regular_edges_data["regular_edges"]["edges"]:
            x_edge = [positions[edge[0]][0], positions[edge[1]][0]]
            y_edge = [positions[edge[0]][1], positions[edge[1]][1]]
            z_edge = [positions[edge[0]][2], positions[edge[1]][2]]
            ax.plot(x_edge, y_edge, z_edge, color='green')

        irregular_connection_generator: IrregularConnectionsGenerator = IrregularConnectionsGenerator(graph, number_of_clusters)
        graph = irregular_connection_generator.graph
        irregular_edges_data = irregular_connection_generator.edges_data

        for edge in irregular_edges_data["irregular_edges"]["edges"]:
            x_edge = [positions[edge[0]][0], positions[edge[1]][0]]
            y_edge = [positions[edge[0]][1], positions[edge[1]][1]]
            z_edge = [positions[edge[0]][2], positions[edge[1]][2]]
            ax.plot(x_edge, y_edge, z_edge, color='red')

        # Hide the axes
        ax.set_axis_off()
        for node in graph.nodes():
            ax.text(positions[node][0], positions[node][1], positions[node][2], str(node), color='black', fontsize=4, ha='center', va='center')

        plt.show()

