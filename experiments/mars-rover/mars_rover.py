from dataclasses import dataclass, replace
from enum import Enum


class Heading(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"


# Headings in clockwise order; turning is a step of +1 (right) or -1 (left), mod 4.
_CLOCKWISE = (Heading.N, Heading.E, Heading.S, Heading.W)

# One forward cell per heading (the N=+y / E=+x coordinate convention).
_MOVE = {
    Heading.N: (0, 1),
    Heading.E: (1, 0),
    Heading.S: (0, -1),
    Heading.W: (-1, 0),
}


@dataclass(frozen=True)  # immutable per F1 decision
class Rover:
    x: int
    y: int
    heading: Heading

    def report(self):
        return f"{self.x} {self.y} {self.heading.value}"

    def _rotate(self, step):
        i = _CLOCKWISE.index(self.heading)
        return replace(self, heading=_CLOCKWISE[(i + step) % 4])

    def turn_left(self):
        return self._rotate(-1)

    def turn_right(self):
        return self._rotate(+1)

    def move_forward(self):
        dx, dy = _MOVE[self.heading]
        return replace(self, x=self.x + dx, y=self.y + dy)

    def execute(self, commands):
        # A fold over the command string: the rover is the accumulator, threaded
        # through one command at a time. (Unknown chars are silently skipped for now;
        # raise-vs-ignore is the deferred F9 decision.)
        rover = self
        for command in commands:
            if command == "l":
                rover = rover.turn_left()
            elif command == "r":
                rover = rover.turn_right()
            elif command == "m":
                rover = rover.move_forward()
        return rover
