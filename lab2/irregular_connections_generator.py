import networkx as nx
from typing import List, Tuple


class IrregularConnectionsGenerator:
    def __init__(self, graph: nx.Graph, number_of_clusters: int):
        self.__graph = graph
        self.__number_of_clusters = number_of_clusters
        self.__irregular_edges = []
        self.__generate()

    def __generate(self):
        nodes: List[int] = [node for node in self.graph.nodes]
        edges: List[Tuple[int, int]] = []

        if self.__number_of_clusters > 3:
            for node in range(19, len(nodes), 8):
                if node + 6 < len(nodes):
                    edges.append((node, node + 6))
                else:
                    edges.append((node, 17))

        if self.__number_of_clusters > 5:
            for node in range(24, len(nodes), 16):
                if node + 14 < len(nodes):
                    edges.append((node, node + 14))

            if self.__number_of_clusters % 2 != 0:
                edges.append((nodes[-1], 30))
            else:
                edges.append((nodes[-1] - 8, 22))

            for node in range(32, len(nodes), 16):
                if node + 14 < len(nodes):
                    edges.append((node, node + 14))

            if self.__number_of_clusters % 2 != 0:
                edges.append((nodes[-1] - 8, 22))
            else:
                edges.append((nodes[-1], 30))

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