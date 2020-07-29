from __future__ import annotations
import pandemic as pd
from typing import MutableSequence, Optional, MutableMapping
import os


class Simulator:
    def __init__(self, params: pd.Parameters):
        self.params = params
        self.generator = pd.Generator(params)
        self.mobility = pd.Mobility(params, self.generator)
        self.map = pd.Map(self)

        self.susceptible_peers: MutableMapping[int, pd.Peer] = dict()
        self.new_infected_peers: MutableMapping[int, pd.Peer] = dict()
        self.infected_peers: MutableMapping[int, pd.Peer] = dict()
        self.patched_peers: MutableMapping[int, pd.Peer] = dict()

        for peer in self.map.peers:
            self.susceptible_peers[peer.id] = peer

        self.data_epochs: MutableSequence[pd.DataEpoch] = []

        self.epoch: int = 0
        self._init_infected()

        self._add_data_epoch()

    @staticmethod
    def from_params(path: str) -> Optional[Simulator]:
        params: Optional[pd.Parameters] = pd.Parameters.from_json(path)

        if(params is None):
            return None

        return pd.Simulator(params)

    def step(self) -> bool:
        if self.stop_condition():
            return False

        self.epoch += 1

        for peer in self.map.peers:
            peer.step_mobility()

        for peer in list(self.susceptible_peers.values()) + list(self.infected_peers.values()):
            peer.step_patch()

        for peer in self.generator.permute(list(self.infected_peers.values())):
            peer.step_infection()

        for peer in list(self.new_infected_peers.values()):
            peer.commit_infection()

        self._add_data_epoch()

        return True

    def stop_condition(self):
        if self._epoch_limit_reached():
            return True

        if(
            self.params.patching_begin_epoch is None
            and self.params.peers_number == len(self.infected_peers)
        ):
            return True

        if self.params.peers_number == len(self.patched_peers):
            return True

        return False

    def output(self) -> bool:
        directory: Optional[str] = self.params.output_directory

        if directory is not None:
            gml_file = os.path.join(directory, "graph.gml")
            csv_file = os.path.join(directory, "epochs.csv")

            if(pd.save_gml(gml_file, self.map.peers)):
                print("Error saving the file {}".format(gml_file))
                return True

            if(pd.save_csv(csv_file, self.data_epochs)):
                print("Error saving the file {}".format(csv_file))
                return True

        else:
            pd.print_gml(self.map.peers)
            pd.print_csv(self.data_epochs)

        return False

    def _init_infected(self):
        peers_os0 = list(filter(lambda peer: peer.os == self.params.oss[0].name, self.map.peers))
        choosen_peers = self.generator.choice(peers_os0, self.params.initial_infected_number)

        for peer in choosen_peers:
            peer.infect(None)

        for peer in list(self.new_infected_peers.values()):
            peer.commit_infection()

    def _epoch_limit_reached(self):
        if self.params.epoch_limit is None:
            return False

        if self.epoch < self.params.epoch_limit:
            return False

        return True

    def _add_data_epoch(self):
        self.data_epochs.append(pd.DataEpoch(
            epoch=self.epoch,
            n_susceptible=len(self.susceptible_peers),
            n_infected=len(self.infected_peers),
            n_patched=len(self.patched_peers),
        ))
