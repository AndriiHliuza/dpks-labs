from . import utils
import networkx as nx
import pandas as pd

def generate_cluster_node_graph(number_of_clusters, angle, radius):
    graph = nx.Graph()

    nodes = [9 * number_of_clusters - i for i in range(8, -1, -1)]

    edges = [
        (9 * number_of_clusters - 8, 9 * number_of_clusters - 7),
        (9 * number_of_clusters - 8, 9 * number_of_clusters - 5),
        (9 * number_of_clusters - 8, 9 * number_of_clusters - 4),

        (9 * number_of_clusters - 6, 9 * number_of_clusters - 7),
        (9 * number_of_clusters - 6, 9 * number_of_clusters - 3),
        (9 * number_of_clusters - 6, 9 * number_of_clusters - 4),

        (9 * number_of_clusters - 2, 9 * number_of_clusters - 5),
        (9 * number_of_clusters - 2, 9 * number_of_clusters - 1),
        (9 * number_of_clusters - 2, 9 * number_of_clusters - 4),

        (9 * number_of_clusters, 9 * number_of_clusters - 1),
        (9 * number_of_clusters, 9 * number_of_clusters - 3),
        (9 * number_of_clusters, 9 * number_of_clusters - 4),
    ]

    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    base_nodes_positions = {
        9 * number_of_clusters - 8: (-1, radius),
        9 * number_of_clusters - 7: (0, radius),
        9 * number_of_clusters - 6: (1, radius),

        9 * number_of_clusters - 5: (-1, radius - 1),
        9 * number_of_clusters - 4: (0, radius - 1),
        9 * number_of_clusters - 3: (1, radius - 1),

        9 * number_of_clusters - 2: (-1, radius - 2),
        9 * number_of_clusters - 1: (0, radius - 2),
        9 * number_of_clusters: (1, radius - 2),
    }

    rotated_nodes_positions = {node: utils.rotate_dot(node_position, angle) for node, node_position in
                               base_nodes_positions.items()}

    return graph, rotated_nodes_positions, edges

def generate_separate_clusters_edges(number_of_clusters, complex_graph, complex_graph_positions, complex_graph_edges_data):
    angle_step = 360 / number_of_clusters
    radius = number_of_clusters * (1.25 if number_of_clusters < 10 else 1)
    for cluster_number in range(1, number_of_clusters + 1):
        angle_offset = angle_step * (cluster_number - 1)
        cluster_node_graph, cluster_node_graph_positions, cluster_node_graph_edges = generate_cluster_node_graph(
            cluster_number,
            angle_offset,
            radius
        )

        complex_graph = nx.compose(complex_graph, cluster_node_graph)

        complex_graph_positions.update(cluster_node_graph_positions)
        complex_graph_edges_data["cluster_edges"]["edges"].extend(cluster_node_graph_edges)

    return complex_graph

def generate_regular_connections_in_cluster(number_of_clusters, complex_graph, complex_graph_edges_data):
    for cluster_number in range(1, number_of_clusters + 1):
        regular_edges = []

        if number_of_clusters == 1:
            break

        if cluster_number == number_of_clusters:
            regular_edges.extend([
                (9 * cluster_number - 8, 1),
                (9 * cluster_number - 7, 2),
                (9 * cluster_number - 6, 3),
                (9 * cluster_number - 5, 4),
                (9 * cluster_number - 4, 5),
                (9 * cluster_number - 3, 6),
                (9 * cluster_number - 2, 7),
                (9 * cluster_number - 1, 8),
                (9 * cluster_number - 0, 9),
            ])
        else:
            for j in range(0, 9):
                regular_edges.append((9 * cluster_number - j, 9 * (cluster_number + 1) - j))

        complex_graph.add_edges_from(regular_edges)
        complex_graph_edges_data["regular_edges"]["edges"].extend(regular_edges)


def add_irregular_connections_of_type1(number_of_clusters, irregular_connections):
    if number_of_clusters > 3:
        for cluster_number in range(1, number_of_clusters + 1):
            if cluster_number + 2 <= number_of_clusters:
                irregular_connections.append((9 * cluster_number - 7, 9 * (cluster_number + 2) - 7))


            if cluster_number >= 3:
                irregular_connections.append((9 * cluster_number - 7, 9 * (cluster_number - 2) - 7))
            else:
                if cluster_number == 1:
                    irregular_connections.append((2, 9 * (number_of_clusters - 1) - 7))
                elif cluster_number == 2:
                    irregular_connections.append((11, 9 * number_of_clusters - 7))


def add_irregular_connections_of_type2(number_of_clusters, irregular_connections):
    if number_of_clusters > 4:
        for cluster_number in range(1, number_of_clusters + 1):
            if cluster_number + 3 <= number_of_clusters:
                irregular_connections.append((9 * cluster_number - 4, 9 * (cluster_number + 3) - 4))

            if cluster_number >= 4:
                irregular_connections.append((9 * cluster_number - 4, 9 * (cluster_number - 3) - 4))
            else:
                if cluster_number == 1:
                    irregular_connections.append((5, 9 * (number_of_clusters - 2) - 4))
                elif cluster_number == 2:
                    irregular_connections.append((14, 9 * (number_of_clusters - 1) - 4))
                elif cluster_number == 3:
                    irregular_connections.append((23, 9 * number_of_clusters - 4))


