import networkx as nx
from typing import List, Tuple

from lab3 import utils


class RegularConnectionsGenerator:
    def __init__(self, graph: nx.Graph):
        self.__graph = graph
        self.__regular_edges = []
        self.__generate()

    def __generate(self):
        nodes: List[int] = [node for node in self.graph.nodes]
        edges: List[Tuple[int, int]] = []

        cluster_nodes_groups: List[List[List[int]]] = utils.get_clusters_nodes_groups(nodes)

        for i in range(len(cluster_nodes_groups)):
            for j in range(len(cluster_nodes_groups[i])):
                if j + 1 < len(cluster_nodes_groups[i]):
                    edges.append((cluster_nodes_groups[i][j][1], cluster_nodes_groups[i][j + 1][0]))
                    edges.append((cluster_nodes_groups[i][j][4], cluster_nodes_groups[i][j + 1][2]))
                    edges.append((cluster_nodes_groups[i][j][7], cluster_nodes_groups[i][j + 1][5]))

                if i + 1 < len(cluster_nodes_groups) and j + 1 <= len(cluster_nodes_groups[i + 1]):
                    edges.append((cluster_nodes_groups[i][j][2], cluster_nodes_groups[i + 1][j][2]))
                    edges.append((cluster_nodes_groups[i][j][4], cluster_nodes_groups[i + 1][j][4]))
                    edges.append((cluster_nodes_groups[i][j][5], cluster_nodes_groups[i + 1][j][5]))
                    edges.append((cluster_nodes_groups[i][j][7], cluster_nodes_groups[i + 1][j][7]))

                    edges.append((cluster_nodes_groups[i][j][3], cluster_nodes_groups[i + 1][j][0]))
                    edges.append((cluster_nodes_groups[i][j][3], cluster_nodes_groups[i + 1][j][1]))

                    edges.append((cluster_nodes_groups[i][j][6], cluster_nodes_groups[i + 1][j][0]))
                    edges.append((cluster_nodes_groups[i][j][6], cluster_nodes_groups[i + 1][j][1]))

        self.__graph.add_edges_from(edges)
        self.__regular_edges = edges

    @property
    def graph(self) -> nx.Graph:
        return self.__graph

    @property
    def edges_data(self):
        return {
            "regular_edges": {
                "edges": self.__regular_edges,
                "color": "#4bf542",
                "style": "solid"
            }
        }
