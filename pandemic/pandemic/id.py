class Id:
    def __init__(self):
        self.value: int = 0

    def __call__(self) -> int:
        value = self.value
        self.value += 1
        return value
