import networkx as nx
import numpy as np
from typing import Dict, List, Tuple
from . import utils
import math


class BasicClustersGenerator:
    def __init__(self, number_of_clusters: int):
        self.__all_clusters_graph = None
        self.__positions = None
        self.__basic_edges = []
        self.__number_of_clusters = number_of_clusters
        self.__generate_all_clusters_graph()

    def __generate_cluster_with_provided_number(self, cluster_number: int) -> nx.Graph:
        cluster: nx.Graph = nx.Graph()

        nodes_for_cluster: List[int] = [8 * cluster_number - i for i in range(7, -1, -1)]
        edges_for_cluster: List[Tuple[int, int]] = [
            (8 * cluster_number - 7, 8 * cluster_number - 5),
            (8 * cluster_number - 7, 8 * cluster_number - 4),
            (8 * cluster_number - 7, 8 * cluster_number - 2),
            (8 * cluster_number - 7, 8 * cluster_number - 1),

            (8 * cluster_number - 6, 8 * cluster_number - 4),
            (8 * cluster_number - 6, 8 * cluster_number - 3),
            (8 * cluster_number - 6, 8 * cluster_number - 1),
            (8 * cluster_number - 6, 8 * cluster_number),

            (8 * cluster_number - 5, 8 * cluster_number - 4),
            (8 * cluster_number - 5, 8 * cluster_number - 2),
            (8 * cluster_number - 1, 8 * cluster_number - 4),
            (8 * cluster_number - 1, 8 * cluster_number - 2),

            (8 * cluster_number - 3, 8 * cluster_number - 4),
            (8 * cluster_number, 8 * cluster_number - 3),
            (8 * cluster_number, 8 * cluster_number - 1),
        ]

        cluster.add_nodes_from(nodes_for_cluster)
        cluster.add_edges_from(edges_for_cluster)
        self.__basic_edges.extend(edges_for_cluster)

        return cluster

    def __generate_nodes_positions_for_basic_cluster(self, graph: nx.Graph) -> None:
        nodes: List[int] = [node for node in graph.nodes()]
        positions: Dict[int, Tuple[float, float, float]] = {}

        cluster_nodes_groups: List[List[List[int]]] = utils.get_clusters_nodes_groups(nodes)

        right_offset = 0
        bottom_offset = 0

        for i in range(len(cluster_nodes_groups)):
            for j in range(len(cluster_nodes_groups[i])):
                if cluster_nodes_groups[i][j] == [1, 2, 3, 4, 5, 6, 7, 8]:
                    positions.update({
                        1: (1, 1, 0),
                        2: (1, 3, 0),
                        3: (0, 0, -1),
                        4: (0, 2, -1),
                        5: (0, 4, -1),
                        6: (2, 0, -1),
                        7: (2, 2, -1),
                        8: (2, 4, -1),
                    })
                else:
                    positions.update({
                        cluster_nodes_groups[i][j][0]: (positions.get(1)[0], positions.get(1)[1] + right_offset, positions.get(1)[2] - bottom_offset),
                        cluster_nodes_groups[i][j][1]: (positions.get(2)[0], positions.get(2)[1] + right_offset, positions.get(2)[2] - bottom_offset),
                        cluster_nodes_groups[i][j][2]: (positions.get(3)[0], positions.get(3)[1] + right_offset, positions.get(3)[2] - bottom_offset),
                        cluster_nodes_groups[i][j][3]: (positions.get(4)[0], positions.get(4)[1] + right_offset, positions.get(4)[2] - bottom_offset),
                        cluster_nodes_groups[i][j][4]: (positions.get(5)[0], positions.get(5)[1] + right_offset, positions.get(5)[2] - bottom_offset),
                        cluster_nodes_groups[i][j][5]: (positions.get(6)[0], positions.get(6)[1] + right_offset, positions.get(6)[2] - bottom_offset),
                        cluster_nodes_groups[i][j][6]: (positions.get(7)[0], positions.get(7)[1] + right_offset, positions.get(7)[2] - bottom_offset),
                        cluster_nodes_groups[i][j][7]: (positions.get(8)[0], positions.get(8)[1] + right_offset, positions.get(8)[2] - bottom_offset),
                    })
                right_offset += 6
            right_offset = 0
            bottom_offset += 2

        self.__positions = positions


    def __generate_all_clusters_graph(self) -> None:
        self.__all_clusters_graph: nx.Graph = nx.Graph()

        for i in range(1, self.__number_of_clusters + 1):
            cluster: nx.Graph = self.__generate_cluster_with_provided_number(i)
            self.__all_clusters_graph.add_nodes_from(cluster.nodes)
            self.__all_clusters_graph.add_edges_from(cluster.edges)

        self.__generate_nodes_positions_for_basic_cluster(self.__all_clusters_graph)

    @property
    def basic_cluster(self) -> nx.Graph:
        return self.__all_clusters_graph

    @property
    def positions(self) -> Dict[int, Tuple[float, float, float]]:
        return self.__positions

    @property
    def edges_data(self):
        return {
            "basic_cluster_edges": {
                "edges": self.__basic_edges,
                "color": "#4245f5",
                "style": "solid"
            }
        }
