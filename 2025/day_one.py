import structlog

from utils import read_file

logger = structlog.get_logger()


def parse_lines(lines: list[str]) -> list[tuple[str, int]]:
    parsed_lines = []
    for line in lines:
        parsed_line = (line[0], int(line[1:]))
        parsed_lines.append(parsed_line)
    return parsed_lines


def operation(origin: int, direction: str, value: int) -> tuple[int, int]:
    passed = 0
    passed = value // 100
    value = value % 100
    if direction == "R":
        result = origin + value
        if result == 100:
            result -= 100
        if result > 99:
            result -= 100
            passed += 1
    if direction == "L":
        result = origin - value
        if result < 0:
            result += 100
            if origin > 0:
                passed += 1
    return result, passed


def solve_one(origin, parsed_lines: list[tuple[str, int]]) -> int:
    value = origin
    result = 0
    for line in parsed_lines:
        value, _ = operation(
            origin=value,
            direction=line[0],
            value=line[1],
        )
        if value == 0:
            result += 1
    return result


def solve_two(origin, parsed_lines: list[tuple[str, int]]) -> int:
    value = origin
    result = 0
    for line in parsed_lines:
        value, passed = operation(
            origin=value,
            direction=line[0],
            value=line[1],
        )

        result += passed
        if value == 0:
            result += 1

    return result


def main():
    lines = read_file("input_1.txt")
    parsed_lines = parse_lines(lines)
    first = solve_one(50, parsed_lines)
    logger.info("First part", answer=first)

    second = solve_two(50, parsed_lines)
    logger.info("Second part", answer=second)


if __name__ == "__main__":
    main()
