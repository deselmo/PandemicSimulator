import os
from pandemic_analyzer import AnalyzerEpochs, AnalyzerGraph


class Analyzer:
    gml_file: str = "graph.gml"
    csv_file: str = "epochs.csv"

    def __init__(self, path: str):
        if not os.path.isdir(path):
            raise RuntimeError("Analyzer error: invalid path in costructor")

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        if self.gml_file not in files:
            raise RuntimeError("Analyzer error: {} not in {}".format(self.gml_file, path))
        if self.csv_file not in files:
            raise RuntimeError("Analyzer error: {} not in {}".format(self.csv_file, path))

        self.directory: str = path
        self.analyzer_epochs = AnalyzerEpochs(os.path.join(path, self.csv_file))
        self.analyzer_graph = AnalyzerGraph(os.path.join(path, self.gml_file))

    def __call__(self) -> None:
        print("Analyzing {}".format(self.directory))

        self.analyzer_epochs()
        self.analyzer_graph()
