import pandemic as pd
from typing import NamedTuple, Optional


class DataInfection:
    def __init__(self, epoch: int, source: pd.Peer, target: pd.Peer):
        self.epoch: int = epoch
        self.source: int = source.id
        self.target: int = target.id
        self.position: pd.Vector = target.position
        self.hotspot: Optional[int] = None if target.hotspot is None else target.hotspot.id


class DataPatch:
    def __init__(self, epoch: int, target: pd.Peer):
        self.epoch: int = epoch
        self.target: int = target.id
        self.position: pd.Vector = target.position
        self.hotspot: Optional[pd.Hotspot] = target.hotspot


class DataEpoch(NamedTuple):
    epoch: int
    n_susceptible: int
    n_infected: int
    n_patched: int
