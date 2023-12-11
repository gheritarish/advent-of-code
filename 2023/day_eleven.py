import structlog
import uuid

from day_three import Position
from utils import read_file

logger = structlog.get_logger()


class Galaxy:
    def __init__(self, position: Position):
        self.id = uuid.uuid4()
        self.position = position

    def get_distance(
        self,
        other_galaxy,
        rows: list[int] | None = None,
        columns: list[int] | None = None,
    ) -> int:
        if not rows and not columns:
            return abs(self.position.x - other_galaxy.position.x) + abs(
                self.position.y - other_galaxy.position.y
            )
        else:
            if self.id == other_galaxy.id:
                return 0
            distance = abs(self.position.x - other_galaxy.position.x) + abs(
                self.position.y - other_galaxy.position.y
            )
            encountered = 0
            for row in rows:
                if (
                    min(self.position.y, other_galaxy.position.y)
                    <= row
                    <= max(self.position.y, other_galaxy.position.y)
                ):
                    # logger.info(
                    # "add_y",
                    # y=self.position.y,
                    # other_y=other_galaxy.position.y,
                    # row=row,
                    # )
                    encountered += 1
            for column in columns:
                if (
                    min(self.position.x, other_galaxy.position.x)
                    <= column
                    <= max(self.position.x, other_galaxy.position.x)
                ):
                    # logger.info(
                    # "add_x",
                    # x=self.position.x,
                    # other_x=other_galaxy.position.x,
                    # column=column,
                    # )
                    encountered += 1

            # logger.info(
            # "encountered",
            # encountered=encountered,
            # distance=distance,
            # new_distance=distance + (encountered * 10),
            # )
            return distance + (encountered * 1_000_000) - encountered


def get_map_from_file(file_name: str) -> list[str]:
    lines = []
    with open(file_name, "r") as file:
        for line in file.readlines():
            if "#" in line:
                lines.append(line.strip())
            else:
                lines.append(line.strip())
                lines.append(line.strip())

    map = ["" for _ in range(len(lines))]
    for k in range(len(lines[0])):
        next = False
        for line in lines:
            if line[k] == "#":
                next = True
                for i in range(len(lines)):
                    map[i] += lines[i][k]
                break
            else:
                continue
        if not next:
            for i in range(len(lines)):
                map[i] += lines[i][k]
                map[i] += lines[i][k]

    return map


def get_galaxies_from_map(map: list[str]) -> list[Galaxy]:
    galaxies = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "#":
                galaxies.append(Galaxy(position=Position(x=j, y=i)))
    return galaxies


def get_distance(
    galaxies: list[Galaxy],
    rows: list[int] | None = None,
    columns: list[int] | None = None,
):
    distances = {}
    for galaxy in galaxies:
        for other_galaxy in galaxies:
            if (galaxy.id, other_galaxy.id) not in distances and (
                other_galaxy.id,
                galaxy.id,
            ) not in distances:
                distances[(galaxy.id, other_galaxy.id)] = galaxy.get_distance(
                    other_galaxy,
                    rows,
                    columns,
                )
    return distances


def get_empty_rows_columns(map: list[str]) -> (list[int], list[int]):
    rows = []
    columns = []
    for k in range(len(map)):
        if "#" not in map[k]:
            rows.append(k)
    for k in range(len(map)):
        next = False
        for line in map:
            if line[k] == "#":
                next = True
                break
        if not next:
            columns.append(k)

    return rows, columns


def main():
    map = get_map_from_file("input_eleven.txt")
    galaxies = get_galaxies_from_map(map)
    first_answer = sum(distance for distance in get_distance(galaxies).values())
    logger.info("first_question", answer=first_answer)

    lines = read_file("input_eleven.txt")
    new_galaxies = get_galaxies_from_map(lines)
    rows, columns = get_empty_rows_columns(lines)
    import ipdb; ipdb.set_trace()  # fmt: skip
    second_answer = sum(
        distance for distance in get_distance(new_galaxies, rows, columns).values()
    )
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
