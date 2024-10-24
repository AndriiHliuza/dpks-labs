from lab2.basic_clusters_generator_3d import BasicClustersGenerator
import networkx as nx
from typing import Dict, Tuple
import matplotlib.pyplot as plt

from lab2.irregular_connections_generator import IrregularConnectionsGenerator
from lab2.regular_connections_generator import RegularConnectionsGenerator


def main(number_of_clusters):
    basic_clusters_generator: BasicClustersGenerator = BasicClustersGenerator(number_of_clusters)
    graph: nx.Graph = basic_clusters_generator.basic_cluster
    positions: Dict[int, Tuple[float, float, float]] = basic_clusters_generator.positions

    # Extract x, y, z values
    x_values = [positions[i][0] for i in graph.nodes()]
    y_values = [positions[i][1] for i in graph.nodes()]
    z_values = [positions[i][2] for i in graph.nodes()]

    # Create the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the nodes
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

    for node in graph.nodes():
        ax.text(positions[node][0], positions[node][1], positions[node][2], str(node), color='black', fontsize=10, ha='center', va='center')

    # Hide the axes
    ax.set_axis_off()

    # Show the plot
    plt.show()
