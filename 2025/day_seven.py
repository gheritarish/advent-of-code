import structlog

from utils import read_file

logger = structlog.get_logger()


def get_splits_and_beams(line: str, beams: list[int]):
    line = line.strip()
    if len(beams) == 0:
        for index, char in enumerate(line):
            if char == "S":
                beams.append(index)
                return 0, beams

    returned_beams = []
    splits = 0
    for beam in beams:
        if line[beam] == "^":
            returned_beams.append(beam - 1)
            returned_beams.append(beam + 1)
            splits += 1
        else:
            returned_beams.append(beam)
    return splits, list(set(returned_beams))


def get_all_splits_and_beams(line: str, beams: dict[int, int]) -> dict[int, int]:
    line = line.strip()
    if len(beams.keys()) == 0:
        for index, char in enumerate(line):
            if char == "S":
                beams[index] = 1
                return beams

    returned_beams = {}
    for key, number_beams in beams.items():
        if line[key] == "^":
            if key - 1 in returned_beams.keys():
                returned_beams[key - 1] += number_beams
            else:
                returned_beams[key - 1] = number_beams

            if key + 1 in returned_beams.keys():
                returned_beams[key + 1] += number_beams
            else:
                returned_beams[key + 1] = number_beams
        else:
            if key in returned_beams.keys():
                returned_beams[key] += number_beams
            else:
                returned_beams[key] = number_beams
    return returned_beams


def solve_one(lines: list[str]) -> int:
    splits_used = 0
    beams = []
    for i in range(0, len(lines), 2):
        splits, beams = get_splits_and_beams(lines[i], beams)
        splits_used += splits
    return splits_used


def solve_two(lines: list[str]) -> int:
    beams = {}
    for i in range(0, len(lines), 2):
        beams = get_all_splits_and_beams(lines[i], beams)

    result = 0
    for key, count in beams.items():
        result += count
    return result


def main():
    lines = read_file("input_7.txt")
    part_one = solve_one(lines)
    logger.info("Part one", result=part_one)

    part_two = solve_two(lines)
    logger.info("Part two", result=part_two)


if __name__ == "__main__":
    main()
