import os
import sys
from typing import NamedTuple, Sequence, Tuple
import numpy as np
import matplotlib.pyplot as plt
import csv
import seaborn

try:
    import graph_tool
    import graph_tool.all as gt
except ModuleNotFoundError as error:
    print(error)
    print("graph-tool must be installed manually, follow instructions in " +
          "https://git.skewed.de/count0/graph-tool/wikis/installation-instructions")
    sys.exit(1)


max_int32 = 2**31-1
red_green_map = {0: [0.6, 0, 0, 0.5], 1: [0, 0.5, 0, 0.5]}


class GraphProperties(NamedTuple):
    density: float
    diameter: int
    avg_path_lengths: float
    var_path_lengths: float
    min_cc: float
    max_cc: float
    avg_out_degree: float
    max_out_degree: int
    avg_in_degree: float
    max_in_degree: int
    count_0_in_degree: int
    count_1_in_degree: int


class AnalyzerGraph:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise RuntimeError("AnalyzerGraph error: invalid path in costructor")

        self.graph: gt.Graph = gt.load_graph(path)

        directory = os.path.dirname(path)

        self.output_network: str = os.path.join(directory, "network.pdf")
        self.output_out_degree: str = os.path.join(directory, "chart_out_degree.png")
        self.output_graph_properties: str = os.path.join(directory, "graph_properties.csv")

        self.plot_color = self.graph.new_vertex_property('vector<double>')
        for v in self.graph.vertices():
            self.plot_color[v] = red_green_map[self.graph.vertex_properties['label'][v] != ""]

    def __call__(self):
        self.graph_draw()
        self.graph_properties()

    def graph_properties(self):
        seaborn.set()

        diameter, avg_path_lengths, var_path_lengths = self.path_lengths()
        density = self.density()
        min_cc, max_cc = self.clustering_coefficient()
        (
            max_in_degree, max_out_degree,
            avg_in_degree, avg_out_degree,
            count_0_in_degree, count_1_in_degree,
        ) = self.degrees()

        graph_properties = GraphProperties(
            density, diameter, avg_path_lengths, var_path_lengths,
            min_cc, max_cc,
            avg_out_degree, max_out_degree,
            avg_in_degree, max_in_degree,
            count_0_in_degree, count_1_in_degree,
        )

        with open(self.output_graph_properties, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(GraphProperties._fields)
            writer.writerow(graph_properties._asdict().values())

        print("Graph properties saved in {}".format(self.output_graph_properties))

    def path_lengths(self) -> Tuple[int, float, float]:
        path_lengths = gt.shortest_distance(self.graph)
        valid_path_length = []

        for v in self.graph.vertices():
            for path_length in path_lengths[v]:
                if 0 < path_length < max_int32:
                    valid_path_length.append(path_length)

        diameter = np.max(valid_path_length)
        avg_path_lengths = np.mean(valid_path_length)
        var_path_lengths = np.var(valid_path_length)

        return diameter, avg_path_lengths, var_path_lengths

    def density(self):
        return self.graph.num_edges() / (self.graph.num_vertices() * (self.graph.num_vertices()-1))

    def clustering_coefficient(self) -> Tuple[float, float]:
        local_ccs = list(graph_tool.clustering.local_clustering(self.graph))

        min_local_cc = min(local_ccs)
        max_local_cc = max(local_ccs)

        return min_local_cc, max_local_cc

    def degrees(self) -> Tuple[int, int, float, float, int, int]:
        in_degrees = [v.in_degree() for v in self.graph.vertices()]
        out_degrees = [v.out_degree() for v in self.graph.vertices()]

        count_in_degrees = list(zip(np.unique(in_degrees, return_counts=True)))
        count_0_in_degree = count_in_degrees[0][0][1]
        count_1_in_degree = count_in_degrees[1][0][1]

        max_in_degree = np.max(in_degrees)
        max_out_degree = np.max(out_degrees)
        avg_in_degree = np.average(in_degrees)
        avg_out_degree = np.average(out_degrees)

        plt.rcParams["font.family"] = "monospace"
        values, occurrences = np.unique(out_degrees, return_counts=True)
        plt.xticks(np.arange(0, max_out_degree+1, 1))
        plt.bar(values, occurrences, width=1)
        plt.savefig(self.output_out_degree, bbox_inches='tight')
        plt.close()
        print("Chart out-degree distribution saved in {}".format(self.output_out_degree))

        return (
            max_in_degree, max_out_degree,
            avg_in_degree, avg_out_degree,
            count_0_in_degree, count_1_in_degree,
        )

    def graph_draw(self):
        gt.graph_draw(
            self.graph,
            output_size=(800, 800),
            output=self.output_network,
            vertex_text=self.graph.vertex_properties["label"],
            edge_text=self.graph.edge_properties["label"],
            vertex_fill_color=self.plot_color,
            vertex_text_color="black",
            ink_scale=0.5,
            pos=gt.sfdp_layout(self.graph, p=2.2)
        )

        print("Network saved in {}".format(self.output_network))
