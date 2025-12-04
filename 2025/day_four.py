import structlog

from utils import read_file

logger = structlog.get_logger()


def is_accessible_roll(i: int, j: int, lines: list[str]) -> bool:
    if lines[i][j] == ".":
        return False

    around_rolls = 0
    for k in [i - 1, i, i + 1]:
        if k < 0 or k > len(lines) - 1:
            continue
        for l in [j - 1, j, j + 1]:
            if l < 0 or l > len(lines[k]) - 1:
                continue
            if k == i and l == j:
                continue

            if lines[k][l] == "@":
                around_rolls += 1
    return around_rolls < 4


def count_all_accessible_rolls(lines: list[str]) -> int:
    result = 0
    accessibles = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if is_accessible_roll(i, j, lines):
                result += 1
                accessibles.append([i, j])
    return result, accessibles


def solve_one(lines):
    return count_all_accessible_rolls(lines)[0]


def solve_two(lines):
    result = 0
    while count_all_accessible_rolls(lines)[0] > 0:
        count_accessibles, accessibles = count_all_accessible_rolls(lines)
        result += count_accessibles
        for accessible in accessibles:
            lines[accessible[0]][accessible[1]] = "."
    return result


def main():
    lines = read_file("input_4.txt")
    lines = [line.strip() for line in lines]
    lines = [[element for element in line] for line in lines]

    part_one = solve_one(lines)
    logger.info("Part one", result=part_one)

    part_two = solve_two(lines)
    logger.info("Part two", result=part_two)


if __name__ == "__main__":
    main()
