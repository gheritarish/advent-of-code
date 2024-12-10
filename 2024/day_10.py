import structlog

from utils import read_file

logger = structlog.get_logger()


DIRECTIONS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}


def find_trailheads(lines, line_number, column_number, value):
    trailheads = []
    line_count = len(lines)
    column_count = len(lines[0])
    for direction in DIRECTIONS.values():
        line = line_number + direction[0]
        column = column_number + direction[1]
        if (
            0 <= line < line_count
            and 0 <= column < column_count
            and int(lines[line][column]) - value == 1
        ):
            if int(lines[line][column]) == 9:
                trailheads.extend([(line, column)])
            trailheads.extend(find_trailheads(
                lines, line, column, int(lines[line][column])
            ))
    return trailheads


def solve_first(lines):
    trailheads = {}
    for line_number, line in enumerate(lines):
        for column_number, char in enumerate(line):
            if int(char) == 0:
                trailheads[(line_number, column_number)] = find_trailheads(
                    lines, line_number, column_number, int(char)
                )
    trailhead_count = 0
    for trailhead in trailheads.values():
        trailhead_count += len(set(trailhead))
    return trailhead_count

def solve_second(lines):
    trailheads = {}
    for line_number, line in enumerate(lines):
        for column_number, char in enumerate(line):
            if int(char) == 0:
                trailheads[(line_number, column_number)] = find_trailheads(
                    lines, line_number, column_number, int(char)
                )
    trailhead_count = 0
    for trailhead in trailheads.values():
        trailhead_count += len(trailhead)
    return trailhead_count


def main():
    lines = read_file("input_10.txt")
    lines = [line.strip() for line in lines]
    first = solve_first(lines)
    logger.info("First part", first=first)

    second = solve_second(lines)
    logger.info("Second part", second=second)


if __name__ == "__main__":
    main()
