import structlog

from utils import read_file

logger = structlog.get_logger()


def find(lines, line_number, column_number, direction):
    if direction == "south":
        if (
            lines[line_number][column_number] == "X"
            and lines[line_number + 1][column_number] == "M"
            and lines[line_number + 2][column_number] == "A"
            and lines[line_number + 3][column_number] == "S"
        ):
            return 1
    elif direction == "north":
        if (
            lines[line_number][column_number] == "X"
            and lines[line_number - 1][column_number] == "M"
            and lines[line_number - 2][column_number] == "A"
            and lines[line_number - 3][column_number] == "S"
        ):
            return 1
    elif direction == "east":
        if (
            lines[line_number][column_number] == "X"
            and lines[line_number][column_number + 1] == "M"
            and lines[line_number][column_number + 2] == "A"
            and lines[line_number][column_number + 3] == "S"
        ):
            return 1
    elif direction == "west":
        if (
            lines[line_number][column_number] == "X"
            and lines[line_number][column_number - 1] == "M"
            and lines[line_number][column_number - 2] == "A"
            and lines[line_number][column_number - 3] == "S"
        ):
            return 1
    elif direction == "nw":
        if (
            lines[line_number][column_number] == "X"
            and lines[line_number - 1][column_number - 1] == "M"
            and lines[line_number - 2][column_number - 2] == "A"
            and lines[line_number - 3][column_number - 3] == "S"
        ):
            return 1
    elif direction == "ne":
        if (
            lines[line_number][column_number] == "X"
            and lines[line_number - 1][column_number + 1] == "M"
            and lines[line_number - 2][column_number + 2] == "A"
            and lines[line_number - 3][column_number + 3] == "S"
        ):
            return 1
    elif direction == "sw":
        if (
            lines[line_number][column_number] == "X"
            and lines[line_number + 1][column_number - 1] == "M"
            and lines[line_number + 2][column_number - 2] == "A"
            and lines[line_number + 3][column_number - 3] == "S"
        ):
            return 1
    elif direction == "se":
        if (
            lines[line_number][column_number] == "X"
            and lines[line_number + 1][column_number + 1] == "M"
            and lines[line_number + 2][column_number + 2] == "A"
            and lines[line_number + 3][column_number + 3] == "S"
        ):
            return 1
    return 0


def find_x_mas(lines, line_number, column_number):
    if (
        (
            lines[line_number - 1][column_number - 1] == lines[line_number + 1][column_number - 1] == "M"
            and lines[line_number - 1][column_number + 1] == lines[line_number + 1][column_number + 1] == "S"
        )
        or (
            lines[line_number - 1][column_number + 1] == lines[line_number + 1][column_number + 1] == "M"
            and lines[line_number - 1][column_number - 1] == lines[line_number + 1][column_number - 1] == "S"
        )
        or (
            lines[line_number - 1][column_number - 1] == lines[line_number - 1][column_number + 1] == "M"
            and lines[line_number + 1][column_number - 1] == lines[line_number + 1][column_number + 1] == "S"
        )
        or (
            lines[line_number + 1][column_number - 1] == lines[line_number + 1][column_number + 1] == "M"
            and lines[line_number - 1][column_number - 1] == lines[line_number - 1][column_number + 1] == "S"
        )
    ):
        return 1
    return 0


def solve_first(lines: list[list[str]]) -> int:
    xmas_found = 0
    line_count = len(lines)
    for line_number, line in enumerate(lines):
        column_count = len(line)
        for column_number, character in enumerate(line):
            if character == "X":
                if column_number < column_count - 3:
                    xmas_found += find(lines, line_number, column_number, "east")
                if column_number >= 3:
                    xmas_found += find(lines, line_number, column_number, "west")
                if line_number < line_count - 3:
                    xmas_found += find(lines, line_number, column_number, "south")
                if line_number >= 3:
                    xmas_found += find(lines, line_number, column_number, "north")
                if line_number >= 3 and column_number >= 3:
                    xmas_found += find(lines, line_number, column_number, "nw")
                if line_number >= 3 and column_number < column_count - 3:
                    xmas_found += find(lines, line_number, column_number, "ne")
                if line_number < line_count - 3 and column_count >= 3:
                    xmas_found += find(lines, line_number, column_number, "sw")
                if line_number < line_count - 3 and column_number < column_count - 3:
                    xmas_found += find(lines, line_number, column_number, "se")
    return xmas_found


def solve_second(lines: list[list[str]]) -> int:
    x_mas_found = 0
    line_count = len(lines)
    for line_number, line in enumerate(lines):
        column_count = len(line)
        for column_number, character in enumerate(line):
            if character == "A":
                if column_number < 1 or column_number > column_count - 2 or line_number < 1 or line_number > line_count - 2:
                    continue
                else:
                    x_mas_found += find_x_mas(lines, line_number, column_number)
    return x_mas_found



def main():
    lines = read_file("input_4.txt")
    first = solve_first(lines)
    logger.info("First part", first=first)

    second = solve_second(lines)
    logger.info("Second part", second=second)


if __name__ == "__main__":
    main()
