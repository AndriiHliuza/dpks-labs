import networkx as nx
from typing import List, Tuple


class RegularConnectionsGenerator:
    def __init__(self, graph: nx.Graph):
        self.__graph = graph
        self.__regular_edges = []
        self.__generate()

    def __generate(self):
        nodes: List[int] = [node for node in self.graph.nodes]
        edges: List[Tuple[int, int]] = []

        for node in range(18, len(nodes), 8):
            edges.append((2, node))
            edges.append((10, node))

        for node in range(20, len(nodes), 8):
            edges.append((4, node))
            edges.append((12, node))

        for node in range(21, len(nodes), 8):
            edges.append((5, node))
            edges.append((13, node))

        for node in range(23, len(nodes), 8):
            edges.append((7, node))
            edges.append((15, node))

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
