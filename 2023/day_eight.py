import structlog
from math import gcd

from utils import read_file

logger = structlog.get_logger()


def parse_directions(line: str) -> list[int]:
    directions = []
    for value in line:
        if value == "L":
            directions.append(0)
        elif value == "R":
            directions.append(1)
        else:
            continue

    return directions


def parse_elements(lines: list[str]) -> dict[str, tuple[str, str]]:
    elements = {}
    for line in lines:
        origin = line.split(" = ")[0]
        left = line.split("(")[1].split(",")[0]
        right= line.split(", ")[1].split(")")[0]
        elements[origin] = (left, right)
    return elements


def get_path(directions: list[int], elements: dict[str, tuple[str, str]], origin: str, destinations: list[str]) -> int:
    k = 0
    actual_place = origin
    length = 0
    while actual_place not in destinations:
        next_place = elements[actual_place][directions[k]]
        actual_place = next_place
        length += 1
        if k == len(directions) - 1:
            k = 0
        else:
            k += 1
    return length


def get_destinations(elements: dict[str, tuple[str, str]]) -> list[str]:
    result = []
    for element in elements.keys():
        if element[2] == "Z":
            result.append(element)
    return result


def get_lcm(lengths: list[int]) -> int:
    lcm = 1
    for elt in lengths:
        lcm = (lcm * elt) // gcd(lcm, elt)
    return lcm


def main():
    lines = read_file("input_eight.txt")
    directions = parse_directions(lines[0])
    elements = parse_elements(lines[2:])
    first_answer = get_path(directions, elements, origin="AAA", destinations=["ZZZ"])
    logger.info("first_question", answer=first_answer)

    destinations = get_destinations(elements)
    lengths = []
    for element in elements.keys():
        if element[2] == "A":
            lengths.append(get_path(directions, elements, origin=element, destinations=destinations))

    second_answer = get_lcm(lengths)
    logger.info("second_question", answer=second_answer)




if __name__ == "__main__":
    main()
