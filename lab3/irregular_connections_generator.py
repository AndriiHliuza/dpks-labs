import networkx as nx
from typing import List, Tuple

from lab3 import utils


class IrregularConnectionsGenerator:
    def __init__(self, graph: nx.Graph, number_of_clusters: int):
        self.__graph = graph
        self.__irregular_edges = []
        self.__number_of_clusters = number_of_clusters
        self.__generate()

    def __generate(self):
        nodes: List[int] = [node for node in self.graph.nodes]
        edges: List[Tuple[int, int]] = []

        cluster_nodes_groups: List[List[List[int]]] = utils.get_clusters_nodes_groups(nodes)

        if self.__number_of_clusters >= 2:
            for i in range(len(cluster_nodes_groups)):
                for j in range(len(cluster_nodes_groups[i])):
                    if j + 1 < len(cluster_nodes_groups[i]) and i + 1 < len(cluster_nodes_groups) and j + 2 <= len(cluster_nodes_groups[i + 1]):
                        edges.append((cluster_nodes_groups[i][j][0], cluster_nodes_groups[i + 1][j + 1][0]))

                    if ((i == 0 or j == 0) and
                            i < len(cluster_nodes_groups) and
                            j < len(cluster_nodes_groups[i]) and
                            len(cluster_nodes_groups) - 1 - j < len(cluster_nodes_groups) and
                            len(cluster_nodes_groups) - 1 - i < len(cluster_nodes_groups[len(cluster_nodes_groups) - 1 - j]) and
                            cluster_nodes_groups[i][j][1] in nodes and
                            cluster_nodes_groups[len(cluster_nodes_groups) - 1 - j][len(cluster_nodes_groups) - 1 - i][1] in nodes and
                            cluster_nodes_groups[i][j][1] != cluster_nodes_groups[len(cluster_nodes_groups) - 1 - j][len(cluster_nodes_groups) - 1 - i][1]):
                        edges.append((cluster_nodes_groups[i][j][1], cluster_nodes_groups[len(cluster_nodes_groups) - 1 - j][len(cluster_nodes_groups) - 1 - i][1]))

                    if j > 0 and i + 1 < len(cluster_nodes_groups) and j - 1 < len(cluster_nodes_groups[i + 1]):
                        edges.append((cluster_nodes_groups[i][j][0], cluster_nodes_groups[i + 1][j - 1][0]))


        self.__graph.add_edges_from(edges)
        self.__irregular_edges = edges

    @property
    def graph(self) -> nx.Graph:
        return self.__graph

    @property
    def edges_data(self):
        return {
            "irregular_edges": {
                "edges": self.__irregular_edges,
                "color": "#eb4034",
                "style": "dashed"
            }
        }