import networkx as nx
from typing import Dict, List, Tuple
from . import utils


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
            (8 * cluster_number - 7, 8 * cluster_number - 4),
            (8 * cluster_number - 6, 8 * cluster_number - 4),
            (8 * cluster_number - 2, 8 * cluster_number - 4),
            (8 * cluster_number - 1, 8 * cluster_number - 4),

            (8 * cluster_number - 6, 8 * cluster_number - 3),
            (8 * cluster_number - 5, 8 * cluster_number - 3),
            (8 * cluster_number - 1, 8 * cluster_number - 3),
            (8 * cluster_number, 8 * cluster_number - 3),
        ]

        cluster.add_nodes_from(nodes_for_cluster)
        cluster.add_edges_from(edges_for_cluster)
        self.__basic_edges.extend(edges_for_cluster)

        return cluster

    def __generate_nodes_positions_for_provided_cluster(
            self,
            graph: nx.Graph,
            cluster_number: int
    ) -> Dict[int, Tuple[float, float]]:
        nodes: List[int] = [node for node in graph.nodes()]
        positions: Dict[int, Tuple[float, float]]

        if sorted(nodes) == [1, 2, 3, 4, 5, 6, 7, 8]:
            positions = {
                1: (-5, 1),
                2: (-3, 1),
                3: (-1, 1),
                4: (-4, 0),
                5: (-2, 0),
                6: (-5, -1),
                7: (-3, -1),
                8: (-1, -1),
            }
        elif sorted(nodes) == [9, 10, 11, 12, 13, 14, 15, 16]:
            positions = {
                9: (1, 1),
                10: (3, 1),
                11: (5, 1),
                12: (2, 0),
                13: (4, 0),
                14: (1, -1),
                15: (3, -1),
                16: (5, -1),
            }
        else:
            radius: float = utils.get_radius_for_cluster_with_provided_number_of_nodes(self.__number_of_clusters - 2)
            offset_angle: float = utils.get_offset_angle(self.__number_of_clusters - 2)
            offset_angle_for_current_cluster = utils.get_offset_angle_for_current_cluster(offset_angle, cluster_number)

            positions = {
                8 * cluster_number - 7: (-2, radius + 1),
                8 * cluster_number - 6: (0, radius + 1),
                8 * cluster_number - 5: (2, radius + 1),
                8 * cluster_number - 4: (-1, radius),
                8 * cluster_number - 3: (1, radius),
                8 * cluster_number - 2: (-2, radius - 1),
                8 * cluster_number - 1: (0, radius - 1),
                8 * cluster_number: (2, radius - 1),
            }

            positions = {node: utils.rotate_dot(position, offset_angle_for_current_cluster) for node, position in
                         positions.items()}

        return positions

    def __generate_all_clusters_graph(self) -> None:
        self.__all_clusters_graph: nx.Graph = nx.Graph()
        self.__positions: Dict[int, Tuple[float, float]] = {}

        for i in range(1, self.__number_of_clusters + 1):
            cluster: nx.Graph = self.__generate_cluster_with_provided_number(i)
            self.__all_clusters_graph.add_nodes_from(cluster.nodes)
            self.__all_clusters_graph.add_edges_from(cluster.edges)
            self.__positions.update(self.__generate_nodes_positions_for_provided_cluster(cluster, i))

    @property
    def basic_cluster(self) -> nx.Graph:
        return self.__all_clusters_graph

    @property
    def positions(self) -> Dict[int, Tuple[float, float]]:
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
