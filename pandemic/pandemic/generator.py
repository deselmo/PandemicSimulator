import pandemic as pd
from typing import Sequence, MutableSequence, List
import numpy as np


class Generator:
    def __init__(self, params: pd.Parameters):
        np.random.seed(params.seed)

        self.params: pd.Parameters = params
        self._hotspot_pos_start = pd.Vector(1, 1) * self.params.hotspots_radius
        self._hotspot_pos_mult = pd.Vector(
            self.params.map_size.x-2*self.params.hotspots_radius,
            self.params.map_size.y-2*self.params.hotspots_radius
        )

        self.distributon_size = self.params.peers_number * self.params.epoch_limit
        self._uniform_mobility: MutableSequence[float] = []
        self._uniform_in_hotspot: MutableSequence[float] = []
        self._uniform_infection: MutableSequence[float] = []
        self._uniform_patch: MutableSequence[float] = []
        self._uniform_map: MutableSequence[pd.Vector] = []
        self._uniform_hotspot_choice: MutableSequence[int] = []
        self._uniform_hotspot_rads: MutableSequence[float] = []
        self._zipf_hotspot_radius: MutableSequence[float] = []

        self.hotspots: MutableSequence[pd.Vector] = []
        self._hotspots()


    @property
    def uniform_mobility(self) -> float:
        if not len(self._uniform_mobility):
            self._uniform_mobility = list(np.random.uniform(0, 1, self.distributon_size))

        return self._uniform_mobility.pop()

    @property
    def uniform_in_hotspot(self) -> float:
        if not len(self._uniform_in_hotspot):
            self._uniform_in_hotspot = list(np.random.uniform(0, 1, self.distributon_size))

        return self._uniform_in_hotspot.pop()

    @property
    def uniform_patch(self) -> float:
        if not len(self._uniform_patch):
            self._uniform_patch = list(np.random.uniform(0, 1, self.distributon_size))

        return self._uniform_patch.pop()

    @property
    def uniform_infection(self) -> float:
        if not len(self._uniform_infection):
            self._uniform_infection = list(np.random.uniform(0, 1, self.distributon_size))

        return self._uniform_infection.pop()

    @property
    def uniform_map(self) -> pd.Vector:
        if not len(self._uniform_map):
            xs = np.random.uniform(0, 1, int(self.distributon_size * 1.2))
            ys = np.random.uniform(0, 1, int(self.distributon_size * 1.2))
            self._uniform_map = [pd.Vector(x, y) for x, y in zip(xs, ys)]

        return self._uniform_map.pop()

    @property
    def uniform_hotspot_choice(self) -> int:
        if not len(self._uniform_hotspot_choice):
            self._uniform_hotspot_choice = list(map(
                lambda x: int(x),
                np.random.uniform(0, len(self.hotspots), self.distributon_size)
            ))

        return self._uniform_hotspot_choice.pop()

    @property
    def uniform_hotspot_rads(self) -> float:
        if not len(self._uniform_hotspot_rads):
            self._uniform_hotspot_rads = list(np.random.uniform(0, 2*np.pi, self.distributon_size))

        return self._uniform_hotspot_rads.pop()

    @property
    def zipf_hotspot_radius(self) -> float:
        if not len(self._zipf_hotspot_radius):
            self._zipf_hotspot_radius = list(np.random.zipf(self.params.zipf_alpha, self.distributon_size))

        return self._zipf_hotspot_radius.pop()

    def choice(self, peers: Sequence["pd.Peer"], size) -> Sequence["pd.Peer"]:
        return list(np.random.choice(peers, size, replace=False))

    def permute(self, peers: Sequence["pd.Peer"]) -> Sequence["pd.Peer"]:
        return np.random.permutation(peers)

    def _hotspots(self) -> None:
        while len(self.hotspots) < self.params.hotspots_number:
            self.hotspots.append(self.hotspot())

    def hotspot(self) -> pd.Vector:
        position: pd.Vector = pd.Vector()

        for _ in range(1000):
            position = self._hotspot_pos_start + pd.Vector(
                self.uniform_map.x * self._hotspot_pos_mult.x,
                self.uniform_map.y * self._hotspot_pos_mult.y
            )

            found: bool = False
            for hotspot_position in self.hotspots:
                if abs(position - hotspot_position) < 2 * self.params.hotspots_radius:
                    found = True
                    break
            if not found:
                return position

        raise RuntimeError("Too many attempts to create unjoined hotspots")

    def peers(self) -> Sequence[pd.Vector]:
        positions: MutableSequence[pd.Vector] = []

        for _ in range(self.params.peers_number):
            positions.append(self.peer())

        return np.random.permutation(positions)

    def peer(self) -> pd.Vector:
        in_hotspot = self.uniform_in_hotspot < self.params.in_hotspots_probability

        return self.in_hotspots() if in_hotspot else self.in_world()

    def in_world(self) -> pd.Vector:
        p: pd.Vector = self.uniform_map

        return pd.Vector(p.x*self.params.map_size.x, p.y*self.params.map_size.y)

    def in_hotspot(self, hotspot_position: pd.Vector) -> pd.Vector:
        direction = pd.Vector.rad(self.uniform_hotspot_rads)
        zipf = self.zipf_hotspot_radius
        zipf_range = np.max([1, self.params.zipf_range-1])

        distance = ((zipf if zipf <= self.params.zipf_range else 1) - 1) / zipf_range

        return hotspot_position + (direction * distance * self.params.hotspots_radius)

    def in_hotspots(self) -> pd.Vector:
        return self.in_hotspot(self.hotspots[self.uniform_hotspot_choice])

    def oss(self) -> Sequence[pd.OS]:
        oss: MutableSequence[pd.OS] = []

        ossd: List[pd.OSp] = list(self.params.oss)
        ossd.sort(key=lambda x: x[1], reverse=True)

        for os in ossd:
            os_name: pd.OS = os.name
            os_prop: float = os.prop

            for _ in range(int(os_prop * self.params.peers_number)):
                oss.append(os_name)

        i: int = 0
        while len(oss) < self.params.peers_number:
            oss.append(ossd[i][0])
            i += 1

        return np.random.permutation(oss)
