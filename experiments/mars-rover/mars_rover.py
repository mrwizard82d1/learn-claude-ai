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


# --- F7: grid bounds (halt-and-report) ---
@dataclass(frozen=True)
class Completed:
    rover: Rover


@dataclass(frozen=True)
class Halted:
    rover: Rover
    index: int
    command: str


@dataclass(frozen=True)
class PlacedRover:
    """A Rover known to be on a Grid. Create only via Grid.place (convention; Python can't seal this)."""
    rover: Rover


@dataclass(frozen=True)
class Placed:
    placed: PlacedRover


@dataclass(frozen=True)
class OffGrid:
    rover: Rover
    half_extent: int


@dataclass(frozen=True)
class Grid:
    half_extent: int

    def place(self, rover):
        if not self._in_bounds(rover):
            return OffGrid(rover, self.half_extent)
        return Placed(PlacedRover(rover))

    def _in_bounds(self, rover):
        return abs(rover.x) <= self.half_extent and abs(rover.y) <= self.half_extent

    def execute(self, rover, commands):
        # One command at a time; the first step that would leave the grid halts the batch,
        # reporting the last good rover, the command's index, and the command itself.
        current = rover
        for index, command in enumerate(commands):
            stepped = current.execute(command)
            if not self._in_bounds(stepped):
                return Halted(current, index, command)
            current = stepped
        return Completed(current)
