import structlog

from utils import read_file

logger = structlog.get_logger()


def get_levels(lines: list[str]) -> list[list[int]]:
    str_levels = [line.split(" ") for line in lines]
    levels = []
    for str_level in str_levels:
        levels.append([int(value) for value in str_level])
    return levels


def is_valid(level: list[int]) -> bool:
    previous = level[0] - level[1]
    if abs(previous) == 0 or abs(previous) > 3:
        return False
    for i in range(1, len(level) - 1):
        next_value = level[i] - level[i + 1]
        if next_value * previous <= 0:
            return False
        if abs(next_value) == 0 or abs(next_value) > 3:
            return False
        previous = next_value

    return True


def is_valid_tolerance(level: list[int]) -> bool:
    if is_valid(level):
        return True

    for i in range(len(level)):
        if is_valid([level[j] for j in range(len(level)) if j != i]):
            return True

    return False


def solve_first(levels: list[list[int]]) -> tuple[int, list]:
    counter = 0
    indexes = []
    for index, level in enumerate(levels):
        if is_valid(level):
            counter += 1
            indexes.append(index)
    return counter, indexes


def solve_second(levels: list[list[int]]) -> tuple[int, list]:
    counter = 0
    indexes = []
    for index, level in enumerate(levels):
        if is_valid_tolerance(level):
            counter += 1
            indexes.append(index)
    return counter, indexes


def main():
    lines = read_file("input_2.txt")
    levels = get_levels(lines)
    first, _ = solve_first(levels)
    logger.info("First part", first=first)

    second, _ = solve_second(levels)
    logger.info("Second part", second=second)


if __name__ == "__main__":
    main()
