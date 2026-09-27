from dataclasses import dataclass, replace
from enum import Enum


class Heading(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"


_TURN_LEFT = {
    Heading.N: Heading.W,
    Heading.W: Heading.S,
    Heading.S: Heading.E,
    Heading.E: Heading.N,
}


@dataclass(frozen=True)  # immutable per F1 decision
class Rover:
    x: int
    y: int
    heading: Heading

    def report(self):
        return f"{self.x} {self.y} {self.heading.value}"

    def turn_left(self):
        return replace(self, heading=_TURN_LEFT[self.heading])
