from copy import deepcopy

import structlog

from utils import read_file

logger = structlog.get_logger()


def parse_ranges_and_elements(lines):
    ranges = []
    elements = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue

        if len(line.split("-")) > 1:
            ranges.append([int(line.split("-")[0]), int(line.split("-")[1])])
        else:
            elements.append(int(line))
    return ranges, elements


def is_in_ranges(element, ranges):
    for range in ranges:
        if range[0] <= element <= range[1]:
            return True
    return False


def merge_ranges(ranges):
    new_ranges = deepcopy(ranges)
    new_ranges.sort()

    merged_ranges = []

    i = 0

    while i < len(new_ranges) - 1:
        new_range = [new_ranges[i][0], new_ranges[i][1]]
        j = 1
        while (
            i + j < len(new_ranges)
            and new_range[0] <= new_ranges[i + j][0] <= new_range[1]
            and (
                new_ranges[i + j][1] >= new_range[1]
                or new_range[1] >= new_ranges[i + j][1]
            )
        ):
            new_range[1] = max(new_ranges[i + j][1], new_range[1])
            j += 1
        merged_ranges.append(new_range)
        i += j
    return merged_ranges


def solve_one(ranges, elements):
    result = 0
    for element in elements:
        if is_in_ranges(element, ranges):
            result += 1
    return result


def solve_two(ranges):
    new_ranges = merge_ranges(ranges)
    # fmt:off
    import ipdb; ipdb.set_trace()
    # fmt:on

    return sum([range[1] - range[0] + 1 for range in new_ranges])


def main():
    lines = read_file("input_5.txt")
    ranges, elements = parse_ranges_and_elements(lines)
    part_one = solve_one(ranges, elements)
    logger.info("Part one", result=part_one)

    part_two = solve_two(ranges)
    logger.info("Part two", result=part_two)


if __name__ == "__main__":
    main()
