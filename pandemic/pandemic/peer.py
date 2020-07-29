from __future__ import annotations
import pandemic as pd
from typing import Optional
from enum import Enum, auto
import numpy as np
from pandemic import hotspot

id = pd.Id()


class InfectionState(Enum):
    SUSCEPTIBLE = auto()
    INFECTIOUS = auto()
    PATCHED = auto()


class Peer:
    def __init__(
        self,
        position: pd.Vector,
        os: pd.OS,
        simulator: pd.Simulator
    ) -> None:
        self.id = id()
        self.position: pd.Vector = position
        self.radius: float = simulator.params.peer_radius
        self.os: pd.OS = os

        self.simulator: pd.Simulator = simulator

        self.infection_state: pd.IState = pd.IState.SUSCEPTIBLE
        self.mobility_state: pd.MState = pd.MState.HALTED

        self.to_commit_infection: bool = False

        self.speed: float = 0
        self.destination: Optional[pd.Vector] = None
        self.hotspot: Optional[pd.Hotspot] = None

        self.data_infection: Optional[pd.DataInfection] = None
        self.data_patch: Optional[pd.DataPatch] = None

    def step_mobility(self) -> None:
        self.mobility_state, new_destination = self.simulator.mobility(self.mobility_state)

        if(new_destination):
            self.speed = 0
            self._new_destination()

        self._accelerate()
        self._move()
        self.update_hotspot()

    def step_patch(self) -> bool:
        if(
            self.simulator.params.patching_begin_epoch is None or
            self.simulator.epoch < self.simulator.params.patching_begin_epoch
        ):
            return False

        if self.infection_state == pd.IState.PATCHED:
            return True

        if self.simulator.generator.uniform_patch < self.simulator.params.patch_probability:
            self.patch()
            return True

        return False

    def step_infection(self) -> None:
        if self.infection_state != pd.IState.INFECTIOUS:
            return

        for peer in list(self.simulator.susceptible_peers.values()):
            if(
                self.os == peer.os and
                not peer.to_commit_infection and
                abs(self.position - peer.position) < self.radius and
                self.simulator.generator.uniform_infection < self.simulator.params.infection_probability
            ):
                peer.infect(self)

    def commit_infection(self) -> None:
        if self.to_commit_infection:
            del self.simulator.new_infected_peers[self.id]
            self.simulator.infected_peers[self.id] = self

            self.infection_state = pd.IState.INFECTIOUS
            self.to_commit_infection = False

    def patch(self) -> None:
        if self.infection_state == pd.IState.PATCHED:
            return

        elif self.infection_state == pd.IState.SUSCEPTIBLE:
            del self.simulator.susceptible_peers[self.id]
        elif self.infection_state == pd.IState.INFECTIOUS:
            del self.simulator.infected_peers[self.id]

        self.simulator.patched_peers[self.id] = self
        self.infection_state = pd.IState.PATCHED

        self.data_patch = pd.DataPatch(self.simulator.epoch, self)

    def infect(self, source: Optional[Peer]) -> None:
        del self.simulator.susceptible_peers[self.id]

        self.simulator.new_infected_peers[self.id] = self
        self.to_commit_infection = True

        if source is not None:
            self.data_infection = pd.DataInfection(self.simulator.epoch, source, self)

    def _new_destination(self):
        if self.mobility_state == pd.MState.TRAVELING:
            self.destination = self.simulator.generator.peer()

        elif self.mobility_state == pd.MState.EXPLORING:
            if self.hotspot is None:
                self.destination = self.simulator.generator.peer()
            else:
                self.destination = self.simulator.generator.in_hotspot(self.hotspot.position)

        elif self.mobility_state == pd.MState.HALTED:
            self.destination = None

    def _accelerate(self):
        if self.mobility_state == pd.MState.HALTED:
            self.speed = 0
            return

        self.speed += self.simulator.params.acceleration

        if self.simulator.mobility == pd.MState.EXPLORING:
            self.speed = min(self.speed, self.simulator.params.exploringSpeedMax)
        elif self.simulator.mobility == pd.MState.TRAVELING:
            self.speed = min(self.speed, self.simulator.params.travelingSpeedMax)

    def _move(self):
        if self.destination is None:
            return

        if self.destination == self.position:
            self._destination_reached()
            return

        direction = +(self.destination - self.position)
        new_position = self.position + direction * self.speed

        if self.destination == new_position:
            self.position = self.destination
            self._destination_reached()
            return

        new_direction = +(self.destination - new_position)

        if np.isclose(abs(direction-new_direction), 0):
            self.position = new_position
        else:
            self.position = self.destination
            self._destination_reached()

    def update_hotspot(self, map: Optional[pd.Map] = None):
        map = self.simulator.map if map is None else map
        for hotspot in map.hotspots:
            if abs(hotspot.position - self.position) < hotspot.radius:
                self.hotspot = hotspot
                return
        self.hotspot = None

    def _destination_reached(self):
        self.mobility_state = pd.MState.HALTED
        self.destination = None
        self.speed = 0