def add_irregular_connections_of_type3(number_of_clusters, irregular_connections):
    if number_of_clusters > 5:
        for cluster_number in range(1, number_of_clusters + 1):
            if cluster_number + 4 <= number_of_clusters:
                irregular_connections.append((9 * cluster_number - 1, 9 * (cluster_number + 4) - 1))

            if cluster_number >= 5:
                irregular_connections.append((9 * cluster_number - 1, 9 * (cluster_number - 4) - 1))
            else:
                if cluster_number == 1:
                    irregular_connections.append((8, 9 * (number_of_clusters - 3) - 1))
                elif cluster_number == 2:
                    irregular_connections.append((17, 9 * (number_of_clusters - 2) - 1))
                elif cluster_number == 3:
                    irregular_connections.append((26, 9 * (number_of_clusters - 1) - 1))
                elif cluster_number == 4:
                    irregular_connections.append((35, 9 * number_of_clusters - 1))


def add_irregular_connections(number_of_clusters, irregular_connections, number_of_clusters_between_clusters, node_number_in_base_cluster):
    node_offset = 9 - node_number_in_base_cluster

    if (number_of_clusters_between_clusters == 1 and number_of_clusters < 4) or \
            (number_of_clusters_between_clusters == 2 and number_of_clusters < 6) or \
            (number_of_clusters_between_clusters == 3 and number_of_clusters < 8):
        return

    for cluster_number in range(1, number_of_clusters + 1):
        if cluster_number + number_of_clusters_between_clusters + 1 <= number_of_clusters:
            irregular_connections.append((9 * cluster_number - node_offset, 9 * (cluster_number + number_of_clusters_between_clusters + 1) - node_offset))

        if cluster_number >= number_of_clusters_between_clusters + 2:
            irregular_connections.append((9 * cluster_number - node_offset, 9 * (cluster_number - number_of_clusters_between_clusters - 1) - node_offset))
        else:
            for i in range(1, number_of_clusters_between_clusters + 2):
                if cluster_number == i:
                    irregular_connections.append((9 * cluster_number - node_offset, 9 * (number_of_clusters - ((number_of_clusters_between_clusters + 1) - i)) - node_offset))




def generate_irregular_connections_in_cluster(number_of_clusters, complex_graph, complex_graph_edges_data):
    irregular_connections = []

    add_irregular_connections(number_of_clusters, irregular_connections, 1, 2)
    add_irregular_connections(number_of_clusters, irregular_connections, 2, 5)
    add_irregular_connections(number_of_clusters, irregular_connections, 3, 8)

    unique_irregular_connections = {tuple(sorted(irregular_connection)) for irregular_connection in irregular_connections}
    irregular_connections = list(unique_irregular_connections)

    complex_graph.add_edges_from(irregular_connections)
    complex_graph_edges_data["irregular_edges"]["edges"].extend(irregular_connections)



def generate_cluster(number_of_clusters):
    complex_graph = nx.Graph()
    complex_graph_edges_data = {
        "cluster_edges": {
            "edges": [],
            "color": "#4245f5",
            "style": "solid"
        },

        "regular_edges": {
            "edges": [],
            "color": "#4bf542",
            "style": "solid"
        },

        "irregular_edges": {
            "edges": [],
            "color": "#f54242",
            "style": "dashed"
        }
    }
    complex_graph_positions = {}

    complex_graph = generate_separate_clusters_edges(number_of_clusters, complex_graph, complex_graph_positions, complex_graph_edges_data)
    generate_regular_connections_in_cluster(number_of_clusters, complex_graph, complex_graph_edges_data)
    generate_irregular_connections_in_cluster(number_of_clusters, complex_graph, complex_graph_edges_data)

    return complex_graph, complex_graph_positions, complex_graph_edges_data, number_of_clusters


def main(number_of_clusters, draw = False, save_topology_characteristics = False):
    data = []

    complex_graph, complex_graph_positions, complex_graph_edges_data, number_of_clusters = generate_cluster(number_of_clusters)

    print("№ processors | № clusters | Diameter |  Avr diameter | S (Degree) | Cost | Traffic")
    for i in range(1, number_of_clusters + 1):
        graph_in_range, graph_in_range_positions, graph_in_range_edges_data, graph_in_range_number_of_clusters = generate_cluster(i)
        diameter, node_pair = utils.calculate_diameter(graph_in_range)
        avr_diameter = utils.calculate_avr_diameter(graph_in_range)
        degree = utils.calculate_degree(graph_in_range)
        cost = utils.calculate_cost(graph_in_range)
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
        data_frame.to_csv("lab1_results.csv", index = False)

    if draw:
        utils.draw_graph(complex_graph, complex_graph_positions, complex_graph_edges_data, number_of_clusters)
