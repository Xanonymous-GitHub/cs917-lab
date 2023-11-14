from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Final

EXPECTED_MAZE_NEIGHBOUR_DIRECTIONS: Final[tuple[tuple[int, int], ...]] = (
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
    (-1, 0),  # up
)


@unique
class MazeBlockType(Enum):
    EMPTY = 1
    WALL = 0


@dataclass(frozen=False)
class MazeBlock:
    x: int
    y: int
    category: MazeBlockType

    # The distance from another block (maybe the start point when finding route) to this block.
    distance: int = 0

    # The last visited block when finding route.
    last_visited_block: MazeBlock = None

    def __eq__(self, other):
        if isinstance(other, MazeBlock):
            return self.x == other.x and self.y == other.y
        return False
