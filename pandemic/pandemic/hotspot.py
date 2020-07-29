import pandemic as pd

id = pd.Id()


class Hotspot:
    def __init__(self, position: pd.Vector, radius: float):
        self.id = id()
        self.position: pd.Vector = position
        self.radius: float = radius
