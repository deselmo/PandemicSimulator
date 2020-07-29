from typing import Sequence, NamedTuple
import os
import csv
import matplotlib.pyplot as plt
import numpy as np


class DataEpoch(NamedTuple):
    epoch: int
    n_susceptible: int
    n_infected: int
    n_patched: int


class AnalyzerEpochs:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise RuntimeError("AnalyzerEpochs error: invalid path in costructor")

        self.output: str = os.path.join(os.path.dirname(path), "chart_epochs.png")
        self.data_epochs: Sequence[DataEpoch] = self._init_epochs(path)

    def _init_epochs(self, path: str) -> Sequence[DataEpoch]:
        try:
            with open(path, mode="r") as file:
                reader = csv.reader(file)
                next(reader)

                lines: Sequence[DataEpoch] = [DataEpoch(*map(int, row)) for row in reader]
        except Exception as error:
            print(error)
            raise RuntimeError("AnalyzerEpochs error: invalid {} file".format(path))

        return lines

    def __call__(self) -> None:
        plt.rcdefaults()

        if not len(self.data_epochs):
            return

        epoch, n_susceptible, n_infected, n_patched = zip(*self.data_epochs)
        n_not_patched = [n_infected[i] + n_susceptible[i] for i, _ in enumerate(self.data_epochs)]
        counters = np.arange(0, sum(self.data_epochs[0][1:])+1, sum(self.data_epochs[0])/10)
        percentages = np.arange(0, 1001, 10)
        yaxislabels = [
            '{}'.format(int(np.round(c))) +
            '{}%'.format(p).rjust(5)
            for p, c in zip(percentages, counters)
        ]

        plt.rcParams["font.family"] = "monospace"
        _, ax = plt.subplots()
        plt.xlim(-0.6, len(self.data_epochs)-0.5)
        plt.yticks(counters)
        ax.set_yticklabels(yaxislabels)
        ax.bar(epoch, n_infected, color="red", width=1)
        ax.bar(epoch, n_susceptible, color="blue", width=1, bottom=n_infected)
        ax.bar(epoch, n_patched, color="green", width=1, bottom=n_not_patched)
        plt.savefig(self.output, bbox_inches='tight')
        plt.close()
        print("Chart epochs infection desitribution saved in {}".format(self.output))
