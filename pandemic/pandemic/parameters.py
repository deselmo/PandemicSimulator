from __future__ import annotations
import pandemic as pd
from typing import NamedTuple, Optional, Sequence
import numpy as np
import json
import os


class Parameters(NamedTuple):
    peers_number: int
    hotspots_number: int

    initial_infected_number: int
    patching_begin_epoch: Optional[int]

    map_size: pd.Vector
    in_hotspots_probability: float

    infection_probability: float
    patch_probability: float

    epoch_limit: Optional[int]

    peer_radius: float
    hotspots_radius: float

    oss: Sequence[pd.OSp]

    HtoH: float
    HtoT: float
    HtoE: float

    TtoH: float
    TtoT: float
    TtoE: float

    EtoH: float
    EtoT: float
    EtoE1: float
    EtoE2: float

    exploringSpeedMax: float
    travelingSpeedMax: float
    acceleration: float

    output_directory: Optional[str] = None

    seed: Optional[int] = None

    zipf_alpha: float = 1.5
    zipf_range: int = 30

    width: int = 720
    ms: int = 16

    def error(self) -> bool:
        if not isinstance(self.peers_number, int):
            print("parameter error: not peers_number instance of int")
            return True

        if not self.peers_number > 0:
            print("parameter error: not peers_number > 0")
            return True

        if not isinstance(self.hotspots_number, int):
            print("parameter error: not hotspots_number instance of int")
            return True

        if not self.hotspots_number >= 0:
            print("parameter error: not hotspots_number >= 0")
            return True

        if not isinstance(self.initial_infected_number, int):
            print("parameter error: not initial_infected_number instance of int")
            return True

        if not 0 <= self.initial_infected_number <= self.peers_number:
            print("parameter error: not 0 < initial_infected_number <= peers_number")
            return True

        if self.patching_begin_epoch is not None:
            if not isinstance(self.patching_begin_epoch, int):
                print("parameter error: not patching_begin_epoch instance of int")
                return True

            if not self.patching_begin_epoch >= 0:
                print("parameter error: not patching_begin_epoch >= 0")
                return True

        if not isinstance(self.map_size, pd.Vector):
            print("parameter error: not map_size instance of pd.Vector")
            return True

        if not self.map_size.x > 0 or not self.map_size.y > 0:
            print("parameter error: not map_size.x > 0 or not map_size.y > 0")
            return True

        if not isinstance(self.in_hotspots_probability, (int, float)):
            print("parameter error: not in_hotspots_probability instance of float")
            return True

        if not 0 <= self.in_hotspots_probability <= 1:
            print("parameter error: not 0 < in_hotspots_probability < 1")
            return True

        if self.hotspots_number == 0 and not self.in_hotspots_probability == 0:
            print("parameter error: hotspots_number == 0 and not in_hotspots_probability == 0")
            return True

        if not isinstance(self.infection_probability, (int, float)):
            print("parameter error: not infection_probability instance of float")
            return True

        if not 0 <= self.infection_probability <= 1:
            print("parameter error: not 0 < infection_probability < 1")
            return True

        if not isinstance(self.patch_probability, (int, float)):
            print("parameter error: not patch_probability instance of float")
            return True

        if not 0 <= self.patch_probability <= 1:
            print("parameter error: not 0 < patch_probability < 1")
            return True

        if self.epoch_limit is not None:
            if not isinstance(self.epoch_limit, int):
                print("parameter error: not epoch_limit instance of int")
                return True

            if not self.epoch_limit >= 0:
                print("parameter error: not epoch_limit >= 0")
                return True

        if not isinstance(self.peer_radius, (int, float)):
            print("parameter error: not peer_radius instance of float")
            return True

        if not self.peer_radius > 0:
            print("parameter error: not peer_radius > 0")
            return True

        if not isinstance(self.hotspots_radius, (int, float)):
            print("parameter error: not hotspots_radius instance of float")
            return True

        if not self.hotspots_radius > 0:
            print("parameter error: not hotspots_radius > 0")
            return True

        if not isinstance(self.oss, Sequence):
            print("parameter error: not oss instance of list")
            return True

        for osp in self.oss:
            if not isinstance(osp, pd.OSp):
                print("parameter error: not oss instance of list of pd.OSp")

        if not len(set(map(lambda osp: osp.name, self.oss))) == len(self.oss):
            print("parameter error: not OSs all different")
            return True

        if not np.isclose(sum(map(lambda osp: osp.prop, self.oss)), 1):
            print("parameter error: not sum of OSs distributions == 1")
            return True

        if not isinstance(self.HtoH, (int, float)):
            print("parameter error: not HtoH instance of float")
            return True

        if not isinstance(self.HtoT, (int, float)):
            print("parameter error: not HtoT instance of float")
            return True

        if not isinstance(self.HtoE, (int, float)):
            print("parameter error: not HtoE instance of float")
            return True

        if not np.isclose(self.HtoH + self.HtoT + self.HtoE, 1):
            print("parameter error: not sum of HtoX == 1")
            return True

        if not isinstance(self.TtoH, (int, float)):
            print("parameter error: not TtoH instance of float")
            return True

        if not isinstance(self.TtoT, (int, float)):
            print("parameter error: not TtoT instance of float")
            return True

        if not isinstance(self.TtoE, (int, float)):
            print("parameter error: not TtoE instance of float")
            return True

        if not np.isclose(self.TtoH + self.TtoT + self.TtoE, 1):
            print("parameter error: not sum of TtoX == 1")
            return True

        if not isinstance(self.EtoH, (int, float)):
            print("parameter error: not EtoH instance of float")
            return True

        if not isinstance(self.EtoT, (int, float)):
            print("parameter error: not EtoT instance of float")
            return True

        if not isinstance(self.EtoE1, (int, float)):
            print("parameter error: not EtoE1 instance of float")
            return True

        if not isinstance(self.EtoE2, (int, float)):
            print("parameter error: not EtoE2 instance of float")
            return True

        if not np.isclose(self.EtoH + self.EtoT + self.EtoE1 + self.EtoE2, 1):
            print("parameter error: not sum of EtoX == 1")
            return True

        if not isinstance(self.exploringSpeedMax, (int, float)):
            print("parameter error: not exploringSpeedMax instance of float")
            return True

        if not self.exploringSpeedMax > 0:
            print("parameter error: not exploringSpeedMax > 0")
            return True

        if not isinstance(self.travelingSpeedMax, (int, float)):
            print("parameter error: not travelingSpeedMax instance of float")
            return True

        if not self.travelingSpeedMax > 0:
            print("parameter error: not travelingSpeedMax > 0")
            return True

        if not isinstance(self.acceleration, (int, float)):
            print("parameter error: not acceleration instance of float")
            return True

        if not self.acceleration > 0:
            print("parameter error: not acceleration > 0")
            return True

        if not isinstance(self.zipf_alpha, (int, float)):
            print("parameter error: not zipf_alpha instance of float")
            return True

        if not self.zipf_alpha > 1:
            print("parameter error: not zipf_alpha > 1")
            return True

        if not isinstance(self.zipf_range, int):
            print("parameter error: not zipf_range instance of int")
            return True

        if not self.zipf_range > 0:
            print("parameter error: not hotspot_radius_number_positions > 0")
            return True

        if self.output_directory is not None:
            if not isinstance(self.output_directory, str):
                print("parameter error: not output_directory instance of str")
                return True

            dir = self.output_directory

            try:
                if not os.path.exists(dir):
                    os.mkdir(dir)
                else:
                    if not os.path.isdir(dir):
                        print("parameter error: not output_directory {} is a directory".format(dir))
                        return True

                    if not os.access(dir, os.W_OK):
                        print("parameter error: not output_directory {} is writable".format(dir))

            except Exception as error:
                print("parameter error: not valid output directory {}".format(dir))
                print(error)
                return True

        if self.seed is not None:
            if not isinstance(self.seed, int):
                print("parameter error: not seed instance of int")
                return True
            
            if not self.seed >= 0:
                print("parameter error: not seed >= 0")
                return True

        if not isinstance(self.width, int):
            print("parameter error: not width instance of int")
            return True

        if not self.width >= 100:
            print("parameter error: not width > 100")
            return True

        if not isinstance(self.ms, int):
            print("parameter error: not ms instance of int")
            return True

        if not self.ms > 0:
            print("parameter error: not ms > 0")
            return True

        return False


    @staticmethod
    def from_json(path: str) -> Optional[Parameters]:
        try:
            with open(path, 'r') as f:
                d = json.load(f)
        except Exception as error:
            print("invalid parameters json file")
            print(error)
            return None

        try:
            d["map_size"] = pd.Vector(**d["map_size"])
        except TypeError as error:
            print("parameter error: invalid map_size")
            print(error)
            return None

        try:
            d["oss"] = list(map(lambda osp: pd.OSp(**osp), d["oss"]))
        except TypeError as error:
            print("parameter error: invalid oss")
            print(error)
            return None

        try:
            params = Parameters(**d)
        except TypeError as error:
            miss = error.args[0].split(" ")[-1]
            print("parameter error: mandatory {} parameter not found".format(miss))
            print(error)
            return None

        if params.error():
            return None

        return params
