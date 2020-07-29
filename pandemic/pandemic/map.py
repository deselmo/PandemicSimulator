import pandemic as pd
from typing import MutableSequence, Optional, Sequence


class Map:
    def __init__(self, simulator: pd.Simulator):
        self.simulator: pd.Simulator = simulator
        self.params: pd.Parameters = simulator.params
        self.generator: pd.Generator = simulator.generator
        self.mobility: pd.Mobility = simulator.mobility

        self.peers_number = simulator.params.peers_number
        self.hotspots_radius = simulator.params.hotspots_radius

        self.hotspots: Sequence[pd.Hotspot] = self._init_hotspots()
        self.peers: Sequence[pd.Peer] = self._init_peers()

    def _init_hotspots(self) -> Sequence[pd.Hotspot]:
        hotspots: MutableSequence[pd.Hotspot] = []

        hotspots_positions: Sequence[pd.Vector] = self.generator.hotspots
        for position in hotspots_positions:
            hotspots.append(pd.Hotspot(
                position=position,
                radius=self.hotspots_radius))

        return hotspots

    def _init_peers(self) -> Sequence[pd.Peer]:
        peers: MutableSequence[pd.Peer] = []

        positions: Sequence[pd.Vector] = self.generator.peers()
        oss: Sequence[pd.OS] = self.generator.oss()

        for i in range(self.peers_number):
            peer = pd.Peer(
                positions[i],
                oss[i],
                self.simulator
            )
            peer.update_hotspot(self)
            peers.append(peer)

        return peers
