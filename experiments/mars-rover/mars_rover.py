from dataclasses import dataclass
from enum import Enum


class Heading(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"


@dataclass(frozen=True)  # immutable per F1 decision
class Rover:
    x: int
    y: int
    heading: Heading

    def report(self):
        return f"{self.x} {self.y} {self.heading.value}"
