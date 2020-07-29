import pandemic as pd
from typing import Tuple
from enum import Enum, auto


class MobilityState(Enum):
    HALTED = auto()
    TRAVELING = auto()
    EXPLORING = auto()


class Mobility:
    def __init__(self, params: pd.Parameters, generator: pd.Generator):
        self.HtoH = params.HtoH
        self.HtoT = params.HtoT
        self.HtoE = params.HtoE
        self.TtoH = params.TtoH
        self.TtoT = params.TtoT
        self.TtoE = params.TtoE
        self.EtoH = params.EtoH
        self.EtoT = params.EtoT
        self.EtoE1 = params.EtoE1
        self.EtoE2 = params.EtoE2

        self.generator = generator

    def __call__(self, state: MobilityState) -> Tuple[MobilityState, bool]:
        probability: float = self.generator.uniform_mobility

        if state == MobilityState.HALTED:
            if probability < self.HtoT:
                return MobilityState.TRAVELING, True
            probability -= self.HtoT

            if probability < self.HtoE:
                return MobilityState.EXPLORING, True

            return MobilityState.HALTED, False

        elif state == MobilityState.TRAVELING:
            if probability < self.TtoT:
                return MobilityState.TRAVELING, False
            probability -= self.TtoT

            if probability < self.TtoE:
                return MobilityState.EXPLORING, True

            return MobilityState.HALTED, True

        else:
            if probability < self.EtoT:
                return MobilityState.TRAVELING, True
            probability -= self.EtoT

            if probability < self.EtoE1:
                return MobilityState.EXPLORING, False
            probability -= self.EtoE1

            if probability < self.EtoE2:
                return MobilityState.EXPLORING, True

            return MobilityState.HALTED, True
