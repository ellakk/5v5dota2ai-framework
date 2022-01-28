from typing import Iterator


class Position():
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self) -> Iterator[float]:
        return iter((self.x, self.y, self.z))
