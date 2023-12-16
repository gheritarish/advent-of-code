import sys
from uuid import uuid4

import structlog

from day_three import Position
from utils import read_file

logger = structlog.get_logger()

sys.setrecursionlimit(1_000_000)


DIRECTIONS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}

MIRROR_DIRECTIONS = {
    "/": {
        "S": ["W"],
        "W": ["S"],
        "N": ["E"],
        "E": ["N"],
    },
    "\\": {
        "N": ["W"],
        "W": ["N"],
        "S": ["E"],
        "E": ["S"],
    },
    "|": {
        "N": ["N"],
        "S": ["S"],
        "E": ["N", "S"],
        "W": ["N", "S"],
    },
    "-": {
        "E": ["E"],
        "W": ["W"],
        "S": ["E", "W"],
        "N": ["E", "W"],
    },
}


class Mirror:
    def __init__(self, shape: str, position: Position, exits: set):
        self.id = uuid4()
        self.shape = shape
        self.position = position
        self.exits = exits


def parse_mirrors(lines: list[str]) -> dict[tuple[int, int], Mirror]:
    mirrors = {}
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] in ["/", "\\", "|", "-"]:
                mirrors[(j, i)] = Mirror(
                    shape=lines[i][j],
                    position=Position(x=j, y=i),
                    exits=set(),
                )
    return mirrors


def get_empty_grid(lines: list[str]) -> list[str]:
    grid = []
    for line in lines:
        grid.append(["." for _ in range(len(line.strip()))])
    return grid


def get_path_from_place(
    mirrors,
    full_grid,
    next_coordinates,
    direction,
    restart: bool = False,
):
    if restart:
        for mirror in mirrors.values():
            mirror.exits = set()
    while (
        0 <= next_coordinates.y <= len(full_grid) - 1
        and 0 <= next_coordinates.x <= len(full_grid[0]) - 1
    ):
        if (next_coordinates.x, next_coordinates.y) not in mirrors:
            full_grid[next_coordinates.y][next_coordinates.x] = "#"
            next_coordinates = Position(
                x=next_coordinates.x + DIRECTIONS[direction][0],
                y=next_coordinates.y + DIRECTIONS[direction][1],
            )
            return get_path_from_place(mirrors, full_grid, next_coordinates, direction)
        else:
            full_grid[next_coordinates.y][next_coordinates.x] = "#"
            mirror = mirrors[(next_coordinates.x, next_coordinates.y)]
            directions = MIRROR_DIRECTIONS[mirror.shape][direction]
            for direction in directions:
                next_coordinates = Position(
                    x=next_coordinates.x + DIRECTIONS[direction][0],
                    y=next_coordinates.y + DIRECTIONS[direction][1],
                )
                if (next_coordinates.x, next_coordinates.y) in mirror.exits:
                    continue
                else:
                    mirror.exits.add((next_coordinates.x, next_coordinates.y))
                    full_grid = get_path_from_place(
                        mirrors,
                        full_grid,
                        next_coordinates,
                        direction,
                    )
            return full_grid

    return full_grid


def get_first_answer(full_grid):
    answer = 0
    for line in full_grid:
        answer += line.count("#")
    return answer


def get_second_answer(lines, mirrors):
    max_top = max(
        [
            get_first_answer(
                get_path_from_place(
                    mirrors,
                    get_empty_grid(lines),
                    Position(y=0, x=i),
                    direction="S",
                    restart=True,
                ),
            )
            for i in range(len(lines[0]))
        ],
    )

    max_bot = max(
        [
            get_first_answer(
                get_path_from_place(
                    mirrors,
                    get_empty_grid(lines),
                    Position(y=len(lines) - 1, x=i),
                    direction="N",
                    restart=True,
                ),
            )
            for i in range(len(lines[0]))
        ],
    )

    max_left = max(
        [
            get_first_answer(
                get_path_from_place(
                    mirrors,
                    get_empty_grid(lines),
                    Position(y=i, x=0),
                    direction="E",
                    restart=True,
                ),
            )
            for i in range(len(lines))
        ],
    )

    max_right = max(
        [
            get_first_answer(
                get_path_from_place(
                    mirrors,
                    get_empty_grid(lines),
                    Position(y=i, x=len(lines[0]) - 1),
                    direction="W",
                    restart=True,
                ),
            )
            for i in range(len(lines))
        ],
    )

    return max([max_right, max_bot, max_top, max_left])


def main():
    lines = read_file("input_16.txt")
    mirrors = parse_mirrors(lines)
    empty_grid = get_empty_grid(lines)
    full_grid = get_path_from_place(
        mirrors,
        empty_grid,
        next_coordinates=Position(x=0, y=0),
        direction="E",
    )
    first_answer = get_first_answer(full_grid)
    logger.info("first_question", answer=first_answer)

    part_two = get_second_answer(lines, mirrors)
    logger.info("second_question", answer=part_two)


if __name__ == "__main__":
    main()
